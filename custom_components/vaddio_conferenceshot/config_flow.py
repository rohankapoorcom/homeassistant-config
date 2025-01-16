import logging

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import format_mac

from .const import DATA_SCHEMA, DOMAIN
from .device import CannotConnect, FIFOError, InvalidAuth, VaddioDevice

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict) -> VaddioDevice:
    """Validate the user input allows us to connect.
    Data has the keys from DATA_SCHEMA with the values provided by the user.
    """
    vaddio_device = VaddioDevice(hass, **data)
    await vaddio_device.async_retrieve_info()
    return vaddio_device


class VaddioConferenceShotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Vaddio Conferenceshot."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            vaddio_device = None
            try:
                vaddio_device = await validate_input(self.hass, user_input)

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except InvalidAuth:
                errors["base"] = "invalid_auth"

            except FIFOError:
                errors["base"] = "reboot_camera"

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if vaddio_device is not None:
                await self.async_set_unique_id(format_mac(vaddio_device._mac_address))
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Vaddio {vaddio_device.model}", data=user_input
                )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
