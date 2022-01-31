from datetime import timedelta

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import format_mac

from .const import DOMAIN
from .device import VaddioDevice

SCAN_INTERVAL = timedelta(seconds=1)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup the Vaddio Conferenceshot switch platform from a config entry."""
    vaddio_device = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([VaddioSwitch(vaddio_device)], False)


class VaddioSwitch(SwitchEntity):
    """Representation of a Vaddio Camera switch."""

    def __init__(self, vaddio_device: VaddioDevice):
        """Initialize the switch."""
        self._vaddio_device = vaddio_device
        self._state = None
        self._unique_id = format_mac(vaddio_device._mac_address)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._vaddio_device.name

    @property
    def unique_id(self):
        """Return the unique_id of this device."""
        return self._unique_id

    async def async_update(self):
        """Update the switch value."""
        self._state = await self._vaddio_device.async_is_on()

    @property
    def should_poll(self):
        """Update the state periodically."""
        return True

    @property
    def is_on(self):
        """Return True if the camera is on."""
        return self._state

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

    async def async_turn_on(self, **kwargs):
        """Turn the camera on."""
        await self._vaddio_device.async_turn_on()

    async def async_turn_off(self, **kwargs):
        """Turn the camera off."""
        await self._vaddio_device.async_turn_off()
