# Adaptive Lighting Sleep Mode Blueprint Documentation

## Overview
A blueprint for enabling Adaptive Lighting Sleep Mode at specific times for lights that are triggered by motion detectors. This blueprint automatically adjusts lighting behavior based on time of day.

## Blueprint Information
- **Name**: Adaptive Lighting Sleep Mode
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `adaptive_lighting_switch`: Adaptive Lighting Switch entity
- `bedtime`: Time to reduce the default brightness
- `wakeup_time`: Time to increase the default brightness

## Functionality
This blueprint creates an automation that:
- Automatically enables sleep mode at bedtime
- Disables sleep mode at wake-up time
- Adjusts lighting behavior for motion-triggered lights
- Uses single mode execution for reliable operation
- Handles time-based triggers

## Usage Examples
```yaml
# Example: Bedroom adaptive lighting sleep mode
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml
    input:
      adaptive_lighting_switch: switch.adaptive_lighting_bedroom
      bedtime: "22:00:00"
      wakeup_time: "07:00:00"
```

## Dependencies
- Adaptive Lighting integration
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Specifically designed for Adaptive Lighting integration
- Uses time-based triggers for automatic operation
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [General Blueprint Index](README.md)*
