# Downstairs Bathroom Package

## Overview

The `downstairs_bathroom` package manages lighting, climate control, and comfort features in the downstairs bathroom. It provides automated lighting control, humidity-based fan operation, towel warmer management, and adaptive lighting adjustments.

## Functionality

This package creates a comfortable and automated bathroom environment with:
- **Motion-activated lighting** with automatic shutoff
- **Humidity-controlled ventilation** with smart fan operation
- **Towel warmer automation** with timed operation and notifications
- **Adaptive lighting** with sleep mode integration
- **Scene controls** via Inovelli switch integration

## Key Components

### Lighting System
- Motion-activated lights with 60-second delay
- Adaptive lighting integration with sleep mode
- Scene controls for towel warmer toggle

### Climate Control
- Humidity-based fan operation
- Relative humidity calculation from multiple sensors
- Smart fan timing with motion and humidity conditions

### Comfort Features
- Towel warmer with 2-hour auto-shutoff
- LED notifications for towel warmer status
- Scene control integration

## Entities

### Sensors
- `sensor.downstairs_bathroom_relative_humidity` - Calculated relative humidity
- `sensor.downstairs_bathroom_humidity` - Raw humidity reading
- `sensor.downstairs_humidity` - Reference humidity sensor

### Binary Sensors
- `binary_sensor.downstairs_bathroom_motion` - Motion detection

### Lights
- `light.downstairs_bathroom_lights` - Main bathroom lighting

### Fans
- `fan.downstairs_bathroom_fan` - Ventilation fan

### Switches
- `switch.downstairs_bathroom_towel_warmer` - Towel warmer control
- `switch.adaptive_lighting_sleep_mode_downstairs_bathroom` - Adaptive lighting sleep mode

## Automations

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `55251546-2ec9-422a-a8cd-761c7c752e32` | Control the Downstairs Bathroom Lights | Motion-activated lighting with automatic shutoff | Motion sensor | Uses `motion_light` blueprint |
| `634b14d2-658f-4407-aa76-b444a867c678` | Control the Downstairs Bathroom Fan | Humidity and motion-based fan control | Motion, humidity >20% | Fan on/off with smart timing |
| `358ac3b0-b113-4024-bd6d-02941d42601c` | Adjust the Downstairs Bathroom Default Brightness | Adaptive lighting sleep mode integration | Time-based | Uses `adaptive-lighting-sleep-mode` blueprint |
| `c9c77d3e-8f32-4d60-ac07-247717b746ad` | Downstairs Bathroom Light Switch Scene Controls | Scene control for towel warmer | Inovelli switch | Uses `inovelli-vzm31-sn-blue-series-switch` blueprint |
| `85f136e3-f4a8-42fa-b8b6-9d419f3ffbcb` | Notify when the Downstairs Bathroom Towel Warmer is on | LED notification for towel warmer status | Towel warmer state change | LED pulse/clear notifications |
| `d47d0430-2b3b-40eb-8ea0-f0bf1e61b5b7` | Control the Downtairs Bathroom Towel Warmer | 2-hour auto-shutoff for towel warmer | Home Assistant start, towel warmer on | 120-minute timer with auto-shutoff |

### Automation Details

#### Control the Downstairs Bathroom Lights
- **Blueprint**: `rohankapoorcom/motion_light.yaml`
- **Motion Entity**: `binary_sensor.downstairs_bathroom_motion`
- **Light Target**: `light.downstairs_bathroom_lights`
- **No Motion Wait**: 60 seconds

#### Control the Downstairs Bathroom Fan
- **Triggers**: Motion detection, humidity >20%, Home Assistant start
- **Logic**: Fan turns on when motion detected OR humidity >20%
- **Shutoff Conditions**: Humidity ≤10% AND no motion for 5 minutes
- **Mode**: Restart with silent max exceeded

#### Adjust the Downstairs Bathroom Default Brightness
- **Blueprint**: `rohankapoorcom/adaptive-lighting-sleep-mode.yaml`
- **Bedtime**: 01:00:00
- **Wakeup Time**: 08:00:00

#### Downstairs Bathroom Light Switch Scene Controls
- **Blueprint**: `rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`
- **Device ID**: `33460b8b136ed24ff7e8b0cc47d6e2c5`
- **Config Button Action**: Toggle towel warmer

#### Notify when the Downstairs Bathroom Towel Warmer is on
- **LED Color**: Red
- **LED Level**: 40%
- **Effect**: Pulse when on, Clear when off
- **Duration**: Indefinitely

#### Control the Downtairs Bathroom Towel Warmer
- **Auto-shutoff**: 120 minutes (2 hours)
- **Startup Behavior**: Turns off on Home Assistant start
- **Mode**: Restart with silent max exceeded

## Dependencies

### Core Integrations
- `binary_sensor` - Motion detection
- `sensor` - Humidity monitoring
- `light` - Lighting control
- `fan` - Ventilation control
- `switch` - Towel warmer control

### Custom Integrations
- None

### Blueprints
- `rohankapoorcom/motion_light.yaml`
- `rohankapoorcom/adaptive-lighting-sleep-mode.yaml`
- `rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`

### Scripts
- `script.inovelli_blue_notifications` - LED notification control

## Usage

### Manual Control
- **Lights**: Motion-activated, can be manually controlled
- **Fan**: Automatic based on humidity/motion, can be manually overridden
- **Towel Warmer**: Scene control via Inovelli switch, 2-hour auto-shutoff

### Automation Behavior
- **Lighting**: Automatically turns on with motion, off after 60 seconds of no motion
- **Ventilation**: Fan runs when humidity >20% OR motion detected, stops when conditions improve
- **Comfort**: Towel warmer provides 2 hours of operation with LED status indication

## Configuration

### Humidity Calculation
The relative humidity is calculated as the difference between the bathroom humidity sensor and a reference humidity sensor:
```yaml
value_template: >
  {{ states('sensor.downstairs_bathroom_humidity') | float(0) - states('sensor.downstairs_humidity') | float(0) }}
```

### Fan Control Logic
- **Turn On**: Motion detected OR humidity >20%
- **Turn Off**: Humidity ≤10% AND no motion for 5 minutes
- **Mode**: Restart with silent max exceeded

### Towel Warmer Settings
- **Auto-shutoff**: 120 minutes
- **LED Notification**: Red pulse when active
- **Startup Behavior**: Off on Home Assistant restart

## Notes

- The package uses relative humidity calculation to determine when ventilation is needed
- Fan operation is optimized for both comfort and energy efficiency
- Towel warmer includes safety features with auto-shutoff and status notifications
- Adaptive lighting integration provides automatic brightness adjustments
- All automations use restart mode for reliability
