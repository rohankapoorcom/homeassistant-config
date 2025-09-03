# Zooz ZEN32 Scene Controls Blueprint Documentation

## Overview
A comprehensive blueprint for creating automations for the Zooz ZEN32 Scene Controller. This blueprint supports all button press combinations and scene configurations.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml)

## Blueprint Information
- **Name**: Zooz ZEN32 Scene Controls
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zooz_switch`: Zooz ZEN32 Scene Controller device
- `large_button_scene`: Scene to activate when large button is pressed
- `small_1_button_scene`: Scene to activate when upper left small button is pressed
- `small_2_button_scene`: Scene to activate when upper right small button is pressed
- `small_3_button_scene`: Scene to activate when lower left small button is pressed
- `small_4_button_scene`: Scene to activate when lower right small button is pressed
- `large_button_2x_scene`: Scene to activate when large button is double-pressed
- `small_1_button_2x_scene`: Scene to activate when upper left small button is double-pressed
- `small_2_button_2x_scene`: Scene to activate when upper right small button is double-pressed
- `small_3_button_2x_scene`: Scene to activate when lower left small button is double-pressed
- `small_4_button_2x_scene`: Scene to activate when lower right small button is double-pressed
- `large_button_3x_scene`: Scene to activate when large button is triple-pressed
- `small_1_button_3x_scene`: Scene to activate when upper left small button is triple-pressed
- `small_2_button_3x_scene`: Scene to activate when upper right small button is triple-pressed
- `small_3_button_3x_scene`: Scene to activate when lower left small button is triple-pressed
- `small_4_button_3x_scene`: Scene to activate when lower right small button is triple-pressed
- `large_button_4x_scene`: Scene to activate when large button is quadruple-pressed
- `small_1_button_4x_scene`: Scene to activate when upper left small button is quadruple-pressed
- `small_2_button_4x_scene`: Scene to activate when upper right small button is quadruple-pressed
- `small_3_button_4x_scene`: Scene to activate when lower left small button is quadruple-pressed
- `small_4_button_4x_scene`: Scene to activate when lower right small button is quadruple-pressed
- `large_button_5x_scene`: Scene to activate when large button is quintuple-pressed
- `small_1_button_5x_scene`: Scene to activate when upper left small button is quintuple-pressed
- `small_2_button_5x_scene`: Scene to activate when upper right small button is quintuple-pressed
- `small_3_button_5x_scene`: Scene to activate when lower left small button is quintuple-pressed
- `small_4_button_5x_scene`: Scene to activate when lower right small button is quintuple-pressed

## Functionality
This blueprint creates an automation that:
- Monitors Zooz ZEN32 Scene Controller for button events
- Supports up to 5 press combinations for each button
- Maps Z-Wave JS value notifications to scene activations
- Includes both single press and multiple press configurations
- Uses single mode execution for reliable operation

## Usage Examples
```yaml
# Example: ZEN32 controls living room scenes
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml
    input:
      zooz_switch: "living_room_zen32"
      large_button_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
      small_1_button_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_movie
      small_2_button_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_reading
      small_3_button_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_party
      small_4_button_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_off
      large_button_2x_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_bright
      small_1_button_2x_scene:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_dim
```

## Dependencies
- Z-Wave JS integration
- Zooz ZEN32 Scene Controller
- Scene entities to activate

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Specifically designed for Zooz ZEN32 Scene Controller
- Supports up to 5x press combinations for each button
- Uses Z-Wave JS integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Automation Blueprint Index](README.md)*
