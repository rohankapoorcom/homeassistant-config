import logging
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.camera import Camera, SUPPORT_STREAM
from homeassistant.helpers.device_registry import format_mac
from homeassistant.helpers import entity_platform

from .const import DOMAIN, SERVICE_RECALL_PRESET, ATTR_PRESET_ID
from .device import VaddioDevice

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Vaddio Conferenceshot switch platform from a config entry."""
    vaddio_device = hass.data[DOMAIN][config_entry.entry_id]

    platform = entity_platform.current_platform.get()

    platform.async_register_entity_service(
        SERVICE_RECALL_PRESET,
        {
            vol.Required(ATTR_PRESET_ID): vol.All(
                cv.positive_int, vol.Range(min=1, max=16)
            )
        },
        "async_recall_preset",
    )

    if vaddio_device.streaming_enabled:
        async_add_entities([VaddioCamera(vaddio_device)], False)


class VaddioCamera(Camera):
    """Representation of a Vaddio Camera."""

    def __init__(self, vaddio_device: VaddioDevice):
        """Initialize as a subclass of GenericCamera."""
        super().__init__()
        self._vaddio_device = vaddio_device
        self._name = vaddio_device.name
        self._stream_source = "rtsp://{}:{}/{}".format(
            vaddio_device._hostname, vaddio_device._streaming_port, vaddio_device._path
        )
        self._unique_id = format_mac(vaddio_device._mac_address)

    @property
    def supported_features(self):
        """Return supported features for this camera."""
        return SUPPORT_STREAM

    @property
    def name(self):
        """Return the name of this device."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of this device."""
        return self._unique_id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, format_mac(self._vaddio_device._mac_address))},
            "name": self._vaddio_device.name,
            "manufacturer": VaddioDevice.manufacturer,
            "model": self._vaddio_device.model,
            "sw_version": self._vaddio_device.version,
            "configuration_url": f"http://{self._vaddio_device._hostname}",
        }

    async def stream_source(self):
        """Return the source of the stream."""
        return self._stream_source

    async def async_recall_preset(self, preset):
        """Move the camera to the specified preset."""
        if not await self._vaddio_device.async_is_on():
            _LOGGER.error(
                f"Unable to move Vaddio Conferenceshot camera {self.name} because it is off"
            )
            return
        if not await self._vaddio_device.async_move_to_preset(preset):
            _LOGGER.error(
                f"Unable to move Vaddio Conferenceshot camera {self.name} to preset {preset}"
            )
