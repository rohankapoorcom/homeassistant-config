"""number methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_input_entity import NumberDiscoveryEntity


class DiscoveryItem(NumberDiscoveryEntity):
    """Number class."""

    PLATFORM = Platform.NUMBER
