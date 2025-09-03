# Low Battery Level Detection Notification Blueprint Documentation

## Overview
This blueprint monitors all battery sensors in your Home Assistant system and provides notifications when battery levels fall below a configurable threshold. It runs on a schedule and can exclude specific sensors from monitoring.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml)

## Blueprint Information
- **Name**: Low battery level detection & notification for all battery sensors
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `threshold`: Battery warning level threshold (default: 20%)
- `time`: Time to run the battery check (default: 10:00:00)
- `day`: Weekday to test on (0=everyday, 1=Monday, 7=Sunday, default: 0)
- `exclude`: Battery sensors to exclude from monitoring
- `actions`: Actions to run when low battery is detected (supports {{sensors}} variable)

## Functionality
This blueprint creates an automation that:

1. **Schedules battery checks**: Runs at the specified time and day
2. **Scans all battery sensors**: Automatically finds all sensors with device_class: battery
3. **Filters by threshold**: Identifies sensors below the specified battery level
4. **Excludes hidden sensors**: Skips sensors marked as hidden entities
5. **Handles exclusions**: Respects the exclude list for specific sensors
6. **Executes notifications**: Runs custom actions with sensor information

## Usage Examples
```yaml
# Example: Daily battery check with notification
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml
    input:
      threshold: 15
      time: "09:00:00"
      day: 0
      exclude:
        entity_id:
          - sensor.iphone_battery_level
      actions:
        - service: notify.mobile_app_iphone
          data:
            title: "Low Battery Alert"
            message: "The following devices have low battery: {{sensors}}"

# Example: Weekly battery check
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml
    input:
      threshold: 25
      time: "18:00:00"
      day: 1
      actions:
        - service: notify.notify
          data:
            title: "Weekly Battery Report"
            message: "Devices needing attention: {{sensors}}"
```

## Dependencies
- **Battery sensors**: Must have sensors with device_class: battery
- **Notification service**: Must have a notification service configured
- **No additional integrations required**

## Related Files
- `packages/notifications.yaml`: Notification management configurations
- `packages/tablets.yaml`: Tablet battery management configurations

## Notes
- Based on Sbyx's blueprint and modified for enhanced functionality
- Automatically discovers all battery sensors in the system
- Supports flexible scheduling (daily or weekly)
- Uses template variables to include sensor names and levels in notifications
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- The {{sensors}} variable contains formatted sensor names with battery levels

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
