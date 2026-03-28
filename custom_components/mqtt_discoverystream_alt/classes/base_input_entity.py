"""Base for all discovery entities with input alternatives."""

import logging

from homeassistant.components.button.const import SERVICE_PRESS
from homeassistant.components.number import (
    ATTR_MAX,
    ATTR_MIN,
    ATTR_STEP,
    ATTR_VALUE,
    SERVICE_SET_VALUE,
)
from homeassistant.components.select import ATTR_OPTION, ATTR_OPTIONS
from homeassistant.components.text import ATTR_PATTERN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    SERVICE_SELECT_OPTION,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
)

from ..const import (
    ATTR_MODE,
    COMMAND_SET,
    CONF_CMD_T,
    CONF_MAX,
    CONF_MIN,
    CONF_MODE,
    CONF_OPS,
    CONF_PATTERN,
    CONF_PL_OFF,
    CONF_PL_ON,
    CONF_PL_PRS,
    CONF_STAT_T,
    CONF_STEP,
)
from ..utils import EntityInfo, add_config_command
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class ButtonDiscoveryEntity(DiscoveryEntity):
    """Button class."""

    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a button."""
        del config[CONF_STAT_T]
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a button."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        await self._hass.services.async_call(domain, SERVICE_PRESS, service_payload)


class NumberDiscoveryEntity(DiscoveryEntity):
    """Number class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a number."""
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        config[CONF_MAX] = entity_info.attributes[ATTR_MAX]
        config[CONF_MIN] = entity_info.attributes[ATTR_MIN]
        config[CONF_MODE] = entity_info.attributes[ATTR_MODE]
        config[CONF_STEP] = entity_info.attributes[ATTR_STEP]

    async def _async_handle_message(self, msg):
        """Handle a message for a number."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_VALUE: msg.payload,
        }
        await self._hass.services.async_call(domain, SERVICE_SET_VALUE, service_payload)


class SelectDiscoveryEntity(DiscoveryEntity):
    """Select class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a select."""
        if ATTR_OPTIONS in entity_info.attributes:
            config[CONF_OPS] = entity_info.attributes[ATTR_OPTIONS]
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a select."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_OPTION: msg.payload,
        }
        await self._hass.services.async_call(
            domain, SERVICE_SELECT_OPTION, service_payload
        )


class SwitchDiscoveryEntity(DiscoveryEntity):
    """Switch class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a switch."""
        config[CONF_PL_OFF] = STATE_OFF
        config[CONF_PL_ON] = STATE_ON
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        if msg.payload == STATE_ON:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        elif msg.payload == STATE_OFF:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_OFF, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
        else:
            self.command_error(command, msg.payload, entity)


class ScriptDiscoveryEntity(DiscoveryEntity):
    """Button class."""

    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a button."""
        del config[CONF_STAT_T]
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        ent_parts = entity_info.entity_id.split(".")
        config[CONF_PL_PRS] = ent_parts[1]

    async def _async_handle_message(self, msg):
        """Handle a message for a button."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        await self._hass.services.async_call(domain, msg.payload)


class TextDiscoveryEntity(DiscoveryEntity):
    """Text class."""

    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a text."""
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        config[CONF_MAX] = entity_info.attributes[ATTR_MAX]
        config[CONF_MIN] = entity_info.attributes[ATTR_MIN]
        config[CONF_MODE] = entity_info.attributes[ATTR_MODE]
        if entity_info.attributes[ATTR_PATTERN]:
            config[CONF_PATTERN] = entity_info.attributes[ATTR_PATTERN]

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a text."""

        if new_state.state != STATE_UNKNOWN:
            await self._async_mqtt_publish(ATTR_STATE, new_state.state, mybase)

        await super().async_publish_state(new_state, mybase)

    async def _async_handle_message(self, msg):
        """Handle a message for a text."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_VALUE: msg.payload,
        }
        await self._hass.services.async_call(domain, SERVICE_SET_VALUE, service_payload)
