"""Base for all discovery entities."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.const import ATTR_STATE
from homeassistant.helpers.json import JSONEncoder

from ..const import ATTR_ATTRIBUTES, SUPPORTED_ENTITY_TYPE_COMMANDS
from ..utils import EntityInfo

_LOGGER = logging.getLogger(__name__)


class DiscoveryEntity:
    """Base discovery entity class."""

    def __init__(self, hass, publish_retain, platform, publish_state=True):
        """Initialise the climate class."""
        self._hass = hass
        self._publish_retain = publish_retain
        self._publish_state = publish_state
        self._platform = platform
        self._commands = SUPPORTED_ENTITY_TYPE_COMMANDS[self._platform]

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a discovery entity."""

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a discovery entity."""

        await self._async_publish_base_attributes(
            new_state,
            mybase,
        )

    async def async_subscribe(self, command_topic):
        """Subscribe to messages for a cover."""
        if not self._commands:
            return

        for command in self._commands:
            await mqtt.async_subscribe(
                self._hass,
                f"{command_topic}{self._platform}/+/{command}",
                self._async_handle_message,
            )

        _LOGGER.info("MQTT '%s' subscribe successful", self._platform)

    async def _async_handle_message(self, msg):
        """Handle a message for a discovery entity."""

    async def _async_publish_base_attributes(self, new_state, mybase):
        """Publish the basic attributes for the entity state."""
        if self._publish_state:
            await mqtt.async_publish(
                self._hass,
                f"{mybase}{ATTR_STATE}",
                new_state.state,
                1,
                self._publish_retain,
            )

        attributes = dict(new_state.attributes.items())
        encoded = json.dumps(attributes, cls=JSONEncoder)
        await mqtt.async_publish(
            self._hass, f"{mybase}{ATTR_ATTRIBUTES}", encoded, 1, self._publish_retain
        )
