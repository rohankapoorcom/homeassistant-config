"""button methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_input_entity import ButtonDiscoveryEntity


class DiscoveryItem(ButtonDiscoveryEntity):
    """Button class."""

    PLATFORM = Platform.BUTTON
