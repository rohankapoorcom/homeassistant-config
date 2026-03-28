"""text methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_input_entity import TextDiscoveryEntity


class DiscoveryItem(TextDiscoveryEntity):
    """Text class."""

    PLATFORM = Platform.TEXT
