"""Vacuum methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components.mqtt.vacuum import (
    CONF_FAN_SPEED_LIST,
    CONF_SEND_COMMAND_TOPIC,
    CONF_SET_FAN_SPEED_TOPIC,
    CONF_SUPPORTED_FEATURES,
    DEFAULT_PAYLOAD_RETURN_TO_BASE,
    STRING_TO_SERVICE,
)
from homeassistant.components.vacuum import (
    ATTR_FAN_SPEED,
    ATTR_FAN_SPEED_LIST,
    ATTR_PARAMS,
    SERVICE_SEND_COMMAND,
    SERVICE_SET_FAN_SPEED,
    VacuumEntityFeature,
)
from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    ATTR_COMMAND,
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_SUPPORTED_FEATURES,
    Platform,
)

from ..const import (
    COMMAND_SEND,
    COMMAND_SET,
    COMMAND_SET_FAN_SPEED,
    CONF_CMD_T,
)
from ..utils import (
    EntityInfo,
    add_config_command,
    simple_attribute_add,
)
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Vacuum class."""

    PLATFORM = Platform.VACUUM
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a vacuum."""

        add_config_command(config, entity_info, CONF_CMD_T, COMMAND_SET)
        config[CONF_SUPPORTED_FEATURES] = self._build_supported_features(
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
        )

        if ATTR_FAN_SPEED_LIST in entity_info.attributes or (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & VacuumEntityFeature.FAN_SPEED
        ):
            config[CONF_FAN_SPEED_LIST] = entity_info.attributes[ATTR_FAN_SPEED_LIST]

            add_config_command(
                config,
                entity_info,
                CONF_SET_FAN_SPEED_TOPIC,
                COMMAND_SET_FAN_SPEED,
            )
        if (
            entity_info.attributes[ATTR_SUPPORTED_FEATURES]
            & VacuumEntityFeature.SEND_COMMAND
        ):
            add_config_command(
                config,
                entity_info,
                CONF_SEND_COMMAND_TOPIC,
                COMMAND_SEND,
            )

    async def async_publish_state(self, new_state, mybase):
        """Build the state for a update."""
        await super().async_publish_state(new_state, mybase)
        attributes = new_state.attributes
        state = {ATTR_STATE: new_state.state}
        simple_attribute_add(state, attributes, ATTR_BATTERY_LEVEL)
        simple_attribute_add(state, attributes, ATTR_FAN_SPEED)
        await self._async_mqtt_publish(ATTR_STATE, state, mybase, encoded=True)

    def _build_supported_features(self, feat_list):
        sup_feat = []
        for key, value in STRING_TO_SERVICE.items():
            self._check_feature(
                sup_feat,
                feat_list,
                value,
                key,
            )
        return sup_feat

    def _check_feature(self, supported_features, feature_list, feature, feature_name):
        if feature_list & feature:
            supported_features.append(feature_name)

    async def _async_handle_message(self, msg):
        """Handle a message for a vacuum."""
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
            if msg.payload in STRING_TO_SERVICE or msg.payload in [
                DEFAULT_PAYLOAD_RETURN_TO_BASE
            ]:
                await self._hass.services.async_call(
                    domain, msg.payload, service_payload
                )
            else:
                self.command_error(command, msg.payload, entity)

        elif command == COMMAND_SET_FAN_SPEED:
            service_payload[ATTR_FAN_SPEED] = msg.payload
            await self._hass.services.async_call(
                domain, SERVICE_SET_FAN_SPEED, service_payload
            )
        elif command == COMMAND_SEND:
            payload_json = json.loads(msg.payload)
            service_payload[ATTR_COMMAND] = payload_json[ATTR_COMMAND]
            del payload_json[ATTR_COMMAND]
            service_payload[ATTR_PARAMS] = payload_json

            await self._hass.services.async_call(
                domain, SERVICE_SEND_COMMAND, service_payload
            )
