# Lock Light Controls Blueprint Documentation

## Overview
This blueprint creates a simple automation that turns on a light when a lock is unlocked. It's perfect for providing immediate illumination when someone enters a room or building, enhancing safety and convenience.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/lock-light-controls.yaml)

## Blueprint Information
- **Name**: Lock Light Controls
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/lock-light-controls.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `lock_entity`: Lock entity to monitor
- `light_entity`: Light entity to control

## Functionality
This blueprint creates an automation that:

1. **Monitors lock state**: Listens for lock state changes from 'locked' to 'unlocked'
2. **Triggers light**: Automatically turns on the specified light when lock is unlocked
3. **Sets brightness**: Turns on the light at 100% brightness for maximum visibility
4. **Simple operation**: Straightforward automation without complex conditions

## Usage Examples
```yaml
# Example: Front door lock controls entry light
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/lock-light-controls.yaml
    input:
      lock_entity: lock.front_door
      light_entity: light.entry_hallway

# Example: Garage door lock controls garage light
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/lock-light-controls.yaml
    input:
      lock_entity: lock.garage_door
      light_entity: light.garage_ceiling
```

## Dependencies
- **Lock entity**: Must have a lock entity available
- **Light entity**: Must have a light entity available
- **No additional integrations required**

## Related Files
- `packages/front_door.yaml`: Front door automation configurations
- `packages/garage.yaml`: Garage automation configurations
- `packages/security.yaml`: Security automation configurations

## Notes
- Simple and reliable automation for basic lock-light coordination
- Turns on light at full brightness for maximum visibility
- Single mode execution ensures reliable operation
- Silent error handling for maximum exceeded scenarios
- Perfect for entry points where immediate lighting is needed
- Can be combined with other automations for more complex scenarios

---

*This documentation is part of the [Blueprint Documentation Index](../../../README.md)*
