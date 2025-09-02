# Zooz ZEN32 Scene Controller Status Lights Blueprint Documentation

## Overview
A blueprint for mapping lights on the Zooz ZEN32 Scene Controller buttons to Home Assistant lights. This blueprint synchronizes the status lights on the ZEN32 controller with the state of Home Assistant light entities.

## Blueprint Information
- **Name**: Zooz ZEN32 Scene Controller Status Lights
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zooz_switch`: Zooz ZEN32 Scene Controller device
- `large_button_light`: Light to track status on the large button
- `small_1_button_light`: Light to track status on the upper left small button
- `small_2_button_light`: Light to track status on the upper right small button
- `small_3_button_light`: Light to track status on the lower left small button
- `small_4_button_light`: Light to track status on the lower right small button

## Functionality
This blueprint creates an automation that:
- Monitors the state of specified Home Assistant light entities
- Updates the corresponding status lights on the ZEN32 controller
- Synchronizes the large button light with its assigned entity
- Controls the four small button lights using Z-Wave JS commands
- Uses single mode execution for reliable operation

## Usage Examples
```yaml
# Example: ZEN32 status lights for living room
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml
    input:
      zooz_switch: "living_room_zen32"
      large_button_light: light.living_room_main
      small_1_button_light: light.living_room_lamp
      small_2_button_light: light.living_room_ceiling
      small_3_button_light: light.living_room_accent
      small_4_button_light: light.living_room_floor
```

## Dependencies
- Z-Wave JS integration
- Zooz ZEN32 Scene Controller
- Light entities to track

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Specifically designed for Zooz ZEN32 Scene Controller
- Uses Z-Wave JS integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Zooz Blueprint Index](README.md)*
