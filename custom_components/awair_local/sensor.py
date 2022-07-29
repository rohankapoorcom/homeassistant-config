from homeassistant.const import ATTR_ATTRIBUTION, ATTR_CONNECTIONS
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import aqi

from . import AwairDataUpdateCoordinator
from .const import (
    API_SCORE,
    ATTRIBUTION,
    DOMAIN,
    SENSOR_TYPES,
    AwairSensorEntityDescription,
    API_CO2,
    API_HUMID,
    API_PM10,
    API_PM25,
    API_TEMP,
    API_VOC,
    SENSOR_US_AQI,
)
from .device import AwairDevice


async def async_setup_entry(
    hass: HomeAssistantType,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup the Awair Local sensor platform from a config entry."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []

    await coordinator.async_config_entry_first_refresh()
    entities.extend(
        [
            AwairSensor(coordinator.awair, coordinator, description)
            for description in SENSOR_TYPES
            if description.key in coordinator.data.keys()
        ]
    )
    entities.extend([AwairSensor(coordinator.awair, coordinator, SENSOR_US_AQI)])

    async_add_entities(entities)


class AwairSensor(CoordinatorEntity[AwairDataUpdateCoordinator], SensorEntity):
    """Defines an Awair sensor entity."""

    entity_description: AwairSensorEntityDescription

    def __init__(
        self,
        device: AwairDevice,
        coordinator: AwairDataUpdateCoordinator,
        description: AwairSensorEntityDescription,
    ) -> None:
        """Set up an individual AwairSensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device

    @property
    def name(self) -> str | None:
        """Return the name of the sensor."""
        if self._device.uuid:
            return f"{self._device.uuid} {self.entity_description.name}"

        return self.entity_description.name

    @property
    def unique_id(self) -> str:
        """Return the uuid as the unique_id."""
        unique_id_tag = self.entity_description.unique_id_tag

        return f"{self._device.uuid}_{unique_id_tag}"

    @property
    def available(self) -> bool:
        """Determine if the sensor is available based on API results."""
        # If the last update was successful...
        if self.coordinator.last_update_success and self._air_data:
            # and the results included our sensor type...
            sensor_type = self.entity_description.key
            if sensor_type in self._air_data:
                # then we are available.
                return True

            # or we are derived values
            if sensor_type in (API_SCORE, SensorDeviceClass.AQI):
                # then we are available.
                return True

        # Otherwise, we are not.
        return False

    @property
    def native_value(self) -> float | None:
        """Return the state."""
        if not self._air_data:
            return None

        sensor_type = self.entity_description.key
        if sensor_type == SensorDeviceClass.AQI:
            return aqi.to_iaqi(
                aqi.constants.POLLUTANT_PM25,
                self._air_data[API_PM25],
                algo=aqi.ALGO_EPA,
            )
        return self._air_data[sensor_type]

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        sensor_type = self.entity_description.key
        return {ATTR_ATTRIBUTION: ATTRIBUTION}

    @property
    def device_info(self) -> DeviceInfo:
        """Device information."""
        info = DeviceInfo(
            identifiers={(DOMAIN, self._device.uuid)},
            manufacturer="Awair",
        )

        if self._device.mac_address:
            info[ATTR_CONNECTIONS] = {
                (dr.CONNECTION_NETWORK_MAC, self._device.mac_address)
            }

        return info

    @property
    def _air_data(self) -> dict | None:
        """Return the latest data for our device, or None."""
        result: dict | None = self.coordinator.data
        if result:
            return result

        return None
