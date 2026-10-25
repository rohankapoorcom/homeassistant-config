"""Coordinator for the InvisOutlet integration.

Owns the persistent client connection. Everything is event-driven: sensor and
outlet pushes update entities directly, the library auto-reconnects on drops,
and the connect/disconnect callbacks drive a state re-pull and availability.
There is no polling.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady, HomeAssistantError
from homeassistant.helpers.event import async_call_later, async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from invisoutlet import (
    ColorEffect,
    ColorLightState,
    DeviceConfig,
    DeviceInfo,
    FirmwareRelease,
    InvisOutletClient,
    InvisOutletConnectionError,
    InvisOutletError,
    NightlightState,
    OtaProgress,
    OtaResult,
    OtaTarget,
    OutletStatus,
    SensorData,
    target_for_device_type,
)
from invisoutlet.client import (
    CALLBACK_COLOR_LIGHT,
    CALLBACK_DEVICE_INFO,
    CALLBACK_NIGHTLIGHT_STATUS,
    LIGHT_NIGHTLIGHT,
)

from .const import (
    CONF_OUTLETS,
    CONF_SUB_DEVICE_UPDATE_METHOD,
    DEFAULT_SUB_DEVICE_UPDATE_METHOD,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# How often to re-check the firmware-update service for each module.
_FIRMWARE_CHECK_INTERVAL = timedelta(hours=6)

# Delays (seconds) between device-info re-reads after a successful update, while
# waiting for the rebooted device to come back and report its new revision. The
# InvisDeco's reboot doesn't drop our connection to the outlet, so nothing else
# triggers a refresh for it. Spans ~4 minutes.
_POST_UPDATE_REFRESH_DELAYS = (10, 20, 30, 30, 30, 60, 60)

# Seconds without a sub-device push before it's considered offline. The attached
# faceplate (InvisDeco today, Aura later) streams sensor data every few seconds
# while it's up, so a gap means it has dropped.
_SUB_DEVICE_OFFLINE_TIMEOUT = 15

# The hub entry's runtime_data maps each outlet subentry_id to its coordinator.
type InvisOutletConfigEntry = ConfigEntry[dict[str, InvisOutletCoordinator]]


def _model_or(raw: str | None, fallback: str) -> str:
    """A module's model name, falling back when it reports blank or 'Unknown'.

    The firmware returns a blank or literal ``"Unknown"`` device name while a
    module is in a degraded state; callers want a stable label instead.
    """
    return raw if raw and raw != "Unknown" else fallback


class InvisOutletCoordinator(DataUpdateCoordinator[OutletStatus]):
    """Surface device state to entities, fully event-driven (no polling).

    ``data`` holds the latest :class:`OutletStatus`; ``sensor`` holds the latest
    :class:`SensorData` (or ``None`` until the first push).
    """

    config_entry: InvisOutletConfigEntry
    device_info: DeviceInfo
    config: DeviceConfig

    def __init__(
        self,
        hass: HomeAssistant,
        entry: InvisOutletConfigEntry,
        serial: str,
        client: InvisOutletClient,
    ) -> None:
        """Initialize the coordinator (no ``update_interval`` -> no polling).

        ``entry`` is the shared hub; ``serial`` keys this outlet's stored config
        (host and per-outlet settings) in ``entry.data[CONF_OUTLETS]``.
        """
        super().__init__(hass, _LOGGER, config_entry=entry, name=DOMAIN)
        self._serial = serial
        self.client = client
        self.sensor: SensorData | None = None
        # Latest faceplate nightlight state; pushed (callback 15) on every change.
        self.nightlight: NightlightState | None = None
        # Latest Aura color-array state per light selector (nightlight 5,
        # indicator 1); both push on callback 18, keyed by the frame's light id.
        self.color_lights: dict[int, ColorLightState] = {}
        # Latest firmware release per module, and the in-flight OTA percentage
        # per module (key present == currently updating).
        self.firmware: dict[OtaTarget, FirmwareRelease | None] = {}
        self.ota_progress: dict[OtaTarget, int] = {}
        # The device_type of the phase currently reporting progress (e.g. the
        # outlet update runs device_type 3 = WWW partition, then 1 = firmware).
        self.ota_phase: dict[OtaTarget, int] = {}
        # Installed version per module when an update was started, used to detect
        # completion by the version actually changing (independent of the result
        # push, which is the more reliable signal after a post-update reboot).
        self._ota_start_version: dict[OtaTarget, str | None] = {}
        # Per-target future an in-flight ``async_install`` awaits; resolved with
        # the terminal success flag so the install can raise on failure.
        self._ota_install_results: dict[OtaTarget, asyncio.Future[bool]] = {}
        # Whether the attached sub-device (faceplate) is currently up, inferred
        # from its sensor pushes; ``False`` until the first push confirms it.
        self.sub_device_online: bool = False
        self._sub_device_watchdog: CALLBACK_TYPE | None = None
        # Connection-health counters, surfaced as disabled-by-default diagnostic
        # sensors. They separate the two ways an outlet degrades: the connection
        # dropping (reconnects) and the faceplate going quiet while the
        # connection is fine (faceplate dropouts).
        self.reconnects: int = 0
        self.faceplate_dropouts: int = 0
        self.connected_since: datetime | None = None
        self.last_sensor_push: datetime | None = None
        # Recurring firmware-check timer; canceled per-outlet on teardown so a
        # single outlet can be removed without reloading the whole hub.
        self._unsub_firmware: CALLBACK_TYPE | None = None

    async def _async_setup(self) -> None:
        """Connect, read device info and config, and subscribe to events."""
        try:
            await self.client.connect()
            self.device_info = await self.client.get_device_info()
            self.config = await self.client.get_config()
        except InvisOutletError as err:
            raise ConfigEntryNotReady(
                f"Could not connect to InvisOutlet device: {err}"
            ) from err
        self.client.on_sensor_data(self._handle_sensor)
        self.client.on_outlet_status(self._handle_outlets)
        self.client.on_connect(self._handle_connect)
        self.client.on_disconnect(self._handle_disconnect)
        self.client.on_ota_progress(self._handle_ota_progress)
        self.client.on_ota_result(self._handle_ota_result)
        # The device pushes device-info when it restarts; re-sync on it.
        self.client.on_message(CALLBACK_DEVICE_INFO, self._handle_device_info_push)
        # The faceplate pushes its nightlight state (callback 15) on every change.
        self.client.on_message(CALLBACK_NIGHTLIGHT_STATUS, self._handle_nightlight)
        await self._refresh_nightlight()
        # An Aura pushes its color-array state (callback 18) on every change.
        self.client.on_message(CALLBACK_COLOR_LIGHT, self._handle_color_light)
        await self._refresh_color_lights()
        # Read sensors once up front so platforms know which the faceplate has
        # (it omits the ones it lacks). Failure just leaves them unknown.
        try:
            self.sensor = await self.client.get_sensor_data()
        except InvisOutletError as err:
            _LOGGER.debug("Initial sensor fetch failed: %s", err)
        # Check firmware now (in the background, so a slow update service can't
        # delay setup) and on a slow recurring timer thereafter.
        self.config_entry.async_create_background_task(
            self.hass,
            self.async_check_firmware(),
            f"invisoutlet_firmware_check_{self._serial}",
        )
        self._unsub_firmware = async_track_time_interval(
            self.hass,
            self._scheduled_firmware_check,
            _FIRMWARE_CHECK_INTERVAL,
        )

    async def async_teardown(self) -> None:
        """Tear down this one outlet: timers, watchdog, and the connection.

        Used on full unload and when a single outlet is removed, so removal
        doesn't require reloading the whole hub. ``async_shutdown`` is idempotent
        (also auto-called on full entry unload), so a double call is harmless.
        """
        await self.async_shutdown()
        if self._unsub_firmware is not None:
            self._unsub_firmware()
            self._unsub_firmware = None
        self._cancel_sub_device_watchdog()
        await self.client.close()

    async def async_dynamic_setup(self) -> None:
        """Set up + first refresh for an outlet added after the entry is loaded.

        ``async_config_entry_first_refresh`` is only valid while the entry is
        being set up, so an outlet added to the already-loaded hub replicates it
        here. Raises ``ConfigEntryNotReady`` if the outlet can't be reached.
        """
        await self._async_setup()
        await self.async_refresh()
        if not self.last_update_success:
            raise ConfigEntryNotReady("Initial refresh failed")

    def _firmware_targets(
        self,
    ) -> list[tuple[OtaTarget, str, str | None, str | None, str | None]]:
        """Return ``(target, model, hw_rev, current_fw, variant)`` for each module.

        ``variant`` is the faceplate's ``type`` (e.g. ``"Aura"``), which picks the
        right product code since faceplates share the model name "InvisDeco".
        """
        info = self.device_info
        targets: list[tuple[OtaTarget, str, str | None, str | None, str | None]] = [
            (OtaTarget.INVISOUTLET, info.device, info.hw_rev, info.fw_rev, None)
        ]
        if (sub := info.sub_device) is not None:
            targets.append(
                (
                    OtaTarget.INVISDECO,
                    sub.device,
                    sub.hw_rev,
                    sub.fw_rev,
                    sub.device_type,
                )
            )
        return targets

    async def async_check_firmware(self) -> None:
        """Refresh the latest-firmware info for every module."""
        for target, model, hw_rev, current, variant in self._firmware_targets():
            if not (model and hw_rev and current):
                continue
            try:
                self.firmware[target] = await self.client.check_firmware(
                    target, model, hw_rev, current, variant
                )
            except InvisOutletError as err:
                _LOGGER.debug("Firmware check failed for %s: %s", model, err)
        self.async_update_listeners()

    async def _scheduled_firmware_check(self, _now: object) -> None:
        """Run the recurring firmware check."""
        await self.async_check_firmware()

    def installed_version(self, target: OtaTarget) -> str | None:
        """Return the installed firmware revision for a module."""
        info = self.device_info
        if target is OtaTarget.INVISDECO:
            return info.sub_device.fw_rev if info.sub_device else None
        return info.fw_rev

    @property
    def outlet_name(self) -> str:
        """The outlet's model name, stable through degraded reporting."""
        return _model_or(self.device_info.device, "Outlet")

    @property
    def sub_device_name(self) -> str:
        """The faceplate's model name, stable through degraded/absent reporting."""
        sub = self.device_info.sub_device
        return _model_or(sub.device if sub is not None else None, "Sub-device")

    def model_name(self, target: OtaTarget) -> str:
        """The model name for a module (outlet or faceplate)."""
        if target is OtaTarget.INVISDECO:
            return self.sub_device_name
        return self.outlet_name

    async def async_install_firmware(self, target: OtaTarget) -> None:
        """Start an OTA update and wait for the outcome, raising on failure.

        Progress is surfaced live via the pushes while this awaits the terminal
        result the client provides (a real success/failure or a synthesized
        stall failure). Raising ``HomeAssistantError`` makes the frontend show a
        "Failed to install update" notification.
        """
        method = (
            self.config_entry.data[CONF_OUTLETS]
            .get(self._serial, {})
            .get(CONF_SUB_DEVICE_UPDATE_METHOD, DEFAULT_SUB_DEVICE_UPDATE_METHOD)
            if target is OtaTarget.INVISDECO
            else 0
        )
        self._ota_start_version[target] = self.installed_version(target)
        self.ota_progress[target] = 0
        result: asyncio.Future[bool] = self.hass.loop.create_future()
        stale = self._ota_install_results.pop(target, None)
        if stale is not None and not stale.done():
            stale.cancel()
        self._ota_install_results[target] = result
        self.async_update_listeners()
        try:
            await self.client.perform_ota_update(target, method)
        except InvisOutletError as err:
            self._ota_install_results.pop(target, None)
            self._clear_ota(target)
            self.async_update_listeners()
            raise HomeAssistantError(f"Could not start firmware update: {err}") from err
        try:
            success = await result
        finally:
            self._ota_install_results.pop(target, None)
        if not success:
            raise HomeAssistantError(
                "Firmware update failed or the device stopped responding"
            )

    def _clear_ota(self, target: OtaTarget) -> None:
        """Drop the in-progress state for a module."""
        self.ota_progress.pop(target, None)
        self.ota_phase.pop(target, None)
        self._ota_start_version.pop(target, None)

    def _reconcile_completed_ota(self) -> list[OtaTarget]:
        """Finish any in-progress OTA whose module now reports a new version.

        The single definition of "the version moved past where the update
        started, so it's done" — used after every device-info refresh. Returns
        the targets that just completed.
        """
        completed: list[OtaTarget] = []
        for target in list(self.ota_progress):
            start = self._ota_start_version.get(target)
            current = self.installed_version(target)
            if start is not None and current is not None and current != start:
                self._clear_ota(target)
                completed.append(target)
        return completed

    async def _async_update_data(self) -> OutletStatus:
        """Fetch outlet state.

        Called for the initial read and again after each reconnect (outlet
        changes otherwise arrive via push).
        """
        try:
            return await self.client.get_outlet_status()
        except InvisOutletError as err:
            raise UpdateFailed(f"Error talking to InvisOutlet device: {err}") from err

    async def async_set_config(self, **changes: object) -> None:
        """Write config changes, then re-read so entities reflect the result."""
        await self.client.set_config(**changes)
        self.config = await self.client.get_config()
        self.async_update_listeners()

    @callback
    def _handle_outlets(self, outlets: OutletStatus) -> None:
        """Apply a pushed outlet-status update immediately."""
        self.async_set_updated_data(outlets)

    @callback
    def _handle_sensor(self, data: SensorData) -> None:
        """Push a sensor update to entities without altering outlet state.

        A sensor push also means the sub-device (faceplate) is up, so mark it
        online and (re)arm the offline watchdog.
        """
        self.sensor = data
        self.last_sensor_push = dt_util.utcnow()
        self._mark_sub_device_online()
        self.async_update_listeners()

    @callback
    def _handle_nightlight(self, msg: dict[str, object]) -> None:
        """Apply a pushed nightlight-state update (callback 15)."""
        payload = msg.get("payload", {})
        args = payload.get("callbackArgs", []) if isinstance(payload, dict) else []
        self.nightlight = NightlightState.from_raw(args)
        self.async_update_listeners()

    async def _refresh_nightlight(self) -> None:
        """Read the current nightlight state (no-op if the faceplate can't answer)."""
        try:
            self.nightlight = await self.client.get_nightlight()
        except InvisOutletError as err:
            _LOGGER.debug("Could not refresh nightlight state: %s", err)

    async def async_set_nightlight(
        self, *, on: bool, brightness: int | None = None
    ) -> None:
        """Set the nightlight on/off and brightness, then update entities.

        Brightness defaults to the last-known level (or full) so a plain turn-on
        restores the previous brightness. The callback-15 push that follows
        confirms or corrects the optimistic state set here.
        """
        mode = 1 if on else 0
        level = (
            brightness
            if brightness is not None
            else (self.nightlight.brightness if self.nightlight else 100)
        )
        await self.client.set_nightlight(mode, level)
        self.nightlight = NightlightState(mode=mode, brightness=level)
        self.async_update_listeners()

    @callback
    def _handle_color_light(self, msg: dict[str, object]) -> None:
        """Apply a pushed Aura color-array update (callback 18), keyed by light id."""
        payload = msg.get("payload", {})
        args = payload.get("callbackArgs", []) if isinstance(payload, dict) else []
        if isinstance(args, list) and len(args) >= 3:
            state = ColorLightState.from_raw(args)
            self.color_lights[state.light] = state
            self.async_update_listeners()

    async def _refresh_color_lights(self) -> None:
        """Read each exposed color array's state (just the nightlight for now)."""
        for light in (LIGHT_NIGHTLIGHT,):
            try:
                state = await self.client.get_color(light)
            except InvisOutletError as err:
                _LOGGER.debug("Could not refresh color light %s: %s", light, err)
                continue
            self.color_lights[state.light] = state

    def _color_led_count(self, light: int) -> int:
        """LED count of a color array, for filling a whole-array set call."""
        cl = self.color_lights.get(light)
        return len(cl.leds) if cl is not None and cl.leds else 1

    async def async_set_color_hsv(
        self, light: int, *, hue: int, saturation: int, brightness: int, on: bool = True
    ) -> None:
        """Set a color array to an HSV color (state follows via push).

        Fill the whole array in one call so the firmware doesn't animate the fill.
        """
        await self.client.set_color_hsv(
            light, hue, saturation, brightness, on, count=self._color_led_count(light)
        )

    async def async_set_color_temperature(
        self, light: int, *, kelvin: int, brightness: int, on: bool = True
    ) -> None:
        """Set a color array to a white temperature (state follows via push).

        The firmware needs one entry per LED for temperature, so size it to the
        array we last read.
        """
        await self.client.set_color_temperature(
            light, kelvin, brightness, on, count=self._color_led_count(light)
        )

    async def async_set_temperature_pixels(
        self,
        light: int,
        *,
        temperatures: list[int],
        brightness: list[int] | None = None,
        states: list[bool] | None = None,
    ) -> None:
        """Write a per-LED white-temperature palette; state follows push."""
        await self.client.set_color_temperatures(
            light, temperatures, brightness=brightness, states=states
        )

    async def async_set_effect_pixels(
        self,
        light: int,
        *,
        colors: list[tuple[int, int]],
        effect: ColorEffect,
        speed: int,
        randomize: bool,
        level: int,
        brightness: list[int] | None = None,
    ) -> None:
        """Run an animated effect over a per-LED palette (speed/randomize/level)."""
        await self.client.set_color_effect_pixels(
            light, colors, effect, speed, randomize, level, brightness=brightness
        )

    def _mark_sub_device_online(self) -> None:
        """Note a sub-device push and (re)arm the offline watchdog."""
        came_online = not self.sub_device_online
        self._cancel_sub_device_watchdog()
        self._sub_device_watchdog = async_call_later(
            self.hass, _SUB_DEVICE_OFFLINE_TIMEOUT, self._sub_device_timed_out
        )
        self.sub_device_online = True
        if came_online:
            # It just reappeared; re-read device info so its name and fw_rev
            # refresh from the degraded values it was reporting while down.
            self.config_entry.async_create_background_task(
                self.hass, self._refresh_device_info(), "invisoutlet_subdevice_online"
            )

    def _cancel_sub_device_watchdog(self) -> None:
        """Cancel the sub-device offline watchdog if armed."""
        if self._sub_device_watchdog is not None:
            self._sub_device_watchdog()
            self._sub_device_watchdog = None

    @callback
    def _sub_device_timed_out(self, _now: object) -> None:
        """No sub-device pushes within the window -> it's offline."""
        self._sub_device_watchdog = None
        if self.sub_device_online:
            self.sub_device_online = False
            self.faceplate_dropouts += 1
            self.async_update_listeners()

    @callback
    def _handle_connect(self) -> None:
        """Re-pull state after a (re)connect (pushes were missed)."""
        self.connected_since = dt_util.utcnow()
        self.hass.async_create_task(self._handle_reconnect())

    async def _handle_reconnect(self) -> None:
        """Refresh outlet and device state after reconnecting.

        A reconnect often follows a firmware update's reboot, so re-read device
        info to pick up the new revision.
        """
        await self.async_request_refresh()
        await self._resync()

    @callback
    def _handle_device_info_push(self, msg: dict[str, object]) -> None:
        """Re-sync when the device announces a restart via a device-info push."""
        self.config_entry.async_create_background_task(
            self.hass, self._resync(), "invisoutlet_restart_resync"
        )

    def _faceplate_serial(self) -> str | None:
        """The attached faceplate's serial, or None if there isn't one."""
        sub = self.device_info.sub_device
        return sub.serial_number if sub is not None else None

    async def _resync(self) -> None:
        """Re-read device info, firmware and config after a (re)connect/restart.

        None of these refresh on their own, so without this a device restart
        leaves the config switches and the update entities' "latest version"
        stuck on stale values.
        """
        previous_faceplate = self._faceplate_serial()
        await self._refresh_device_info()
        if self._faceplate_serial() != previous_faceplate:
            # The faceplate was swapped (different serial); its entity set differs,
            # so rebuild from scratch rather than patching entities in place. A
            # reboot keeps the same serial and falls through to a normal resync.
            self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)
            return
        await self.async_check_firmware()
        await self._refresh_nightlight()
        await self._refresh_color_lights()
        try:
            self.config = await self.client.get_config()
        except InvisOutletError as err:
            _LOGGER.debug("Could not refresh config: %s", err)
            return
        self.async_update_listeners()

    @callback
    def _handle_disconnect(self) -> None:
        """Mark entities unavailable while the connection is down."""
        # The sub-device's status is unknown until pushes resume after reconnect.
        self._cancel_sub_device_watchdog()
        self.sub_device_online = False
        self.reconnects += 1
        self.connected_since = None
        self.async_set_update_error(InvisOutletConnectionError("Connection lost"))

    @callback
    def _handle_ota_progress(self, progress: OtaProgress) -> None:
        """Apply a pushed OTA progress update for the targeted module."""
        target = target_for_device_type(progress.device_type)
        if target is None:
            return
        self.ota_progress[target] = progress.progress
        self.ota_phase[target] = progress.device_type
        self.async_update_listeners()

    @callback
    def _handle_ota_result(self, result: OtaResult) -> None:
        """Apply a terminal OTA result.

        The client gates results, so this fires once per update: a real success,
        a real post-progress failure, or a synthesized stall failure. A failure
        just clears the in-progress state (reverting to "Update available"); a
        success additionally polls for the new installed version.
        """
        target = target_for_device_type(result.device_type)
        if target is None:
            return
        # Hand the outcome to a waiting async_install so it can raise on failure.
        future = self._ota_install_results.get(target)
        if future is not None and not future.done():
            future.set_result(result.success)
        if result.success:
            # Keep showing "Installing (100%)" rather than clearing now: the
            # device still has to reboot and report the new revision, and
            # clearing here would briefly read "Update available" in between.
            # _refresh_after_update clears it once the new version is live.
            self.async_update_listeners()
            self.config_entry.async_create_background_task(
                self.hass,
                self._refresh_after_update(target),
                "invisoutlet_post_update_refresh",
            )
        else:
            self._clear_ota(target)
            self.async_update_listeners()

    def _store_device_info(self, new: DeviceInfo, *, preserve_subdevice: bool) -> None:
        """Store a refreshed device info, optionally keeping the known deco.

        A device-info read taken while the InvisDeco is rebooting omits its PM
        block (the offline sub-device isn't reported), which would null the
        deco's version and leave its update entity blank/"up-to-date". During an
        update that absence is just the reboot, so keep the last-known deco; with
        no update in flight we trust the report, so a genuinely removed deco
        drops out instead of showing a phantom update.
        """
        if (
            preserve_subdevice
            and new.sub_device is None
            and self.device_info.sub_device is not None
        ):
            new.sub_device = self.device_info.sub_device
        self.device_info = new

    async def _refresh_after_update(self, target: OtaTarget) -> None:
        """Hold "Installing" until the updated module reports its new version.

        Polls device info through the post-update reboot; once the revision
        changes the in-progress state clears (so it flips straight to
        "Up-to-date") and the release info refreshes. If the version never shows
        within the window, clear anyway so the bar doesn't stick at 100%.
        """
        for delay in _POST_UPDATE_REFRESH_DELAYS:
            await asyncio.sleep(delay)
            try:
                # This poll exists because of a post-update reboot, so absence of
                # the deco here is the reboot, not a removal: preserve it.
                self._store_device_info(
                    await self.client.get_device_info(), preserve_subdevice=True
                )
            except InvisOutletError as err:
                _LOGGER.debug("Post-update device-info refresh failed: %s", err)
                continue
            if target in self._reconcile_completed_ota():
                await self.async_check_firmware()
                self.async_update_listeners()
                return
            self.async_update_listeners()
        self._clear_ota(target)
        self.async_update_listeners()

    async def _refresh_device_info(self) -> None:
        """Re-read device info, marking an update complete if the version moved."""
        try:
            # Only hold a missing deco across the reboot if it's mid-update;
            # otherwise an absent deco is taken at face value (e.g. removed).
            self._store_device_info(
                await self.client.get_device_info(),
                preserve_subdevice=OtaTarget.INVISDECO in self.ota_progress,
            )
        except InvisOutletError as err:
            _LOGGER.debug("Could not refresh device info: %s", err)
            return
        self._reconcile_completed_ota()
        self.async_update_listeners()
