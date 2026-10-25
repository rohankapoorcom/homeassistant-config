"""Infrared methods for MQTT Discovery Statestream."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.components.infrared import (
    InfraredDeviceClass,
    InfraredReceivedSignal,
    async_subscribe_receiver,
)
from homeassistant.components.mqtt.infrared import CONF_SCHEMA
from homeassistant.const import ATTR_STATE, EntityStateAttribute, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.json import JSONEncoder

from ..const import ATTR_MODULATION, ATTR_TIMINGS
from ..helpers.base_entity import DiscoveryEntity
from ..utils import EntityInfo

_LOGGER = logging.getLogger(__name__)


class DiscoveryItem(DiscoveryEntity):
    """Infrared class."""

    PLATFORM = Platform.INFRARED
    PUBLISH_STATE = False

    def build_config(self, config, entity_info: EntityInfo):
        """Build the config for a infrared."""

        schema = entity_info.attributes[EntityStateAttribute.DEVICE_CLASS]
        if schema == InfraredDeviceClass.EMITTER:
            _LOGGER.warning(
                "Infrared emitter not supported - %s", entity_info.entity_id
            )
            return False
        config[CONF_SCHEMA] = schema
        SignalConsumer(self._hass, self._publish_retain, self._base_topic, entity_info)
        return True


class SignalConsumer:
    """Class to handle infrared receiver signals."""

    def __init__(
        self, hass: HomeAssistant, publish_retain, base_topic, entity_info: EntityInfo
    ) -> None:
        """Class to manage signal receiver subscription."""
        self._hass = hass
        self._publish_retain = publish_retain
        self._mybase = f"{base_topic}/{entity_info.entity_id.replace('.', '/')}/"
        async_subscribe_receiver(hass, entity_info.entity_id, self._handle_signal)

    @callback
    def _handle_signal(self, signal: InfraredReceivedSignal):
        state = {ATTR_TIMINGS: signal.timings}
        if signal.modulation:
            state[ATTR_MODULATION] = signal.modulation
        self._mqtt_publish(ATTR_STATE, state, self._mybase, encoded=True)

    def _mqtt_publish(self, topic, value, mybase, encoded=False):
        if encoded:
            value = json.dumps(value, cls=JSONEncoder)
        mqtt.publish(
            self._hass,
            f"{mybase}{topic}",
            value,
            1,
            self._publish_retain,
        )
