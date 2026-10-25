"""Select platform: how the attached faceplate's firmware is delivered."""

from __future__ import annotations

from typing import ClassVar

from homeassistant.components.select import SelectEntity
from homeassistant.const import CONF_NAME, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import (
    CONF_EFFECTS,
    CONF_OUTLETS,
    CONF_SUB_DEVICE_UPDATE_METHOD,
    DEFAULT_SUB_DEVICE_UPDATE_METHOD,
    DOMAIN,
    EFFECT_STATIC_COLOR,
    EFFECT_STATIC_TEMPERATURE,
    SUBENTRY_AURA_EFFECT,
)
from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import InvisOutletEntity
from .helpers import (
    async_add_outlet_entities,
    async_update_effect_data,
    effect_data,
    effect_mode_signal,
)

# Display label -> device method (callback 21 arg 1): 0 = the faceplate's own
# Wi-Fi, 1 = relayed via the InvisOutlet it's attached to.
_METHODS = {"Wi-Fi": 0, "Via InvisOutlet": 1}
_LABELS = {value: label for label, value in _METHODS.items()}

# Animated Aura effect options (machine values) offered by the effect-mode
# select, alongside the two static variants. The option -> device effect mode
# mapping lives in effects.py; here we only need the option names. Labels live in
# strings.json (selector.aura_effect).
_EFFECT_OPTIONS = (
    "breathing",
    "strobing",
    "color_cycle",
    "rainbow",
    "starry_night",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the per-effect mode selects and the per-outlet selects."""
    # One effect-mode select per added effect's virtual device: state only, no
    # hardware — mirrors the virtual pixel lights.
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        for effect_id, effect in subentry.data.get(CONF_EFFECTS, {}).items():
            async_add_entities(
                [AuraEffectVirtualSelect(entry, effect_id, effect[CONF_NAME])],
                config_subentry_id=subentry.subentry_id,
            )

    def build(coordinator: InvisOutletCoordinator) -> list[SelectEntity]:
        sub = coordinator.device_info.sub_device
        if sub is None:
            return []
        return [InvisOutletUpdateMethodSelect(coordinator)]

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletUpdateMethodSelect(InvisOutletEntity, SelectEntity):
    """Choose how the attached faceplate's firmware update is delivered."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_options: ClassVar[list[str]] = list(_METHODS)

    def __init__(self, coordinator: InvisOutletCoordinator) -> None:
        """Initialize the select."""
        super().__init__(coordinator)
        self._attr_name = f"{coordinator.sub_device_name} update method"
        self._attr_unique_id = f"{coordinator.device_info.serial_number}_update_method"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Refresh the name when the model repopulates from a degraded state."""
        self._attr_name = f"{self.coordinator.sub_device_name} update method"
        super()._handle_coordinator_update()

    @property
    def current_option(self) -> str | None:
        """Return the currently selected method label."""
        serial = self.coordinator.device_info.serial_number
        outlet = self.coordinator.config_entry.data[CONF_OUTLETS].get(serial, {})
        value = outlet.get(
            CONF_SUB_DEVICE_UPDATE_METHOD, DEFAULT_SUB_DEVICE_UPDATE_METHOD
        )
        return _LABELS.get(value)

    async def async_select_option(self, option: str) -> None:
        """Persist the chosen method in this outlet's stored config."""
        entry = self.coordinator.config_entry
        serial = self.coordinator.device_info.serial_number
        outlets = entry.data[CONF_OUTLETS]
        self.hass.config_entries.async_update_entry(
            entry,
            data={
                **entry.data,
                CONF_OUTLETS: {
                    **outlets,
                    serial: {
                        **outlets[serial],
                        CONF_SUB_DEVICE_UPDATE_METHOD: _METHODS[option],
                    },
                },
            },
        )
        self.async_write_ha_state()


class AuraEffectVirtualSelect(SelectEntity):
    """Effect mode for one Aura effect template.

    Holds the chosen mode as state only — no hardware. Stored in the effect's
    subentry data (written on change), so it survives reloads and restarts.
    """

    _attr_has_entity_name = True
    _attr_translation_key = "aura_effect"
    _attr_options: ClassVar[list[str]] = [
        EFFECT_STATIC_COLOR,
        EFFECT_STATIC_TEMPERATURE,
        *_EFFECT_OPTIONS,
    ]
    _attr_entity_category = EntityCategory.CONFIG
    _attr_should_poll = False

    def __init__(
        self, entry: InvisOutletConfigEntry, effect_id: str, name: str
    ) -> None:
        """Initialize the virtual effect select for one effect's device."""
        self._entry = entry
        self._effect_id = effect_id
        self._attr_unique_id = f"{effect_id}_effect"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, effect_id)},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
        )
        mode = effect_data(entry, effect_id).get("mode", EFFECT_STATIC_COLOR)
        self._attr_current_option = (
            mode if mode in self._attr_options else EFFECT_STATIC_COLOR
        )

    async def async_added_to_hass(self) -> None:
        """Announce the current mode to this effect's pixels (setup-order safe)."""
        await super().async_added_to_hass()
        async_dispatcher_send(self.hass, effect_mode_signal(self._effect_id))

    async def async_select_option(self, option: str) -> None:
        """Store the chosen mode (no hardware) and notify the pixels."""
        self._attr_current_option = option
        async_update_effect_data(
            self.hass, self._entry, self._effect_id, {"mode": option}
        )
        self.async_write_ha_state()
        async_dispatcher_send(self.hass, effect_mode_signal(self._effect_id))
