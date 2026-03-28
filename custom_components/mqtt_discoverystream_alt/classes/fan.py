"""Fan methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.fan import (
    ATTR_DIRECTION,
    ATTR_OSCILLATING,
    ATTR_PERCENTAGE,
    ATTR_PERCENTAGE_STEP,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    SERVICE_OSCILLATE,
    SERVICE_SET_DIRECTION,
    SERVICE_SET_PERCENTAGE,
    SERVICE_SET_PRESET_MODE,
    FanEntityFeature,
)
from homeassistant.components.mqtt.fan import (
    CONF_DIRECTION_COMMAND_TOPIC,
    CONF_DIRECTION_STATE_TOPIC,
    CONF_DIRECTION_VALUE_TEMPLATE,
    CONF_OSCILLATION_COMMAND_TOPIC,
    CONF_OSCILLATION_STATE_TOPIC,
    CONF_OSCILLATION_VALUE_TEMPLATE,
    CONF_PAYLOAD_OSCILLATION_OFF,
    CONF_PAYLOAD_OSCILLATION_ON,
    CONF_PERCENTAGE_COMMAND_TOPIC,
    CONF_PERCENTAGE_STATE_TOPIC,
    CONF_PRESET_MODE_COMMAND_TOPIC,
    CONF_PRESET_MODE_STATE_TOPIC,
    CONF_PRESET_MODE_VALUE_TEMPLATE,
    CONF_PRESET_MODES_LIST,
    CONF_SPEED_RANGE_MAX,
    CONF_SPEED_RANGE_MIN,
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

from ..const import (
    ATTR_ATTRIBUTES,
    COMMAND_DIRECTION,
    COMMAND_OSCILLATION,
    COMMAND_PERCENTAGE,
    COMMAND_PRESET,
    COMMAND_SET,
    CONF_CMD_T,
)
from ..utils import (
    EntityInfo,
    add_config_command,
    build_topic,
)
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Fan class."""

    PLATFORM = Platform.FAN

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a fan."""
        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)

        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        if ATTR_DIRECTION in entity_info.attributes or (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES] & FanEntityFeature.DIRECTION
        ):
            config[CONF_DIRECTION_STATE_TOPIC] = build_topic(ATTR_ATTRIBUTES)
            config[CONF_DIRECTION_VALUE_TEMPLATE] = (
                "{{ value_json['" + ATTR_DIRECTION + "'] }}"
            )
            add_config_command(
                config,
                entity_info,
                CONF_DIRECTION_COMMAND_TOPIC,
                COMMAND_DIRECTION,
            )

        if ATTR_OSCILLATING in entity_info.attributes or (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES] & FanEntityFeature.OSCILLATE
        ):
            config[CONF_OSCILLATION_STATE_TOPIC] = build_topic(ATTR_ATTRIBUTES)
            config[CONF_OSCILLATION_VALUE_TEMPLATE] = (
                "{{ value_json['" + ATTR_OSCILLATING + "'] }}"
            )
            add_config_command(
                config,
                entity_info,
                CONF_OSCILLATION_COMMAND_TOPIC,
                COMMAND_OSCILLATION,
            )
            config[CONF_PAYLOAD_OSCILLATION_ON] = True
            config[CONF_PAYLOAD_OSCILLATION_OFF] = False

        if (
            ATTR_PRESET_MODES in entity_info.attributes
            and entity_info.attributes[ATTR_PRESET_MODES]
        ) or (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & FanEntityFeature.PRESET_MODE
        ):
            config[CONF_PRESET_MODES_LIST] = entity_info.attributes[ATTR_PRESET_MODES]
            add_config_command(
                config,
                entity_info,
                CONF_PRESET_MODE_COMMAND_TOPIC,
                COMMAND_PRESET,
            )
            config[CONF_PRESET_MODE_STATE_TOPIC] = build_topic(ATTR_ATTRIBUTES)
            config[CONF_PRESET_MODE_VALUE_TEMPLATE] = (
                "{{ value_json['" + ATTR_PRESET_MODE + "'] }}"
            )
        if ATTR_PERCENTAGE in entity_info.attributes or (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES] & FanEntityFeature.SET_SPEED
        ):
            config[CONF_PERCENTAGE_STATE_TOPIC] = build_topic(ATTR_PERCENTAGE)

        if entity_info.attributes[ATTR_SUPPORTED_FEATURES] & FanEntityFeature.SET_SPEED:
            add_config_command(
                config,
                entity_info,
                CONF_PERCENTAGE_COMMAND_TOPIC,
                COMMAND_PERCENTAGE,
            )

        if ATTR_PERCENTAGE_STEP in entity_info.attributes:
            config[CONF_SPEED_RANGE_MIN] = 1
            config[CONF_SPEED_RANGE_MAX] = (
                100 / entity_info.attributes[ATTR_PERCENTAGE_STEP]
            )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a fan"""
        await super().async_publish_state(new_state, mybase)
        if ATTR_PERCENTAGE in new_state.attributes:
            percentage = new_state.attributes[ATTR_PERCENTAGE]
            if ATTR_PERCENTAGE_STEP in new_state.attributes:
                percentage = (
                    new_state.attributes[ATTR_PERCENTAGE]
                    / new_state.attributes[ATTR_PERCENTAGE_STEP]
                )
            await self._async_mqtt_publish(ATTR_PERCENTAGE, int(percentage), mybase)

    def _add_attribute(self, payload, new_state, attribute):
        if attribute in new_state.attributes and new_state.attributes[attribute]:
            payload[attribute] = new_state.attributes[attribute]

    async def _async_handle_message(self, msg):
        """Handle a message for a fan."""
        valid, domain, entity, command = self.validate_message(
            msg,
        )
        if not valid:
            return

        entity_id = f"{domain}.{entity}"
        service_payload = {
            ATTR_ENTITY_ID: entity_id,
        }
        if command == COMMAND_SET:
            if msg.payload == STATE_ON:
                await self._hass.services.async_call(
                    domain, SERVICE_TURN_ON, service_payload
                )
            elif msg.payload == STATE_OFF:
                await self._hass.services.async_call(
                    domain, SERVICE_TURN_OFF, service_payload
                )
            else:
                self.command_error(command, msg.payload, entity)

        elif command == COMMAND_DIRECTION:
            service_payload[ATTR_DIRECTION] = msg.payload
            await self._hass.services.async_call(
                domain, SERVICE_SET_DIRECTION, service_payload
            )
        elif command == COMMAND_OSCILLATION:
            service_payload[ATTR_OSCILLATING] = msg.payload
            await self._hass.services.async_call(
                domain, SERVICE_OSCILLATE, service_payload
            )
        elif command == COMMAND_PERCENTAGE:
            state_obj = self._hass.states.get(entity_id)
            if pct_step := state_obj.attributes.get(ATTR_PERCENTAGE_STEP):
                service_payload[ATTR_PERCENTAGE] = int(msg.payload) * pct_step
            else:
                service_payload[ATTR_PERCENTAGE] = msg.payload
            await self._hass.services.async_call(
                domain, SERVICE_SET_PERCENTAGE, service_payload
            )
        elif command == COMMAND_PRESET:
            service_payload[ATTR_PRESET_MODE] = msg.payload
            await self._hass.services.async_call(
                domain, SERVICE_SET_PRESET_MODE, service_payload
            )
