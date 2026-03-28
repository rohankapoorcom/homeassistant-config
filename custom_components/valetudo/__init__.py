import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ICONS, ENTRY_TYPE_AUGMENTATIONS
from .custom_icons import async_setup_icons
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry_type = entry.data.get(CONF_ENTRY_TYPE)

    if entry_type == ENTRY_TYPE_ICONS:
        await async_setup_icons(hass)
    elif entry_type == ENTRY_TYPE_AUGMENTATIONS:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    await async_setup_services(hass)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry_type = entry.data.get(CONF_ENTRY_TYPE)

    if entry_type == ENTRY_TYPE_AUGMENTATIONS:
        return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return True

