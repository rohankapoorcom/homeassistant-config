"""input_select methods for MQTT Discovery Statestream."""

from homeassistant.components.input_select import DOMAIN as INPUT_SELECT_DOMAIN

from .base_input_entity import SelectDiscoveryEntity


class DiscoveryItem(SelectDiscoveryEntity):
    """Input_Select class."""

    PLATFORM = INPUT_SELECT_DOMAIN
