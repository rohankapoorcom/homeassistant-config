"""Light platform: the faceplate's dimmable nightlight."""

from __future__ import annotations

import json
import logging
from typing import Any, ClassVar

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.const import CONF_NAME
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import (
    EVENT_DEVICE_REGISTRY_UPDATED,
    DeviceEntryType,
    DeviceInfo,
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import (
    EventStateChangedData,
    async_track_state_change_event,
)
from homeassistant.util.color import (
    brightness_to_value,
    color_hs_to_RGB,
    value_to_brightness,
)

from invisoutlet import ColorLedEntry, ColorLightState, InvisOutletError
from invisoutlet.client import LIGHT_NIGHTLIGHT, MAX_KELVIN, MIN_KELVIN

from .const import (
    CONF_COLOR_EFFECTS,
    CONF_EFFECTS,
    CONF_OUTLETS,
    DOMAIN,
    SUBENTRY_AURA_EFFECT,
)
from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .effects import (
    ApplyContext,
    EffectMode,
    PixelKind,
    PixelSpec,
    PixelState,
    get_effect_mode,
    mode_label,
)
from .entity import InvisOutletEntity
from .helpers import (
    async_add_outlet_entities,
    async_update_effect_data,
    effect_data,
    effect_mode_signal,
)

_LOGGER = logging.getLogger(__name__)

# How many virtual pixels the standalone "Aura Effects" pseudo-device exposes.
_EFFECT_PIXELS = 9

# The Color Light's "no effect" option (plain static color), always first in
# its effect list.
EFFECT_NONE = "Static"

# Shown (and selected) only while another controller is driving the array; HA
# goes passive until the user picks a real effect again.
EFFECT_EXTERNAL = "External"

# A template pixel's role -> the color mode it exposes.
_COLOR_MODES = {
    PixelKind.HS: ColorMode.HS,
    PixelKind.TEMPERATURE: ColorMode.COLOR_TEMP,
    PixelKind.BRIGHTNESS: ColorMode.BRIGHTNESS,
}

# The device reports brightness as a 0-100 percentage.
_BRIGHTNESS_SCALE = (1, 100)

# Device color-array mode (callback 18): 2 = static white color-temperature.
_COLOR_MODE_TEMPERATURE = 2


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the per-effect virtual pixels and the per-outlet lights."""
    # Each added Aura effect is its own virtual device of HSV pixels that only
    # hold state and drive no hardware; all effects share one subentry.
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        for effect_id, effect in subentry.data.get(CONF_EFFECTS, {}).items():
            async_add_entities(
                (
                    AuraEffectVirtualLight(entry, effect_id, effect[CONF_NAME], index)
                    for index in range(_EFFECT_PIXELS)
                ),
                config_subentry_id=subentry.subentry_id,
            )

    def build(coordinator: InvisOutletCoordinator) -> list[LightEntity]:
        serial = coordinator.device_info.serial_number
        ent_reg = er.async_get(hass)

        def _drop_stale_light(key: str) -> None:
            # A live faceplate swap changes which light exists (nightlight vs
            # color array); remove the other one so it doesn't linger as a
            # "no longer provided" entity.
            if entity_id := ent_reg.async_get_entity_id(
                "light", DOMAIN, f"{serial}_{key}"
            ):
                ent_reg.async_remove(entity_id)

        sub = coordinator.device_info.sub_device
        if sub is None:
            _drop_stale_light("nightlight")
            _drop_stale_light("colorlight")
            return []
        if sub.device_type == "Aura":
            # The Aura's nightlight is a color array — one standard HSV light.
            _drop_stale_light("nightlight")
            return [
                InvisOutletColorLight(
                    coordinator, LIGHT_NIGHTLIGHT, "Color Light", "colorlight"
                )
            ]
        _drop_stale_light("colorlight")
        return [InvisOutletNightlight(coordinator)]

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletNightlight(InvisOutletEntity, LightEntity):
    """The faceplate's dimmable white nightlight."""

    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes: ClassVar[set[ColorMode]] = {ColorMode.BRIGHTNESS}
    _attr_name = "Nightlight"

    def __init__(self, coordinator: InvisOutletCoordinator) -> None:
        """Initialize the nightlight."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_info.serial_number}_nightlight"

    @property
    def available(self) -> bool:
        """Gray the nightlight out while the faceplate is offline.

        It lives on the faceplate, so there's nothing to control until that's
        back up and streaming.
        """
        if not self.coordinator.sub_device_online:
            return False
        return super().available

    @property
    def is_on(self) -> bool:
        """Return whether the nightlight is on."""
        return (nl := self.coordinator.nightlight) is not None and nl.on

    @property
    def brightness(self) -> int | None:
        """Return the brightness (0-255), scaled from the device's 0-100."""
        if (nl := self.coordinator.nightlight) is None:
            return None
        return value_to_brightness(_BRIGHTNESS_SCALE, nl.brightness)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the nightlight on, optionally at a given brightness."""
        brightness: int | None = None
        if ATTR_BRIGHTNESS in kwargs:
            brightness = round(
                brightness_to_value(_BRIGHTNESS_SCALE, kwargs[ATTR_BRIGHTNESS])
            )
        try:
            await self.coordinator.async_set_nightlight(on=True, brightness=brightness)
        except InvisOutletError as err:
            raise HomeAssistantError(f"Could not set nightlight: {err}") from err

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the nightlight off."""
        try:
            await self.coordinator.async_set_nightlight(on=False)
        except InvisOutletError as err:
            raise HomeAssistantError(f"Could not set nightlight: {err}") from err


class InvisOutletColorLight(InvisOutletEntity, LightEntity):
    """An Aura color LED array (nightlight or indicator), set as one unit.

    Its effect dropdown lists the defined Aura Effect templates (plus "None").
    While an effect is selected the light exposes only on/off + brightness — the
    brightness acts as a master ceiling that scales the whole animation — and the
    effect keeps running across off/on. Selecting "None" restores the light's own
    color. The selection, that base color, and the master brightness all
    persist in the config entry (see CONF_COLOR_EFFECTS).
    """

    _attr_supported_features = LightEntityFeature.EFFECT
    _attr_min_color_temp_kelvin = MIN_KELVIN
    _attr_max_color_temp_kelvin = MAX_KELVIN

    def __init__(
        self, coordinator: InvisOutletCoordinator, light: int, name: str, key: str
    ) -> None:
        """Initialize a color array (``light`` is the device's light selector)."""
        super().__init__(coordinator)
        self._light = light
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.device_info.serial_number}_{key}"
        # The per-light record (effect selection, base color, master brightness)
        # is persisted in the entry so it survives the frequent reloads. It's kept
        # by stable effect id (not name, so renaming the effect device doesn't
        # drop it).
        outlet = coordinator.config_entry.data.get(CONF_OUTLETS, {}).get(
            coordinator.device_info.serial_number, {}
        )
        record = outlet.get(CONF_COLOR_EFFECTS, {}).get(str(light)) or {}
        self._selected_effect_id: str | None = record.get("effect")
        # The light's own color, kept so "None" can revert to it after a template
        # effect has overwritten the device's LEDs.
        base = record.get("base_hs")
        self._base_hs: tuple[float, float] | None = (base[0], base[1]) if base else None
        # The static base can be a color or a white temperature; remember both and
        # which was last set, so "Static" restores whichever the user had.
        self._base_temp: int | None = record.get("base_temp")
        self._base_is_temp: bool = record.get("base_is_temp", False)
        # Master brightness (0-255): the slider value, used as the ceiling that
        # effect pixel brightnesses render relative to. None until first set.
        self._master: int | None = record.get("master")
        # Cancels the subscription to the active effect template's entities.
        self._unsub_effect: CALLBACK_TYPE | None = None
        # The inputs of the last frame we pushed, to skip redundant re-applies.
        self._last_apply_key: object = None

    async def async_added_to_hass(self) -> None:
        """Apply the persisted selection, track its template, follow renames."""
        await super().async_added_to_hass()
        if self._selected_effect_id is not None:
            self._track_effect()
            await self._async_apply()
        # Re-render when an effect device is renamed, so the dropdown follows.
        self.async_on_remove(
            self.hass.bus.async_listen(
                EVENT_DEVICE_REGISTRY_UPDATED, self._device_registry_updated
            )
        )

    @callback
    def _persist(self) -> None:
        """Store this light's record (effect, base color, master) in the entry."""
        entry = self.coordinator.config_entry
        serial = self.coordinator.device_info.serial_number
        outlets = entry.data.get(CONF_OUTLETS, {})
        outlet = outlets.get(serial, {})
        record: dict[str, Any] = {}
        if self._selected_effect_id is not None:
            record["effect"] = self._selected_effect_id
        if self._base_hs is not None:
            record["base_hs"] = list(self._base_hs)
        if self._base_temp is not None:
            record["base_temp"] = self._base_temp
        if self._base_is_temp:
            record["base_is_temp"] = True
        if self._master is not None:
            record["master"] = self._master
        records = {**outlet.get(CONF_COLOR_EFFECTS, {})}
        if record:
            records[str(self._light)] = record
        else:
            records.pop(str(self._light), None)
        self.hass.config_entries.async_update_entry(
            entry,
            data={
                **entry.data,
                CONF_OUTLETS: {
                    **outlets,
                    serial: {**outlet, CONF_COLOR_EFFECTS: records},
                },
            },
        )

    async def async_will_remove_from_hass(self) -> None:
        """Drop the template subscription."""
        await super().async_will_remove_from_hass()
        if self._unsub_effect is not None:
            self._unsub_effect()
            self._unsub_effect = None

    def _effects(self) -> list[tuple[str, str]]:
        """(effect_id, display name) for every effect, honoring device renames.

        Sorted by display name (case-insensitive) so the dropdown reads
        alphabetically rather than in whatever order the effects were added.
        """
        dev_reg = dr.async_get(self.hass)
        effects: list[tuple[str, str]] = []
        for subentry in self.coordinator.config_entry.get_subentries_of_type(
            SUBENTRY_AURA_EFFECT
        ):
            for effect_id, effect in subentry.data.get(CONF_EFFECTS, {}).items():
                name = effect[CONF_NAME]
                device = dev_reg.async_get_device(identifiers={(DOMAIN, effect_id)})
                if device is not None:
                    name = device.name_by_user or device.name or name
                effects.append((effect_id, name))
        return sorted(effects, key=lambda effect: effect[1].casefold())

    def _effect_id_for_name(self, name: str) -> str | None:
        """Map a display name back to its effect id."""
        for effect_id, effect_name in self._effects():
            if effect_name == name:
                return effect_id
        return None

    def _matches_selection(self, cl: ColorLightState) -> bool:
        """Whether the device state matches our current selection (mode + colors).

        Recomputed from the persisted selection, so it's stateless / restart-safe.
        Only the LEDs we actually drive are compared (off pixels aren't sent,
        static collapses to one); "random" modes compare mode only, since the
        device picks its own colors.
        """
        if self._selected_effect_id is None:
            return cl.mode < 3  # "Static": any static device state is us
        data = effect_data(self.coordinator.config_entry, self._selected_effect_id)
        mode = get_effect_mode(data.get("mode"))
        if cl.mode != mode.device_mode:
            return False
        pixels = self._resolve_pixels(data, mode)
        if not pixels:
            return True
        pixels_kind = mode.pixels(bool(data.get("random", False)))[0].kind
        if pixels_kind is PixelKind.BRIGHTNESS:
            return True  # random: the device chooses the colors
        if pixels_kind is PixelKind.TEMPERATURE:
            want = [p.temperature for p in pixels]
            have = [led.temperature for led in cl.leds[: len(want)]]
            return have == want
        want = [(p.hue, p.saturation) for p in pixels if p.on]
        have = [
            (int(led.hue or 0), int(led.saturation or 0))
            for led in cl.leds[: len(want)]
        ]
        return have == want

    @property
    def _external(self) -> bool:
        """Whether the device is running an animated effect we can't render.

        Static states are renderable (we drop to "Static"), so only an unmatched
        animated mode (3-7) counts as external.
        """
        cl = self._state
        return cl is not None and cl.mode >= 3 and not self._matches_selection(cl)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Adopt "Static" when an external source sets a static color we can show."""
        cl = self._state
        if (
            cl is not None
            and cl.mode < 3
            and cl.leds
            and cl.leds[0].state  # only adopt a static color while actually on
            and self._selected_effect_id is not None
            and not self._matches_selection(cl)
        ):
            self._selected_effect_id = None
            led = cl.leds[0] if cl.leds else None
            if led is not None:
                if cl.mode == 2 and led.temperature is not None:
                    self._base_temp = led.temperature
                    self._base_is_temp = True
                elif led.hue is not None and led.saturation is not None:
                    self._base_hs = (led.hue, led.saturation)
                    self._base_is_temp = False
            self._persist()
            self._track_effect()
        super()._handle_coordinator_update()

    @property
    def _external_name(self) -> str:
        """The external entry's label, e.g. "Rainbow (External)" from the mode."""
        cl = self._state
        label = mode_label(cl.mode) if cl is not None else None
        return f"{label} ({EFFECT_EXTERNAL})" if label else EFFECT_EXTERNAL

    @property
    def effect_list(self) -> list[str]:
        """ "Static" first, then every effect; the external entry while out of control."""
        names = [EFFECT_NONE, *(name for _, name in self._effects())]
        if self._external:
            names.append(self._external_name)
        return names

    @property
    def effect(self) -> str:
        """The current effect name; the external label when something else drives it."""
        if self._external:
            return self._external_name
        for effect_id, name in self._effects():
            if effect_id == self._selected_effect_id:
                return name
        return EFFECT_NONE

    @callback
    def _device_registry_updated(self, event: Event) -> None:
        """Re-render when one of the effect devices is renamed."""
        if event.data.get("action") != "update":
            return
        effect_ids = {effect_id for effect_id, _ in self._effects()}
        device = dr.async_get(self.hass).async_get(event.data["device_id"])
        if device is not None and any(
            i[0] == DOMAIN and i[1] in effect_ids for i in device.identifiers
        ):
            self.async_write_ha_state()

    @callback
    def _track_effect(self) -> None:
        """(Re)subscribe to the active template's select + pixel entities."""
        if self._unsub_effect is not None:
            self._unsub_effect()
            self._unsub_effect = None
        effect_id = self._selected_effect_id
        if effect_id is None:
            return
        registry = er.async_get(self.hass)
        # Re-apply when any of the effect's controls change.
        targets = [
            ("select", f"{effect_id}_effect"),
            ("number", f"{effect_id}_speed"),
            ("switch", f"{effect_id}_random"),
            *(("light", f"{effect_id}_pixel_{i}") for i in range(_EFFECT_PIXELS)),
        ]
        entity_ids = [
            eid
            for domain, uid in targets
            if (eid := registry.async_get_entity_id(domain, DOMAIN, uid))
        ]
        if entity_ids:
            self._unsub_effect = async_track_state_change_event(
                self.hass, entity_ids, self._template_changed
            )

    @callback
    def _template_changed(self, event: Event[EventStateChangedData]) -> None:
        """Re-apply when the active effect template's entities change."""
        self.hass.async_create_task(self._async_apply())

    def _apply_key(self) -> object:
        """A hashable snapshot of everything that shapes the frame we'd send.

        Lets us skip redundant re-applies (e.g. template entities settling at
        startup all fire identical applies).
        """
        if self._selected_effect_id is None:
            return (
                "base",
                self._base_hs,
                self._base_temp,
                self._base_is_temp,
                self._master,
            )
        data = effect_data(self.coordinator.config_entry, self._selected_effect_id)
        return (
            "effect",
            self._selected_effect_id,
            self._master,
            json.dumps(data, sort_keys=True, default=list),
        )

    async def _async_apply(self, force: bool = False) -> None:
        """Resolve the selected effect to the physical array.

        ``force`` re-applies even while external / unchanged (the user explicitly
        reasserting control).
        """
        # The selected template was deleted: fall back to None.
        if self._selected_effect_id is not None and not any(
            effect_id == self._selected_effect_id for effect_id, _ in self._effects()
        ):
            self._selected_effect_id = None
            self._track_effect()
            self._persist()
            self.async_write_ha_state()
        # Something else is driving the array — stay passive unless reasserting.
        if self._external and not force:
            return
        key = self._apply_key()
        if not force and key == self._last_apply_key:
            return
        self._last_apply_key = key
        try:
            if self._selected_effect_id is None:
                await self._async_apply_base()
            else:
                await self._async_apply_template(self._selected_effect_id)
        except InvisOutletError as err:
            _LOGGER.warning("Could not apply effect to %s: %s", self.name, err)

    def _master_device_brightness(self) -> int:
        """The master brightness as the device's 0-100 scale (full when unset)."""
        master = self._master if self._master is not None else 255
        return round(brightness_to_value(_BRIGHTNESS_SCALE, master))

    async def _async_apply_base(self) -> None:
        """Set the array to this light's own color/temperature at master brightness."""
        if self._base_is_temp and self._base_temp is not None:
            await self.coordinator.async_set_color_temperature(
                self._light,
                kelvin=self._base_temp,
                brightness=self._master_device_brightness(),
            )
            return
        hs = self._base_hs
        if hs is None:
            led = self._led
            hs = (led.hue or 0, led.saturation or 0) if led is not None else (0, 0)
        await self.coordinator.async_set_color_hsv(
            self._light,
            hue=int(hs[0]),
            saturation=int(hs[1]),
            brightness=self._master_device_brightness(),
        )

    def _resolve_pixels(
        self, data: dict[str, Any], mode: EffectMode
    ) -> list[PixelState]:
        """The active pixels' resolved state (brightness scaled by master)."""
        random = bool(data.get("random", False))
        master_fraction = (self._master if self._master is not None else 255) / 255
        pixels: list[PixelState] = []
        for index in range(len(mode.pixels(random))):
            pixel = data.get(f"pixel_{index}", {})
            hs = pixel.get("hs", (0, 0))
            level = pixel.get("brightness", 255) * master_fraction
            pixels.append(
                PixelState(
                    on=pixel.get("on", False),
                    hue=int(hs[0]),
                    saturation=int(hs[1]),
                    brightness=round(brightness_to_value(_BRIGHTNESS_SCALE, level)),
                    temperature=pixel.get("temp", 4000),
                )
            )
        return pixels

    async def _async_apply_template(self, effect_id: str) -> None:
        """Hand the template's mode + pixel state to that mode's payload.

        Each pixel's brightness is scaled by the master brightness, so the slider
        dims the whole animation (pixel 50% at master 50% renders 25%).
        """
        data = effect_data(self.coordinator.config_entry, effect_id)
        mode = get_effect_mode(data.get("mode"))
        pixels = self._resolve_pixels(data, mode)
        if pixels:
            await mode.apply(
                ApplyContext(
                    self.coordinator,
                    self._light,
                    pixels,
                    data.get("speed", 0),
                    bool(data.get("random", False)),
                )
            )

    @property
    def _state(self) -> ColorLightState | None:
        """This array's last-known state."""
        return self.coordinator.color_lights.get(self._light)

    @property
    def _led(self) -> ColorLedEntry | None:
        """The first LED, taken as the array's representative color."""
        cl = self._state
        return cl.leds[0] if cl is not None and cl.leds else None

    @property
    def available(self) -> bool:
        """Gray out while the faceplate is offline (see InvisOutletNightlight)."""
        if not self.coordinator.sub_device_online:
            return False
        return super().available

    @property
    def _effect_active(self) -> bool:
        """Whether an effect (ours or external) is driving the array — no color picker."""
        return self._selected_effect_id is not None or self._external

    @property
    def supported_color_modes(self) -> set[ColorMode]:
        """Only brightness while an effect runs; full color otherwise."""
        if self._effect_active:
            return {ColorMode.BRIGHTNESS}
        return {ColorMode.HS, ColorMode.COLOR_TEMP}

    @property
    def color_mode(self) -> ColorMode:
        """Brightness while an effect runs, else HS / color-temp per the array."""
        if self._effect_active:
            return ColorMode.BRIGHTNESS
        cl = self._state
        if cl is not None and cl.mode == _COLOR_MODE_TEMPERATURE:
            return ColorMode.COLOR_TEMP
        return ColorMode.HS

    @property
    def is_on(self) -> bool:
        """Return whether the array is on."""
        return (led := self._led) is not None and led.state

    @property
    def brightness(self) -> int | None:
        """Return the brightness (0-255): the master while set, else the array's."""
        if self._master is not None:
            return self._master
        if (led := self._led) is None:
            return None
        return value_to_brightness(_BRIGHTNESS_SCALE, led.brightness)

    @property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the array's hue/saturation (hidden while an effect runs)."""
        led = self._led
        if (
            self._effect_active
            or led is None
            or led.hue is None
            or led.saturation is None
        ):
            return None
        return (led.hue, led.saturation)

    @property
    def color_temp_kelvin(self) -> int | None:
        """Return the white temperature when in color-temp mode."""
        cl = self._state
        if (
            self._effect_active
            or cl is None
            or cl.mode != _COLOR_MODE_TEMPERATURE
            or self._led is None
        ):
            return None
        return self._led.temperature

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Expose the full per-LED palette (RGB) — the part the light card can't show."""
        cl = self._state
        if cl is None:
            return None
        return {
            "colors": [
                list(color_hs_to_RGB(led.hue or 0, led.saturation or 0))
                for led in cl.leds
            ]
        }

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Select an effect, or set a color/temperature/brightness."""
        if ATTR_EFFECT in kwargs:
            name = kwargs[ATTR_EFFECT]
            # The external entry ("External" / "… (External)") isn't selectable.
            if name == EFFECT_EXTERNAL or name.endswith(f" ({EFFECT_EXTERNAL})"):
                return
            new_id = None if name == EFFECT_NONE else self._effect_id_for_name(name)
            # Snapshot the current color before an effect takes over the LEDs, so
            # "None" can restore it later even if no color was ever set by hand.
            if new_id is not None and self._base_hs is None:
                led = self._led
                if (
                    led is not None
                    and led.hue is not None
                    and led.saturation is not None
                ):
                    self._base_hs = (led.hue, led.saturation)
            self._selected_effect_id = new_id
            self._persist()
            self._track_effect()
            # Force: the user is explicitly (re)taking control, even from External.
            await self._async_apply(force=True)
            self.async_write_ha_state()
            return

        # No effect toggled: update master brightness / base color or temp, apply.
        if ATTR_BRIGHTNESS in kwargs:
            self._master = kwargs[ATTR_BRIGHTNESS]
        if ATTR_HS_COLOR in kwargs:
            self._base_hs = kwargs[ATTR_HS_COLOR]
            self._base_is_temp = False
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            self._base_temp = kwargs[ATTR_COLOR_TEMP_KELVIN]
            self._base_is_temp = True
        self._persist()

        # Stay passive while another controller owns the array.
        if self._external:
            self.async_write_ha_state()
            return

        try:
            if self._effect_active:
                # Brightness-only while an effect runs: resume/rescale the
                # animation at the new master brightness (never a static color).
                await self._async_apply_template(self._selected_effect_id)
            else:
                # Static: apply whichever base (color or temperature) is current.
                await self._async_apply_base()
        except InvisOutletError as err:
            raise HomeAssistantError(f"Could not set {self.name}: {err}") from err
        # Keep the dedupe key in step with what we just pushed.
        self._last_apply_key = self._apply_key()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the array off, keeping its color for the next turn-on."""
        led = self._led
        try:
            await self.coordinator.async_set_color_hsv(
                self._light,
                hue=led.hue if led and led.hue is not None else 0,
                saturation=led.saturation if led and led.saturation is not None else 0,
                brightness=led.brightness if led is not None else 0,
                on=False,
            )
        except InvisOutletError as err:
            raise HomeAssistantError(f"Could not set {self.name}: {err}") from err


class AuraEffectVirtualLight(LightEntity):
    """A virtual HSV pixel of one Aura effect template.

    It only holds on/off, color and brightness — it drives no hardware and is
    tied to no outlet. State lives in the effect's subentry data (written on
    every change), so it survives reloads, restarts, and entity-id churn.
    """

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_min_color_temp_kelvin = MIN_KELVIN
    _attr_max_color_temp_kelvin = MAX_KELVIN
    # Created hidden: the pixels are edit-time controls, not everyday entities, so
    # they stay out of dashboards and pickers until the user unhides them.
    _attr_entity_registry_visible_default = False

    def __init__(
        self, entry: InvisOutletConfigEntry, effect_id: str, name: str, index: int
    ) -> None:
        """Initialize pixel ``index`` (0-based; surfaced 1-based) of one effect."""
        self._entry = entry
        self._effect_id = effect_id
        self._index = index
        self._attr_unique_id = f"{effect_id}_pixel_{index}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, effect_id)},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
        )
        pixel = effect_data(entry, effect_id).get(f"pixel_{index}", {})
        self._attr_is_on = pixel.get("on", False)
        self._attr_brightness = pixel.get("brightness", 255)
        hs = pixel.get("hs", (0.0, 0.0))
        self._attr_hs_color = (float(hs[0]), float(hs[1]))
        self._attr_color_temp_kelvin = pixel.get("temp", 4000)

    @property
    def _spec(self) -> PixelSpec | None:
        """This pixel's role in the current mode/random state (None = inactive)."""
        data = effect_data(self._entry, self._effect_id)
        mode = get_effect_mode(data.get("mode"))
        return mode.spec(self._index, bool(data.get("random", False)))

    @property
    def name(self) -> str:
        """The mode's display name for this pixel; 'Unused' when inactive (sorts last)."""
        spec = self._spec
        return spec.name if spec is not None else "Unused"

    @property
    def available(self) -> bool:
        """Gray out pixels the current mode/random state doesn't use."""
        return self._spec is not None

    @property
    def color_mode(self) -> ColorMode:
        """HS, temperature, or brightness-only per the pixel's role."""
        return _COLOR_MODES.get(
            self._spec.kind if self._spec is not None else PixelKind.HS, ColorMode.HS
        )

    @property
    def supported_color_modes(self) -> set[ColorMode]:
        """Advertise only the color mode this pixel's role uses."""
        return {self.color_mode}

    @property
    def _forced_on(self) -> bool:
        """Whether the current mode forces this pixel on."""
        return (spec := self._spec) is not None and spec.forced_on

    async def async_added_to_hass(self) -> None:
        """Re-render when the effect mode (or random) changes."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                effect_mode_signal(self._effect_id),
                self.async_write_ha_state,
            )
        )

    @callback
    def _persist(self) -> None:
        """Write this pixel's state into the effect's subentry data."""
        async_update_effect_data(
            self.hass,
            self._entry,
            self._effect_id,
            {
                f"pixel_{self._index}": {
                    "on": self._attr_is_on,
                    "hs": list(self._attr_hs_color),
                    "brightness": self._attr_brightness,
                    "temp": self._attr_color_temp_kelvin,
                }
            },
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Store the new color/temperature/brightness; no hardware is touched."""
        self._attr_is_on = True
        if ATTR_HS_COLOR in kwargs:
            self._attr_hs_color = kwargs[ATTR_HS_COLOR]
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            self._attr_color_temp_kelvin = kwargs[ATTR_COLOR_TEMP_KELVIN]
        if ATTR_BRIGHTNESS in kwargs:
            self._attr_brightness = kwargs[ATTR_BRIGHTNESS]
        self._persist()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Store the off state; refused for pixels the mode forces on."""
        if self._forced_on:
            # Bounce off→on so the optimistic UI corrects at once (a same-state
            # write fires no event, so it'd otherwise wait to revert).
            self._attr_is_on = False
            self.async_write_ha_state()
            self._attr_is_on = True
            self.async_write_ha_state()
            return
        self._attr_is_on = False
        self._persist()
        self.async_write_ha_state()
