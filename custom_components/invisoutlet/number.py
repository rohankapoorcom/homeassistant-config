"""Number platform: the numeric device-config settings (brightness)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import CONF_NAME, EntityCategory, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
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
class InvisOutletConfigNumberDescription(NumberEntityDescription):
    """A numeric device-config setting. ``key`` is the ``set_config`` field."""

    value_fn: Callable[[DeviceConfig], int | None]


CONFIG_NUMBERS: tuple[InvisOutletConfigNumberDescription, ...] = (
    InvisOutletConfigNumberDescription(
        key="pm_indicator_brightness",
        name="PM indicator brightness",
        entity_category=EntityCategory.CONFIG,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda c: c.pm_indicator_brightness,
    ),
    InvisOutletConfigNumberDescription(
        key="adaptive_min_brightness",
        name="Adaptive minimum brightness",
        entity_category=EntityCategory.CONFIG,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda c: c.adaptive_min_brightness,
    ),
    InvisOutletConfigNumberDescription(
        key="adaptive_max_brightness",
        name="Adaptive maximum brightness",
        entity_category=EntityCategory.CONFIG,
        native_min_value=0,
        native_max_value=100,
        native_step=1,
        mode=NumberMode.SLIDER,
        value_fn=lambda c: c.adaptive_max_brightness,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the numeric config settings the faceplate reports (see sensor.py)."""
    # A speed slider per Aura effect template (state only).
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        for effect_id, effect in subentry.data.get(CONF_EFFECTS, {}).items():
            async_add_entities(
                [AuraEffectSpeedNumber(entry, effect_id, effect[CONF_NAME])],
                config_subentry_id=subentry.subentry_id,
            )

    def build(coordinator: InvisOutletCoordinator) -> list[NumberEntity]:
        supported = supported_for_faceplate(
            hass, coordinator, Platform.NUMBER, CONFIG_NUMBERS, coordinator.config
        )
        return [
            InvisOutletConfigNumber(coordinator, description)
            for description in supported
        ]

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletConfigNumber(InvisOutletEntity, NumberEntity):
    """A numeric device-config setting."""

    entity_description: InvisOutletConfigNumberDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletConfigNumberDescription,
    ) -> None:
        """Initialize the config number."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )

    @property
    def native_value(self) -> float | None:
        """Return the current setting value."""
        return self.entity_description.value_fn(self.coordinator.config)

    async def async_set_native_value(self, value: float) -> None:
        """Write the new setting value."""
        await self.coordinator.async_set_config(
            **{self.entity_description.key: int(value)}
        )


class AuraEffectSpeedNumber(NumberEntity):
    """Animation speed for one Aura effect template (state only, no hardware).

    Stored in the effect's subentry data (written on change) so it survives
    reloads and restarts.
    """

    _attr_has_entity_name = True
    _attr_name = "Speed"
    _attr_native_min_value = 0
    _attr_native_max_value = 7
    _attr_native_step = 1
    _attr_mode = NumberMode.SLIDER
    _attr_entity_category = EntityCategory.CONFIG
    _attr_should_poll = False

    def __init__(
        self, entry: InvisOutletConfigEntry, effect_id: str, name: str
    ) -> None:
        """Initialize the speed slider for one effect's device."""
        self._entry = entry
        self._effect_id = effect_id
        self._attr_unique_id = f"{effect_id}_speed"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, effect_id)},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
        )
        self._attr_native_value = effect_data(entry, effect_id).get("speed", 0)

    @property
    def available(self) -> bool:
        """Gray out for modes that don't use speed (e.g. the static modes)."""
        mode = effect_data(self._entry, self._effect_id).get("mode")
        return get_effect_mode(mode).has_speed

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

    async def async_set_native_value(self, value: float) -> None:
        """Store the new speed; no hardware is touched."""
        self._attr_native_value = value
        async_update_effect_data(
            self.hass, self._entry, self._effect_id, {"speed": value}
        )
        self.async_write_ha_state()
