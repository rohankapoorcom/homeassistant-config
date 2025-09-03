# Tuya TS0044 4-Button Remote Blueprint Documentation

## Overview
A blueprint for creating automations triggered by Tuya TS0044 4-button remote control presses. This blueprint enables custom actions for each of the four buttons on the remote.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml)

## Blueprint Information
- **Name**: Tuya TS0044 4-Button Remote
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `remote_device`: The Tuya TS0044 remote device
- `button_1_action`: Action to run when button 1 is pressed
- `button_2_action`: Action to run when button 2 is pressed
- `button_3_action`: Action to run when button 3 is pressed
- `button_4_action`: Action to run when button 4 is pressed

## Functionality
This blueprint creates an automation that:
- Monitors Tuya TS0044 remotes for button press events
- Maps each of the four buttons to customizable actions
- Supports both single press and long press events
- Uses single mode execution for reliable operation
- Handles Tuya integration events

## Usage Examples
```yaml
# Example: Remote controls bedroom lights
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml
    input:
      remote_device: "bedroom_remote"
      button_1_action:
        - service: light.turn_on
          target:
            entity_id: light.bedroom_main
      button_2_action:
        - service: light.turn_off
          target:
            entity_id: light.bedroom_main
      button_3_action:
        - service: scene.turn_on
          target:
            entity_id: scene.bedroom_night
      button_4_action:
        - service: scene.turn_on
          target:
            entity_id: scene.bedroom_morning
```

## Dependencies
- Tuya integration
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Supports 4 physical buttons on the Tuya TS0044 remote
- Uses Tuya integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Automation Blueprint Index](README.md)*
