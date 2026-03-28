"""device_tracker methods for MQTT Discovery Statestream."""

from homeassistant.const import Platform

from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Device Tracker class."""

    PLATFORM = Platform.DEVICE_TRACKER
