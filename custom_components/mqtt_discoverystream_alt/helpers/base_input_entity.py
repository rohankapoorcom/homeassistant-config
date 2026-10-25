"""Base for all discovery entities with input alternatives."""

import logging

from homeassistant.components.button import SERVICE_PRESS
from homeassistant.components.input_datetime import (
    CONF_HAS_DATE,
    CONF_HAS_TIME,
    DOMAIN as INPUT_DATETIME_DOMAIN,
)
from homeassistant.components.mqtt.const import (  # pylint: disable=home-assistant-component-root-import
    CONF_COMMAND_TOPIC,
    CONF_MAX,
    CONF_MIN,
    CONF_PATTERN,
    CONF_PAYLOAD_PRESS,
    CONF_STATE_TOPIC,
    CONF_STEP,
)
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
    ATTR_DATE,
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_TIME,
    CONF_MODE,
    CONF_OPTIONS,
    CONF_PAYLOAD_OFF,
    CONF_PAYLOAD_ON,
    SERVICE_SELECT_OPTION,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    STATE_UNKNOWN,
    Platform,
)
from homeassistant.util import dt as dt_util

from ..const import (
    ATTR_DATETIME,
    ATTR_MODE,
    COMMAND_SET,
    COMMAND_SET_DATE,
    COMMAND_SET_DATETIME,
    COMMAND_SET_TIME,
    SERVICE_SET_DATETIME,
)
from ..utils import EntityInfo, add_config_command
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class ButtonDiscoveryEntity(DiscoveryEntity):
    """Button class."""

    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a button."""
        del config[CONF_STATE_TOPIC]
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a button."""
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
            msg
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        await self._hass.services.async_call(domain, SERVICE_PRESS, service_payload)


class DateTimeDiscoveryEntity(DiscoveryEntity):
    """DateTime class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a datetime."""
        if self.PLATFORM == Platform.DATETIME:
            command = COMMAND_SET_DATETIME
        elif self.PLATFORM == Platform.DATE:
            command = COMMAND_SET_DATE
        elif self.PLATFORM == Platform.TIME:
            command = COMMAND_SET_TIME
        elif _is_datetime(entity_info.attributes):
            command = COMMAND_SET_DATETIME
        elif entity_info.attributes[CONF_HAS_DATE]:
            command = COMMAND_SET_DATE
        else:
            command = COMMAND_SET_TIME
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, command)

    async def _async_publish_base_attributes(self, new_state, mybase):
        """Publish the basic attributes for the entity state."""

        if self.PLATFORM == INPUT_DATETIME_DOMAIN and _is_datetime(
            new_state.attributes
        ):
            publish_dt = dt_util.parse_datetime(new_state.state).replace(
                tzinfo=dt_util.get_default_time_zone()
            )
        else:
            publish_dt = new_state.state

        await self._async_mqtt_publish(ATTR_STATE, publish_dt, mybase)

    async def _async_handle_message(self, msg):
        """Handle a message for a datetime."""
        valid, domain, entity, command = self.validate_message(  # pylint: disable=unused-variable
            msg
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        if command == COMMAND_SET_DATETIME:
            service_payload[ATTR_DATETIME] = msg.payload
        elif command == COMMAND_SET_DATE:
            service_payload[ATTR_DATE] = msg.payload
        elif command == COMMAND_SET_TIME:
            service_payload[ATTR_TIME] = msg.payload

        if self.PLATFORM == INPUT_DATETIME_DOMAIN:
            await self._hass.services.async_call(
                domain, SERVICE_SET_DATETIME, service_payload
            )
        else:
            await self._hass.services.async_call(
                domain, SERVICE_SET_VALUE, service_payload
            )

    def translate_entity_type(self, entity_id, attributes=None):
        """Translate the entity type to the output type."""
        ent_parts = entity_id.split(".")
        if self.PLATFORM in [Platform.DATETIME, Platform.DATE, Platform.TIME]:
            output_entity = self.PLATFORM
        elif _is_datetime(attributes):
            output_entity = Platform.DATETIME
        elif attributes[CONF_HAS_DATE]:
            output_entity = Platform.DATE
        else:
            output_entity = Platform.TIME

        return f"{output_entity}.{ent_parts[1]}"


class NumberDiscoveryEntity(DiscoveryEntity):
    """Number class."""

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a number."""
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)
        config[CONF_MAX] = entity_info.attributes[ATTR_MAX]
        config[CONF_MIN] = entity_info.attributes[ATTR_MIN]
        config[CONF_MODE] = entity_info.attributes[ATTR_MODE]
        config[CONF_STEP] = entity_info.attributes[ATTR_STEP]

    async def _async_handle_message(self, msg):
        """Handle a message for a number."""
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
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
            config[CONF_OPTIONS] = entity_info.attributes[ATTR_OPTIONS]
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a select."""
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
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
        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)

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
        del config[CONF_STATE_TOPIC]
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)
        ent_parts = entity_info.entity_id.split(".")
        config[CONF_PAYLOAD_PRESS] = ent_parts[1]

    async def _async_handle_message(self, msg):
        """Handle a message for a button."""
        valid, domain, _entity, _command = self.validate_message(  # pylint: disable=unused-variable
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
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)
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
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
            ATTR_VALUE: msg.payload,
        }
        await self._hass.services.async_call(domain, SERVICE_SET_VALUE, service_payload)


def _is_datetime(attributes):
    return bool(attributes[CONF_HAS_DATE] and attributes[CONF_HAS_TIME])
