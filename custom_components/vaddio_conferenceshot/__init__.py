"""Support for Vaddio Conferenceshot Cameras."""
import logging
import re
import telnetlib
import threading

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PATH, CONF_USERNAME
from homeassistant.helpers.discovery import async_load_platform

DOMAIN = "vaddio_conferenceshot"
_LOGGER = logging.getLogger(__name__)

DEFAULT_CAMERA_PATH = "/vaddio-conferenceshot-stream"

HOST_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_PATH, default=DEFAULT_CAMERA_PATH): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [HOST_CONFIG_SCHEMA])}, extra=vol.ALLOW_EXTRA
)

SERVICE_RECALL_PRESET = "move_to_preset"
ATTR_MAC_ADDRESS = "mac_address"
ATTR_PRESET_ID = "preset"


def _mac_address(value: str) -> str:
    """Validate a Mac Address and convert to standard format."""
    regex = re.compile("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$")
    if not re.match(regex, value.lower()):
        raise vol.Invalid("Invalid Mac Address")
    return value.upper().replace("-", "").replace(":", "")


RECALL_PRESET_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_MAC_ADDRESS): vol.All(cv.string, _mac_address),
        vol.Required(ATTR_PRESET_ID): vol.All(
            cv.positive_int, vol.Range(min=1, max=16)
        ),
    }
)


def setup(hass, config):
    """Set up the Vaddio Conferenceshot Component."""

    hass.data[DOMAIN] = {}

    for conf in config[DOMAIN]:
        vaddio_device = VaddioDevice(
            conf[CONF_HOST], conf[CONF_USERNAME], conf[CONF_PASSWORD], conf[CONF_PATH]
        )
        hass.data[DOMAIN][vaddio_device.mac_address] = vaddio_device

    def recall_preset(call):
        """Move the specified camera to the specified preset."""
        vaddio_id = call.data[ATTR_MAC_ADDRESS]
        if vaddio_id not in hass.data[DOMAIN]:
            _LOGGER.error(
                "Invalid Vaddio Conferenceshot mac address provided: %s", vaddio_id
            )
            return

        if not hass.data[DOMAIN][vaddio_id].is_on:
            _LOGGER.error(
                "Unable to move Vaddio COnferenshot camera %s " "because it is off",
                vaddio_id,
            )
            return

        preset_id = call.data[ATTR_PRESET_ID]
        if not hass.data[DOMAIN][vaddio_id].move_to_preset(preset_id):
            _LOGGER.error(
                "Unable to move Vaddio COnferenceshot camera %s to preset %s",
                vaddio_id,
                preset_id,
            )
            return

    hass.services.register(
        DOMAIN, SERVICE_RECALL_PRESET, recall_preset, schema=RECALL_PRESET_SCHEMA
    )

    for platform in ["switch", "camera"]:
        hass.async_create_task(async_load_platform(hass, platform, DOMAIN, {}, config))
    return True


class VaddioDevice:
    def __init__(self, hostname: str, username: str, password: str, path: str):
        """Initiate a Vaddio Conferenceshot Device."""
        self._hostname = hostname
        self._username = username
        self._password = password
        self._path = path
        self._lock = threading.Lock()
        self._mac_address = ""
        self._name = ""
        self._port = 23
        self._timeout = 0.5
        self._was_on = None

        self._telnet = self._create_telnet_client()
        self._retrieve_info()

    def _create_telnet_client(self):
        """Create a telnet client for communication."""
        try:
            telnet = telnetlib.Telnet(self._hostname, self._port)
            telnet.read_until(b"login: ")
            telnet.write(self._username.encode("ASCII") + b"\r")
            telnet.read_until(b"Password: ")
            telnet.write(self._password.encode("ASCII") + b"\r")
            telnet.read_until(b"> ")
            return telnet
        except OSError as error:
            _LOGGER.error(
                "Unable to connect via Telnet to %s. Received exception: %s",
                self._hostname,
                repr(error),
            )
        return None

    def _telnet_command(self, command: str) -> [str]:
        """Send a telnet command to the camera."""
        with self._lock:
            try:
                self._telnet.write(command.encode("ASCII") + b"\r")
                response = self._telnet.read_until(b">", timeout=self._timeout)
                _LOGGER.debug("telnet response: %s", response.decode("ASCII").strip())
                return response.decode("ASCII").strip().splitlines()[1:]
            except OSError as error:
                _LOGGER.error(
                    'Command "%s" failed with exception: %s', command, repr(error)
                )
            return None

    def _retrieve_info(self):
        """Retrieve the name and mac address from the camera."""
        response = self._telnet_command("network settings get")
        self._mac_address = response[1].split()[-1].replace(":", "")
        self._name = response[6].split()[-1]

    @property
    def mac_address(self) -> str:
        """Return the mac address of the camera."""
        return self._mac_address

    @property
    def name(self) -> str:
        """Return the name of the camera."""
        return self._name

    def turn_on(self) -> bool:
        """Turn on the camera."""
        response = self._telnet_command("camera standby off")
        return response[0] == "OK"

    def turn_off(self) -> bool:
        """Turn off the camera."""
        response = self._telnet_command("camera standby on")
        return response[0] == "OK"

    @property
    def is_on(self) -> bool:
        """Return true if the camera is on"""
        tries = 5
        while tries > 0:
            response = self._telnet_command("camera standby get")
            if len(response) < 1:
                _LOGGER.debug("Received invalid response from camera. Trying again...")
                continue
            self._was_on = not response[0] == "standby:        on"
            return self._was_on
        _LOGGER.error(
            "Received invalid response from camera 5 times." "Assuming no state change."
        )
        return self._was_on

    def move_to_preset(self, preset: int) -> bool:
        """Move the camera to a specified preset."""
        if preset < 1 or preset > 16:
            _LOGGER.error('Preset "%s" out of range. Valid range is 1-16.', preset)
            return False

        response = self._telnet_command("camera preset recall {}".format(preset))
        return response[0] == "OK"
