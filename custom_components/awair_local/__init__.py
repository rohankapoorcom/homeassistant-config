"""Support for Awair Local Sensors."""
from typing import Any
import asyncio
import logging

import voluptuous as vol

from aiohttp import ClientSession
from async_timeout import timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_TIMEOUT, DOMAIN, UPDATE_INTERVAL
from .device import AwairDevice

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

PLATFORMS = [Platform.SENSOR]


async def async_setup(hass: HomeAssistantType, config: dict):
    """Set up the Awair Local Component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up an instance of a Awair Local Sensor from a config entry."""
    session = async_get_clientsession(hass)

    coordinator = AwairDataUpdateCoordinator(hass, entry, session)
    await coordinator.awair.async_retrieve_device_info()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
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


class AwairDataUpdateCoordinator(DataUpdateCoordinator):
    """Define a wrapper class to update Awair data."""

    def __init__(
        self, hass: HomeAssistantType, entry: ConfigEntry, session: ClientSession
    ) -> None:
        """Set up the AwairDataUpdateCoordinator class."""
        self.awair = AwairDevice(entry.data[CONF_HOST], session)
        self._entry = entry

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=UPDATE_INTERVAL)

    async def _async_update_data(self) -> Any | None:
        """Update data from the Awair Air Sensor."""
        async with timeout(API_TIMEOUT):
            _LOGGER.debug("Fetching data from device %s", self.awair.host)
            return await self.awair.async_retrieve_sensor_info()
