# Emulated Roku Blueprint Documentation

## Overview
A customizable blueprint for creating automations triggered by emulated Roku device keypresses. This blueprint allows you to map Roku remote button presses to custom Home Assistant actions.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml)

## Blueprint Information
- **Name**: Emulated Roku
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `emulated_roku_name`: The name of the Emulated Roku device
- `up_action`: Action to run when the "Up" button is pressed
- `right_action`: Action to run when the "Right" button is pressed
- `down_action`: Action to run when the "Down" button is pressed
- `left_action`: Action to run when the "Left" button is pressed
- `home_action`: Action to run when the "Home" button is pressed
- `search_action`: Action to run when the "Search" button is pressed
- `rewind_action`: Action to run when the "Rewind" button is pressed
- `forward_action`: Action to run when the "Forward" button is pressed
- `play_action`: Action to run when the "Play" button is pressed
- `select_action`: Action to run when the "Select" button is pressed
- `back_action`: Action to run when the "Back" button is pressed
- `instant_replay_action`: Action to run when the "InstantReplay" button is pressed
- `info_action`: Action to run when the "Info" button is pressed
- `back_space_action`: Action to run when the "BackSpace" button is pressed
- `enter_action`: Action to run when the "Enter" button is pressed

## Functionality
This blueprint creates an automation that:
- Monitors emulated Roku devices for keypress events
- Maps each button press to a customizable action
- Supports all standard Roku remote buttons (16 total buttons)
- Uses single mode execution for reliable operation
- Handles Z-Wave JS value notifications for button events

## Usage Examples
```yaml
# Example: Roku remote controls living room lights
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml
    input:
      emulated_roku_name: "Living Room Roku"
      up_action:
        - service: light.turn_on
          target:
            entity_id: light.living_room_ceiling
      down_action:
        - service: light.turn_off
          target:
            entity_id: light.living_room_ceiling
      home_action:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
      play_action:
        - service: media_player.play
          target:
            entity_id: media_player.living_room_tv
```

## Dependencies
- Emulated Roku integration
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Based on the Home Assistant default motion-light blueprint
- Supports restart mode for reliable operation
- Silent error handling for maximum exceeded scenarios
- All 16 standard Roku remote buttons are supported

---
*This documentation is part of the [Automation Blueprint Index](README.md)*
