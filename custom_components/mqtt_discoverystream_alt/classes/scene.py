"""scene methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.mqtt.const import (  # pylint: disable=home-assistant-component-root-import
    CONF_COMMAND_TOPIC,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    CONF_PAYLOAD_ON,
    SERVICE_TURN_ON,
    STATE_ON,
    Platform,
)

from ..const import COMMAND_SET
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, add_config_command

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """scene class."""

    PLATFORM = Platform.SCENE
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a scene."""
        config[CONF_PAYLOAD_ON] = STATE_ON
        add_config_command(config, entity_info, CONF_COMMAND_TOPIC, COMMAND_SET)

    async def _async_handle_message(self, msg):
        """Handle a message for a scene."""
        valid, domain, entity, _command = self.validate_message(  # pylint: disable=unused-variable
            msg,
        )
        if not valid:
            return

        if msg.payload == STATE_ON:
            await self._hass.services.async_call(
                domain, SERVICE_TURN_ON, {ATTR_ENTITY_ID: f"{domain}.{entity}"}
            )
