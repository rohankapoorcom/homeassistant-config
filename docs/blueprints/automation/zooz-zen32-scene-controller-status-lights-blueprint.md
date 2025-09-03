# Zooz ZEN32 Scene Controller Status Lights Blueprint Documentation

## Overview
This blueprint synchronizes the status lights on Zooz ZEN32 Scene Controllers with Home Assistant light entities. It provides visual feedback on the physical controller by illuminating the appropriate button lights based on the state of connected lights.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml)

## Blueprint Information
- **Name**: Zooz ZEN32 Scene Controller Status Lights
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zooz_switch`: Zooz ZEN32 Scene Controller device(s)
- `large_button_light`: Light entity for the large button status
- `small_1_button_light`: Light entity for upper left small button status
- `small_2_button_light`: Light entity for upper right small button status
- `small_3_button_light`: Light entity for lower left small button status
- `small_4_button_light`: Light entity for lower right small button status

## Functionality
This blueprint creates an automation that:

1. **Monitors light states**: Listens for state changes in all connected light entities
2. **Synchronizes status lights**: Updates the physical controller's LED indicators
3. **Handles system events**: Responds to Home Assistant startup and automation reloads
4. **Supports multiple devices**: Can handle multiple Zooz ZEN32 controllers
5. **Uses Z-Wave commands**: Directly controls the device's status lights via Z-Wave JS

## Usage Examples
```yaml
# Example: Living room scene controller status lights
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml
    input:
      zooz_switch: "Living Room Controller"
      large_button_light: light.living_room_main
      small_1_button_light: light.living_room_accent
      small_2_button_light: light.living_room_lamp
      small_3_button_light: light.living_room_ceiling
      small_4_button_light: light.living_room_fan

# Example: Kitchen scene controller with fewer lights
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml
    input:
      zooz_switch: "Kitchen Controller"
      large_button_light: light.kitchen_ceiling
      small_1_button_light: light.kitchen_under_cabinet
      small_2_button_light: light.kitchen_island
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Zooz ZEN32 Scene Controller**: Must be properly paired and configured
- **Z-Wave network**: Must have a stable Z-Wave network connection
- **Light entities**: Must have light entities to track

## Related Files
- `packages/living_room/`: Living room automation configurations
- `packages/kitchen/`: Kitchen automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Provides visual feedback on the physical controller for connected lights
- Uses Z-Wave JS set_value commands for direct device control
- Supports all 5 buttons on the Zooz ZEN32 (1 large + 4 small)
- Automatically handles system restarts and automation reloads
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for creating intuitive physical controls with status feedback

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
