"""Humidifier methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.humidifier import (
    SERVICE_SET_HUMIDITY,
    SERVICE_SET_MODE,
    HumidifierEntityCapabilityAttribute,
    HumidifierEntityFeature,
    HumidifierEntityStateAttribute,
)
from homeassistant.components.mqtt import CONF_COMMAND_TOPIC
from homeassistant.components.mqtt.humidifier import (
    CONF_AVAILABLE_MODES_LIST,
    CONF_CURRENT_HUMIDITY_TOPIC,
    CONF_MODE_COMMAND_TOPIC,
    CONF_MODE_STATE_TOPIC,
    CONF_TARGET_HUMIDITY_COMMAND_TOPIC,
    CONF_TARGET_HUMIDITY_MAX,
    CONF_TARGET_HUMIDITY_MIN,
    CONF_TARGET_HUMIDITY_STATE_TOPIC,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    CONF_PAYLOAD_OFF,
    CONF_PAYLOAD_ON,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)

from ..const import COMMAND_HUMIDITY, COMMAND_MODE, COMMAND_SET
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command, build_topic

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Humidifier class."""

    PLATFORM = Platform.HUMIDIFIER

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a humidifier."""
        attributes = entity_info.attributes
        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)
        add_config_command(
            config, entity_info, CONF_TARGET_HUMIDITY_COMMAND_TOPIC, COMMAND_HUMIDITY
        )
        if (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & HumidifierEntityFeature.MODES
        ):
            config[CONF_AVAILABLE_MODES_LIST] = attributes[
                HumidifierEntityCapabilityAttribute.AVAILABLE_MODES
            ]
            config[CONF_MODE_STATE_TOPIC] = build_topic(
                HumidifierEntityStateAttribute.MODE
            )
            add_config_command(
                config, entity_info, CONF_MODE_COMMAND_TOPIC, COMMAND_MODE
            )
        config[CONF_CURRENT_HUMIDITY_TOPIC] = build_topic(
            HumidifierEntityStateAttribute.CURRENT_HUMIDITY
        )
        config[CONF_TARGET_HUMIDITY_STATE_TOPIC] = build_topic(
            HumidifierEntityStateAttribute.HUMIDITY
        )
        if HumidifierEntityCapabilityAttribute.MAX_HUMIDITY in attributes:
            config[CONF_TARGET_HUMIDITY_MAX] = attributes[
                HumidifierEntityCapabilityAttribute.MAX_HUMIDITY
            ]
            config[CONF_TARGET_HUMIDITY_MIN] = attributes[
                HumidifierEntityCapabilityAttribute.MIN_HUMIDITY
            ]

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a humidifier."""
        await super().async_publish_state(new_state, mybase)
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            HumidifierEntityStateAttribute.CURRENT_HUMIDITY,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            HumidifierEntityStateAttribute.HUMIDITY,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            HumidifierEntityStateAttribute.MODE,
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a humidifier."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        entity_id = f"{domain}.{entity}"
        service_payload = {
            ATTR_ENTITY_ID: entity_id,
        }
        service_name = None
        if command == COMMAND_SET:
            if msg.payload == STATE_ON:
                service_name = SERVICE_TURN_ON
            elif msg.payload == STATE_OFF:
                service_name = SERVICE_TURN_OFF
            else:
                self.command_error(command, msg.payload, entity)
                return
        elif command == COMMAND_MODE:
            service_payload[HumidifierEntityStateAttribute.MODE] = msg.payload
            service_name = SERVICE_SET_MODE
        elif command == COMMAND_HUMIDITY:
            service_payload[HumidifierEntityStateAttribute.HUMIDITY] = msg.payload
            service_name = SERVICE_SET_HUMIDITY
        await self._hass.services.async_call(domain, service_name, service_payload)
