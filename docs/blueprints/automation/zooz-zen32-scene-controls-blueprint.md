# Zooz ZEN32 Scene Controls Blueprint Documentation

## Overview
This blueprint provides comprehensive automation for Zooz ZEN32 Scene Controllers using Z-Wave JS integration. It supports all button press combinations including single, double, triple, quadruple, and quintuple presses, plus hold and release actions for all five buttons (1 large + 4 small).

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml)

## Blueprint Information
- **Name**: Zooz ZEN32 Scene Controller (ZWave-JS)
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zooz_switch`: Zooz ZEN32 Scene Controller device(s)
- `scene_1`: Action for Scene 1/Upper Left single press
- `scene_1h`: Action for Scene 1/Upper Left hold
- `scene_1r`: Action for Scene 1/Upper Left release
- `scene_12`: Action for Scene 1/Upper Left double press
- `scene_13`: Action for Scene 1/Upper Left triple press
- `scene_14`: Action for Scene 1/Upper Left quadruple press
- `scene_15`: Action for Scene 1/Upper Left quintuple press
- `scene_2`: Action for Scene 2/Upper Right single press
- `scene_2h`: Action for Scene 2/Upper Right hold
- `scene_2r`: Action for Scene 2/Upper Right release
- `scene_22`: Action for Scene 2/Upper Right double press
- `scene_23`: Action for Scene 2/Upper Right triple press
- `scene_24`: Action for Scene 2/Upper Right quadruple press
- `scene_25`: Action for Scene 2/Upper Right quintuple press
- `scene_3`: Action for Scene 3/Lower Left single press
- `scene_3h`: Action for Scene 3/Lower Left hold
- `scene_3r`: Action for Scene 3/Lower Left release
- `scene_32`: Action for Scene 3/Lower Left double press
- `scene_33`: Action for Scene 3/Lower Left triple press
- `scene_34`: Action for Scene 3/Lower Left quadruple press
- `scene_35`: Action for Scene 3/Lower Left quintuple press
- `scene_4`: Action for Scene 4/Lower Right single press
- `scene_4h`: Action for Scene 4/Lower Right hold
- `scene_4r`: Action for Scene 4/Lower Right release
- `scene_42`: Action for Scene 4/Lower Right double press
- `scene_43`: Action for Scene 4/Lower Right triple press
- `scene_44`: Action for Scene 4/Lower Right quadruple press
- `scene_45`: Action for Scene 4/Lower Right quintuple press
- `scene_5`: Action for Scene 5/Large Button single press
- `scene_5h`: Action for Scene 5/Large Button hold
- `scene_5r`: Action for Scene 5/Large Button release
- `scene_52`: Action for Scene 5/Large Button double press
- `scene_53`: Action for Scene 5/Large Button triple press
- `scene_54`: Action for Scene 5/Large Button quadruple press
- `scene_55`: Action for Scene 5/Large Button quintuple press

## Functionality
This blueprint creates an automation that:

1. **Monitors Z-Wave events**: Listens for `zwave_js_value_notification` events
2. **Filters by device**: Only responds to events from specified Zooz ZEN32 controllers
3. **Handles button actions**: Processes all button press combinations (1x-5x, hold, release)
4. **Maps to actions**: Executes the appropriate action based on button and press type
5. **Supports multiple devices**: Can handle multiple Zooz ZEN32 controllers simultaneously
6. **Logs events**: Records all button events in the logbook for debugging

## Usage Examples
```yaml
# Example: Living room scene controller with comprehensive control
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml
    input:
      zooz_switch: "Living Room Controller"
      scene_1:
        - service: light.turn_on
          target:
            entity_id: light.living_room_ceiling
      scene_12:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_bright
      scene_2:
        - service: light.turn_on
          target:
            entity_id: light.living_room_lamp
      scene_22:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_dim
      scene_5:
        - service: scene.turn_on
          target:
            entity_id: scene.living_room_normal
      scene_5h:
        - service: light.turn_on
          target:
            entity_id: light.living_room_ceiling
          data:
            brightness_pct: 100
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Zooz ZEN32 Scene Controller**: Must be properly paired and configured
- **Z-Wave network**: Must have a stable Z-Wave network connection

## Related Files
- `packages/living_room/`: Living room automation configurations
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Based on Matt-PMCT's work and modified for enhanced functionality
- Supports all button press types: single, double, triple, quadruple, quintuple, hold, and release
- Can handle multiple Zooz ZEN32 controllers in a single automation
- Uses Z-Wave JS value notifications for reliable button detection
- Logs all button events for debugging and monitoring
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Designed specifically for Zooz ZEN32 Scene Controller with 5 buttons

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
