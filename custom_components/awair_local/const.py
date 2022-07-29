from datetime import timedelta
from dataclasses import dataclass
import voluptuous as vol

from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_BILLION,
    CONCENTRATION_PARTS_PER_MILLION,
    CONF_HOST,
    PERCENTAGE,
    TEMP_CELSIUS,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorEntityDescription
import homeassistant.helpers.config_validation as cv

API_CO2 = "co2"
API_HUMID = "humid"
API_PM10 = "pm10_est"
API_PM25 = "pm25"
API_SCORE = "score"
API_TIMEOUT = 10
API_TEMP = "temp"
API_VOC = "voc"

ATTRIBUTION = "Awair air quality sensor"

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
    }
)

DOMAIN = "awair_local"
UPDATE_INTERVAL = timedelta(seconds=10)


@dataclass
class AwairRequiredKeysMixin:
    """Mixin for required keys."""

    unique_id_tag: str


@dataclass
class AwairSensorEntityDescription(SensorEntityDescription, AwairRequiredKeysMixin):
    """Describes Awair sensor entity."""


SENSOR_TYPES: tuple[AwairSensorEntityDescription, ...] = (
    AwairSensorEntityDescription(
        key=API_HUMID,
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        name="Humidity",
        unique_id_tag="HUMID",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_VOC,
        icon="mdi:cloud",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_BILLION,
        name="Volatile organic compounds",
        unique_id_tag="VOC",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_TEMP,
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=TEMP_CELSIUS,
        name="Temperature",
        unique_id_tag="TEMP",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_CO2,
        device_class=SensorDeviceClass.CO2,
        icon="mdi:cloud",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        name="Carbon dioxide",
        unique_id_tag="CO2",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_PM25,
        icon="mdi:blur",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        name="PM2.5",
        unique_id_tag="PM25",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_PM10,
        icon="mdi:blur",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        name="PM10",
        unique_id_tag="PM10",  # matches legacy format
    ),
    AwairSensorEntityDescription(
        key=API_SCORE,
        icon="mdi:blur",
        native_unit_of_measurement=PERCENTAGE,
        name="Awair score",
        unique_id_tag="score",  # matches legacy format
    ),
)

SENSOR_US_AQI = AwairSensorEntityDescription(
    key=SensorDeviceClass.AQI,
    icon="mdi:air-filter",
    native_unit_of_measurement="AQI",
    name="US Air Quality Index",
    unique_id_tag="USAQI",  # matches legacy format
)
