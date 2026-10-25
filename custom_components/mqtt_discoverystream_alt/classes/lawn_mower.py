"""Lawn Mower methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.lawn_mower import (
    SERVICE_DOCK,
    SERVICE_PAUSE,
    SERVICE_START_MOWING,
    LawnMowerEntityFeature,
)
from homeassistant.components.mqtt.const import CONF_STATE_TOPIC
from homeassistant.components.mqtt.lawn_mower import (
    CONF_ACTIVITY_STATE_TOPIC,
    CONF_DOCK_COMMAND_TOPIC,
    CONF_PAUSE_COMMAND_TOPIC,
    CONF_START_MOWING_COMMAND_TOPIC,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_STATE,
    ATTR_SUPPORTED_FEATURES,
    Platform,
)

from ..const import COMMAND_SET
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command, build_topic

SERVICE_LIST = [SERVICE_DOCK, SERVICE_PAUSE, SERVICE_START_MOWING]

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Lawn Mower class."""

    PLATFORM = Platform.LAWN_MOWER

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a lawn mower."""
        attributes = entity_info.attributes
        del config[CONF_STATE_TOPIC]
        config[CONF_ACTIVITY_STATE_TOPIC] = build_topic(ATTR_STATE)
        if attributes[ATTR_SUPPORTED_FEATURES] & LawnMowerEntityFeature.DOCK:
            add_config_command(
                config, entity_info, CONF_DOCK_COMMAND_TOPIC, COMMAND_SET
            )
        if attributes[ATTR_SUPPORTED_FEATURES] & LawnMowerEntityFeature.PAUSE:
            add_config_command(
                config, entity_info, CONF_PAUSE_COMMAND_TOPIC, COMMAND_SET
            )
        if attributes[ATTR_SUPPORTED_FEATURES] & LawnMowerEntityFeature.START_MOWING:
            add_config_command(
                config, entity_info, CONF_START_MOWING_COMMAND_TOPIC, COMMAND_SET
            )

    async def _async_handle_message(self, msg):
        """Handle a message for a lawn_mower."""
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
            if msg.payload in SERVICE_LIST:
                service_name = msg.payload
            else:
                self.command_error(command, msg.payload, entity)
                return
        await self._hass.services.async_call(domain, service_name, service_payload)
