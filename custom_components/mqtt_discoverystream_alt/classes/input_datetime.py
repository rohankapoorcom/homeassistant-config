"""input_datetime methods for MQTT Discovery Statestream."""

from homeassistant.components.input_datetime import DOMAIN as INPUT_DATETIME_DOMAIN

from ..helpers.base_input_entity import DateTimeDiscoveryEntity


class DiscoveryItem(DateTimeDiscoveryEntity):
    """Input_DateTime class."""

    PLATFORM = INPUT_DATETIME_DOMAIN
