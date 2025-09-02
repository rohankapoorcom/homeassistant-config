# Solum M3 E-Paper Tag Buttons Blueprint Documentation

## Overview
A blueprint for creating automations triggered by Solum M3 e-paper tag button presses. This blueprint enables custom actions when the physical buttons on e-paper tags are pressed.

## Blueprint Information
- **Name**: Solum M3 E-Paper Tag Buttons
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `tag_device`: The Solum M3 e-paper tag device
- `button_1_action`: Action to run when button 1 is pressed
- `button_2_action`: Action to run when button 2 is pressed
- `button_3_action`: Action to run when button 3 is pressed

## Functionality
This blueprint creates an automation that:
- Monitors Solum M3 e-paper tags for button press events
- Maps each button to a customizable action
- Supports up to 3 physical buttons per tag
- Uses single mode execution for reliable operation
- Handles Open E-Paper Link integration events

## Usage Examples
```yaml
# Example: E-paper tag controls kitchen scene
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml
    input:
      tag_device: "kitchen_tag"
      button_1_action:
        - service: scene.turn_on
          target:
            entity_id: scene.kitchen_cooking
      button_2_action:
        - service: scene.turn_on
          target:
            entity_id: scene.kitchen_cleaning
      button_3_action:
        - service: scene.turn_on
          target:
            entity_id: scene.kitchen_off
```

## Dependencies
- Open E-Paper Link integration
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Supports up to 3 physical buttons on each e-paper tag
- Uses Open E-Paper Link integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Device-Specific Blueprint Index](README.md)*
