"""Config flow for the InvisOutlet integration."""

from __future__ import annotations

import asyncio
from types import MappingProxyType
from typing import Any
from uuid import uuid4

import voluptuous as vol
from homeassistant.config_entries import (
    SOURCE_SYSTEM,
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    ConfigSubentry,
    ConfigSubentryFlow,
    SubentryFlowResult,
)
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import discovery_flow
from homeassistant.helpers.selector import AreaSelector
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

from invisoutlet import InvisOutletClient, InvisOutletError

from .commission import EVENT_COMMISSION_FINISHED, EVENT_COMMISSIONED
from .const import (
    CONF_AREA,
    CONF_EFFECTS,
    CONF_ENTRY_TYPE,
    CONF_OUTLETS,
    DOMAIN,
    ENTRY_TYPE_HUB,
    MANUFACTURER,
    MODEL_OUTLET,
    SUBENTRY_AURA_EFFECT,
)

# How long to wait for the phone to finish commissioning before giving up.
COMMISSION_TIMEOUT = 180
# Overall cap on the reboot-and-reconnect phase, so a hung connect can never
# leave the flow in progress and block zeroconf discovery indefinitely.
FINALIZE_TIMEOUT = 120

STEP_OUTLET_DATA_SCHEMA = vol.Schema({vol.Required(CONF_HOST): str})
OUTLET_NAME_SCHEMA = vol.Schema(
    {vol.Required(CONF_NAME): str, vol.Optional(CONF_AREA): AreaSelector()}
)
AURA_EFFECT_SCHEMA = vol.Schema({vol.Required(CONF_NAME): str})


def _named_outlet(outlet: dict[str, Any], user_input: dict[str, Any]) -> dict[str, Any]:
    """The outlet config with the chosen device name (and area, if picked)."""
    named = {**outlet, CONF_NAME: user_input[CONF_NAME]}
    if area := user_input.get(CONF_AREA):
        named[CONF_AREA] = area
    return named


def _previously_known(hass: HomeAssistant, serial: str) -> bool:
    """Whether this outlet was configured before (a tombstoned device exists).

    Re-adding it restores the old identity — name, area, entity ids — so the
    flow skips the naming step for it.
    """
    dev_reg = dr.async_get(hass)
    return dev_reg.deleted_devices.get_entry({(DOMAIN, serial)}, None) is not None


async def _async_confirm_rebooted(
    host: str, *, attempts: int = 30, interval: float = 2.0
) -> None:
    """Block until the outlet has rebooted and its API answers again.

    Confirms a real down→up cycle with live reads, so the caller only proceeds
    once the device is back — otherwise the coordinator's first refresh reads a
    half-booted device and it comes up with no entities. Raises if it never does.
    """
    went_down = False
    for _ in range(attempts):
        client = InvisOutletClient(host)
        try:
            await client.connect()
            await client.get_device_info()
            if went_down:
                return
        except InvisOutletError:
            went_down = True
        finally:
            await client.close()
        await asyncio.sleep(interval)
    raise InvisOutletError(f"{host} did not come back after reboot")


async def _probe_outlet(
    host: str, *, restart: bool = False
) -> tuple[str, dict[str, Any]]:
    """Connect to an outlet, returning ``(serial, outlet_config)``.

    Raises :class:`InvisOutletError` if unreachable. ``restart=True`` reboots the
    outlet (to stop the setup-light blink) then blocks until its API answers
    again, so setup doesn't read a half-booted device.
    """
    client = InvisOutletClient(host)
    try:
        await client.connect()
        info = await client.get_device_info()
        if restart:
            await client.restart()
    finally:
        await client.close()
    if restart:
        await _async_confirm_rebooted(host)
    return info.serial_number, {CONF_HOST: host}


class InvisOutletConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for InvisOutlet."""

    def __init__(self) -> None:
        """Initialize the flow."""
        self._discovered: dict[str, Any] | None = None
        self._probed: dict[str, Any] | None = None
        self._commissioned: dict[str, Any] | None = None
        self._commission_task: asyncio.Task[dict[str, Any] | None] | None = None
        self._finalize_task: asyncio.Task[dict[str, Any] | None] | None = None

    @classmethod
    @callback
    def async_get_supported_subentry_types(
        cls, config_entry: ConfigEntry
    ) -> dict[str, type[ConfigSubentryFlow]]:
        """Offer the Add Aura Effect button on the hub."""
        if config_entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_HUB:
            return {SUBENTRY_AURA_EFFECT: AuraEffectSubentryFlowHandler}
        return {}

    def _find_hub(self) -> ConfigEntry | None:
        """Return the single InvisOutlet hub entry, if it exists."""
        for entry in self.hass.config_entries.async_entries(DOMAIN):
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_HUB:
                return entry
        return None

    def _commission_in_progress(self) -> bool:
        """Whether an outlet is currently being commissioned via the QR flow."""
        return any(
            flow["flow_id"] != self.flow_id
            and flow.get("step_id") in ("commission", "finalize")
            for flow in self.hass.config_entries.flow.async_progress_by_handler(
                DOMAIN, include_uninitialized=True
            )
        )

    async def async_step_system(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Create the hub entry in the background (never user-visible).

        Started by ``_async_add_outlet`` when no hub exists yet. Because the
        user-facing flow aborts instead of creating the entry itself, the
        stock entry-created dialog never shows.
        """
        assert user_input is not None
        if self._find_hub() is not None:
            # The hub appeared while this flow was queued: append instead.
            return await self._async_add_outlet(
                user_input["serial"], user_input["outlet"]
            )
        return self.async_create_entry(
            title="InvisOutlet Devices",
            data={
                CONF_ENTRY_TYPE: ENTRY_TYPE_HUB,
                CONF_OUTLETS: {user_input["serial"]: user_input["outlet"]},
            },
        )

    async def _async_add_outlet(
        self, serial: str, outlet: dict[str, Any]
    ) -> ConfigFlowResult:
        """Add the outlet to the hub, creating the hub in the background.

        Always aborts: the hub entry itself is only ever created by the
        system-source flow above, so no add ever surfaces the stock dialog.
        """
        hub = self._find_hub()
        if hub is None:
            discovery_flow.async_create_flow(
                self.hass,
                DOMAIN,
                context={"source": SOURCE_SYSTEM},
                data={"serial": serial, "outlet": outlet},
            )
            return self.async_abort(reason="outlet_added")

        outlets = hub.data.get(CONF_OUTLETS, {})
        if serial in outlets:
            return self.async_abort(reason="already_configured")
        # Appending fires the hub's update listener, which reloads it and brings
        # up the new outlet's device.
        self.hass.config_entries.async_update_entry(
            hub, data={**hub.data, CONF_OUTLETS: {**outlets, serial: outlet}}
        )
        return self.async_abort(reason="outlet_added")

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """First add creates the hub; later adds offer a way to add an outlet."""
        if self._find_hub() is None:
            return self.async_create_entry(
                title="InvisOutlet",
                data={CONF_ENTRY_TYPE: ENTRY_TYPE_HUB, CONF_OUTLETS: {}},
            )
        return self.async_show_menu(
            step_id="user", menu_options=["commission", "outlet"]
        )

    async def async_step_commission(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Wait for the phone (commission_bridge.js launches it) to commission an outlet.

        The frontend hack fires the app's Matter commissioning when this
        progress step appears; the interceptor resolves the new outlet and
        fires ``EVENT_COMMISSIONED``. Both paths converge on the name step.
        """
        if self._commission_task is None:
            self._commission_task = self.hass.async_create_task(
                self._async_wait_for_commission()
            )
        if not self._commission_task.done():
            return self.async_show_progress(
                step_id="commission",
                progress_action="commissioning",
                progress_task=self._commission_task,
            )

        commissioned = self._commission_task.result()
        self._commission_task = None
        if commissioned is None:
            return self.async_show_progress_done(next_step_id="commission_failed")
        self._commissioned = commissioned
        return self.async_show_progress_done(next_step_id="finalize")

    async def async_step_finalize(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Reboot the outlet (to stop the setup-light blink) and wait for it back."""
        if self._finalize_task is None:
            self._finalize_task = self.hass.async_create_task(
                self._async_finalize_outlet()
            )
        if not self._finalize_task.done():
            return self.async_show_progress(
                step_id="finalize",
                progress_action="finalize",
                progress_task=self._finalize_task,
            )

        probed = self._finalize_task.result()
        self._finalize_task = None
        if probed is None:
            return self.async_show_progress_done(next_step_id="commission_failed")
        self._probed = probed
        return self.async_show_progress_done(next_step_id="name")

    async def async_step_commission_failed(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Commissioning didn't complete (timeout or unreachable)."""
        return self.async_abort(reason="commission_failed")

    async def _async_finalize_outlet(self) -> dict[str, Any] | None:
        """Reboot the freshly commissioned outlet and read it once it's back."""
        assert self._commissioned is not None
        try:
            async with asyncio.timeout(FINALIZE_TIMEOUT):
                serial, outlet = await _probe_outlet(
                    self._commissioned["ip"], restart=True
                )
        except (InvisOutletError, TimeoutError):
            return None
        return {"serial": serial, "outlet": outlet, "name": self._commissioned["name"]}

    async def _async_wait_for_commission(self) -> dict[str, Any] | None:
        """Await an outlet being commissioned and the app reporting finished.

        The interceptor's event carries the IP (fired at network setup); the
        finish event carries the phone-set name (fired after the phone's naming
        dialog). Waiting for finish keeps the flow on the spinner until the
        phone's dialog closes, instead of surfacing the name step behind it.

        The finish ``success`` flag is unreliable — canceling before doing
        anything still reports ``success: true`` — so we decide on the
        interceptor's event instead. Await finish first (keeps the spinner up
        until the phone's dialog closes); by then a real provision has already
        fired the interceptor's event. So if it fired, proceed (carrying the
        phone-set ``name`` when present, else ``None`` for the default); if not,
        the user canceled, so abort. Returns ``{"ip", "name"}`` for the finalize
        step, or ``None`` to abort.
        """
        commissioned: asyncio.Future[dict[str, Any]] = self.hass.loop.create_future()
        finished: asyncio.Future[dict[str, Any]] = self.hass.loop.create_future()

        @callback
        def _on_commissioned(event) -> None:
            if event.data.get("is_invisoutlet") and not commissioned.done():
                commissioned.set_result(event.data)

        @callback
        def _on_finished(event) -> None:
            if not finished.done():
                finished.set_result(event.data)

        unsubs = [
            self.hass.bus.async_listen(EVENT_COMMISSIONED, _on_commissioned),
            self.hass.bus.async_listen(EVENT_COMMISSION_FINISHED, _on_finished),
        ]
        try:
            try:
                await asyncio.wait_for(finished, COMMISSION_TIMEOUT)
            except TimeoutError:
                return None
            if not commissioned.done():
                return None  # canceled: nothing was provisioned
            detail = commissioned.result()
            finish = finished.result()
        finally:
            for unsub in unsubs:
                unsub()

        if not (ip := detail.get("ip")):
            return None
        return {"ip": ip, "name": finish.get("name")}

    async def async_step_outlet(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Add an outlet by host, then name it (creates the hub if needed)."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                serial, outlet = await _probe_outlet(user_input[CONF_HOST])
            except InvisOutletError:
                errors["base"] = "cannot_connect"
            else:
                hub = self._find_hub()
                if hub is not None and serial in hub.data.get(CONF_OUTLETS, {}):
                    return self.async_abort(reason="already_configured")
                if _previously_known(self.hass, serial):
                    # Re-add: the old identity restores; no naming step.
                    return await self._async_add_outlet(serial, outlet)
                self._probed = {"serial": serial, "outlet": outlet}
                return await self.async_step_name()

        return self.async_show_form(
            step_id="outlet", data_schema=STEP_OUTLET_DATA_SCHEMA, errors=errors
        )

    async def async_step_name(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Name the outlet's device, then add it."""
        probed = self._probed
        assert probed is not None
        if user_input is not None:
            return await self._async_add_outlet(
                probed["serial"], _named_outlet(probed["outlet"], user_input)
            )
        # Pre-fill with the phone-set name from commissioning when we have one.
        suggested = probed.get("name") or f"InvisOutlet {probed['serial']}"
        return self.async_show_form(
            step_id="name",
            data_schema=self.add_suggested_values_to_schema(
                OUTLET_NAME_SCHEMA, {CONF_NAME: suggested}
            ),
        )

    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> ConfigFlowResult:
        """Handle an outlet discovered over mDNS."""
        # A faceplate mid-update advertises its own service, with its own serial
        # under "sn". Adding that as an outlet yields an entity-less device bound
        # to a lease that disappears when the update finishes.
        model = discovery_info.properties.get("device")
        if model is not None and model != MODEL_OUTLET:
            return self.async_abort(reason="not_an_outlet")

        serial = discovery_info.properties.get("sn")
        if not serial:
            return self.async_abort(reason="no_serial")

        host = str(discovery_info.ip_address)
        # A commission flow is running: this discovery is the device being
        # commissioned (it advertises before the interceptor knows its serial),
        # so let that flow add it — don't surface a competing card.
        if self._commission_in_progress():
            return self.async_abort(reason="commission_in_progress")

        # Already an outlet on the hub? Keep its host current and stop.
        hub = self._find_hub()
        if hub is not None:
            outlets = hub.data.get(CONF_OUTLETS, {})
            if serial in outlets:
                if outlets[serial].get(CONF_HOST) != host:
                    self.hass.config_entries.async_update_entry(
                        hub,
                        data={
                            **hub.data,
                            CONF_OUTLETS: {
                                **outlets,
                                serial: {**outlets[serial], CONF_HOST: host},
                            },
                        },
                    )
                return self.async_abort(reason="already_configured")

        await self.async_set_unique_id(serial)
        title = " ".join(p for p in (model or "", serial) if p) or MANUFACTURER
        self._discovered = {"serial": serial, "title": title, "host": host}
        self.context["title_placeholders"] = {"name": title}
        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm and name a discovered outlet.

        A previously known outlet restores its old identity, so it gets a
        plain confirm with no naming fields.
        """
        assert self._discovered is not None
        known = _previously_known(self.hass, self._discovered["serial"])
        if user_input is not None:
            outlet: dict[str, Any] = {CONF_HOST: self._discovered["host"]}
            if not known:
                outlet = _named_outlet(outlet, user_input)
            return await self._async_add_outlet(self._discovered["serial"], outlet)

        if known:
            self._set_confirm_only()
            return self.async_show_form(
                step_id="zeroconf_confirm",
                description_placeholders={"name": self._discovered["title"]},
            )
        return self.async_show_form(
            step_id="zeroconf_confirm",
            data_schema=self.add_suggested_values_to_schema(
                OUTLET_NAME_SCHEMA, {CONF_NAME: self._discovered["title"]}
            ),
            description_placeholders={"name": self._discovered["title"]},
        )


class AuraEffectSubentryFlowHandler(ConfigSubentryFlow):
    """Add an Aura effect, appended into the single shared Aura Effects subentry.

    The first add creates the subentry; every add after appends another effect
    (one device each) to the same subentry's data, so they group together
    instead of spawning a subentry per effect.
    """

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> SubentryFlowResult:
        """Add an Aura effect."""
        if user_input is not None:
            effect = {CONF_NAME: user_input[CONF_NAME]}
            entry = self.hass.config_entries.async_get_entry(self.handler[0])
            assert entry is not None
            existing = entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT)
            if existing:
                subentry = existing[0]
                effects = {**subentry.data.get(CONF_EFFECTS, {}), uuid4().hex: effect}
                self.hass.config_entries.async_update_subentry(
                    entry, subentry, data={CONF_EFFECTS: effects}
                )
            else:
                self.hass.config_entries.async_add_subentry(
                    entry,
                    ConfigSubentry(
                        data=MappingProxyType({CONF_EFFECTS: {uuid4().hex: effect}}),
                        subentry_type=SUBENTRY_AURA_EFFECT,
                        title="InvisOutlet Aura Effects",
                        unique_id=None,
                    ),
                )
            # The subentry now exists, so reload to bring the new effect's virtual
            # device up. (update_reload_and_abort is rejected on entries with
            # update listeners, which the hub has, so reload separately.)
            self.hass.config_entries.async_schedule_reload(entry.entry_id)
            return self.async_abort(reason="added")
        return self.async_show_form(step_id="user", data_schema=AURA_EFFECT_SCHEMA)
