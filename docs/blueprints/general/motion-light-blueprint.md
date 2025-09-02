# Motion Light Blueprint Documentation

## Overview
A customizable blueprint for creating motion-activated lighting automations. This blueprint turns on lights when motion is detected and automatically turns them off after a specified delay when no motion is detected.

## Blueprint Information
- **Name**: Motion-activated Light
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `motion_entity`: Motion sensor entity (binary_sensor with device_class: motion)
- `light_target`: Light entity to control
- `no_motion_wait`: Time to wait after last motion before turning off light (default: 120 seconds)

## Functionality
This blueprint creates an automation that:
- Monitors a motion sensor for state changes
- Turns on the specified light when motion is detected
- Waits for motion to stop, then delays for the specified time
- Automatically turns off the light after the delay period
- Handles multiple motion events during the delay period

## Usage Examples
```yaml
# Example: Hallway motion light
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
    input:
      motion_entity: binary_sensor.hallway_motion
      light_target: light.hallway_lights
      no_motion_wait: 180
```

## Dependencies
- Binary sensor with device_class: motion
- Light entity for control
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Based on the Home Assistant default motion-light blueprint
- Supports restart mode for reliable operation
- Silent error handling for maximum exceeded scenarios
- Configurable delay time for motion detection

---
*This documentation is part of the [General Blueprint Index](README.md)*
