# Tablet Battery Charging Blueprint Documentation

## Overview
A blueprint for keeping a tablet's battery between the low and high point. This blueprint automatically controls charging to maintain optimal battery health.

## Blueprint Information
- **Name**: Tablet Battery Charging
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `battery_entity`: The sensor entity which tracks the tablet's charge percentage
- `switch_entity`: The switch entity which turns the charger on/off
- `max_percent`: The percentage charge that the charger will turn off (default: 85%)
- `min_percent`: The percentage charge that the charger will turn on (default: 40%)

## Functionality
This blueprint creates an automation that:
- Monitors tablet battery level continuously
- Automatically turns on charger when battery drops below minimum
- Automatically turns off charger when battery reaches maximum
- Maintains battery health by preventing overcharging
- Uses single mode execution for reliable operation

## Usage Examples
```yaml
# Example: Kitchen tablet battery management
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml
    input:
      battery_entity: sensor.kitchen_tablet_battery
      switch_entity: switch.kitchen_tablet_charger
      max_percent: 80
      min_percent: 30
```

## Dependencies
- Battery sensor with device_class: battery
- Switch entity for charger control
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Designed for tablet battery health management
- Uses numeric state triggers for battery monitoring
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [General Blueprint Index](README.md)*
