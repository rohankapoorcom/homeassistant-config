# Inovelli VZW31-SN Red Series Switch Blueprint Documentation

## Overview
This blueprint provides comprehensive automation for Inovelli VZW31-SN Red Series switches using Z-Wave JS integration. It supports all button press combinations including single, double, triple, quadruple, and quintuple presses, plus hold and release actions for both the main switch and auxiliary switch (6 buttons total).

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml)

## Blueprint Information
- **Name**: Inovelli Red Series VZW31-SN Red Series Switch (ZWave-JS)
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zwave_device`: Inovelli VZW31-SN switch device(s)
- `config_button`: Action for main config button single press
- `button_a`: Action for main Up/On button single press
- `button_b`: Action for main Down/Off button single press
- `config_button2`: Action for main config button double press
- `button_a2`: Action for main Up/On button double press
- `button_b2`: Action for main Down/Off button double press
- `config_button3`: Action for main config button triple press
- `button_a3`: Action for main Up/On button triple press
- `button_b3`: Action for main Down/Off button triple press
- `config_button4`: Action for main config button quadruple press
- `button_a4`: Action for main Up/On button quadruple press
- `button_b4`: Action for main Down/Off button quadruple press
- `config_button5`: Action for main config button quintuple press
- `button_a5`: Action for main Up/On button quintuple press
- `button_b5`: Action for main Down/Off button quintuple press
- `config_button_held`: Action for main config button hold
- `button_a_held`: Action for main Up/On button hold
- `button_b_held`: Action for main Down/Off button hold
- `config_button_released`: Action for main config button release
- `button_a_released`: Action for main Up/On button release
- `button_b_released`: Action for main Down/Off button release
- `aux_config_button`: Action for auxiliary config button single press
- `aux_button_a`: Action for auxiliary Up/On button single press
- `aux_button_b`: Action for auxiliary Down/Off button single press
- `aux_config_button2`: Action for auxiliary config button double press
- `aux_button_a2`: Action for auxiliary Up/On button double press
- `aux_button_b2`: Action for auxiliary Down/Off button double press
- `aux_config_button3`: Action for auxiliary config button triple press
- `aux_button_a3`: Action for auxiliary Up/On button triple press
- `aux_button_b3`: Action for auxiliary Down/Off button triple press
- `aux_config_button4`: Action for auxiliary config button quadruple press
- `aux_button_a4`: Action for auxiliary Up/On button quadruple press
- `aux_button_b4`: Action for auxiliary Down/Off button quadruple press
- `aux_config_button5`: Action for auxiliary config button quintuple press
- `aux_button_a5`: Action for auxiliary Up/On button quintuple press
- `aux_button_b5`: Action for auxiliary Down/Off button quintuple press
- `aux_config_button_held`: Action for auxiliary config button hold
- `aux_button_a_held`: Action for auxiliary Up/On button hold
- `aux_button_b_held`: Action for auxiliary Down/Off button hold
- `aux_config_button_released`: Action for auxiliary config button release
- `aux_button_a_released`: Action for auxiliary Up/On button release
- `aux_button_b_released`: Action for auxiliary Down/Off button release

## Functionality
This blueprint creates an automation that:

1. **Monitors Z-Wave events**: Listens for `zwave_js_value_notification` events
2. **Filters by device**: Only responds to events from specified Inovelli switches
3. **Handles button presses**: Processes all button press combinations (1x-5x, hold, release)
4. **Maps to actions**: Executes the appropriate action based on button and press count
5. **Supports dual switches**: Handles both main and auxiliary switch buttons (6 total buttons)

## Usage Examples
```yaml
# Example: Dual switch with comprehensive control
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml
    input:
      zwave_device: "Dual Switch"
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
      aux_button_a:
        - service: light.turn_on
          target:
            entity_id: light.living_room_lamp
      aux_button_b:
        - service: light.turn_off
          target:
            entity_id: light.living_room_lamp
      config_button:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Inovelli VZW31-SN Red Series switch**: Must be properly paired and configured
- **Z-Wave network**: Must have a stable Z-Wave network connection

## Related Files
- `packages/living_room/`: Living room automation configurations
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Supports all button press types: single, double, triple, quadruple, quintuple, hold, and release
- Handles both main and auxiliary switches (6 total buttons)
- Can handle multiple Inovelli VZW31-SN switches simultaneously
- Uses Z-Wave JS value notifications for reliable button detection
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Designed specifically for VZW31-SN model switches with auxiliary control

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
