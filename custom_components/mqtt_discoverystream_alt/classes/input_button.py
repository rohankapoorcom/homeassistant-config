"""input_button methods for MQTT Discovery Statestream."""

from homeassistant.components.input_button import DOMAIN as INPUT_BUTTON_DOMAIN

from .base_input_entity import ButtonDiscoveryEntity


class DiscoveryItem(ButtonDiscoveryEntity):
    """Input_Button class."""

    PLATFORM = INPUT_BUTTON_DOMAIN
