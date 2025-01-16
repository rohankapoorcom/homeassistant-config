"""A representation of the Vaddio device."""
import asyncio
import logging
import telnetlib
from typing import List

from homeassistant import exceptions
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class VaddioDevice:
    """VaddioDevice used for communication with Vaddio Cameras."""

    manufacturer = "Vaddio, LLC"

    def __init__(self, hass: HomeAssistant, host: str, username: str, password: str):
        """Initiate a Vaddio Conferenceshot Device."""
        self._hass = hass
        self._hostname = host
        self._username = username
        self._password = password
        self._path = ""
        self._mac_address = ""
        self._name = ""
        self._model = ""
        self._version = ""
        self._port = 23
        self._streaming_port = 554
        self._timeout = 10
        self._was_on = None
        self._streaming_enabled = False
        self._semaphore = asyncio.Semaphore(1)
        self._telnet = self._create_telnet_client()

    def _create_telnet_client(self):
        """Create a telnet client for communication."""
        try:
            telnet = telnetlib.Telnet(self._hostname, self._port)
            telnet.read_until(b"login: ", self._timeout)
            telnet.write(self._username.encode("ASCII") + b"\r")
            telnet.read_until(b"Password: ", self._timeout)
            telnet.write(self._password.encode("ASCII") + b"\r")
            response = telnet.read_until(b"> ", self._timeout).decode("ASCII").strip()
            if "Login incorrect" in response:
                _LOGGER.error("Invalid credentials to connect to %s.", self._hostname)
                raise InvalidAuth
            if "System error. Can't create temporary FIFO." in response:
                _LOGGER.error(
                    "Received an error from the Vaddio Conferenceshot Camera."
                    + " Please restart the camera."
                )
                raise FIFOError
            if f"Welcome {self._username}" in response:
                return telnet
        except OSError as error:
            _LOGGER.error(
                "Unable to connect via Telnet to %s. Received exception: %s",
                self._hostname,
                repr(error),
            )
        raise CannotConnect

    def _telnet_command(self, command: str) -> List[str]:
        """Send a telnet command to the camera."""
        try:
            self._telnet.write(command.encode("ASCII") + b"\r")
            response = self._telnet.read_until(b">", timeout=self._timeout)
            _LOGGER.debug("telnet response: %s", response.decode("ASCII").strip())
            return response.decode("ASCII").strip().splitlines()[1:]
        except (OSError, InvalidAuth, FIFOError, CannotConnect) as error:
            _LOGGER.error(
                'Command "%s" failed with exception: %s', command, repr(error)
            )
        return None

    async def async_telnet_command(self, command: str) -> List[str]:
        """Send a telnet command to the camera (async) after grabbing the semaphore."""
        async with self._semaphore:
            return await self._hass.async_add_executor_job(
                self._telnet_command, command
            )

    async def async_retrieve_info(self):
        """Retrieve the name and mac address from the camera."""
        response = await self.async_telnet_command("network settings get")
        if not response:
            _LOGGER.error("Response was invalid, unable to retrieve network settings")
            return
        self._mac_address = response[1].split()[-1].replace(":", "")
        self._name = response[6].split()[-1]

        response = await self.async_telnet_command("version")
        if not response:
            _LOGGER.error("Response was invalid, unable to retrieve version info")
            return
        self._model = response[2][15:-5]
        self._version = response[2][-5:]

        response = await self.async_telnet_command("streaming settings get")
        if not response:
            _LOGGER.error("Response was invalid, unable to retrieve streaming settings")
            return
        self._path = response[8].split()[-1]
        self._streaming_enabled = response[2].split()[-1] == "true"
        self._streaming_port = int(response[4].split()[-1])

    @property
    def mac_address(self) -> str:
        """Return the mac address of the camera."""
        return self._mac_address

    @property
    def name(self) -> str:
        """Return the name of the camera."""
        return self._name

    @property
    def model(self) -> str:
        """Return the model of the camera."""
        return self._model

    @property
    def version(self) -> str:
        """Return the version of the camera."""
        return self._version

    async def async_turn_on(self) -> bool:
        """Turn on the camera."""
        response = await self.async_telnet_command("camera standby off")
        return response[0] == "OK"

    async def async_turn_off(self) -> bool:
        """Turn off the camera."""
        response = await self.async_telnet_command("camera standby on")
        return response[0] == "OK"

    async def async_is_on(self) -> bool:
        """Return true if the camera is on"""
        tries = 5
        while tries > 0:
            response = await self.async_telnet_command("camera standby get")
            if len(response) < 1:
                _LOGGER.debug("Received invalid response from camera. Trying again...")
                continue
            self._was_on = not response[0] == "standby:        on"
            return self._was_on
        _LOGGER.error(
            "Received invalid response from camera 5 times." "Assuming no state change."
        )
        return self._was_on

    @property
    def streaming_enabled(self) -> bool:
        """Return true if the camera has streaming enabled"""
        return self._streaming_enabled

    async def async_move_to_preset(self, preset: int) -> bool:
        """Move the camera to a specified preset."""
        if preset < 1 or preset > 16:
            _LOGGER.error(f"Preset {preset} out of range. Valid range is 1-16.")
            return False

        response = await self.async_telnet_command(f"camera preset recall {preset}")
        return response[0] == "OK"


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""


class FIFOError(exceptions.HomeAssistantError):
    """Error to indicate the camera needs to be restarted."""
