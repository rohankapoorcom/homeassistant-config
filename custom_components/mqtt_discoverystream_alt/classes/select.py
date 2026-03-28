"""select methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_input_entity import SelectDiscoveryEntity


class DiscoveryItem(SelectDiscoveryEntity):
    """Select class."""

    PLATFORM = Platform.SELECT
