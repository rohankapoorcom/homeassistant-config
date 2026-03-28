"""event methods for MQTT Discovery Statestream."""

import logging

from homeassistant.components.event import ATTR_EVENT_TYPE, ATTR_EVENT_TYPES
from homeassistant.const import ATTR_STATE, Platform

from ..const import (
    CONF_EVT_TYP,
)
from ..utils import EntityInfo
from .base_entity import DiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Event class."""

    PLATFORM = Platform.EVENT
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a event."""
        config[CONF_EVT_TYP] = entity_info.attributes[ATTR_EVENT_TYPES]

    async def async_publish_state(self, new_state, mybase):
        """Publish the state for a text."""

        if (
            new_state.attributes[ATTR_EVENT_TYPE]
            in new_state.attributes[ATTR_EVENT_TYPES]
        ):
            payload = {ATTR_EVENT_TYPE: new_state.attributes[ATTR_EVENT_TYPE]}
            await self._async_mqtt_publish(ATTR_STATE, payload, mybase, encoded=True)

        await super().async_publish_state(new_state, mybase)
