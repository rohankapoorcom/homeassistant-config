"""Support for Vaddio Conferenceshot Cameras."""
import asyncio
import logging

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DATA_SCHEMA
from .device import VaddioDevice

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = ["switch", "camera"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Vaddio Conferenceshot Component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up an instance of a Vaddio Conferenceshot Camera from a config entry."""
    vaddio_device = VaddioDevice(hass, **entry.data)
    await vaddio_device.async_retrieve_info()

    hass.data[DOMAIN][entry.entry_id] = vaddio_device

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
