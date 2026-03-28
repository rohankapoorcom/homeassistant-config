"""input_boolean methods for MQTT Discovery Statestream."""

from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN

from .base_input_entity import SwitchDiscoveryEntity


class DiscoveryItem(SwitchDiscoveryEntity):
    """Input_Boolean class."""

    PLATFORM = INPUT_BOOLEAN_DOMAIN
