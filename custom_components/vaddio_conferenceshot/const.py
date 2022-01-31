import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_PATH, CONF_USERNAME

DOMAIN = "vaddio_conferenceshot"

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

SERVICE_RECALL_PRESET = "move_to_preset"
ATTR_PRESET_ID = "preset"
