# Sun-Based Cover Control Blueprint Documentation

## Overview
Automatically opens and closes curtains or shades based on sun position and window/door status with customizable notification actions. This blueprint provides intelligent window covering automation that responds to natural light cycles while respecting window and door positions.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/sun-based-cover-control.yaml)

## Blueprint Information
- **Name**: Sun-Based Cover Control
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/sun-based-cover-control.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `cover_entity`: Cover entity to control (curtains, shades, blinds)
- `open_status_sensor`: Binary sensor for window/door open/closed status
- `sunrise_offset`: Time offset after sunrise to open shades (default: "01:30:00")
- `close_delay`: Optional delay in seconds before closing shades (default: 0)
- `presence_sensor`: Optional presence sensor to check before opening shades
- `notification_action`: Action to run for LED notifications (optional, default: [])

## Functionality
This blueprint creates an automation that:

### Triggers
- **Sunset**: Closes shades after sunset
- **Sunrise + Offset**: Opens shades after sunrise with configurable offset (default 90 minutes)
- **Window/Door Close**: Closes shades immediately when windows/doors are closed
- **System Start**: Runs on Home Assistant startup
- **Automation Reload**: Runs when automation is reloaded

### Actions
- **Close Sequence**: 
  - Checks if windows/doors are closed
  - Applies optional delay before closing
  - Closes the cover entity
  - Executes notification action
  
- **Open Sequence**:
  - Waits for presence sensor to be off (if configured)
  - Opens the cover entity
  - Executes notification action

### Smart Features
- **Window/Door Integration**: Prevents closing shades when windows/doors are open
- **Presence Awareness**: Optional presence sensor check before opening
- **Configurable Timing**: Customizable sunrise offset and close delay
- **Notification Support**: LED feedback or script execution
- **Safe Template Handling**: Uses `states()` function to handle undefined entities

## Usage Examples

### Basic Living Room Curtains
```yaml
- use_blueprint:
    path: rohankapoorcom/sun-based-cover-control.yaml
    input:
      cover_entity: cover.living_room_curtains
      open_status_sensor: binary_sensor.living_room_windows
      sunrise_offset: "01:30:00"
      close_delay: 5
      notification_action:
        - action: zwave_js.bulk_set_partial_config_parameters
          target:
            device_id: !input living_room_light_switch_device_id
          data:
            parameter: 99
            value:
              All LED Strip Effect - Color: 170
              All LED Strip Effect - Level: 40
              All LED Strip Effect - Duration: 10
              All LED Strip Effect - Effect: Open/close
```

### Master Bedroom with Presence Sensor
```yaml
- use_blueprint:
    path: rohankapoorcom/sun-based-cover-control.yaml
    input:
      cover_entity: cover.master_bedroom_shades
      open_status_sensor: binary_sensor.master_bedroom_sliding_door_window_door_is_open
      sunrise_offset: "01:30:00"
      close_delay: 0
      presence_sensor: binary_sensor.master_bedroom_occupancy
      notification_action:
        - action: script.inovelli_blue_notifications
          data:
            led: All
            color: 170
            level: 40
            duration: 10
            effect: Open/close
```

### Gym Shades (No Presence Sensor)
```yaml
- use_blueprint:
    path: rohankapoorcom/sun-based-cover-control.yaml
    input:
      cover_entity: cover.gym_shades
      open_status_sensor: binary_sensor.gym_sliding_door_window_door_is_open
      sunrise_offset: "01:30:00"
      close_delay: 0
      notification_action:
        - action: zwave_js.bulk_set_partial_config_parameters
          target:
            device_id: !input gym_light_switch_device_id
          data:
            parameter: 99
            value:
              All LED Strip Effect - Color: 170
              All LED Strip Effect - Level: 40
              All LED Strip Effect - Duration: 10
              All LED Strip Effect - Effect: Open/close
```

## Dependencies
- **Sun Integration**: Built-in Home Assistant integration for sunrise/sunset events
- **Cover Domain**: For controlling curtains, shades, and blinds
- **Binary Sensor**: For window/door status monitoring
- **Optional**: Z-Wave JS integration for LED notifications
- **Optional**: Custom scripts for notification actions

## Related Files
- `packages/living_room/living_room_lights.yaml`: Original automation this blueprint was based on
- `packages/master_bedroom.yaml`: Master bedroom automation using similar logic
- `packages/gym.yaml`: Gym automation with similar functionality
- `packages/kitchen/kitchen_lights.yaml`: Kitchen automation with variations

## Notes
- **Template Safety**: Uses `states()` function to safely handle undefined presence sensors
- **Flexible Configuration**: All timing and sensor inputs are configurable
- **Notification Support**: Supports any action sequence for LED feedback or scripts
- **Window/Door Awareness**: Automatically prevents closing when windows/doors are open
- **Presence Integration**: Optional presence sensor prevents opening when room is occupied
- **Multiple Triggers**: Responds to sun events, window status, and system events
- **Based on Real Usage**: Derived from actual automations in use across multiple rooms

## Troubleshooting
- **Shades not opening**: Check sunrise offset timing and presence sensor configuration
- **Shades not closing**: Verify window/door sensor is working correctly
- **Notifications not working**: Ensure notification action is properly configured for your devices
- **Template errors**: Verify all sensor entities exist and are accessible

---
*This documentation is part of the [Blueprint Documentation Index](../README.md)*
