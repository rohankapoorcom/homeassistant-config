# Motion Light Blueprint Documentation

## Overview
This blueprint creates motion-activated lighting automation that turns on lights when motion is detected and automatically turns them off after a specified delay when no motion is detected. Based on the Home Assistant default motion-light blueprint with enhanced functionality.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml)

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

1. **Monitors motion sensor**: Listens for state changes from 'off' to 'on'
2. **Turns on light**: When motion is detected and light is off
3. **Waits for motion to stop**: Monitors for motion sensor to return to 'off' state
4. **Delays before turning off**: Waits for the specified time after motion stops
5. **Turns off light**: Automatically turns off the light after the delay period
6. **Handles multiple events**: Restart mode ensures proper handling of multiple motion events

## Usage Examples
```yaml
# Example: Hallway motion light
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
    input:
      motion_entity: binary_sensor.hallway_motion
      light_target: light.hallway_lights
      no_motion_wait: 180

# Example: Bathroom motion light with shorter delay
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
    input:
      motion_entity: binary_sensor.bathroom_motion
      light_target: light.bathroom_vanity
      no_motion_wait: 60
```

## Dependencies
- **Binary sensor with device_class: motion**: Motion sensor must be properly configured
- **Light entity**: Target light must be available and controllable
- **No additional integrations required**

## Related Files
- `packages/hallway.yaml`: Hallway automation configurations
- `packages/downstairs_bathroom.yaml`: Bathroom automation configurations
- `packages/master_bathroom.yaml`: Master bathroom automation configurations

## Notes
- Based on the Home Assistant default motion-light blueprint
- Uses restart mode for reliable operation with multiple motion events
- Silent error handling for maximum exceeded scenarios
- Automatically handles system restarts and automation reloads
- Configurable delay time allows for different use cases (hallways vs bathrooms)

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
