"""sensor methods for MQTT Discovery Statestream."""

from homeassistant.components.sensor import DOMAIN as sensordomain
from homeassistant.const import Platform
from homeassistant.helpers import entity_registry

from ..const import ATTR_SUGGESTED_DISPLAY_PRECISION, CONF_SUG_DSP_PRC
from ..utils import EntityInfo
from .base_entity import DiscoveryEntity


class DiscoveryItem(DiscoveryEntity):
    """Sensor class."""

    PLATFORM = Platform.SENSOR

    def __init__(
        self,
        hass,
        base_topic,
        publish_retain,
        discovered_entities,
        platform,
        publish_state,
    ):
        """Initialise the sensor class."""
        super().__init__(
            hass,
            base_topic,
            publish_retain,
            discovered_entities,
            platform,
            publish_state,
        )
        self._ent_reg = entity_registry.async_get(hass)

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a sensor."""

        if entry := self._ent_reg.async_get(entity_info.entity_id):
            if options := entry.options:
                if sensordomain in options:
                    sensor_options = options[sensordomain]
                    if ATTR_SUGGESTED_DISPLAY_PRECISION in sensor_options:
                        config[CONF_SUG_DSP_PRC] = sensor_options[
                            ATTR_SUGGESTED_DISPLAY_PRECISION
                        ]
