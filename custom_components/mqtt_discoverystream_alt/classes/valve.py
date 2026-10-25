"""Valve methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.mqtt.const import (  # pylint: disable=home-assistant-component-root-import
    CONF_COMMAND_TOPIC,
    DEFAULT_PAYLOAD_STOP,
)
from homeassistant.components.mqtt.valve import (  # pylint: disable=home-assistant-component-root-import
    CONF_PAYLOAD_CLOSE,
    CONF_PAYLOAD_OPEN,
    CONF_PAYLOAD_STOP,
    CONF_REPORTS_POSITION,
    DEFAULT_PAYLOAD_CLOSE,
    DEFAULT_PAYLOAD_OPEN,
)
from homeassistant.components.valve import (
    ATTR_POSITION,
    SERVICE_CLOSE_VALVE,
    SERVICE_OPEN_VALVE,
    SERVICE_SET_VALVE_POSITION,
    SERVICE_STOP_VALVE,
    ValveEntityFeature,
    ValveEntityStateAttribute,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_SUPPORTED_FEATURES,
    Platform,
)

from ..const import COMMAND_SET
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Valve class."""

    PLATFORM = Platform.VALVE
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a valve."""
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)

        config[CONF_REPORTS_POSITION] = (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & ValveEntityFeature.SET_POSITION
        )

        if not config[CONF_REPORTS_POSITION]:
            if (
                entity_info.attributes[ATTR_SUPPORTED_FEATURES]
                & ValveEntityFeature.OPEN
            ):
                config[CONF_PAYLOAD_OPEN] = DEFAULT_PAYLOAD_OPEN
            if (
                entity_info.attributes[ATTR_SUPPORTED_FEATURES]
                & ValveEntityFeature.CLOSE
            ):
                config[CONF_PAYLOAD_CLOSE] = DEFAULT_PAYLOAD_CLOSE
            if (
                entity_info.attributes[ATTR_SUPPORTED_FEATURES]
                & ValveEntityFeature.STOP
            ):
                config[CONF_PAYLOAD_STOP] = DEFAULT_PAYLOAD_STOP

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a update."""
        await super().async_publish_state(new_state, mybase)
        attributes = new_state.attributes
        state = new_state.state
        if attributes.get(ValveEntityStateAttribute.CURRENT_POSITION):
            state = attributes[ValveEntityStateAttribute.CURRENT_POSITION]

        await self._async_mqtt_publish(ATTR_STATE, state, mybase)

    async def _async_handle_message(self, msg):
        """Handle a message for a valve."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        service_name = None
        if command == COMMAND_SET:
            if msg.payload == DEFAULT_PAYLOAD_OPEN:
                service_name = SERVICE_OPEN_VALVE
            elif msg.payload == DEFAULT_PAYLOAD_CLOSE:
                service_name = SERVICE_CLOSE_VALVE
            elif msg.payload == DEFAULT_PAYLOAD_STOP:
                service_name = SERVICE_STOP_VALVE
            elif msg.payload.isdigit():
                service_name = SERVICE_SET_VALVE_POSITION
                service_payload[ATTR_POSITION] = msg.payload
            else:
                self.command_error(command, msg.payload, entity)
                return
            await self._hass.services.async_call(domain, service_name, service_payload)
