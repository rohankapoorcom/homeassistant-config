# Inovelli Red Series Night Mode Blueprint Documentation

## Overview
This blueprint automatically adjusts the default brightness of Inovelli Red Series dimmers based on time of day. It sets lower brightness levels during bedtime hours and higher brightness during wake-up hours, perfect for motion-activated lights that need different illumination levels throughout the day.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml)

## Blueprint Information
- **Name**: Inovelli Red Series Night Mode
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `zwave_device`: Inovelli Red Series dimmer device
- `bedtime`: Time to reduce default brightness
- `bedtime_brightness`: Default brightness percentage at bedtime (0-99%)
- `wakeup_time`: Time to increase default brightness
- `wakeup_time_brightness`: Default brightness percentage at wake-up time (0-99%)

## Functionality
This blueprint creates an automation that:

1. **Monitors time changes**: Listens for bedtime and wake-up time triggers
2. **Adjusts default levels**: Changes the dimmer's default brightness based on time
3. **Handles different models**: Supports both LZW31-SN and VZW31-SN dimmer models
4. **Sets both parameters**: Updates both local and remote/Z-Wave default levels
5. **Responds to system events**: Handles Home Assistant startup and automation reloads

## Usage Examples
```yaml
# Example: Hallway dimmer with night mode
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml
    input:
      zwave_device: "Hallway Dimmer"
      bedtime: "22:00:00"
      bedtime_brightness: 15
      wakeup_time: "07:00:00"
      wakeup_time_brightness: 75

# Example: Bathroom dimmer with conservative night mode
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml
    input:
      zwave_device: "Bathroom Dimmer"
      bedtime: "23:00:00"
      bedtime_brightness: 10
      wakeup_time: "06:00:00"
      wakeup_time_brightness: 60
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Inovelli Red Series dimmer**: Must be properly paired and configured
- **Z-Wave network**: Must have a stable Z-Wave network connection

## Related Files
- `packages/hallway.yaml`: Hallway automation configurations
- `packages/master_bedroom.yaml`: Master bedroom automation configurations
- `packages/downstairs_bathroom.yaml`: Bathroom automation configurations

## Notes
- Designed specifically for Inovelli Red Series dimmers (LZW31-SN, VZW31-SN)
- Automatically adjusts default brightness for motion-activated lights
- Supports different brightness levels for bedtime and wake-up periods
- Updates both local and remote/Z-Wave default level parameters
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for creating comfortable lighting transitions throughout the day

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
