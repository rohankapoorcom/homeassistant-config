# Adaptive Lighting Sleep Mode Blueprint Documentation

## Overview
This blueprint automates the Adaptive Lighting sleep mode based on configurable bedtime and wake-up times. It enables sleep mode at bedtime to reduce brightness and disables it at wake-up time to restore normal lighting levels.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml)

## Blueprint Information
- **Name**: Adaptive Lighting Sleep Mode
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `adaptive_lighting_switch`: Adaptive Lighting switch entity to control sleep mode
- `bedtime`: Time to enable sleep mode (reduce brightness)
- `wakeup_time`: Time to disable sleep mode (restore normal brightness)

## Functionality
This blueprint creates an automation that:

1. **Triggers on multiple events**:
   - Home Assistant startup
   - Automation reload
   - Bedtime (configurable time)
   - Wake-up time (configurable time)

2. **Conditional logic**:
   - If current time is between bedtime and wake-up time: enables sleep mode
   - Otherwise: disables sleep mode

3. **Actions**:
   - Turns on the Adaptive Lighting sleep mode switch during sleep hours
   - Turns off the Adaptive Lighting sleep mode switch during wake hours

## Usage Examples
```yaml
# Example: Sleep mode from 10 PM to 7 AM
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml
    input:
      adaptive_lighting_switch: switch.adaptive_lighting_sleep_mode
      bedtime: "22:00:00"
      wakeup_time: "07:00:00"
```

## Dependencies
- **Adaptive Lighting integration**: Must be installed and configured
- **Adaptive Lighting switch**: Must have a sleep mode switch entity available

## Related Files
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/living_room/`: Living room automation configurations

## Notes
- This blueprint works with the Adaptive Lighting integration to provide automatic sleep mode control
- The sleep mode reduces brightness and adjusts color temperature for better sleep
- Automatically handles time transitions and system restarts
- Silent error handling for maximum exceeded scenarios

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
