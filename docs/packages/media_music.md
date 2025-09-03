# Media Music Package Documentation

## Overview
The media music package manages whole-home audio and entertainment systems, including Chromecast Audio devices, Harmony remote integration, and automated speaker control. This package provides comprehensive audio distribution, volume management, and entertainment system automation across multiple zones.

## Configuration Files
- `packages/media_music.yaml`: Main media and music configuration

## Functionality
The media music package provides:
- **Whole-Home Audio**: Multi-zone audio distribution via Chromecast Audio devices
- **Harmony Integration**: Logitech Harmony remote control for entertainment systems
- **Automated Speaker Control**: Intelligent power management for audio equipment
- **Volume Management**: Centralized volume control with increment-based adjustment
- **Roku Integration**: Emulated Roku device for media control automation
- **Multi-Zone Coordination**: Synchronized audio control across upstairs and downstairs areas
- **Activity-Based Automation**: Automatic speaker activation based on entertainment activities

## Key Components

### Audio Zones
- **Downstairs Zone**: Living room audio system with Harmony hub integration
- **Upstairs Zone**: Upstairs audio system with PC and music activity support
- **All Speakers Group**: Unified control for all audio devices across the home

### Harmony Integration
- **Living Room Hub**: Primary downstairs entertainment control
- **Upstairs Hub**: Upstairs entertainment and PC audio control
- **Activity Management**: Automated activity switching for different entertainment modes
- **Volume Control**: Centralized volume management through Harmony devices

### Chromecast Audio
- **Multi-Device Support**: Multiple Chromecast Audio devices for zone-based audio
- **Synchronized Playback**: Coordinated audio across different zones
- **Media Information**: Real-time track and artist information display

### Roku Integration
- **Emulated Device**: Virtual Roku device for automation triggers
- **Key Press Events**: Event-driven automation based on Roku commands
- **Media Control**: Integration with Roku media devices for unified control

## Entities

### Remotes
- `remote.living_room_hub`: Downstairs Harmony hub with music activity support
- `remote.upstairs_hub`: Upstairs Harmony hub with PC and music activities

### Input Numbers
- `input_number.volume_increment`: Volume adjustment increment value
- `input_number.speakers_playing`: Speaker playback status tracking

### Media Players
- `media_player.upstairs_speakers_2`: Upstairs speaker group
- `media_player.downstairs_speakers_2`: Downstairs speaker group
- `media_player.all_speakers`: Unified speaker group for whole-home control

### Switches
- `switch.upstairs_speakers`: Upstairs speaker power control
- `switch.upstairs_pc_speakers`: Upstairs PC speaker control
- `switch.downstairs_speakers`: Downstairs speaker power control

### Sensors
- `sensor.all_speakers_media_title`: Current track title across all speakers
- `sensor.all_speakers_media_artist`: Current artist across all speakers

### Custom Attributes
- **Music Activity ID**: Harmony activity identifiers for music playback
- **PC Activity ID**: Harmony activity identifiers for PC audio
- **Volume Device**: Device IDs for volume control integration
- **Location**: Zone identification for downstairs/upstairs areas

## Automations

### Speaker Power Management
- **Automated Power On**: Speakers activate automatically when music activities are triggered
- **Power Off Coordination**: Intelligent power management to conserve energy
- **Activity-Based Control**: Speaker power states synchronized with Harmony activities

### Volume Control
- **Increment-Based Adjustment**: Volume changes using configurable increment values
- **Zone-Specific Control**: Individual volume management for upstairs and downstairs zones
- **Unified Volume Control**: Centralized volume adjustment across all speakers

### Media Synchronization
- **Track Information**: Real-time display of current media title and artist
- **Multi-Zone Coordination**: Synchronized playback information across zones
- **Playback Status**: Unified status tracking for all audio devices

### Roku Integration
- **Event-Driven Automation**: Roku key press events trigger related automations
- **Media Control**: Integration with Roku devices for unified entertainment control
- **Activity Coordination**: Synchronized activities between Roku and audio systems

## Dependencies
- **Logitech Harmony**: Remote control integration for entertainment systems
- **Chromecast Audio**: Multi-zone audio distribution and control
- **Roku Integration**: Media device control and automation triggers
- **Template Sensors**: For media information aggregation and display
- **Custom Attributes**: For activity and device management

## Usage
The media music package provides several interaction methods:
- **Harmony Remote**: Direct control through Logitech Harmony remotes
- **Voice Commands**: Integration with voice assistants for hands-free control
- **Dashboard Controls**: Direct control via Lovelace dashboard
- **Activity Automation**: Automatic speaker activation based on entertainment activities
- **Volume Management**: Centralized volume control with increment-based adjustment

## Related Files
- `packages/media_music.yaml`: Main media and music package configuration
- `blueprints/automation/rohankapoorcom/emulated-roku.yaml`: Roku device emulation blueprint
- `dashboards/home.yaml`: Main dashboard configuration

## Notes
- The package uses YAML anchors for consistent configuration across multiple entities
- Speaker power management is coordinated with Harmony activities for seamless operation
- Volume control uses increment-based adjustment for precise audio level management
- Multi-zone audio provides synchronized playback across upstairs and downstairs areas
- Roku integration enables event-driven automation for enhanced entertainment control
- Custom attributes store activity IDs and device information for Harmony integration
