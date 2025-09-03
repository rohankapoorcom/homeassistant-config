# Inovelli Red Series Night Mode Blueprint Documentation

## Overview
A blueprint for creating night mode automations for Inovelli Red Series switches. This blueprint enables automatic dimming and color temperature adjustments during night hours.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml)

## Blueprint Information
- **Name**: Inovelli Red Series Night Mode
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `light_entity`: The light entity to control
- `night_start_time`: Time to start night mode
- `night_end_time`: Time to end night mode
- `night_brightness`: Brightness level during night mode (0-255)
- `night_color_temp`: Color temperature during night mode (K)

## Functionality
This blueprint creates an automation that:
- Automatically adjusts lighting based on time of day
- Reduces brightness and changes color temperature at night
- Restores normal lighting during day hours
- Uses single mode execution for reliable operation
- Handles time-based triggers

## Usage Examples
```yaml
# Example: Bedroom night mode automation
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml
    input:
      light_entity: light.bedroom
      night_start_time: "22:00:00"
      night_end_time: "07:00:00"
      night_brightness: 64
      night_color_temp: 2700
```

## Dependencies
- Light integration
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Specifically designed for Inovelli Red Series switches
- Uses time-based triggers for automatic operation
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Automation Blueprint Index](README.md)*
