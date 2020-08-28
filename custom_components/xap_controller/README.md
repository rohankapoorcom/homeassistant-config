## The XAPController platform allows the use of a ClearOne XAP 400 or 800 unit as an audio routing matrix with HomeAssistant.

At this time, it is set up only for routing audio, not for use with microphones.

Support for interfacing with ClearOne XAP800 and XAP400 units via serial port.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/media_player.xap_controller/
(no docs there until release)

There are two components in the platform: output Zones and input Sources.  The input sources are assumed to be XAP type I inputs, the output zones type O outputs.

The XAP system can have multple units linked together.  The configured Sources and Zones can specify only the channel for input or output, in which case it is assumed they are on unit 0.  They can also specify the unit, and optionally, for sources, an expansion bus that the source is also mapped to, so that it can be used on other units in the systems.  In this case, list the unit:channel of the source, and then the expansion channel and optinoally expansion group (E or P).  When sources or zones are specified with units and expansion buses, the items should be listed as a string of the format "<Unit#>:<Channel#>:<Expansion Bus Channel Letter>:<Expansion BUs Group>".  See below for an example.  For the expansion bus setup to work the matrix needs to have the sources mapped to the expansin channels through the G-Ware software.

The system can assume that the channels are set up for stereo, so that there are 2 channels paired 
together.  If stereo=1, the module will take each action twice, once on the listed source/zone number and again on the source/zone + 1.  This functionality may be removed in the future to promote clarity, so if ia stereo setup is used, it is recommneded to list each channel explicitly.

For each source or zone, multiple channels can be listed, as a list.  If multiple channels are listed for a source and an output, they will be paired sequentially, source item 1 to zone item 1, source item 2 to zone item 2, etc.  If there are more source channels than zone channels, only the first channels in the source will be used.  If there are more channels in a zone than in the source being applied ot it, the source channels will be repeated.  This multiple channel apporach can be used to handle stereo (instead of the stereo=1 approach), but it was added to handle surround sound sources / zones. The XAP system will mix multiple source channels applied to one output zone channel.

The platform will create individual media_player controls for each source and zone.  Each source will be shown with a volume slider, adjusting the gain for that input.  Each Zone will be shown with a dropbox to select from the available sources and a volume slider to adjust the gain for that output zone.

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
   sources are listed as either a digit, indicating the input channel on unit 0, or else a string of the format:  "<unit#>:<input#>:<bus letter>:<bus type>. Bus and Bus type are optional, but are needed if using more than 1 unit and you want a source to be available on outputs in other units.
* path: serial device path (can be a virtual serial port, using socat for example)
* name: the name of the platform instance
* stereo: 1=stereo, 0=mono  If stereo=1, each action will be performed twice on the input (output) and input+1 (output)+1
* baud: baud rate of serial port, 38400 (default), 9600, 19200, 57600
* XAPType: XAP unit type, eithr XAP800 (default) or XAP400

