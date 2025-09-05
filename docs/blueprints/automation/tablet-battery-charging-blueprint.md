# Tablet Battery Charging Blueprint Documentation

## Overview
This blueprint provides intelligent battery management for tablets by automatically controlling charging based on battery levels. It keeps the tablet's battery between configurable minimum and maximum percentages to optimize battery health and lifespan.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml)

## Blueprint Information
- **Name**: Tablet Battery Charging
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `battery_entity`: Battery sensor entity (sensor with device_class: battery)
- `switch_entity`: Charger switch entity to control
- `max_percent`: Maximum battery percentage before turning off charger (default: 85%)
- `min_percent`: Minimum battery percentage before turning on charger (default: 40%)

## Functionality
This blueprint creates an automation that:

1. **Monitors battery levels**: Continuously tracks the tablet's battery percentage
2. **Controls charging**: Automatically turns charger on/off based on battery levels
3. **Optimizes battery health**: Keeps battery between optimal charge ranges
4. **Handles system events**: Responds to Home Assistant startup and automation reloads
5. **Prevents overcharging**: Turns off charger when battery reaches maximum level
6. **Prevents deep discharge**: Turns on charger when battery reaches minimum level

## Usage Examples
```yaml
# Example: Wall-mounted tablet battery management
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml
    input:
      battery_entity: sensor.kitchen_tablet_battery_level
      switch_entity: switch.kitchen_tablet_charger
      max_percent: 80
      min_percent: 30

# Example: Office tablet with conservative charging
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml
    input:
      battery_entity: sensor.office_tablet_battery_level
      switch_entity: switch.office_tablet_charger
      max_percent: 90
      min_percent: 20
```

## Dependencies
- **Battery sensor**: Must have a sensor with device_class: battery
- **Charger switch**: Must have a switch entity to control the charger
- **No additional integrations required**

## Related Files
- `packages/tablets.yaml`: Tablet interface management configurations
- `packages/kitchen/`: Kitchen automation configurations
- `packages/office.yaml`: Office automation configurations

## Notes
- Designed to optimize battery health and lifespan
- Prevents overcharging by stopping at maximum percentage
- Prevents deep discharge by starting at minimum percentage
- Automatically handles system restarts and automation reloads
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Recommended battery ranges: 20-80% for optimal battery health

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
