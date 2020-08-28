"""
Support for interfacing with ClearOne XAP800 and XAP400 units via serial port.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.xap_controller/
(no docs there until release)

There are two components in the platform: output Zones and input Sources.  The input sources are assumed to be XAP
type I inputs, the output zones type O outputs. The XAP system can have multple units linked together.  The configured 
Sources and Zones can specify only the channel for input or output, in which case it is assumed they are on unit 0.  They 
can also specify the unit, and optionally, for sources, an expansion bus that the source is also mapped to, so that it 
can be used on other units in the systems.  In this case, list the unit:channel of the source, and then the expansion 
channel and optinoally expansion group (E or P).  When sources or zones are specified with units and expansion buses, 
the items should be listed as a string of the format "<Unit#>:<Channel#>:<Expansion Bus Channel Letter>:<Expansion BUS 
Group>".  See below for an example.  For the expansion bus setup to work the matrix needs to have the sources mapped to 
the expansin channels through the G-Ware software.

The system can assume that the channels are set up for stereo, so that there are 2 channels paired together.  If 
stereo=1, the module will take each action twice, once on the listed source/zone number and again on the source/zone + 1. 
This functionality may be removed in the future to promote clarity, so if ia stereo setup is used, it is recommneded to list 
each channel explicitly.

For each source or zone, multiple channels can be listed, as a list.  If multiple channels are listed for a source and 
an output, they will be paired sequentially, source item 1 to zone item 1, source item 2 to zone item 2, etc.  If there 
are more source channels than zone channels, only the first channels in the source will be used.  If there are more 
channels in a zone than in the source being applied ot it, the source channels will be repeated.  This multiple channel
 apporach can be used to handle stereo (instead of the stereo=1 approach), but it was added to handle surround sound
  sources / zones. The XAP system will mix multiple source channels applied to one output zone channel.

The platform will create individual media_player controls for each source and zone.  Each source will be shown with a
 volume slider, adjusting the gain for that input.  Each Zone will be shown with a dropbox to select from the available 
 sources and a volume slider to adjust the gain for that output zone.

Basic configuration
```
media_player:
   - platform: xap_controller
     path: /dev/ttyUSB-XAP800
     name: MyXAP
     stereo: 1 # 1 or 0, default is 0, recommend explicitly listing sterero channels
     baud: 38400 #default
     XAPType: XAP800 # XAP800 or XAP400, default is XAP800
     zones:
       'Office':
         - 1
       'Kitchen':
         - 3
       'Outside':
         - 5
       'Upstairs':
         - 7
       'Living/Dining/Library':
         - 9
       'WorkRoom':
         - "2:1"
     sources:
       'Home Audio':
         - 9
       'Family TV Audio':
         - 11
```

Multi-unit example
```
media_player:
   - platform: xap_controller
     path: /dev/ttyUSB-XAP800
     name: MyXAP
     stereo: 0
     baud: 38400
     zones:
       'Office':
         - "1:1"
         - "1:2"
       'Kitchen':
         - "1:3"
         - "1:4"
        'Family Room Surround':
         - "2:1"
         - "2:2"
         - "2:3"
         - "2:4"
         - "2:1"
         - "2:2"
         # Family Room Surround has no center speaker, so list the two front
         # speakers at the end and map the center channel to each of them

     sources:
       'Home Audio':
         - "1:9:O:E"
         - "1:10:P:E"
       'Family TV Surround Audio':
         - "2:1:V:E"
         - "2:2:W:E"
         - "2:3:X:E"
         - "2:4:Y:E"
         - "2:5:Z:E"
         - "2:5:Z:E"
         # Family Room Surround has no center channel, so list the center channel twice at the end,  
         # then it will be connected to the last 2 itens in the zone channel list
```

* zones: a list of output zone names, with a list of one or more outputs for each zone name. 
* sources: a list of source names, with a list of one or more sources per source name.
   sources are listed as either a digit, indicating the input channel on unit 0, or else a string of the format:  
   "<unit#>:<input#>:<bus letter>:<bus type>. 
   Bus and Bus type are optional, but are needed if using more than 1 unit and you want a source to be available 
   on outputs in other units.
* path: serial device path (can be a virtual serial port, using socat for example)
* name: the name of the platform instance
* stereo: 1=stereo, 0=mono  If stereo=1, each action will be performed twice on the input (output) and input+1 (output)+1
* baud: baud rate of serial port, 38400 (default), 9600, 19200, 57600
* XAPType: XAP unit type, eithr XAP800 (default) or XAP400

"""

import time
import logging
import voluptuous as vol
from string import ascii_uppercase

from homeassistant.components.media_player import (
     MediaPlayerEntity, PLATFORM_SCHEMA)

from homeassistant.components.media_player.const import (
    SUPPORT_TURN_OFF, SUPPORT_TURN_ON, SUPPORT_VOLUME_MUTE,
    SUPPORT_VOLUME_SET, SUPPORT_SELECT_SOURCE, MEDIA_TYPE_MUSIC)

from homeassistant.const import (
    STATE_OFF, STATE_ON, CONF_NAME)

import homeassistant.helpers.config_validation as cv

REQUIREMENTS = [
   'https://github.com/jslove/XAPX00/archive/0.2.8.2.zip'
   '#XAPX00==0.2.8.2' ]

testing = 0

DOMAIN = 'xap_controller'

_LOGGER = logging.getLogger(__name__)

CONF_ZONES    = 'zones'
CONF_SOURCES  = 'sources'
CONF_PATH     = 'path'
CONF_STEREO   = 'stereo'
CONF_BAUD     = 'baud'
CONF_TYPE     = 'XAPType'

SRC_OFF = 'Off'

SUPPORT_XAP_ZONE = \
                   SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_SET | \
                   SUPPORT_TURN_ON | SUPPORT_TURN_OFF | \
                   SUPPORT_SELECT_SOURCE

SUPPORT_XAP_SOURCE = SUPPORT_VOLUME_MUTE | SUPPORT_VOLUME_SET | \
                     SUPPORT_TURN_ON | SUPPORT_TURN_OFF


#OUTPUT_SCHEMA = vol.Schema({
#    vol.Required(CONF_NAME): cv.string,
#})

ZONE_SOURCE_SCHEMA = vol.Schema({
    cv.string: vol.All(cv.ensure_list, [vol.Any(int,str)])
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PATH): cv.string,
    vol.Required(CONF_ZONES): ZONE_SOURCE_SCHEMA,
    vol.Required(CONF_SOURCES): ZONE_SOURCE_SCHEMA,
    vol.Optional(CONF_TYPE, default="XAP800"): vol.In(["XAP800","XAP400"]),
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_STEREO): cv.boolean,
    vol.Optional(CONF_BAUD): int,
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the XAPX00 platform."""
    path = config.get(CONF_PATH)

    if path is None:
        _LOGGER.error("Invalid config. Expected %s",
                      CONF_PATH)
        return False

    sources = config[CONF_SOURCES]
    _LOGGER.debug("Conf file sources: {}".format(sources))
    

    from XAPX00 import XAPX00
    _LOGGER.debug('XAPX00 version: {}'.format(XAPX00.__version__))
    _LOGGER.debug('XAP Type: {}'.format(config.get(CONF_TYPE)))
    xapconn = XAPX00.XAPX00(path, XAPType=config.get(CONF_TYPE))

    if config.get(CONF_STEREO, 0) == 0:
        xapconn.stereo = 0
    else:
        xapconn.stereo = 1

    xapconn.baud = config.get(CONF_BAUD, 38400)

    xapconn.convertDb = 1
    if not xapconn.test_connection():
        _LOGGER.error('Not connected to %s', path)
        return

    source_objs=[]
    zonesources = {}
    for source_name, source_input in sources.items():
        sourceobj = XAPSource(
            hass, xapconn, source_name, source_input)
        add_devices([sourceobj])
        source_objs.append(sourceobj)
        zonesources[source_name] = sourceobj

    zonesources[SRC_OFF] = 0

    for zone_name, outputs in config[CONF_ZONES].items():
        add_devices([XAPZone(
            hass, xapconn, zonesources, zone_name, outputs)])


class XAPSource(MediaPlayerEntity):
    """
    Represents one source
    """

    def __init__(self, hass, xapconn, source_name, source_inputs, unitCode=0):
        """Initialise the XAPX00 source pseudo-device"""
        _LOGGER.debug("Setting Up Source %s" % source_name)
        self._name = source_name
        self._xapx00 = xapconn
        self._state = STATE_ON
        self.xunit = 0
        self.xinput = None
        self.xgroup = "I"
        self.xbus = None
        self.xbusgroup = None
        self._inputs = []
        self.parse_source(source_inputs)
        self.numChannels = len(self._inputs)
        self._volume = self.get_volume_level()
        self.set_volume_level(self._volume) # make sure synced
        self.get_mute_status()
        if self._isMuted:
            self._state = STATE_OFF
        self.mute_volume(self._isMuted) # sync
        _LOGGER.info("source {} set up".format(self.__str__()))

    def __str__(self):
        return self._name

    def __repr__(self):
        return "{} ({})".format(self._name, self._inputs)

    def parse_source(self, srcs):
        "Split into input unit, input #, expansion bus, expansion bus group"
        for src in srcs:
            inpdict={'UNIT':0,'CHAN':None,'BUS':None, 'BUSGRP':'E', 'INPGRP':'I'} 
            if type(src) is int:
                inpdict['CHAN'] = src
            elif type(src) is str:
                if ":" in src:
                    comps = src.count(':')
                    if comps == 1:
                        inpdict['UNIT'], inpdict['CHAN']  =  src.split(":")
                    elif comps == 2:
                        inpdict['UNIT'], inpdict['CHAN'], inpdict['BUS'] = src.split(":")
                        XBUSGRP = 'E' # default to E
                    elif comps == 3:
                        inpdict['UNIT'], inpdict['CHAN'], inpdict['BUS'], inpdict['BUSGRP'] = src.split(":")
                    inpdict['CHAN'] = int(inpdict['CHAN'])
                    inpdict['UNIT'] = int(inpdict['UNIT'])
                elif src.isdigit():
                    inpdict['CHAN'] = int(src)
                else:
                    raise Exception('Invalid Input String')
            else:
                # shouldn't be able to get here
                raise Exception('Invalid Source Input config format')
            self._inputs.append(inpdict)
        return

    def getSource(self, outUnit, srcNum=0):
        outUnit = int(outUnit)
        srcNum = srcNum % self.numChannels  # wrap if request is greater than number of sources
        if outUnit == self._inputs[srcNum]['UNIT']:
            return  self._inputs[srcNum]['CHAN'],  self._inputs[srcNum]['INPGRP']
        else:
            if self._inputs[srcNum]['BUS'] is None:
                raise Exception("Different unit but No Expansion Bus Defined")
            return self._inputs[srcNum]['BUS'], self._inputs[srcNum]['BUSGRP']
    
    def source_for_zones(self):
        raise Exception("Not Implemented")
        if self.xbus is not None:
            # either expansion or processing
            group = 'E' if self.xbus in self._xapx00.ExpansionChannels else 'P'
            channel = self.xbus
        else:
            channel = self.xinput
            group = "I"
        return channel, group
    
    @property
    def name(self):
        """Return the name of the source."""
        return "Source: " + self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Flag of media commands that are supported."""
        return SUPPORT_XAP_SOURCE

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def is_volume_muted(self):
        """ return bool mute status"""
        return bool(self._isMuted)

    def get_volume_level(self):
        """Volume level of the media player (0..1)."""
        vinp = self._inputs[0]
        gain = self._xapx00.getPropGain(vinp['CHAN'], group="I", unitCode = vinp['UNIT'])
        self._volume = gain
        return self._volume

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        for s in self._inputs:
            volume = self._xapx00.setPropGain(s['CHAN'], volume,
                                              isAbsolute=1, group="I", unitCode = s['UNIT'])
        self._volume = volume

    def turn_on(self):
        """Turn the media player on."""
        self.mute_volume(mute=0)
        self._state = STATE_ON

    def turn_off(self):
        """Turn off media player."""
        self.mute_volume(mute=1)
        self._state = STATE_OFF

    def mute_volume(self, mute=2):
        """Toggle mute"""
        self._isMuted = self._xapx00.setMute(self._inputs[0]['CHAN'], group="I", isMuted=int(mute), unitCode = self._inputs[0]['UNIT'])
        for s in self._inputs[1:]:
            self._isMuted = self._xapx00.setMute(s['CHAN'], group="I", isMuted=self._isMuted, unitCode = s['UNIT'])            

    def get_mute_status(self):
        self._isMuted = self._xapx00.getMute(self._inputs[0]['CHAN'], group="I", unitCode = self._inputs[0]['UNIT'])
        return self._isMuted


class XAPZone(MediaPlayerEntity):
    """
    Represents one or more XAP outputs, either mono or stereo
    """
    def __init__(self, hass, xapconn, sources, zone_name, outputs, unitCode=0):
        """Initialise the XAPX00 zone pseudo-device"""
        self._name = zone_name
        self._xapx00 = xapconn
        self._unitCode = unitCode
        self._sources = sources #dict of source name:source obj
        self._outputs = outputs
        # outputs is a list of outputs, each element can be a single int or
        # a string of "int:int" (unit:output)
        self._volume = 0
        self._defaultMatrixLevel = 1
        self._isMuted = self.get_mute_status()
        self._active_source = SRC_OFF
        self._active_source = self.get_source()
        self._poweroff_source = self._active_source
        # make sure sources synced across outputs
        self.select_source(self._active_source)
        self.get_volume_level()
        self._sync_volume_level()
        self._state = STATE_ON if self._active_source != SRC_OFF else STATE_OFF
        _LOGGER.info("zone {} set up".format(self.__str__()))

    def __str__(self):
        return self._name
        
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
            
    def update(self):
#        self.get_mute_status()
#        self.get_volume_level()
        pass  # can't be exchanged except by us, so can track state without calls
    
    def select_source(self, source):
        """Set the input source"""
        actsrc = self._active_source  # a string
        _LOGGER.debug('select_source for zone={}: source={}, actsrc={}, self._sources={}'.format(
            self._name, source, actsrc, self._sources.keys()))
        if source not in self._sources:
            raise Exception("Requested source {} not in set up sources".format(source))
        cnt=0
        for xOut in self._outputs:
            XUNIT, XOUT = self.parse_output(xOut)
            if actsrc != SRC_OFF and actsrc != source:
                XIN, XINGRP = self._sources[actsrc].getSource(XUNIT,cnt)
                self._xapx00.setMatrixRouting(XIN, XOUT, 0, inGroup = XINGRP, unitCode = XUNIT) #turn current off
                _LOGGER.debug('Turned off actsrc: {}'.format(actsrc))
            if source != SRC_OFF: #and source in self._sources:
                XIN, XINGRP = self._sources[source].getSource(XUNIT, cnt)
                ON = 3 if (type(XIN) is int and XIN <= (self._xapx00.matrixGeo-4)) else 1
                # if a mike input on=3, if line on=1, last 4 inputs are line
                self._xapx00.setMatrixRouting(XIN, XOUT, ON, inGroup = XINGRP, unitCode = XUNIT)
                self._poweroff_source = source # in case turn_on called without calling turn_off
            cnt += 1
        self._active_source = source
 
    def get_source(self):
        """Get first active source for outputs in this zone
           Since an input can be part of multiple sources, need to make this more sophisticated,
           need to for all channels being on.
        """
        _LOGGER.debug("In get_source for {}".format(self))
        _LOGGER.debug("  Checking: {}".format(self._sources))
        for xIn in self._sources.values():
            if xIn != self._sources[SRC_OFF]:
                XUNIT, XOUT = self.parse_output(self._outputs[0])
                XIN, XINGRP = xIn.getSource(XUNIT)
                z_state = int(self._xapx00.getMatrixRouting(XIN,
                                                            XOUT,
                                                            inGroup = XINGRP,
                                                            unitCode = XUNIT))
                _LOGGER.debug("matrix routing for {}={}". format(xIn, z_state))
                if z_state > 0:
                    self._active_source = xIn.__str__()
                    break
        _LOGGER.debug("get_source for %s = %s" % (self._name, self._active_source))
        return self._active_source
        
    @property
    def name(self):
        """Return the name of the zone."""
        return "Zone: " + self._name

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def supported_features(self):
        """Flag of media commands that are supported."""
        return SUPPORT_XAP_ZONE

    @property
    def volume_level(self):
        """Volume level of the media player (0..1)."""
        return self._volume

    @property
    def media_content_type(self):
        return MEDIA_TYPE_MUSIC

    @property
    def media_title(self):
        """ Return current source"""
        return self._active_source

    @property
    def is_volume_muted(self):
        """ return mute status"""
        return bool(self._isMuted)

    def setDefaultLevel(self):
        """  set all crosspoint levels to default """
        cnt = 0
        for xOut in self._outputs:
            XUNIT, XOUT = self.parse_output(xOut)
            for xIn in self._sources.values():
                XIN, XINGRP = xIn.getSource(XUNIT,cnt)
                self._xapx00.setMatrixLevel(XIN, XOUT,
                                            self._defaultMatrixLevel,
                                            inGroup =  XINGRP,
                                            unitCode = XUNIT)
            cnt += 1

#   not used
    def clear_matrix(self):
        """ set all crosspoints to off"""
        for xOut in self._outputs:
            XUNIT, XOUT = self.parse_output(xOut)
            for xIn in self._xapx00.input_range:
                self._xapx00.setMatrixRouting(xIn, xOut, 0, unitCode=XUNIT)
            for xIn in list(ascii_uppercase[ascii_uppercase.find('O'):]):
                self._xapx00.setMatrixRouting(xIn, xOut, 0, inGroup='E', unitCode=XUNIT)

    def _sync_volume_level(self):
        """set all level of all outputs in zone to the same
        level as the first one in zone"""
        if self._active_source != SRC_OFF:
            XUNIT, XOUT = self.parse_output(self._outputs[0])
            volume = self._xapx00.getPropGain(XOUT, group="O",
                                              unitCode = XUNIT)
            self.set_volume_level(volume)

    def set_volume_level(self, volume):
        """Set volume level, range 0..1."""
        _LOGGER.debug("set_volume_level: {}:{}".format(self, volume))
        for output in self._outputs:
            XUNIT, XOUT = self.parse_output(output)
            _LOGGER.debug("Set Volume for output {} to {}".format(output, volume))
            volume = self._xapx00.setPropGain(XOUT, volume, group="O",
                                              unitCode = XUNIT)
        self._volume = volume

    def get_volume_level(self):
        """Volume level of the media player (0..1)."""
        XUNIT, XOUT = self.parse_output(self._outputs[0])
        gain = self._xapx00.getPropGain(XOUT, group="O", unitCode = XUNIT)
        self._volume = gain
        return self._volume

    def turn_on(self):
        """Turn zone on"""
        _LOGGER.debug("turn_on {}".format(self))
        self.select_source(self._poweroff_source)
        self.mute_volume(0)
        self._state = STATE_ON

    def turn_off(self):
        """Turn off zone"""
        _LOGGER.debug("turn_off {}".format(self))
        self._state = STATE_OFF
        self._poweroff_source = self._active_source
        self.select_source(SRC_OFF)
        self.mute_volume(1)

    def mute_volume(self, mute=2):
        """Send mute command, mute is bool from hass, default is 2 (toggle)"""
        XUNIT, XOUT = self.parse_output(self._outputs[0])
        muted = self._xapx00.setMute(XOUT, group="O", isMuted=int(mute),
                                     unitCode = XUNIT)
        for output in self._outputs[1:]:
            XUNIT, XOUT = self.parse_output(output)
            muted = self._xapx00.setMute(XOUT, group="O", isMuted=int(muted),
                                         unitCode = XUNIT)
        self._isMuted = bool(muted)

    def get_mute_status(self):
        XUNIT, XOUT = self.parse_output(self._outputs[0])
        self._isMuted = bool(self._xapx00.getMute(XOUT, group="O", unitCode=XUNIT))
        return self._isMuted

    @property
    def source_list(self):
        """List of available input sources."""
        return list(self._sources.keys())

    @property
    def source(self):
        """ Current source"""
        return self._active_source

