# Inovelli VZM31-SN Blue Series Switch Blueprint Documentation

## Overview
This blueprint provides comprehensive automation for Inovelli VZM31-SN Blue Series switches using Zigbee2MQTT integration. It supports all button press combinations including single, double, triple, quadruple, and quintuple presses, plus hold and release actions for all three buttons (Up/On, Down/Off, and Config).

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml)

## Blueprint Information
- **Name**: Inovelli Blue Series VZM31-SN Switch (Zigbee2MQTT)
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `inovelli_switch`: Inovelli VZM31-SN switch device(s)
- `command_path_base`: MQTT command path base (default: zigbee2mqtt)
- `config_button`: Action for config button single press
- `button_a`: Action for Up/On button single press
- `button_b`: Action for Down/Off button single press
- `config_button_held`: Action for config button hold
- `button_a_held`: Action for Up/On button hold
- `button_b_held`: Action for Down/Off button hold
- `config_button_released`: Action for config button release
- `button_a_released`: Action for Up/On button release
- `button_b_released`: Action for Down/Off button release
- `config_button2`: Action for config button double press
- `button_a2`: Action for Up/On button double press
- `button_b2`: Action for Down/Off button double press
- `config_button3`: Action for config button triple press
- `button_a3`: Action for Up/On button triple press
- `button_b3`: Action for Down/Off button triple press
- `config_button4`: Action for config button quadruple press
- `button_a4`: Action for Up/On button quadruple press
- `button_b4`: Action for Down/Off button quadruple press
- `config_button5`: Action for config button quintuple press
- `button_a5`: Action for Up/On button quintuple press
- `button_b5`: Action for Down/Off button quintuple press

## Variables
- `switch_name`: Name of the switch that triggered the automation
- `switch_device_id`: Device ID of the switch that triggered the automation
- `switch_entities`: All entities associated with the swich that triggered the automation
- `switch_light_entity_id`: Entity ID of the switch light that triggered the automation

## Functionality
This blueprint creates an automation that:

1. **Monitors MQTT topics**: Listens for Zigbee2MQTT device events
2. **Filters by device**: Only responds to events from specified Inovelli switches
3. **Handles button actions**: Processes single, double, triple, quadruple, quintuple, hold, and release events
4. **Maps to actions**: Executes the appropriate action based on button and press type
5. **Supports multiple devices**: Can handle multiple Inovelli VZM31-SN switches simultaneously
6. **Adds variables for triggering device**: Instead of creating multiple automations per device, pass `switch_device_id` and/or `switch_light_entity_id` to your automation

## Usage Examples
```yaml
# Example: Living room switch with comprehensive control
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml
    input:
      inovelli_switch: "Living Room Switch"
      button_a:
        - service: light.turn_on
          target:
            entity_id: light.living_room_ceiling
      button_b:
        - service: light.turn_off
          target:
            entity_id: light.living_room_ceiling
      button_a2:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_bright
      button_b2:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_dim
      button_a_held:
        - service: light.turn_on
          target:
            entity_id: "{{ switch_light_entity_id }}"
          data:
            brightness_pct: 100
      config_button:
        - action: light.toggle
          target:
            device_id: "{{ switch_device_id }}" 
```

## Dependencies
- **Zigbee2MQTT integration**: Must be installed and configured
- **Inovelli VZM31-SN Blue Series switch**: Must be properly paired and configured
- **MQTT broker**: Must have a stable MQTT connection
- **Zigbee network**: Must have a stable Zigbee network connection

## Related Files
- `packages/living_room/`: Living room automation configurations
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Supports all button press types: single, double, triple, quadruple, quintuple, hold, and release
- Can handle multiple Inovelli VZM31-SN switches in a single automation
- Uses MQTT topic filtering for reliable device identification
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Configurable MQTT path base for different Zigbee2MQTT setups
- Designed specifically for Blue Series VZM31-SN model switches

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
