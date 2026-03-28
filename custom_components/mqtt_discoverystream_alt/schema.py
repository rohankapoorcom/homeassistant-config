"""Schema for MQTT Discovery Stream."""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.mqtt import valid_publish_topic
from homeassistant.components.mqtt.const import (
    CONF_TOPIC,
    DEFAULT_PAYLOAD_AVAILABLE,
    DEFAULT_PAYLOAD_NOT_AVAILABLE,
)
from homeassistant.helpers.entityfilter import INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA

from .const import (
    CONF_BASE_TOPIC,
    CONF_COMMAND_TOPIC,
    CONF_DISCOVERY_TOPIC,
    CONF_LOCAL_STATUS,
    CONF_OFFLINE_STATUS,
    CONF_ONLINE_STATUS,
    CONF_PUBLISH_ATTRIBUTES,
    CONF_PUBLISH_DISCOVERY,
    CONF_PUBLISH_RETAIN,
    CONF_PUBLISH_TIMESTAMPS,
    CONF_REMOTE_STATUS,
    CONF_REPUBLISH_TIME,
    CONF_UNIQUE_PREFIX,
    DEFAULT_REFRESH_TIME,
    DEFAULT_RETAIN,
    DOMAIN,
)

LOCAL_STATUS = vol.Schema(
    {
        vol.Optional(CONF_TOPIC): vol.Any(valid_publish_topic, None),
        vol.Optional(CONF_ONLINE_STATUS, default=DEFAULT_PAYLOAD_AVAILABLE): cv.string,
        vol.Optional(
            CONF_OFFLINE_STATUS, default=DEFAULT_PAYLOAD_NOT_AVAILABLE
        ): cv.string,
    }
)

REMOTE_STATUS = vol.Schema(
    {
        vol.Optional(CONF_TOPIC): vol.Any(valid_publish_topic, None),
        vol.Optional(CONF_ONLINE_STATUS, default=DEFAULT_PAYLOAD_AVAILABLE): cv.string,
    }
)

BASE_SCHEMA = {
    vol.Required(CONF_BASE_TOPIC): valid_publish_topic,
    vol.Optional(CONF_DISCOVERY_TOPIC): vol.Any(valid_publish_topic, None),
    vol.Optional(CONF_COMMAND_TOPIC): vol.Any(valid_publish_topic, None),
    vol.Optional(CONF_REMOTE_STATUS): REMOTE_STATUS,
    vol.Optional(CONF_LOCAL_STATUS): LOCAL_STATUS,
    vol.Optional(CONF_PUBLISH_ATTRIBUTES, default=False): cv.boolean,
    vol.Optional(CONF_PUBLISH_TIMESTAMPS, default=False): cv.boolean,
    vol.Optional(CONF_PUBLISH_DISCOVERY, default=False): cv.boolean,
    vol.Optional(CONF_PUBLISH_RETAIN, default=DEFAULT_RETAIN): cv.boolean,
    vol.Optional(CONF_UNIQUE_PREFIX, default="mqtt"): cv.string,
    vol.Optional(CONF_REPUBLISH_TIME, default=DEFAULT_REFRESH_TIME): cv.time_period,
}


CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            [INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(BASE_SCHEMA)],
            "schema_type",
        ),
    },
    extra=vol.ALLOW_EXTRA,
)
# CONFIG_SCHEMA = vol.Schema(
#     {
#         DOMAIN: [INCLUDE_EXCLUDE_BASE_FILTER_SCHEMA.extend(BASE_SCHEMA)],
#     },
#     extra=vol.ALLOW_EXTRA,
# )
