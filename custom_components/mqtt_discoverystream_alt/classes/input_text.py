"""input_text methods for MQTT Discovery Statestream."""

from homeassistant.components.input_text import DOMAIN as INPUT_TEXT_DOMAIN

from .base_input_entity import TextDiscoveryEntity


class DiscoveryItem(TextDiscoveryEntity):
    """Input_Text class."""

    PLATFORM = INPUT_TEXT_DOMAIN
