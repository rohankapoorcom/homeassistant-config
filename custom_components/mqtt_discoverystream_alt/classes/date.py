"""date methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from ..helpers.base_input_entity import DateTimeDiscoveryEntity


class DiscoveryItem(DateTimeDiscoveryEntity):
    """Date class."""

    PLATFORM = Platform.DATE
