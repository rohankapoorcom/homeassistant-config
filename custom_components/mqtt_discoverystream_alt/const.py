"""Constants for MQTT Discovery Stream."""

from datetime import timedelta

from homeassistant.components.input_boolean import DOMAIN as INPUT_BOOLEAN_DOMAIN
from homeassistant.components.input_button import DOMAIN as INPUT_BUTTON_DOMAIN
from homeassistant.components.input_datetime import DOMAIN as INPUT_DATETIME_DOMAIN
from homeassistant.components.input_number import DOMAIN as INPUT_NUMBER_DOMAIN
from homeassistant.components.input_select import DOMAIN as INPUT_SELECT_DOMAIN
from homeassistant.components.input_text import DOMAIN as INPUT_TEXT_DOMAIN
from homeassistant.components.script import DOMAIN as SCRIPT_DOMAIN
from homeassistant.components.tag import DOMAIN as TAG_DOMAIN
from homeassistant.const import Platform

ATTR_COLOR = "color"  # pylint: disable=invalid-name
ATTR_H = "h"
ATTR_S = "s"
ATTR_X = "x"
ATTR_Y = "y"
ATTR_R = "r"
ATTR_G = "g"
ATTR_B = "b"

ATTR_ATTRIBUTES = "attributes"
ATTR_COLOR = "color"  # pylint: disable=invalid-name
ATTR_CONFIG = "config"
ATTR_DATETIME = "datetime"
ATTR_INSTALL = "install"
ATTR_JSON = "JSON"
ATTR_MODE = "mode"
ATTR_MODULATION = "modulation"
ATTR_TIMINGS = "timings"

COMMAND_ACTION = "action"
COMMAND_CODE = "code"
COMMAND_DIRECTION = "command_direction"
COMMAND_FAN = "command_fan"
COMMAND_HUMIDITY = "command_humidity"
COMMAND_INSTALL = "install"
COMMAND_MODE = "command_mode"
COMMAND_OSCILLATION = "command_oscillation"
COMMAND_PERCENTAGE = "command_percentage"
COMMAND_PRESET = "command_preset"
COMMAND_SEND = "command_send"
COMMAND_SET = "set"
COMMAND_SET_DATE = "set_date"
COMMAND_SET_DATETIME = "set_datetime"
COMMAND_SET_FAN_SPEED = "set_fan_speed"
COMMAND_SET_LIGHT = "set_light"
COMMAND_SET_POSITION = "set_position"
COMMAND_SET_TILT = "set_tilt"
COMMAND_SET_TIME = "set_time"
COMMAND_SWING = "command_swing"
COMMAND_TEMPERATURE = "command_temperature"


CONF_BASE_TOPIC = "base_topic"
CONF_COMMAND_TOPIC = "command_topic"
CONF_DISCOVERY_TOPIC = "discovery_topic"
CONF_LOCAL_STATUS = "local_status"
CONF_OFFLINE_STATUS = "offline_status"
CONF_ONLINE_STATUS = "online_status"
CONF_PUBLISH_ATTRIBUTES = "publish_attributes"
CONF_PUBLISH_TIMESTAMPS = "publish_timestamps"
CONF_PUBLISH_DISCOVERY = "publish_discovery"
CONF_PUBLISH_RETAIN = "publish_retain"
CONF_REMOTE_STATUS = "remote_status"
CONF_REPUBLISH_TIME = "republish_time"
CONF_STALE_AFTER = "stale_after"
CONF_UNIQUE_PREFIX = "unique_prefix"
CONF_UNIQUE_ENTITY_PREFIX = "unique_entity_prefix"

CONF_TILDA = "~"

DEFAULT_REFRESH_TIME = timedelta(minutes=5)
DEFAULT_RETAIN = False
DEFAULT_STATE_SLEEP = 1.5

DOMAIN = "mqtt_discoverystream_alt"

STARTUP_DELAY = 0.5

STATE_CAPITAL_ON = "ON"
STATE_CAPITAL_OFF = "OFF"

SUPPORTED_ENTITY_TYPE_COMMANDS = {
    Platform.ALARM_CONTROL_PANEL: [COMMAND_SET],
    Platform.BINARY_SENSOR: [],
    Platform.BUTTON: [COMMAND_SET],
    Platform.CLIMATE: [
        COMMAND_FAN,
        COMMAND_HUMIDITY,
        COMMAND_MODE,
        COMMAND_SET,
        COMMAND_PRESET,
        COMMAND_SWING,
        COMMAND_TEMPERATURE,
    ],
    Platform.COVER: [COMMAND_SET, COMMAND_SET_POSITION, COMMAND_SET_TILT],
    Platform.DATE: [COMMAND_SET_DATE],
    Platform.DATETIME: [COMMAND_SET_DATETIME],
    Platform.DEVICE_TRACKER: [],
    Platform.EVENT: [],
    Platform.FAN: [
        COMMAND_SET,
        COMMAND_DIRECTION,
        COMMAND_OSCILLATION,
        COMMAND_PERCENTAGE,
        COMMAND_PRESET,
    ],
    Platform.HUMIDIFIER: [COMMAND_SET, COMMAND_HUMIDITY, COMMAND_MODE],
    Platform.IMAGE: [],
    Platform.INFRARED: [],
    Platform.LAWN_MOWER: [COMMAND_SET],
    Platform.LIGHT: [COMMAND_SET_LIGHT],
    Platform.LOCK: [COMMAND_SET],
    Platform.NUMBER: [COMMAND_SET],
    Platform.SCENE: [COMMAND_SET],
    Platform.SELECT: [COMMAND_SET],
    Platform.SENSOR: [],
    Platform.SIREN: [COMMAND_SET],
    Platform.SWITCH: [COMMAND_SET],
    Platform.TEXT: [COMMAND_SET],
    Platform.TIME: [COMMAND_SET_TIME],
    Platform.UPDATE: [COMMAND_INSTALL],
    Platform.VACUUM: [COMMAND_SEND, COMMAND_SET, COMMAND_SET_FAN_SPEED],
    Platform.VALVE: [COMMAND_SET],
    Platform.WATER_HEATER: [COMMAND_MODE, COMMAND_SET, COMMAND_TEMPERATURE],
    INPUT_BOOLEAN_DOMAIN: [COMMAND_SET],
    INPUT_BUTTON_DOMAIN: [COMMAND_SET],
    INPUT_DATETIME_DOMAIN: [COMMAND_SET_DATETIME, COMMAND_SET_DATE, COMMAND_SET_TIME],
    INPUT_NUMBER_DOMAIN: [COMMAND_SET],
    INPUT_SELECT_DOMAIN: [COMMAND_SET],
    INPUT_TEXT_DOMAIN: [COMMAND_SET],
    SCRIPT_DOMAIN: [COMMAND_SET],
    TAG_DOMAIN: [],
}

# INPUT_DATETIME not included here since it is a special case
# and is translated to datetime, date or time as appropriate
OUTPUT_ENTITIES = {
    INPUT_BOOLEAN_DOMAIN: Platform.SWITCH,
    INPUT_BUTTON_DOMAIN: Platform.BUTTON,
    INPUT_NUMBER_DOMAIN: Platform.NUMBER,
    INPUT_SELECT_DOMAIN: Platform.SELECT,
    INPUT_TEXT_DOMAIN: Platform.TEXT,
    SCRIPT_DOMAIN: Platform.BUTTON,
    TAG_DOMAIN: Platform.SENSOR,
}

SERVICE_SET_DATETIME = "set_datetime"
