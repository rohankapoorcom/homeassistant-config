"""binary_sensor methods for MQTT Discovery Statestream."""

from homeassistant.const import STATE_OFF, STATE_ON, Platform

from ..utils import EntityInfo
from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Binary_sensor class."""

    PLATFORM = Platform.BINARY_SENSOR

    def build_config(self, config, entity_info: EntityInfo):  # pylint: disable=unused-argument
        """Build the config for a binary_sensor."""
        config["pl_off"] = STATE_OFF
        config["pl_on"] = STATE_ON
