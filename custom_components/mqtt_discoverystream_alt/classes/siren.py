"""Siren methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components.mqtt.const import CONF_COMMAND_TOPIC
from homeassistant.components.mqtt.siren import (
    CONF_AVAILABLE_TONES,
    CONF_SUPPORT_DURATION,
    CONF_SUPPORT_VOLUME_SET,
)
from homeassistant.components.siren import (
    ATTR_DURATION,
    ATTR_TONE,
    ATTR_VOLUME_LEVEL,
    SirenEntityCapabilityAttribute,
    SirenEntityFeature,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_SUPPORTED_FEATURES,
    CONF_PAYLOAD_OFF,
    CONF_PAYLOAD_ON,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
    Platform,
)

from ..const import COMMAND_SET
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Siren class."""

    PLATFORM = Platform.SIREN
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a siren."""
        attributes = entity_info.attributes
        config[CONF_PAYLOAD_OFF] = STATE_OFF
        config[CONF_PAYLOAD_ON] = STATE_ON
        config[CONF_AVAILABLE_TONES] = attributes[
            SirenEntityCapabilityAttribute.AVAILABLE_TONES
        ]
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)
        if attributes[ATTR_SUPPORTED_FEATURES] & SirenEntityFeature.TONES:
            config[CONF_AVAILABLE_TONES] = attributes[
                SirenEntityCapabilityAttribute.AVAILABLE_TONES
            ]
        config[CONF_SUPPORT_DURATION] = (
            attributes[ATTR_SUPPORTED_FEATURES] & SirenEntityFeature.DURATION
        )
        config[CONF_SUPPORT_VOLUME_SET] = (
            attributes[ATTR_SUPPORTED_FEATURES] & SirenEntityFeature.VOLUME_SET
        )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a siren."""
        await super().async_publish_state(new_state, mybase)
        state = {ATTR_STATE: new_state.state}
        if ATTR_DURATION in new_state.attributes:
            state[ATTR_DURATION] = new_state.attributes[ATTR_DURATION]
        if ATTR_TONE in new_state.attributes:
            state[ATTR_TONE] = new_state.attributes[ATTR_TONE]
        if ATTR_VOLUME_LEVEL in new_state.attributes:
            state[ATTR_VOLUME_LEVEL] = new_state.attributes[ATTR_VOLUME_LEVEL]
        await self._async_mqtt_publish(ATTR_STATE, state, mybase, True)

    async def _async_handle_message(self, msg):
        """Handle a message for a siren."""
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
            payload = json.loads(msg.payload)
            if payload[ATTR_STATE] == STATE_ON:
                service_name = SERVICE_TURN_ON
                if ATTR_DURATION in payload:
                    service_payload[ATTR_DURATION] = payload[ATTR_DURATION]
                if ATTR_TONE in payload:
                    service_payload[ATTR_TONE] = payload[ATTR_TONE]
                if ATTR_VOLUME_LEVEL in payload:
                    service_payload[ATTR_VOLUME_LEVEL] = payload[ATTR_VOLUME_LEVEL]
            else:
                service_name = SERVICE_TURN_OFF

        await self._hass.services.async_call(domain, service_name, service_payload)
