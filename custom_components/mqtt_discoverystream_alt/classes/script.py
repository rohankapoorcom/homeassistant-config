"""script methods for MQTT Discovery Statestream."""

from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN

from .base_input_entity import ScriptDiscoveryEntity


class DiscoveryItem(ScriptDiscoveryEntity):
    """Script class."""

    PLATFORM = SCRIPT_DOMAIN
