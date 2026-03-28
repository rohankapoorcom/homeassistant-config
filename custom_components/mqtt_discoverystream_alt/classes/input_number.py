"""input_number methods for MQTT Discovery Statestream."""

from homeassistant.components.input_number import DOMAIN as INPUT_NUMBER_DOMAIN

from .base_input_entity import NumberDiscoveryEntity


class DiscoveryItem(NumberDiscoveryEntity):
    """Input_Number class."""

    PLATFORM = INPUT_NUMBER_DOMAIN
