# Inovelli LZW30 Red Series Switch Blueprint Documentation

## Overview
A comprehensive blueprint for creating automations for Inovelli LZW30 Red Series switches. This blueprint supports all button press combinations and configurations.

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
- Monitors Inovelli LZW30 Red Series switches for button events
- Supports up to 5 press combinations for each button
- Includes config button functionality
- Maps Z-Wave JS value notifications to custom actions
- Uses single mode execution for reliable operation

## Usage Examples
```yaml
# Example: Switch controls living room lights
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-red-series-switch.yaml
    input:
      zwave_device: "living_room_switch"
      button_a:
        - service: light.turn_on
          target:
            entity_id: light.living_room
      button_b:
        - service: light.turn_off
          target:
            entity_id: light.living_room
      button_a2:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_bright
      button_b2:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_dim
```

## Dependencies
- Z-Wave JS integration
- Inovelli LZW30 Red Series switch

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Based on kylerw's work and modified for specific use cases
- Supports up to 5x press combinations for each button
- Uses Z-Wave JS integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Inovelli Blueprint Index](README.md)*
