import logging

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import HomeAssistantType

from .const import DATA_SCHEMA, DOMAIN
from .device import CannotConnect, AwairDevice

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistantType, data: dict) -> AwairDevice:
    """Validate the user input allows us to connect.
    Data has the keys from DATA_SCHEMA with the values provided by the user.
    """
    session = async_get_clientsession(hass)
    awair_device = AwairDevice(data[CONF_HOST], session)
    await awair_device.async_retrieve_device_info()
    return awair_device


class AwairLocalConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Awair Local."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            awair_device = None
            try:
                awair_device = await validate_input(self.hass, user_input)

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if awair_device is not None:
                await self.async_set_unique_id(awair_device.uuid)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Awair  {awair_device.uuid}", data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
