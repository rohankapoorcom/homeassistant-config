# Solum M3 E-Paper Tag Buttons Blueprint Documentation

## Overview
This blueprint creates automations for the physical buttons on Solum M3 E-Paper tags running OpenEPaperLink firmware. It supports both left and right buttons, allowing you to trigger custom actions when users interact with the e-paper display.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml)

## Blueprint Information
- **Name**: Solum M3 OpenEPaperLink EPaper Tag Buttons
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `epaper_tag`: E-Paper tag device(s) to monitor
- `button_1`: Action for right button press
- `button_2`: Action for left button press

## Functionality
This blueprint creates an automation that:

1. **Monitors e-paper events**: Listens for `open_epaper_link_event` events
2. **Filters by device**: Only responds to events from specified e-paper tags
3. **Handles button presses**: Processes both left and right button events
4. **Maps to actions**: Executes the appropriate action based on which button was pressed
5. **Supports multiple devices**: Can handle multiple e-paper tags simultaneously

## Usage Examples
```yaml
# Example: Kitchen e-paper tag controls
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml
    input:
      epaper_tag: "Kitchen Tag"
      button_1:
        - service: scene.turn_on
          target:
            entity_id: scene.kitchen_bright
      button_2:
        - service: scene.turn_on
          target:
            entity_id: scene.kitchen_dim

# Example: Office e-paper tag with multiple devices
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml
    input:
      epaper_tag: 
        - "Office Tag 1"
        - "Office Tag 2"
      button_1:
        - service: light.turn_on
          target:
            entity_id: light.office_lights
      button_2:
        - service: light.turn_off
          target:
            entity_id: light.office_lights
```

## Dependencies
- **Open E-Paper Link integration**: Must be installed and configured
- **Solum M3 e-paper tag**: Must be properly set up with OpenEPaperLink firmware
- **Network connectivity**: E-paper tag must be connected to the network

## Related Files
- `packages/kitchen/`: Kitchen automation configurations
- `packages/office.yaml`: Office automation configurations
- `custom_components/open_epaper_link/`: Open E-Paper Link integration

## Notes
- Designed specifically for Solum M3 e-paper tags running OpenEPaperLink firmware
- Supports both physical buttons on the e-paper tag
- Can handle multiple e-paper tags in a single automation
- Uses event-based triggers for reliable button detection
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for creating interactive displays with physical controls

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
