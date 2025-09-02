# Inovelli LZW30 Black Series Lock Notifications Blueprint Documentation

## Overview
A blueprint for creating lock notification automations for Inovelli LZW30 Black Series switches. This blueprint provides notifications when the lock state changes.

## Blueprint Information
- **Name**: Inovelli LZW30 Black Series Lock Notifications
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `lock_entity`: The lock entity to monitor
- `notification_action`: Action to run when lock state changes

## Functionality
This blueprint creates an automation that:
- Monitors Inovelli LZW30 Black Series lock state changes
- Triggers customizable notifications on lock/unlock events
- Uses single mode execution for reliable operation
- Handles Z-Wave JS integration events

## Usage Examples
```yaml
# Example: Lock notifications with mobile app
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml
    input:
      lock_entity: lock.front_door
      notification_action:
        - service: notify.mobile_app
          data:
            title: "Front Door Lock"
            message: "{{ 'Locked' if is_state('lock.front_door', 'locked') else 'Unlocked' }}"
```

## Dependencies
- Z-Wave JS integration
- Inovelli LZW30 Black Series switch
- Notification service

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/`: Room-specific automation configurations

## Notes
- Specifically designed for Inovelli LZW30 Black Series switches
- Uses Z-Wave JS integration for device communication
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios

---
*This documentation is part of the [Inovelli Blueprint Index](README.md)*
