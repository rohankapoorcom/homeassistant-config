"""Binary sensor platform for the InvisOutlet integration (occupancy/motion)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from invisoutlet import SensorData

from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import InvisOutletEntity
from .helpers import async_add_outlet_entities, supported_for_faceplate


@dataclass(frozen=True, kw_only=True)
class InvisOutletBinarySensorDescription(BinarySensorEntityDescription):
    """Describes an InvisOutlet binary sensor and how to read its value."""

    value_fn: Callable[[SensorData], bool | None]


BINARY_SENSORS: tuple[InvisOutletBinarySensorDescription, ...] = (
    InvisOutletBinarySensorDescription(
        key="occupancy",
        device_class=BinarySensorDeviceClass.OCCUPANCY,
        value_fn=lambda data: data.occupancy,
    ),
    InvisOutletBinarySensorDescription(
        key="motion",
        device_class=BinarySensorDeviceClass.MOTION,
        value_fn=lambda data: data.motion,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the binary sensors the faceplate reports (see sensor.py)."""

    def build(coordinator: InvisOutletCoordinator) -> list[BinarySensorEntity]:
        supported = supported_for_faceplate(
            hass,
            coordinator,
            Platform.BINARY_SENSOR,
            BINARY_SENSORS,
            coordinator.sensor,
        )
        return [
            InvisOutletBinarySensor(coordinator, description)
            for description in supported
        ]

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletBinarySensor(InvisOutletEntity, BinarySensorEntity):
    """A single occupancy/motion binary sensor."""

    entity_description: InvisOutletBinarySensorDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletBinarySensorDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )

    @property
    def is_on(self) -> bool | None:
        """Return the current state, or None until the first push arrives."""
        if (data := self.coordinator.sensor) is None:
            return None
        return self.entity_description.value_fn(data)
