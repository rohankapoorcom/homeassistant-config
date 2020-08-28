from datetime import timedelta

from homeassistant.components.switch import SwitchEntity

from . import DOMAIN as VADDIO_DOMAIN

SCAN_INTERVAL = timedelta(seconds=1)


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the Vaddio Conferenceshot switch platform."""
    switches = []
    for _, vaddio_device in hass.data[VADDIO_DOMAIN].items():
        switches.append(VaddioSwitch(vaddio_device))
    add_entities(switches)
    return True


class VaddioSwitch(SwitchEntity):
    """Representation of a Vaddio Camera switch."""

    def __init__(self, vaddio_device):
        """Initialize the switch."""
        self._vaddio_device = vaddio_device
        self._state = None

    @property
    def name(self):
        """Return the name of the switch."""
        return self._vaddio_device.name

    def update(self):
        """Update the switch value."""
        self._state = self._vaddio_device.is_on

    @property
    def should_poll(self):
        """Update the state periodically."""
        return True

    @property
    def is_on(self):
        """Return True if the camera is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the camera on."""
        self._vaddio_device.turn_on()

    def turn_off(self, **kwargs):
        """Turn the camera off."""
        self._vaddio_device.turn_off()
