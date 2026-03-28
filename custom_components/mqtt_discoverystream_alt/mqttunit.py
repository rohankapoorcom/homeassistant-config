"""Publish simple item state changes via MQTT."""

import json
import logging

from homeassistant.components import mqtt
from homeassistant.const import EVENT_HOMEASSISTANT_STOP, EVENT_STATE_CHANGED
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.entityfilter import convert_include_exclude_filter
from homeassistant.helpers.json import JSONEncoder
from homeassistant.helpers.start import async_at_start

from .const import (
    CONF_BASE_TOPIC,
    CONF_PUBLISH_ATTRIBUTES,
    CONF_PUBLISH_DISCOVERY,
    CONF_PUBLISH_RETAIN,
    CONF_PUBLISH_TIMESTAMPS,
)
from .publisher import Publisher

_LOGGER = logging.getLogger(__name__)


class MQTTUnit:
    """A single MQTT config."""

    def __init__(self, conf):
        """Initialise MQTT unit."""
        self._conf = conf
        self.publisher = None

    def setup_unit(self, hass):
        """Setup the MQTT Unit."""
        publish_filter = convert_include_exclude_filter(self._conf)
        base_topic: str | None = self._conf.get(CONF_BASE_TOPIC)
        publish_attributes: bool | None = self._conf.get(CONF_PUBLISH_ATTRIBUTES)
        publish_timestamps: bool | None = self._conf.get(CONF_PUBLISH_TIMESTAMPS)
        publish_retain: bool | None = self._conf.get(CONF_PUBLISH_RETAIN)
        if not base_topic.endswith("/"):
            base_topic = f"{base_topic}/"

        publish_discovery = self._conf.get(CONF_PUBLISH_DISCOVERY)
        if publish_discovery:
            self.publisher = Publisher(hass, self._conf, base_topic, publish_retain)

        async def _state_publisher(evt: Event[EventStateChangedData]) -> None:
            entity_id = evt.data["entity_id"]
            new_state = evt.data["new_state"]
            assert new_state

            mybase = f"{base_topic}{entity_id.replace('.', '/')}/"
            if publish_discovery:
                await self.publisher.async_state_publish(entity_id, new_state, mybase)
            else:
                payload = new_state.state
                await _async_mqtt_publish(f"{mybase}state", payload)

            if publish_timestamps:
                if new_state.last_updated:
                    await _async_mqtt_publish(
                        f"{mybase}last_updated", new_state.last_updated.isoformat()
                    )
                if new_state.last_changed:
                    await _async_mqtt_publish(
                        f"{mybase}last_changed", new_state.last_changed.isoformat()
                    )
            if publish_attributes:
                for key, val in new_state.attributes.items():
                    await _async_mqtt_publish(f"{mybase}{key}", val, encoded=True)

        @callback
        def _ha_started(hass: HomeAssistant) -> None:
            @callback
            def _event_filter(event_data: EventStateChangedData) -> bool:
                entity_id = event_data["entity_id"]
                new_state = event_data["new_state"]
                return False if new_state is None else bool(publish_filter(entity_id))

            callback_handler = hass.bus.async_listen(
                EVENT_STATE_CHANGED, _state_publisher, _event_filter
            )

            @callback
            def _ha_stopping(_: Event) -> None:
                callback_handler()

            hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, _ha_stopping)

        async def _async_mqtt_publish(mybase, value, encoded=False):
            if encoded:
                value = json.dumps(value, cls=JSONEncoder)
            await mqtt.async_publish(hass, mybase, value, 1, publish_retain)

        async_at_start(hass, _ha_started)

        return True
