# Inovelli VZM31-SN Blue Series Lock Notifications Blueprint Documentation

## Overview
This blueprint uses an Inovelli Blue Series VZM31-SN dimmer switch to provide visual lock status notifications. The switch's LED indicator changes color based on the lock state - green for locked and red for unlocked - providing immediate visual feedback about door security status.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml)

## Blueprint Information
- **Name**: Inovelli VZM31-SN Lock Notifications
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `lock_entity`: Lock entity to monitor
- `inovelli_switch`: Inovelli VZM31-SN Blue Series dimmer switch device

## Functionality
This blueprint creates an automation that:

1. **Monitors lock state**: Listens for any state changes in the specified lock entity
2. **Updates LED indicator**: Changes the dimmer's LED color based on lock status
3. **Visual feedback**: Green LED indicates locked, red LED indicates unlocked
4. **Configures LED effects**: Sets brightness to 50% and uses solid effect type
5. **Real-time updates**: Immediately reflects lock state changes

## Usage Examples
```yaml
# Example: Front door lock status indicator
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml
    input:
      lock_entity: lock.front_door
      inovelli_switch: "Front Door Status Dimmer"

# Example: Garage door lock status indicator
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml
    input:
      lock_entity: lock.garage_door
      inovelli_switch: "Garage Door Status Dimmer"
```

## Dependencies
- **MQTT integration**: Must be installed and configured
- **Inovelli VZM31-SN Blue Series dimmer**: Must be properly paired and configured
- **Lock entity**: Must have a lock entity available
- **Zigbee network**: Must have a stable Zigbee network connection
- **Custom script**: Requires `script.inovelli_blue_notifications` to be available

## Related Files
- `packages/front_door.yaml`: Front door automation configurations
- `packages/garage.yaml`: Garage automation configurations
- `packages/security.yaml`: Security automation configurations

## Notes
- Uses Inovelli Blue Series VZM31-SN dimmer switches for visual lock status indication
- Green LED = Locked, Red LED = Unlocked for intuitive color coding
- Sets LED brightness to 50% for optimal visibility
- Uses solid LED effect type for consistent indication
- Updates in real-time when lock state changes
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for providing immediate visual feedback about door security

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
