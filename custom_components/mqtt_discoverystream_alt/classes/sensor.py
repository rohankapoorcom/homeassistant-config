"""sensor methods for MQTT Discovery Statestream."""

from homeassistant.components.mqtt.const import CONF_SUGGESTED_DISPLAY_PRECISION
from homeassistant.components.sensor import CONF_STATE_CLASS, DOMAIN as SENSOR_DOMAIN
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo, simple_attribute_add


class DiscoveryItem(DiscoveryEntity):
    """Sensor class."""

    PLATFORM = Platform.SENSOR

    def __init__(
        self,
        hass: HomeAssistant,
        base_topic,
        command_topic,
        publish_retain,
        discovered_entities,
        platform,
        publish_state,
    ) -> None:
        """Initialise the sensor class."""
        super().__init__(
            hass,
            base_topic,
            command_topic,
            publish_retain,
            discovered_entities,
            platform,
            publish_state,
        )
        self._ent_reg = er.async_get(hass)

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a sensor."""

        entry = self._ent_reg.async_get(entity_info.entity_id)
        simple_attribute_add(config, entity_info.attributes, CONF_STATE_CLASS)
        if entry and (options := entry.options) and SENSOR_DOMAIN in options:
            sensor_options = options[SENSOR_DOMAIN]
            if CONF_SUGGESTED_DISPLAY_PRECISION in sensor_options:
                config[CONF_SUGGESTED_DISPLAY_PRECISION] = sensor_options[
                    CONF_SUGGESTED_DISPLAY_PRECISION
                ]
