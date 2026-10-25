"""Switch platform: the outlets, plus the boolean device-config settings."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import (
    SwitchDeviceClass,
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.const import CONF_NAME, EntityCategory, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from invisoutlet import DeviceConfig

from .const import CONF_EFFECTS, DOMAIN, SUBENTRY_AURA_EFFECT
from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .effects import get_effect_mode
from .entity import InvisOutletEntity
from .helpers import (
    async_add_outlet_entities,
    async_update_effect_data,
    effect_data,
    effect_mode_signal,
    supported_for_faceplate,
)


@dataclass(frozen=True, kw_only=True)
class InvisOutletConfigSwitchDescription(SwitchEntityDescription):
    """A boolean device-config setting. ``key`` is the ``set_config`` field."""

    value_fn: Callable[[DeviceConfig], bool | None]


CONFIG_SWITCHES: tuple[InvisOutletConfigSwitchDescription, ...] = (
    InvisOutletConfigSwitchDescription(
        key="outlet_power_indicator_on",
        name="Outlet power indicator",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.outlet_power_indicator_on,
    ),
    InvisOutletConfigSwitchDescription(
        key="capacitive_ctrl",
        name="Capacitive control",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.capacitive_ctrl,
    ),
    InvisOutletConfigSwitchDescription(
        key="magic_touch_ctrl",
        name="Magic-touch control",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.magic_touch_ctrl,
    ),
    InvisOutletConfigSwitchDescription(
        key="aqi_color_rgb_feature",
        name="AQI color RGB",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.aqi_color_rgb_feature,
    ),
    InvisOutletConfigSwitchDescription(
        key="motion_away_feature",
        name="Motion away",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.motion_away_feature,
    ),
    InvisOutletConfigSwitchDescription(
        key="adaptive_nightlight_feature",
        name="Adaptive nightlight",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.adaptive_nightlight_feature,
    ),
    InvisOutletConfigSwitchDescription(
        key="occupancy_nightlight_feature",
        name="Occupancy nightlight",
        entity_category=EntityCategory.CONFIG,
        value_fn=lambda c: c.occupancy_nightlight_feature,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the outlets and config switches for a config entry."""
    # A Random toggle per Aura effect template; grays out unless the mode uses it.
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        for effect_id, effect in subentry.data.get(CONF_EFFECTS, {}).items():
            async_add_entities(
                [AuraEffectRandomSwitch(entry, effect_id, effect[CONF_NAME])],
                config_subentry_id=subentry.subentry_id,
            )

    def build(coordinator: InvisOutletCoordinator) -> list[SwitchEntity]:
        entities: list[SwitchEntity] = [
            InvisOutletOutlet(coordinator, index)
            for index in range(len(coordinator.data.outlets))
        ]
        config_switches = supported_for_faceplate(
            hass, coordinator, Platform.SWITCH, CONFIG_SWITCHES, coordinator.config
        )
        entities.extend(
            InvisOutletConfigSwitch(coordinator, description)
            for description in config_switches
        )
        return entities

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletOutlet(InvisOutletEntity, SwitchEntity):
    """A switchable outlet."""

    _attr_device_class = SwitchDeviceClass.OUTLET
    _attr_translation_key = "outlet"

    def __init__(self, coordinator: InvisOutletCoordinator, index: int) -> None:
        """Initialize the outlet (``index`` is 0-based; outlets are 1-based)."""
        super().__init__(coordinator)
        self._outlet = index + 1
        self._attr_translation_placeholders = {"number": str(self._outlet)}
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_outlet_{self._outlet}"
        )

    @property
    def is_on(self) -> bool:
        """Return whether the outlet is on."""
        return self.coordinator.data.outlets[self._outlet - 1]

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the outlet on."""
        await self.coordinator.client.set_outlet(self._outlet, True)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the outlet off."""
        await self.coordinator.client.set_outlet(self._outlet, False)
        await self.coordinator.async_request_refresh()


class InvisOutletConfigSwitch(InvisOutletEntity, SwitchEntity):
    """A boolean device-config setting."""

    entity_description: InvisOutletConfigSwitchDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletConfigSwitchDescription,
    ) -> None:
        """Initialize the config switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return the current setting value."""
        return self.entity_description.value_fn(self.coordinator.config)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable the setting."""
        await self.coordinator.async_set_config(**{self.entity_description.key: True})

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable the setting."""
        await self.coordinator.async_set_config(**{self.entity_description.key: False})


class AuraEffectRandomSwitch(SwitchEntity):
    """The per-effect 'Random' toggle (state only); grays out unless the mode uses it."""

    _attr_has_entity_name = True
    _attr_name = "Random"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_should_poll = False

    def __init__(
        self, entry: InvisOutletConfigEntry, effect_id: str, name: str
    ) -> None:
        """Initialize the random toggle for one effect's device."""
        self._entry = entry
        self._effect_id = effect_id
        self._attr_unique_id = f"{effect_id}_random"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, effect_id)},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
        )
        self._attr_is_on = bool(effect_data(entry, effect_id).get("random", False))

    @property
    def available(self) -> bool:
        """Only effects whose mode uses randomisation expose this."""
        mode = get_effect_mode(effect_data(self._entry, self._effect_id).get("mode"))
        return mode.has_random

    async def async_added_to_hass(self) -> None:
        """Re-render availability when the effect mode changes."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                effect_mode_signal(self._effect_id),
                self.async_write_ha_state,
            )
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable randomisation."""
        await self._async_set(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable randomisation."""
        await self._async_set(False)

    async def _async_set(self, value: bool) -> None:
        """Persist the toggle and re-render the effect's pixels."""
        self._attr_is_on = value
        async_update_effect_data(
            self.hass, self._entry, self._effect_id, {"random": value}
        )
        self.async_write_ha_state()
        async_dispatcher_send(self.hass, effect_mode_signal(self._effect_id))
