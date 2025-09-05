# Tuya TS0044 4-Button Remote Blueprint Documentation

## Overview
This blueprint provides comprehensive automation for Tuya TS0044 4-Button Wireless Remotes using Zigbee2MQTT integration. It supports single press, double press, and hold actions for all four buttons, making it a versatile remote control solution.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml)

## Blueprint Information
- **Name**: Tuya TS0044 4 Button Wireless Remote (Zigbee2MQTT)
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `tuya_switch`: Tuya TS0044 remote device(s)
- `command_path_base`: MQTT command path base (default: zigbee2mqtt)
- `button_1`: Action for Button 1 single press
- `button_2`: Action for Button 2 single press
- `button_3`: Action for Button 3 single press
- `button_4`: Action for Button 4 single press
- `button_1_double`: Action for Button 1 double press
- `button_2_double`: Action for Button 2 double press
- `button_3_double`: Action for Button 3 double press
- `button_4_double`: Action for Button 4 double press
- `button_1_held`: Action for Button 1 hold
- `button_2_held`: Action for Button 2 hold
- `button_3_held`: Action for Button 3 hold
- `button_4_held`: Action for Button 4 hold

## Functionality
This blueprint creates an automation that:

1. **Monitors MQTT topics**: Listens for Zigbee2MQTT device events
2. **Filters by device**: Only responds to events from specified Tuya remotes
3. **Handles button actions**: Processes single press, double press, and hold events
4. **Maps to actions**: Executes the appropriate action based on button and press type
5. **Supports multiple devices**: Can handle multiple Tuya TS0044 remotes simultaneously

## Usage Examples
```yaml
# Example: Bedroom remote control
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml
    input:
      tuya_switch: "Bedroom Remote"
      button_1:
        - service: light.turn_on
          target:
            entity_id: light.bedroom_ceiling
      button_2:
        - service: light.turn_off
          target:
            entity_id: light.bedroom_ceiling
      button_3:
        - service: scene.turn_on
          target:
            entity_id: scene.bedroom_dim
      button_4:
        - service: scene.turn_on
          target:
            entity_id: scene.bedroom_bright
      button_1_double:
        - service: media_player.media_play_pause
          target:
            entity_id: media_player.bedroom_tv
      button_2_held:
        - service: scene.turn_on
          target:
            entity_id: scene.bedroom_night
```

## Dependencies
- **Zigbee2MQTT integration**: Must be installed and configured
- **Tuya TS0044 remote**: Must be properly paired and configured
- **MQTT broker**: Must have a stable MQTT connection
- **Zigbee network**: Must have a stable Zigbee network connection

## Related Files
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/living_room/`: Living room automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Supports all button press types: single, double, and hold
- Can handle multiple Tuya TS0044 remotes in a single automation
- Uses MQTT topic filtering for reliable device identification
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Configurable MQTT path base for different Zigbee2MQTT setups

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
