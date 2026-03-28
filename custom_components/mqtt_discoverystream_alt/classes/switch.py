"""switch methods for MQTT Discovery Statestream."""

import logging

from homeassistant.const import (
    Platform,
)

from .base_input_entity import SwitchDiscoveryEntity

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(SwitchDiscoveryEntity):
    """Switch class."""

    PLATFORM = Platform.SWITCH
