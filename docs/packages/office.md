# Office Package Documentation

## Overview
The office package manages all automation and configuration for the office space, including lighting, climate control, desk controls, and productivity features. This package provides a comprehensive workspace automation system with intelligent lighting, fan control, standing desk management, and audio/video controls for meetings and productivity.

## Configuration Files
- `packages/office.yaml`: Main office configuration

## Functionality
The office package provides:
- **Automated Lighting**: Multi-zone lighting with brightness presets (25%, 50%, 75%, 100%)
- **Climate Control**: Fan with multiple speed settings (slow, medium, high) and percentage-based control
- **Standing Desk Control**: 4 preset positions for ergonomic workspace adjustment
- **Video Lighting**: Specialized lighting setup for video conferencing and meetings
- **Audio/Video Controls**: Meeting room equipment management including webcam, microphones, and speakers
- **Occupancy-Based Automation**: Intelligent lighting and equipment control based on room occupancy
- **Closet Lighting**: Automatic closet lighting triggered by door sensor

## Key Components

### Lighting System
- **Main Office Lights**: Primary lighting with brightness presets and occupancy-based control
- **Backlighting**: Ambient lighting for reduced eye strain
- **Video Lights**: Specialized lighting for video conferencing with specific color temperature and brightness
- **Key Lights**: Individual lighting for video content creation
- **Shelf Lighting**: Decorative and functional shelf lighting
- **Closet Lights**: Automatic closet lighting

### Climate Control
- **Ceiling Fan**: Multi-speed fan with percentage-based control (33%, 66%, 99%)
- **Temperature Monitoring**: Real-time temperature and humidity tracking
- **Illuminance Sensing**: Natural light detection for adaptive lighting

### Desk Control
- **Standing Desk**: 4 preset height positions for ergonomic workspace adjustment
- **Height Monitoring**: Real-time desk height tracking and status

### Audio/Video Equipment
- **Webcam Monitor**: Video input switching and control
- **Ceiling Microphones**: Audio input management with mute controls
- **PC Speakers**: Audio output control with mute functionality
- **Sentinal Headset**: Audio routing between headset and ceiling speakers

## Entities

### Binary Sensors
- `binary_sensor.office_lights_25_percent`: Indicates if main lights are at 25% brightness
- `binary_sensor.office_lights_50_percent`: Indicates if main lights are at 50% brightness
- `binary_sensor.office_lights_75_percent`: Indicates if main lights are at 75% brightness
- `binary_sensor.office_lights_100_percent`: Indicates if main lights are at 100% brightness
- `binary_sensor.office_fan_is_off`: Indicates if fan is turned off
- `binary_sensor.office_fan_slow`: Indicates if fan is set to slow speed (≤52%)
- `binary_sensor.office_fan_medium`: Indicates if fan is set to medium speed (53-81%)
- `binary_sensor.office_fan_high`: Indicates if fan is set to high speed (>81%)

### Input Booleans
- `input_boolean.sentinal_headset_enabled`: Controls audio routing between headset and speakers

### Lights
- `light.office_closet_lights`: Closet lighting control
- `light.office_video_lights`: Template light for video conferencing setup
- `light.office_play_gradient_tube`: Gradient lighting tube
- `light.office_shelf_lightstrip`: Shelf lighting strip
- `light.office_desk_lower_lights`: Under-desk lighting
- `light.left_key_light`: Left video key light
- `light.center_key_light`: Center video key light
- `light.office_backlighting`: Ambient backlighting

### Switches
- `switch.unused_plug`: Unused electrical outlet
- `switch.office_webcam_monitor`: Webcam monitor control
- `switch.office_ceiling_mics_mute`: Ceiling microphone mute control
- `switch.office_speakers_pc_mute`: PC speakers mute control

### Sensors
- `sensor.office_temperature`: Office temperature monitoring
- `sensor.office_humidity`: Office humidity monitoring
- `sensor.office_illuminance`: Natural light level detection
- `sensor.standing_desk_desk_height`: Current desk height measurement

### Buttons
- `button.standing_desk_preset_1`: Standing desk preset position 1
- `button.standing_desk_preset_2`: Standing desk preset position 2
- `button.standing_desk_preset_3`: Standing desk preset position 3
- `button.standing_desk_preset_4`: Standing desk preset position 4

### Scripts
- `script.set_office_lights_25_percent`: Set main lights to 25% brightness
- `script.set_office_lights_50_percent`: Set main lights to 50% brightness
- `script.set_office_lights_75_percent`: Set main lights to 75% brightness
- `script.set_office_lights_100_percent`: Set main lights to 100% brightness
- `script.set_office_fan_off`: Turn off office fan
- `script.set_office_fan_slow`: Set fan to slow speed (33%)
- `script.set_office_fan_medium`: Set fan to medium speed (66%)
- `script.set_office_fan_high`: Set fan to high speed (99%)

## Automations

### Toggle Sentinal Headset
- **ID**: `0c527fe1-216b-4ace-8e81-004fe00484b9`
- **Description**: Switches Sentinal to route voice communication audio between Jabra Headset and Ceiling Speakers
- **Trigger**: Changes to `input_boolean.sentinal_headset_enabled`
- **Action**: Toggles between headset and speaker audio routing

### Control Office Closet Lights by Door Sensor
- **ID**: `1649041295671`
- **Description**: Automatically controls closet lighting based on door state
- **Trigger**: Changes to `binary_sensor.office_closet_door`
- **Action**: Turns lights on when door opens, off when door closes

### Office Lights Scene Controls
- **ID**: `c6888d4f-2471-450d-a8ee-66a68c388169`
- **Description**: Maps track lighting states to Inovelli VZM31-SN Blue Series Switch
- **Blueprint**: `inovelli-vzm31-sn-blue-series-switch.yaml`
- **Functionality**: Provides scene control for office lighting via Z-Wave switch

### Control Office Lights by Occupancy Sensor
- **ID**: `1050b406-8102-486e-89b7-30f29fb39f35`
- **Description**: Intelligent lighting and equipment control based on office occupancy
- **Trigger**: Home Assistant start, automation reload, or occupancy sensor changes
- **Actions**:
  - **When Unoccupied**: Turns off all lights after 2-minute delay, disables StreamDecks, turns off ThinkSmart display
  - **When Occupied**: Enables backlighting, turns on main lights if illuminance is low and video lights are off, enables StreamDecks, turns on ThinkSmart display

## Dependencies
- **MQTT Discovery Stream**: For entity discovery and management
- **Template Sensors**: For complex state calculations and binary sensor logic
- **Z-Wave JS**: For Z-Wave device communication and control
- **Inovelli Blueprint**: For Z-Wave switch automation (`inovelli-vzm31-sn-blue-series-switch.yaml`)

## Usage
The office package provides several interaction methods:
- **Dashboard Controls**: Direct control via Lovelace dashboard
- **Voice Commands**: Integration with voice assistants for hands-free control
- **Automation Triggers**: Occupancy-based automatic control
- **Manual Controls**: Physical switches and buttons for direct control
- **Scene Controls**: Z-Wave scene controller for preset lighting configurations

## Related Files
- `packages/office.yaml`: Main office package configuration
- `blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`: Z-Wave switch automation blueprint
- `dashboards/home.yaml`: Main dashboard configuration

## Notes
- The office package uses template binary sensors to track lighting and fan states
- Occupancy-based automation includes a 2-minute delay to prevent rapid on/off cycling
- Video lighting uses specific color temperatures (143K) for optimal video quality
- Fan control uses percentage-based speeds for precise control
- The package integrates with the broader home automation system through MQTT discovery
