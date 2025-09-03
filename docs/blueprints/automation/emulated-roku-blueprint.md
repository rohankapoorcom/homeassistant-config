# Emulated Roku Blueprint Documentation

## Overview
This blueprint creates automations triggered by emulated Roku device keypresses. It allows you to map any of the 16 standard Roku remote buttons to custom Home Assistant actions, providing a flexible way to control your smart home through a familiar remote interface.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml)

## Blueprint Information
- **Name**: Emulated Roku
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `emulated_roku_name`: Name of the emulated Roku device
- `up_action`: Action to run when "Up" button is pressed
- `right_action`: Action to run when "Right" button is pressed
- `down_action`: Action to run when "Down" button is pressed
- `left_action`: Action to run when "Left" button is pressed
- `home_action`: Action to run when "Home" button is pressed
- `search_action`: Action to run when "Search" button is pressed
- `rewind_action`: Action to run when "Rewind" button is pressed
- `forward_action`: Action to run when "Forward" button is pressed
- `play_action`: Action to run when "Play" button is pressed
- `select_action`: Action to run when "Select" button is pressed
- `back_action`: Action to run when "Back" button is pressed
- `instant_replay_action`: Action to run when "InstantReplay" button is pressed
- `info_action`: Action to run when "Info" button is pressed
- `back_space_action`: Action to run when "BackSpace" button is pressed
- `enter_action`: Action to run when "Enter" button is pressed

## Functionality
This blueprint creates an automation that:

1. **Listens for Roku commands**: Monitors for `roku_command` events
2. **Filters by device**: Only responds to commands from the specified emulated Roku device
3. **Handles keypresses**: Processes only keypress events (not other command types)
4. **Maps buttons to actions**: Executes the appropriate action based on which button was pressed
5. **Supports 16 buttons**: All standard Roku remote buttons are supported

## Usage Examples
```yaml
# Example: Media control emulated Roku
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml
    input:
      emulated_roku_name: "Media Controller"
      up_action:
        - service: media_player.volume_up
          target:
            entity_id: media_player.living_room_tv
      down_action:
        - service: media_player.volume_down
          target:
            entity_id: media_player.living_room_tv
      play_action:
        - service: media_player.media_play_pause
          target:
            entity_id: media_player.living_room_tv
      home_action:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
```

## Dependencies
- **Emulated Roku integration**: Must be installed and configured
- **Emulated Roku device**: Must have an emulated Roku device set up

## Related Files
- `packages/media_music.yaml`: Media and entertainment automation configurations
- `dashboards/home.yaml`: Dashboard configuration with media controls

## Notes
- This blueprint provides a flexible way to control Home Assistant through a familiar remote interface
- Each button can trigger any Home Assistant action (service calls, scenes, scripts, etc.)
- The emulated Roku device can be controlled via the Roku app or other Roku-compatible remotes
- Silent error handling for maximum exceeded scenarios
- Single mode execution ensures reliable operation

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
