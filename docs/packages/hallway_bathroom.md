# Hallway Bathroom Package

## Overview

The `hallway_bathroom` package manages lighting, climate control, and automation in the hallway bathroom. It provides motion-activated lighting, humidity-based fan operation, adaptive lighting adjustments, and scene controls.

## Functionality

This package creates a comfortable and automated bathroom environment with:
- **Motion-activated lighting** with 5-minute delay
- **Humidity-controlled ventilation** with smart fan operation
- **Adaptive lighting** with sleep mode integration
- **Scene controls** via Inovelli switch integration
- **Relative humidity calculation** from multiple sensors

## Key Components

### Lighting System
- Motion-activated lights with 300-second delay
- Adaptive lighting integration with sleep mode
- Scene controls for manual override

### Climate Control
- Humidity-based fan operation
- Relative humidity calculation from multiple sensors
- Smart fan timing with motion and humidity conditions

### Automation Features
- Motion detection and lighting control
- Humidity monitoring and fan control
- Adaptive lighting sleep mode
- Scene control integration

## Entities

### Sensors
- `sensor.hallway_bathroom_relative_humidity` - Calculated relative humidity
- `sensor.hallway_bathroom_humidity` - Raw bathroom humidity reading
- `sensor.upstairs_humidity` - Reference humidity sensor

### Binary Sensors
- `binary_sensor.hallway_bathroom_motion` - Motion detection

### Lights
- `light.hallway_bathroom_lights` - Main bathroom lighting

### Fans
- `fan.hallway_bathroom_fan` - Ventilation fan

### Switches
- `switch.adaptive_lighting_sleep_mode_hallway_bathroom` - Adaptive lighting sleep mode

## Automations

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `a04b7289-134e-4920-8174-c04e00d1be77` | Control the Hallway Bathroom Lights | Motion-activated lighting with automatic shutoff | Motion sensor | Uses `motion_light` blueprint |
| `5c050332-9c23-4125-82f8-2cec45fb0e7a` | Control the Hallway Bathroom Fan | Humidity and motion-based fan control | Motion, humidity >20% | Fan on/off with smart timing |
| `0b252966-863d-4f1c-93b8-c4d4154b0aff` | Adjust the Hallway Bathroom Default Brightness | Adaptive lighting sleep mode integration | Time-based | Uses `adaptive-lighting-sleep-mode` blueprint |
| `1e07a741-80f4-4c08-b8cd-7cb33849812d` | Hallway Bathroom Light Switch Scene Controls | Scene control for manual lighting | Inovelli switch | Uses `inovelli-lzw31-red-series-switch` blueprint |

### Automation Details

#### Control the Hallway Bathroom Lights
- **Blueprint**: `rohankapoorcom/motion_light.yaml`
- **Motion Entity**: `binary_sensor.hallway_bathroom_motion`
- **Light Target**: `light.hallway_bathroom_lights`
- **No Motion Wait**: 300 seconds (5 minutes)

#### Control the Hallway Bathroom Fan
- **Triggers**: Motion detection, humidity >20%, Home Assistant start
- **Logic**: Fan turns on when motion detected OR humidity >20%
- **Shutoff Conditions**: Humidity ≤10% AND no motion for 5 minutes
- **Mode**: Restart with silent max exceeded

#### Adjust the Hallway Bathroom Default Brightness
- **Blueprint**: `rohankapoorcom/adaptive-lighting-sleep-mode.yaml`
- **Bedtime**: 01:00:00
- **Wakeup Time**: 08:00:00

#### Hallway Bathroom Light Switch Scene Controls
- **Blueprint**: `rohankapoorcom/inovelli-lzw31-red-series-switch.yaml`
- **Device ID**: `b6df24a18353633370965899bb1e9a05`
- **Button A Action**: Turn on lights at 100% brightness

## Dependencies

### Core Integrations
- `binary_sensor` - Motion detection
- `sensor` - Humidity monitoring
- `light` - Lighting control
- `fan` - Ventilation control
- `switch` - Adaptive lighting control

### Custom Integrations
- None

### Blueprints
- `rohankapoorcom/motion_light.yaml`
- `rohankapoorcom/adaptive-lighting-sleep-mode.yaml`
- `rohankapoorcom/inovelli-lzw31-red-series-switch.yaml`

### Scripts
- None

## Usage

### Manual Control
- **Lights**: Motion-activated, can be manually controlled via scene button
- **Fan**: Automatic based on humidity/motion, can be manually overridden
- **Scene Control**: Button A on Inovelli switch turns lights to 100%

### Automation Behavior
- **Lighting**: Automatically turns on with motion, off after 5 minutes of no motion
- **Ventilation**: Fan runs when humidity >20% OR motion detected, stops when conditions improve
- **Adaptive Lighting**: Automatic brightness adjustments based on time of day

## Configuration

### Humidity Calculation
The relative humidity is calculated as the difference between the bathroom humidity sensor and the upstairs humidity sensor:
```yaml
value_template: >
  {{ states('sensor.hallway_bathroom_humidity') | float(0) - states('sensor.upstairs_humidity') | float(0) }}
```

### Fan Control Logic
- **Turn On**: Motion detected OR humidity >20%
- **Turn Off**: Humidity ≤10% AND no motion for 5 minutes
- **Mode**: Restart with silent max exceeded

### Adaptive Lighting Settings
- **Bedtime**: 01:00:00
- **Wakeup Time**: 08:00:00
- **Integration**: Sleep mode switch control

## Notes

- The package uses relative humidity calculation to determine when ventilation is needed
- Fan operation is optimized for both comfort and energy efficiency
- Adaptive lighting integration provides automatic brightness adjustments
- Motion delay is set to 5 minutes for bathroom usage patterns
- All automations use restart mode for reliability
- Scene control provides manual override capability
