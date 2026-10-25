"""Water heater methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.mqtt.const import CONF_STATE_TOPIC
from homeassistant.components.mqtt.water_heater import (
    CONF_CURRENT_TEMP_TOPIC,
    CONF_MODE_COMMAND_TOPIC,
    CONF_MODE_LIST,
    CONF_MODE_STATE_TOPIC,
    CONF_POWER_COMMAND_TOPIC,
    CONF_TEMP_COMMAND_TOPIC,
    CONF_TEMP_MAX,
    CONF_TEMP_MIN,
    CONF_TEMP_STATE_TOPIC,
)
from homeassistant.components.water_heater import (
    SERVICE_SET_OPERATION_MODE,
    SERVICE_SET_TEMPERATURE,
    WaterHeaterCapabilityAttribute,
    WaterHeaterEntityFeature,
    WaterHeaterStateAttribute,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    ATTR_TEMPERATURE,
    CONF_PAYLOAD_OFF,
    CONF_PAYLOAD_ON,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)

from ..const import COMMAND_MODE, COMMAND_SET, COMMAND_TEMPERATURE
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command, build_topic

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Water_Heater class."""

    PLATFORM = Platform.WATER_HEATER
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a water_heater."""
        attributes = entity_info.attributes
        del config[CONF_STATE_TOPIC]
        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        config[CONF_CURRENT_TEMP_TOPIC] = build_topic(
            WaterHeaterStateAttribute.CURRENT_TEMPERATURE
        )
        config[CONF_TEMP_MAX] = attributes[WaterHeaterCapabilityAttribute.MAX_TEMP]
        config[CONF_TEMP_MIN] = attributes[WaterHeaterCapabilityAttribute.MIN_TEMP]
        add_config_command(config, entity_info, CONF_MODE_COMMAND_TOPIC, COMMAND_MODE)
        if (
            attributes[ATTR_SUPPORTED_FEATURES]
            & WaterHeaterEntityFeature.TARGET_TEMPERATURE
        ):
            add_config_command(
                config, entity_info, CONF_TEMP_COMMAND_TOPIC, COMMAND_TEMPERATURE
            )
        config[CONF_TEMP_STATE_TOPIC] = build_topic(ATTR_TEMPERATURE)
        add_config_command(config, entity_info, CONF_POWER_COMMAND_TOPIC, COMMAND_SET)
        config[CONF_MODE_LIST] = attributes[
            WaterHeaterCapabilityAttribute.OPERATION_LIST
        ]
        config[CONF_MODE_STATE_TOPIC] = build_topic(
            WaterHeaterStateAttribute.OPERATION_MODE
        )

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a water_heater."""
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            WaterHeaterStateAttribute.CURRENT_TEMPERATURE,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            WaterHeaterStateAttribute.TARGET_TEMP_LOW,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            WaterHeaterStateAttribute.TARGET_TEMP_HIGH,
        )
        await self.async_publish_attribute_if_exists(
            new_state, mybase, ATTR_TEMPERATURE
        )

        await super().async_publish_state(new_state, mybase)

        payload = new_state.state
        # if payload == STATE_UNAVAILABLE:
        #     payload = STATE_OFF
        await self._async_mqtt_publish(
            WaterHeaterStateAttribute.OPERATION_MODE, payload, mybase
        )

    async def _async_handle_message(self, msg):
        """Handle a message for a switch."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        service_payload = {
            ATTR_ENTITY_ID: f"{domain}.{entity}",
        }
        service_name = None

        if command == COMMAND_MODE:
            service_payload[WaterHeaterStateAttribute.OPERATION_MODE] = msg.payload
            service_name = SERVICE_SET_OPERATION_MODE
        elif command == COMMAND_TEMPERATURE:
            service_payload[ATTR_TEMPERATURE] = msg.payload
            service_name = SERVICE_SET_TEMPERATURE
        elif command == COMMAND_SET:
            if msg.payload == STATE_ON:
                service_name = SERVICE_TURN_ON
            elif msg.payload == STATE_OFF:
                service_name = SERVICE_TURN_OFF
            else:
                self.command_error(command, msg.payload, entity)
        await self._hass.services.async_call(domain, service_name, service_payload)
