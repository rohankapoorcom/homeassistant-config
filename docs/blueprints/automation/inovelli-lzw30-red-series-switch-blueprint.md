# Inovelli LZW30 Red Series Switch Blueprint Documentation

## Overview
This blueprint provides comprehensive automation for Inovelli LZW30-SN Red Series switches using Z-Wave JS integration. It supports all button press combinations including single, double, triple, quadruple, and quintuple presses for both the Up/On and Down/Off buttons, plus the config button.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-red-series-switch.yaml)

## Blueprint Information
- **Name**: Inovelli Red Series LZW30-SN Switch (ZWave-JS)
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-red-series-switch.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zwave_device`: Inovelli LZW30-SN switch device
- `config_button`: Action for config button single press
- `button_a`: Action for Up/On button single press
- `button_b`: Action for Down/Off button single press
- `button_a2`: Action for Up/On button double press
- `button_b2`: Action for Down/Off button double press
- `button_a3`: Action for Up/On button triple press
- `button_b3`: Action for Down/Off button triple press
- `button_a4`: Action for Up/On button quadruple press
- `button_b4`: Action for Down/Off button quadruple press
- `button_a5`: Action for Up/On button quintuple press
- `button_b5`: Action for Down/Off button quintuple press

## Functionality
This blueprint creates an automation that:

1. **Monitors Z-Wave events**: Listens for `zwave_js_value_notification` events
2. **Filters by device**: Only responds to events from the specified Inovelli switch
3. **Handles button presses**: Processes all button press combinations (1x-5x)
4. **Maps to actions**: Executes the appropriate action based on button and press count
5. **Supports all buttons**: Up/On (Button A), Down/Off (Button B), and Config (Button C)

## Usage Examples
```yaml
# Example: Living room switch with scene control
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-red-series-switch.yaml
    input:
      zwave_device: "Living Room Switch"
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
      button_a3:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_movie
      config_button:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Inovelli LZW30-SN switch**: Must be properly paired and configured
- **Z-Wave network**: Must have a stable Z-Wave network connection

## Related Files
- `packages/living_room/`: Living room automation configurations
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Based on kylerw's work and modified for enhanced functionality
- Supports all button press combinations (1x-5x) for maximum flexibility
- Uses Z-Wave JS value notifications for reliable button detection
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Config button provides additional control options

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
