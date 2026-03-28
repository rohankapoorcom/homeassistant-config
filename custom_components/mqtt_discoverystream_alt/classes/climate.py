"""climate methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.climate import (
    ATTR_CURRENT_HUMIDITY,
    ATTR_CURRENT_TEMPERATURE,
    ATTR_FAN_MODE,
    ATTR_FAN_MODES,
    ATTR_HUMIDITY,
    ATTR_HVAC_ACTION,
    ATTR_HVAC_MODES,
    ATTR_MAX_HUMIDITY,
    ATTR_MAX_TEMP,
    ATTR_MIN_HUMIDITY,
    ATTR_MIN_TEMP,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    ATTR_SWING_MODE,
    ATTR_SWING_MODES,
    ATTR_TARGET_TEMP_STEP,
    PRESET_NONE,
    SERVICE_SET_FAN_MODE,
    SERVICE_SET_HUMIDITY,
    SERVICE_SET_HVAC_MODE,
    SERVICE_SET_PRESET_MODE,
    SERVICE_SET_SWING_MODE,
    SERVICE_SET_TEMPERATURE,
    ClimateEntityFeature,
)
from homeassistant.components.mqtt.climate import (
    ATTR_HVAC_MODE,
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    CONF_ACTION_TOPIC,
    CONF_CURRENT_HUMIDITY_TOPIC,
    CONF_CURRENT_TEMP_TOPIC,
    CONF_FAN_MODE_COMMAND_TOPIC,
    CONF_FAN_MODE_LIST,
    CONF_FAN_MODE_STATE_TOPIC,
    CONF_HUMIDITY_COMMAND_TOPIC,
    CONF_HUMIDITY_MAX,
    CONF_HUMIDITY_MIN,
    CONF_HUMIDITY_STATE_TOPIC,
    CONF_MODE_COMMAND_TOPIC,
    CONF_MODE_LIST,
    CONF_MODE_STATE_TOPIC,
    CONF_POWER_COMMAND_TOPIC,
    CONF_PRESET_MODE_COMMAND_TOPIC,
    CONF_PRESET_MODE_STATE_TOPIC,
    CONF_PRESET_MODES_LIST,
    CONF_SWING_MODE_COMMAND_TOPIC,
    CONF_SWING_MODE_LIST,
    CONF_SWING_MODE_STATE_TOPIC,
    CONF_TEMP_COMMAND_TOPIC,
    CONF_TEMP_HIGH_STATE_TOPIC,
    CONF_TEMP_LOW_STATE_TOPIC,
    CONF_TEMP_MAX,
    CONF_TEMP_MIN,
    CONF_TEMP_STATE_TOPIC,
    CONF_TEMP_STEP,
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
    STATE_UNAVAILABLE,
    Platform,
)

from ..const import (
    COMMAND_FAN,
    COMMAND_HUMIDITY,
    COMMAND_MODE,
    COMMAND_PRESET,
    COMMAND_SET,
    COMMAND_SWING,
    COMMAND_TEMPERATURE,
    CONF_STAT_T,
)
from ..utils import (
    EntityInfo,
    add_config_command,
    build_topic,
)
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Climate class."""

    PLATFORM = Platform.CLIMATE
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a climate."""
        attributes = entity_info.attributes
        del config[CONF_STAT_T]
        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        config[CONF_ACTION_TOPIC] = build_topic(ATTR_HVAC_ACTION)
        config[CONF_CURRENT_TEMP_TOPIC] = build_topic(ATTR_CURRENT_TEMPERATURE)
        config[CONF_TEMP_MAX] = attributes[ATTR_MAX_TEMP]
        config[CONF_TEMP_MIN] = attributes[ATTR_MIN_TEMP]
        add_config_command(config, entity_info, CONF_MODE_COMMAND_TOPIC, COMMAND_MODE)
        add_config_command(config, entity_info, CONF_POWER_COMMAND_TOPIC, COMMAND_SET)
        config[CONF_MODE_LIST] = attributes[ATTR_HVAC_MODES]
        config[CONF_MODE_STATE_TOPIC] = build_topic(ATTR_HVAC_MODE)
        if ATTR_PRESET_MODES in attributes:
            preset_modes = attributes[ATTR_PRESET_MODES]
            if PRESET_NONE in preset_modes:
                preset_modes.remove(PRESET_NONE)
            config[CONF_PRESET_MODES_LIST] = preset_modes
            add_config_command(
                config,
                entity_info,
                CONF_PRESET_MODE_COMMAND_TOPIC,
                COMMAND_PRESET,
            )
        if ATTR_PRESET_MODE in attributes:
            config[CONF_PRESET_MODE_STATE_TOPIC] = build_topic(ATTR_PRESET_MODE)
        add_config_command(
            config, entity_info, CONF_TEMP_COMMAND_TOPIC, COMMAND_TEMPERATURE
        )
        config[CONF_TEMP_STATE_TOPIC] = build_topic(ATTR_TEMPERATURE)
        config[CONF_TEMP_STEP] = (
            attributes[ATTR_TARGET_TEMP_STEP]
            if ATTR_TARGET_TEMP_STEP in attributes
            else 0.5
        )
        if ATTR_FAN_MODES in attributes:
            fan_modes = attributes.get(ATTR_FAN_MODES, None)
            config[CONF_FAN_MODE_LIST] = fan_modes
            add_config_command(
                config,
                entity_info,
                CONF_FAN_MODE_COMMAND_TOPIC,
                COMMAND_FAN,
            )
            config[CONF_FAN_MODE_STATE_TOPIC] = build_topic(ATTR_FAN_MODE)
        if ATTR_SWING_MODES in attributes:
            swing_modes = attributes.get(ATTR_SWING_MODES, None)
            config[CONF_SWING_MODE_LIST] = swing_modes
            add_config_command(
                config,
                entity_info,
                CONF_SWING_MODE_COMMAND_TOPIC,
                COMMAND_SWING,
            )
            config[CONF_SWING_MODE_STATE_TOPIC] = build_topic(ATTR_SWING_MODE)
        if ATTR_MAX_HUMIDITY in attributes:
            config[CONF_HUMIDITY_MAX] = attributes[ATTR_MAX_HUMIDITY]
            config[CONF_HUMIDITY_MIN] = attributes[ATTR_MIN_HUMIDITY]
            add_config_command(
                config,
                entity_info,
                CONF_HUMIDITY_COMMAND_TOPIC,
                COMMAND_HUMIDITY,
            )
            config[CONF_HUMIDITY_STATE_TOPIC] = build_topic(ATTR_HUMIDITY)
        if ATTR_CURRENT_HUMIDITY in attributes:
            config[CONF_CURRENT_HUMIDITY_TOPIC] = build_topic(ATTR_CURRENT_HUMIDITY)

        if (
            attributes[ATTR_SUPPORTED_FEATURES]
            & ClimateEntityFeature.TARGET_TEMPERATURE_RANGE
        ):
            # Setting the low and high target temperatures is not supported, because
            # HA core sends the individual temperature items as seperate messages
            # which makes it difficult to combine messages to send to the set_temperature
            # service which does not process individual items.

            config[CONF_TEMP_LOW_STATE_TOPIC] = build_topic(ATTR_TARGET_TEMP_LOW)
            config[CONF_TEMP_HIGH_STATE_TOPIC] = build_topic(ATTR_TARGET_TEMP_HIGH)

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a climate."""
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            ATTR_HVAC_ACTION,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            ATTR_CURRENT_TEMPERATURE,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            ATTR_TARGET_TEMP_LOW,
        )
        await self.async_publish_attribute_if_exists(
            new_state,
            mybase,
            ATTR_TARGET_TEMP_HIGH,
        )
        await self.async_publish_attribute_if_exists(
            new_state, mybase, ATTR_PRESET_MODE
        )
        await self.async_publish_attribute_if_exists(
            new_state, mybase, ATTR_TEMPERATURE
        )
        await self.async_publish_attribute_if_exists(new_state, mybase, ATTR_FAN_MODE)
        await self.async_publish_attribute_if_exists(new_state, mybase, ATTR_SWING_MODE)
        await self.async_publish_attribute_if_exists(new_state, mybase, ATTR_HUMIDITY)
        await self.async_publish_attribute_if_exists(
            new_state, mybase, ATTR_CURRENT_HUMIDITY
        )

        await super().async_publish_state(new_state, mybase)

        payload = new_state.state
        if payload == STATE_UNAVAILABLE:
            payload = STATE_OFF
        await self._async_mqtt_publish(ATTR_HVAC_MODE, payload, mybase)

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
            service_payload[ATTR_HVAC_MODE] = msg.payload
            service_name = SERVICE_SET_HVAC_MODE
        elif command == COMMAND_PRESET:
            service_payload[ATTR_PRESET_MODE] = msg.payload
            service_name = SERVICE_SET_PRESET_MODE
        elif command == COMMAND_TEMPERATURE:
            service_payload[ATTR_TEMPERATURE] = msg.payload
            service_name = SERVICE_SET_TEMPERATURE
        elif command == COMMAND_FAN:
            service_payload[ATTR_FAN_MODE] = msg.payload
            service_name = SERVICE_SET_FAN_MODE
        elif command == COMMAND_SWING:
            service_payload[ATTR_SWING_MODE] = msg.payload
            service_name = SERVICE_SET_SWING_MODE
        elif command == COMMAND_HUMIDITY:
            service_payload[ATTR_HUMIDITY] = msg.payload
            service_name = SERVICE_SET_HUMIDITY
        elif command == COMMAND_SET:
            if msg.payload == STATE_ON:
                service_name = SERVICE_TURN_ON
            elif msg.payload == STATE_OFF:
                service_name = SERVICE_TURN_OFF
            else:
                self.command_error(command, msg.payload, entity)
        await self._hass.services.async_call(domain, service_name, service_payload)
