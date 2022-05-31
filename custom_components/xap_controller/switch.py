from datetime import timedelta

from homeassistant.components.switch import SwitchEntity, PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME, CONF_SWITCHES
import homeassistant.helpers.config_validation as cv

import logging
import voluptuous as vol

DOMAIN = 'xap_controller'
SCAN_INTERVAL = timedelta(seconds=1)

CONF_PATH     = 'path'
CONF_BAUD     = 'baud'
CONF_TYPE     = 'XAPType'

_LOGGER = logging.getLogger(__name__)

ZONE_SOURCE_SCHEMA = vol.Schema({
    cv.string: vol.All(cv.ensure_list, [vol.Any(int,str)])
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PATH): cv.string,
    vol.Required(CONF_SWITCHES): ZONE_SOURCE_SCHEMA,
    vol.Optional(CONF_TYPE, default="XAP800"): vol.In(["XAP800","XAP400"]),
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_BAUD, default=38400): int,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the XAPX00 Switch platform."""
    path = config.get(CONF_PATH)

    if path is None:
        _LOGGER.error("Invalid config. Expected %s",
                      CONF_PATH)
        return False    

    from XAPX00 import XAPX00
    _LOGGER.debug('XAPX00 version: {}'.format(XAPX00.__version__))
    _LOGGER.debug('XAP Type: {}'.format(config.get(CONF_TYPE)))
    xapconn = XAPX00.XAPX00(path, XAPType=config.get(CONF_TYPE))


    xapconn.baud = config[CONF_BAUD]

    xapconn.convertDb = 1
    if not xapconn.test_connection():
        _LOGGER.error('Not connected to %s', path)
        return


    for zone_name, outputs in config[CONF_SWITCHES].items():
        add_devices([XAPMuteSwitch(hass, xapconn, zone_name, outputs)])

class XAPMuteSwitch(SwitchEntity):
    """Representation of a XAPX00 switch."""

    def __init__(self, hass, xapconn, zone_name, outputs):
        """Initialize the switch."""
        self._name = zone_name
        self._xapx00 = xapconn
        self._outputs = outputs
        # outputs is a list of outputs, each element can be a single int or
        # a string of "int:int" (unit:output)
        self._isMuted = None
        self._unique_id = self.compute_unique_id()
        _LOGGER.info("zone {} set up".format(self.__str__()))

    def compute_unique_id(self):
        unique_id = []
        XUNIT, _ = self.parse_output(self._outputs[0])
        unique_id.append(str(self._xapx00.getUniqueId(XUNIT)))
        for output in self._outputs:
            XUNIT, XOUT = self.parse_output(output)
            unique_id.append(str(XOUT))
        unique_id.append("mute")
        return '_'.join(unique_id)
    
    def parse_output(self, output):
        "Returns (unit,output) "
        if type(output) is int:
            XUNIT = 0
            XOUT = output
        elif type(output) is str:
            if ":" in output:
                XUNIT, XOUT =  output.split(":")
            elif output.isdigit():
                XOUT = int(output)
            else:
                raise Exception('Invalid Output String')
        else:
            # shouldn't be able to get here
            raise Exception('Invalid Output config format')
        return int(XUNIT), int(XOUT)

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique_id of this device."""
        return self._unique_id
    
    
    def update(self):
        """Update the state."""
        XUNIT, XOUT = self.parse_output(self._outputs[0])
        self._isMuted = bool(self._xapx00.getMute(XOUT, group="O", unitCode=XUNIT))
        return self._isMuted

    @property
    def should_poll(self):
        """Update the state periodically."""
        return True

    @property
    def is_on(self):
        """Return True if the switch is on."""
        return not self._isMuted


    def turn_on(self, **kwargs):
        """Turn the switch on."""
        for output in self._outputs:
            XUNIT, XOUT = self.parse_output(output)
            muted = self._xapx00.setMute(XOUT, group="O", isMuted=0,
                                         unitCode = XUNIT)
        self._isMuted = False

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        for output in self._outputs:
            XUNIT, XOUT = self.parse_output(output)
            muted = self._xapx00.setMute(XOUT, group="O", isMuted=1,
                                         unitCode = XUNIT)
        self._isMuted = True
