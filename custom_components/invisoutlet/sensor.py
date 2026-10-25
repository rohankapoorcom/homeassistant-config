"""Sensor platform for the InvisOutlet integration (environmental readings)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    LIGHT_LUX,
    PERCENTAGE,
    EntityCategory,
    Platform,
    UnitOfLength,
    UnitOfPressure,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from invisoutlet import SensorData

from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import InvisOutletEntity
from .helpers import async_add_outlet_entities, supported_for_faceplate


def _device_status(coordinator: InvisOutletCoordinator) -> str:
    """Return a one-line device-health status for the status sensor.

    - A blank ``fw_rev`` means that module is in a bad state and needs a restart.
    - Otherwise, if a faceplate is attached but not streaming (no recent sensor
      push), it hasn't come back up yet — we're waiting on it.

    Both are named by the module's model, so the Aura reads naturally too.
    """
    info = coordinator.device_info
    if not info.fw_rev:
        return f"{coordinator.outlet_name} needs restart"
    sub = info.sub_device
    if sub is not None:
        name = coordinator.sub_device_name
        # While the faceplate is offline we always show "Waiting", even if we
        # already know it needs a restart — only surface that once it's back.
        if not coordinator.sub_device_online:
            return f"Waiting for {name}"
        if not sub.fw_rev:
            return f"{name} needs restart"
    return "OK"


@dataclass(frozen=True, kw_only=True)
class InvisOutletSensorDescription(SensorEntityDescription):
    """Describes an InvisOutlet sensor and how to read its value."""

    value_fn: Callable[[SensorData], float | int | None]


SENSORS: tuple[InvisOutletSensorDescription, ...] = (
    InvisOutletSensorDescription(
        key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.temperature,
    ),
    InvisOutletSensorDescription(
        key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.humidity,
    ),
    InvisOutletSensorDescription(
        key="air_quality_index",
        device_class=SensorDeviceClass.AQI,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.air_quality_index,
    ),
    InvisOutletSensorDescription(
        key="co2",
        device_class=SensorDeviceClass.CO2,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.co2,
    ),
    InvisOutletSensorDescription(
        key="voc",
        device_class=SensorDeviceClass.VOLATILE_ORGANIC_COMPOUNDS_PARTS,
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.voc,
    ),
    InvisOutletSensorDescription(
        key="pressure",
        device_class=SensorDeviceClass.ATMOSPHERIC_PRESSURE,
        native_unit_of_measurement=UnitOfPressure.PA,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.pressure,
    ),
    InvisOutletSensorDescription(
        key="illuminance",
        device_class=SensorDeviceClass.ILLUMINANCE,
        native_unit_of_measurement=LIGHT_LUX,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.illuminance,
    ),
    InvisOutletSensorDescription(
        key="distance",
        device_class=SensorDeviceClass.DISTANCE,
        native_unit_of_measurement=UnitOfLength.MILLIMETERS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.distance,
    ),
)


@dataclass(frozen=True, kw_only=True)
class InvisOutletDiagnosticDescription(SensorEntityDescription):
    """Describes a connection-health sensor read off the coordinator."""

    value_fn: Callable[[InvisOutletCoordinator], str | int | datetime | None]


# Connection-health sensors, for telling apart a dropping connection from a
# faceplate that has gone quiet behind a healthy one. Off by default: useful
# when diagnosing a report, noise on a working install.
DIAGNOSTICS: tuple[InvisOutletDiagnosticDescription, ...] = (
    InvisOutletDiagnosticDescription(
        key="transport",
        translation_key="transport",
        device_class=SensorDeviceClass.ENUM,
        options=["tcp", "ws"],
        value_fn=lambda c: c.client.transport_name,
    ),
    InvisOutletDiagnosticDescription(
        key="reconnects",
        translation_key="reconnects",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.reconnects,
    ),
    InvisOutletDiagnosticDescription(
        key="faceplate_dropouts",
        translation_key="faceplate_dropouts",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda c: c.faceplate_dropouts,
    ),
    InvisOutletDiagnosticDescription(
        key="connected_since",
        translation_key="connected_since",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda c: c.connected_since,
    ),
    InvisOutletDiagnosticDescription(
        key="last_sensor_push",
        translation_key="last_sensor_push",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda c: c.last_sensor_push,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the sensors for a config entry.

    The attached faceplate only reports the sensors it actually has (it omits the
    rest), so create only those and remove any left over from a different
    faceplate. If the initial read failed we don't know the set yet, so fall back
    to creating them all and skip the cleanup.
    """
    def build(coordinator: InvisOutletCoordinator) -> list[SensorEntity]:
        supported = supported_for_faceplate(
            hass, coordinator, Platform.SENSOR, SENSORS, coordinator.sensor
        )
        entities: list[SensorEntity] = [
            InvisOutletSensor(coordinator, description) for description in supported
        ]
        entities.append(InvisOutletStatusSensor(coordinator))
        entities.extend(
            InvisOutletDiagnosticSensor(coordinator, description)
            for description in DIAGNOSTICS
        )
        return entities

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletSensor(InvisOutletEntity, SensorEntity):
    """A single environmental sensor reading."""

    entity_description: InvisOutletSensorDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )

    @property
    def native_value(self) -> float | int | None:
        """Return the current reading, or None until the first push arrives."""
        if (data := self.coordinator.sensor) is None:
            return None
        return self.entity_description.value_fn(data)


class InvisOutletStatusSensor(InvisOutletEntity, SensorEntity):
    """Device-health status shown as text on the device page (Diagnostic)."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_name = "Status"

    def __init__(self, coordinator: InvisOutletCoordinator) -> None:
        """Initialize the status sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.device_info.serial_number}_status"

    @property
    def native_value(self) -> str:
        """Return ``OK`` or a short status message (e.g. waiting on a faceplate)."""
        return _device_status(self.coordinator)

    @property
    def icon(self) -> str:
        """Healthy check, hourglass while waiting, alert for anything else."""
        status = _device_status(self.coordinator)
        if status == "OK":
            return "mdi:check-circle"
        if status.startswith("Waiting"):
            return "mdi:timer-sand"
        return "mdi:alert-circle"




class InvisOutletDiagnosticSensor(InvisOutletEntity, SensorEntity):
    """A connection-health reading, disabled until someone goes looking."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False
    entity_description: InvisOutletDiagnosticDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletDiagnosticDescription,
    ) -> None:
        """Initialize the diagnostic sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )

    @property
    def available(self) -> bool:
        """Stay available while the connection is down; that's the point."""
        return True

    @property
    def native_value(self) -> str | int | datetime | None:
        """Return the current value."""
        return self.entity_description.value_fn(self.coordinator)
