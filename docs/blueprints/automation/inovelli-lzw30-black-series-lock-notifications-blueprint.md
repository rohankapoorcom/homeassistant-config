# Inovelli LZW30 Black Series Lock Notifications Blueprint Documentation

## Overview
This blueprint uses an Inovelli Black Series LZW30 switch to provide visual lock status notifications. The switch's LED indicator changes color based on the lock state - green for locked and red for unlocked - providing immediate visual feedback about door security status.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml)

## Blueprint Information
- **Name**: Inovelli LZW30 Lock Notifications
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `lock_entity`: Lock entity to monitor
- `zwave_device`: Inovelli LZW30 Black Series switch device

## Functionality
This blueprint creates an automation that:

1. **Monitors lock state**: Listens for any state changes in the specified lock entity
2. **Updates LED indicator**: Changes the switch's LED color based on lock status
3. **Visual feedback**: Green LED indicates locked, red LED indicates unlocked
4. **Real-time updates**: Immediately reflects lock state changes
5. **Simple operation**: Straightforward automation without complex conditions

## Usage Examples
```yaml
# Example: Front door lock status indicator
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml
    input:
      lock_entity: lock.front_door
      zwave_device: "Front Door Status Switch"

# Example: Garage door lock status indicator
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml
    input:
      lock_entity: lock.garage_door
      zwave_device: "Garage Door Status Switch"
```

## Dependencies
- **Z-Wave JS integration**: Must be installed and configured
- **Inovelli LZW30 Black Series switch**: Must be properly paired and configured
- **Lock entity**: Must have a lock entity available
- **Z-Wave network**: Must have a stable Z-Wave network connection

## Related Files
- `packages/front_door.yaml`: Front door automation configurations
- `packages/garage.yaml`: Garage automation configurations
- `packages/security.yaml`: Security automation configurations

## Notes
- Uses Inovelli Black Series switches for visual lock status indication
- Green LED = Locked, Red LED = Unlocked for intuitive color coding
- Updates in real-time when lock state changes
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for providing immediate visual feedback about door security
- Can be used with any lock entity in Home Assistant

---

*This documentation is part of the [Blueprint Documentation Index](../README.md)*
