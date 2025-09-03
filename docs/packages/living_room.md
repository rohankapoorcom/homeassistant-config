# Living Room Package

## Overview

The `living_room` package manages lighting, climate control, media systems, and automation in the living room. It consists of two sub-packages: `living_room_lights` for lighting and climate control, and `living_room_media_tv` for media system management and entertainment automation.

## Functionality

This package provides comprehensive living room automation with:
- **Multi-speed fan control** with template fan integration
- **Smart curtain management** based on sun position and window state
- **Scene controls** via Zooz and Inovelli switches with LED feedback
- **Media system automation** for TV, Apple TV, Shield, and gaming
- **Video conferencing system** integration
- **Philips Hue Sync Box** integration for ambient lighting
- **Notification system** for appliances and phone calls

## Key Components

### Climate Control
- Template fan with percentage-based speed control
- Binary sensors for fan speed states (off, slow, medium, high)
- Smart curtain automation with sun and window integration

### Lighting System
- Main living room lighting
- Scene controls with LED status indicators
- Curtain and sheer control via switches
- Status light mapping for fan states

### Media Systems
- Shield TV with Harmony integration
- Apple TV automation
- Nintendo Switch integration
- Denon AVR control
- Video conferencing system
- Philips Hue Sync Box

### Automation Features
- Sun-based curtain control
- Appliance notifications
- Phone call notifications
- Remote charging management
- HDMI matrix switching

## Entities

### Fans
- `fan.living_room_fan` - Template fan with percentage control
- `light.living_room_fan` - Underlying light for fan control

### Binary Sensors
- `binary_sensor.living_room_fan_slow` - Fan slow speed state
- `binary_sensor.living_room_fan_medium` - Fan medium speed state
- `binary_sensor.living_room_fan_high` - Fan high speed state
- `binary_sensor.living_room_fan_off` - Fan off state
- `binary_sensor.living_room_windows` - Window state
- `binary_sensor.living_room_tv_remote_plugged_in` - Remote charging state
- `binary_sensor.washer_wash_completed` - Washer completion
- `binary_sensor.dryer_dry_completed` - Dryer completion

### Covers
- `cover.living_room_curtains` - Main curtains
- `cover.living_room_sheers` - Sheer curtains

### Media Players
- `media_player.living_room_tv` - Main TV
- `media_player.living_room_shield_tv` - Shield TV
- `media_player.living_room_apple_tv` - Apple TV
- `media_player.denon_avr_x4300h` - Denon AVR
- `media_player.shield` - Shield device

### Switches
- `switch.living_room_conference_camera` - Conference camera
- `switch.living_room_tv_remote_motion_detection` - Remote motion detection
- `switch.living_room_tv_remote_screen` - Remote screen
- `switch.living_room_sync_box_light_sync` - Sync box light sync

### Sensors
- `sensor.line_103_status` - Phone line status
- `sensor.line_103_caller_name` - Caller name
- `sensor.line_103_caller_number` - Caller number

### Selects
- `select.living_room_sync_box_entertainment_area` - Sync box area selection

## Automations

### Living Room Lights Package

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `8fbfa021-9205-4f56-b3a0-9eea04900c42` | Living Room Scene Controls | Fan speed control via Zooz switch | Zooz switch scenes | Fan percentage control |
| `38a41f0a-5b07-4efc-804c-3e19fadc156b` | Living Room Scene Controller Status Lights | LED status mapping for fan states | Fan state changes | LED status updates |
| `023bc818-9231-4450-b15b-1dc7692f3fbb` | Living Room Light Switch Scene Controls | Curtain and sheer control | Inovelli switch buttons | Cover control with LED feedback |
| `3f0b4ba4-678b-4b37-b956-440b78c98dbe` | Manage the Living Room Curtains | Sun and window-based curtain control | Sun events, window state | Automatic curtain control |

### Living Room Media TV Package

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `faea6bc6-9c9b-439c-9f5a-ac65fbec8cdf` | Handle Shield Emulated Roku Harmony Commands | Shield TV app control | Harmony emulated Roku events | App selection and navigation |
| `c8ff656a-e0d6-4b26-9840-0da9863b1867` | Living Room Shield TV Notify Washer | Washer completion notification | Washer completion | TV notification |
| `e2f38056-ce90-46ca-8138-51a9637e3e50` | Living Room Shield TV Notify Dryer | Dryer completion notification | Dryer completion | TV notification |
| `c34228e0-c6c9-431f-ad73-cef94537ca2c` | Living Room TV Notify Phone Call | Phone call notification | Incoming call | TV notification with caller info |
| `6ed8bef7-8ed6-4278-b79f-fefa9bf2ab8b` | Control the Living Room TV Remote when Charging | Remote charging management | Remote charging state | Motion detection and screen control |

### Automation Details

#### Living Room Scene Controls
- **Blueprint**: `Matt-PMCT/ZoozZen32forZwaveJs.yaml`
- **Zooz Switch**: `f5f0fa81fd632379a87e70da0c55057f`
- **Scene 1**: Fan 100% (high)
- **Scene 2**: Fan 65% (medium)
- **Scene 3**: Fan 27% (slow)
- **Scene 4**: Fan off

#### Living Room Scene Controller Status Lights
- **Blueprint**: `rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml`
- **Large Button**: Main living room lights
- **Small Buttons**: Fan speed states (high, medium, slow, off)

#### Living Room Light Switch Scene Controls
- **Blueprint**: `rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml`
- **Device ID**: `257a7b48517ba7c9cc28fa70842c24f6`
- **Config Button**: Toggle main curtains
- **Button A2**: Open sheers
- **Button B2**: Close sheers
- **LED Feedback**: Open/close effect on all actions

#### Manage the Living Room Curtains
- **Triggers**: Sunset, sunrise +1:30, window state, Home Assistant start
- **Logic**: Close at sunset or when windows closed, open 90 minutes after sunrise
- **Window Integration**: Only closes curtains when windows are closed
- **LED Feedback**: Open/close effect on switch

#### Handle Shield Emulated Roku Harmony Commands
- **Blueprint**: `rohankapoorcom/emulated-roku.yaml`
- **Emulated Roku**: `4t8k7RAjE3TBcfheQvCATZ`
- **Up**: Netflix
- **Right**: Plex
- **Down**: YouTube
- **Left**: Amazon Prime
- **Home**: HBO Now
- **Search**: Search command

#### Living Room TV Notify Phone Call
- **Trigger**: `sensor.line_103_status` to 'incoming'
- **Notification**: Shows caller name and number
- **Duration**: 25 seconds
- **Position**: Top-right with 50% transparency

#### Control the Living Room TV Remote when Charging
- **Trigger**: Remote charging state changes
- **Charging**: Turns off motion detection and screen
- **Not Charging**: Turns on motion detection and screen

## Scripts

### turn_on_watch_living_room_tv
- **Purpose**: Turn on Shield TV system
- **Actions**: TV, AVR, Shield on, Denon Quick1, Shield HOME, camera off

### turn_off_the_living_room_tv
- **Purpose**: Turn off Shield TV system
- **Actions**: TV, AVR, Shield off, camera off

### turn_on_watch_living_room_apple_tv
- **Purpose**: Turn on Apple TV system
- **Actions**: TV, AVR, Apple TV on, Denon Quick3, Apple TV wakeup/home, camera off

### turn_on_the_living_room_speakers
- **Purpose**: Turn on audio-only system
- **Actions**: AVR on, TV/Shield off, Denon Quick4

### turn_on_the_nintendo_switch
- **Purpose**: Turn on Nintendo Switch
- **Actions**: TV, AVR, Shield on, Denon Quick2, camera off

### turn_on_the_living_room_video_conferencing_system
- **Purpose**: Turn on video conferencing
- **Actions**: TV, AVR on, camera on, source PC, stereo mode, volume 30%

### turn_on_the_living_room_tv_light_sync
- **Purpose**: Control Philips Hue Sync Box
- **Logic**: Toggle sync box, set HDMI input, select entertainment area

## Dependencies

### Core Integrations
- `fan` - Fan control
- `light` - Lighting control
- `cover` - Curtain control
- `media_player` - Media system control
- `binary_sensor` - State detection
- `sensor` - Phone system monitoring
- `switch` - Device control
- `select` - Sync box area selection

### Custom Integrations
- `denonavr` - Denon AVR control
- `androidtv` - Shield TV control
- `remote` - Apple TV remote control

### Blueprints
- `Matt-PMCT/ZoozZen32forZwaveJs.yaml`
- `rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml`
- `rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml`
- `rohankapoorcom/emulated-roku.yaml`

### Rest Commands
- `set_philips_hue_syncbox_input_living_room` - HDMI matrix control
- `set_philips_hue_syncbox_input_master_bedroom` - HDMI matrix control

## Usage

### Fan Control
- **Scene Controls**: Use Zooz switch for speed selection
- **LED Feedback**: Visual status indicators for each speed
- **Percentage Mapping**: 0-52% slow, 53-81% medium, 82-100% high

### Curtain Management
- **Automatic**: Sun-based with window state integration
- **Manual Control**: Inovelli switch buttons
- **LED Feedback**: Visual confirmation of actions

### Media Systems
- **Shield TV**: Harmony integration with app shortcuts
- **Apple TV**: Full automation with wakeup sequence
- **Gaming**: Nintendo Switch integration
- **Audio**: Dedicated speaker mode
- **Video Conferencing**: Complete system setup

### Notifications
- **Appliance Alerts**: Washer/dryer completion on TV
- **Phone Calls**: Caller information display
- **Duration Control**: Configurable notification timing

## Configuration

### Template Fan Configuration
```yaml
fan:
  - platform: template
    fans:
      living_room_fan:
        value_template: "{{is_state('light.living_room_fan', 'on')}}"
        percentage_template: >
          {{ (state_attr('light.living_room_fan', 'brightness') | float(0) * 0.392)  | round(0)}}
        speed_count: 3
```

### Fan Speed Binary Sensors
```yaml
binary_sensor:
  - platform: template
    sensors:
      living_room_fan_slow:
        value_template: >
          {% set living_room_fan_percentage = state_attr('fan.living_room_fan', 'percentage') | int(0) %}
          {{ living_room_fan_percentage > 0 and living_room_fan_percentage <= 52 }}
```

### HDMI Matrix Commands
```yaml
rest_command:
  set_philips_hue_syncbox_input_living_room:
    url: !secret hdmi_matrix_address
    payload: '{"comhead":"video switch","language":0,"source":[1,3]}'
```

## Notes

- The package uses template fans for percentage-based speed control
- Fan speed states are calculated from percentage ranges
- Curtain automation includes window state integration for energy efficiency
- Media system automation provides complete entertainment setup
- Philips Hue Sync Box integration enables ambient lighting sync
- All notifications include configurable duration and positioning
- Remote charging management optimizes battery life and user experience
- HDMI matrix switching enables multi-room video distribution
