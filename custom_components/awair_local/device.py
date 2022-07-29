"""A representation of the Awair Air Sensor."""
import logging

from aiohttp import ClientSession
from homeassistant import exceptions

_LOGGER = logging.getLogger(__name__)


class AwairDevice:
    """AwairDevice used for communication with Awair Air Sensors."""

    manufacturer = "Awair"

    def __init__(self, host: str, session: ClientSession):
        """Initiate an Awair Sensor."""
        self._host = host
        self._session = session
        self._uuid = ""
        self._mac_address = ""

    async def async_retrieve_device_info(self):
        """Retrieve the uuid and mac address from the Awair Air Sensor."""
        url = f"http://{self._host}/settings/config/data"
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.error(
                    "Could not retrive configuration from Awair Air Sensor: %s",
                    self._host,
                )
                raise CannotConnect
            json = await response.json()
            self._uuid = json["device_uuid"]
            self._mac_address = json["wifi_mac"]

    async def async_retrieve_sensor_info(self):
        """Retrieve the sensor data from the Awair Air Sensor."""
        url = f"http://{self._host}/air-data/latest"
        async with self._session.get(url) as response:
            if response.status != 200:
                _LOGGER.error(
                    "Could not retrive sensor data from Awair Air Sensor: %s",
                    self._host,
                )
                raise CannotConnect
            return await response.json()

    @property
    def host(self) -> str:
        """Return the host name."""
        return self._host

    @property
    def uuid(self) -> str:
        """Return the device UUID."""
        return self._uuid

    @property
    def mac_address(self) -> str:
        """Return the mac address."""
        return self._mac_address


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""
