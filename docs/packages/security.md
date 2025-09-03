# Security Package Documentation

## Overview
The security package manages comprehensive home security and monitoring systems, including cameras, locks, alarms, and emergency response integration. This package provides a complete security solution with automated lock status indicators, glass break sensor management, smoke/CO alarm notifications, and integration with professional monitoring services.

## Configuration Files
- `packages/security.yaml`: Main security configuration

## Functionality
The security package provides:
- **Lock Status Visualization**: Real-time lock status displayed on Z-Wave switches using LED indicators
- **Glass Break Sensor Management**: Battery-saving automation that enables sensors only when armed
- **Emergency Response Integration**: Automatic emergency service dispatch for fire and CO alarms
- **Ring Alarm Integration**: Synchronization with Ring alarm system and keypad
- **Multi-Door Security**: Comprehensive coverage for front door, side door, and garage door
- **Automated Lighting**: Coordinated lighting control triggered by lock/unlock events

## Key Components

### Lock Status System
- **Front Door Lock**: Status displayed on Inovelli VZW31-SN Red Series Switch
- **Side Door Lock**: Status displayed on Inovelli LZW30 Black Series Switch
- **Garage Door Lock**: Status displayed on Inovelli VZM31-SN Blue Series Dimmer Switch
- **LED Indicators**: Visual status indication using Z-Wave switch LED rings

### Alarm System
- **Alarmo Integration**: Advanced alarm system with multiple zones and automation triggers
- **Ring Keypad Synchronization**: Downstairs Ring keypad integration with Alarmo
- **Glass Break Sensors**: Ring glass break sensors with battery-saving automation
- **Smoke/CO Detection**: Fire and carbon monoxide alarm monitoring and response

### Emergency Response
- **Noonlight Integration**: Professional emergency response service integration
- **Automated Dispatch**: Automatic emergency service notification for critical alarms
- **Mobile Notifications**: High-priority notifications for smoke and CO detection

### Video Surveillance
- **FFmpeg Integration**: Video processing and streaming capabilities
- **Stream Management**: Video stream configuration for security cameras

## Entities

### Scripts
- `script.enable_glass_break_sensors`: Enables Ring glass break sensors for battery conservation
- `script.disable_glass_break_sensors`: Disables Ring glass break sensors when not needed

### Automations
- **Lock Status Automations**: Multiple automations using blueprints for lock status visualization
- **Emergency Response**: Smoke and CO alarm automation with professional monitoring
- **Ring Integration**: Keypad synchronization and glass break sensor management

## Automations

### Show Front Door Lock Status
- **ID**: `d69e14ae-1236-4948-8084-bc162861cbcf`
- **Description**: Displays front door lock status on Inovelli VZW31-SN Red Series Switch
- **Blueprint**: `inovelli-vzw31-sn-red-series-lock-notifications.yaml`
- **Lock Entity**: `lock.front_door_lock`
- **Z-Wave Device**: `64a4dd14224033fa4119a7b1cb66d888`

### Show Side Door Lock Status
- **ID**: `ff131bcc-1a3b-4e2f-adf9-4e92eb98260b`
- **Description**: Displays side door lock status on Inovelli LZW30 Black Series Switch
- **Blueprint**: `inovelli-lzw30-black-series-lock-notifications.yaml`
- **Lock Entity**: `lock.side_door_lock`
- **Z-Wave Device**: `ae0519b39c8bb3cbe6123a6bb612d2d3`

### Show Garage Door Lock Status
- **ID**: `96d57252-86bb-44c7-b6b0-926257312296`
- **Description**: Displays garage door lock status on Inovelli VZM31-SN Blue Series Dimmer Switch
- **Blueprint**: `inovelli-vzm31-sn-blue-series-lock-notifications.yaml`
- **Lock Entity**: `lock.garage_door_lock`
- **Inovelli Switch**: `1b083dd3571388e94041b98699fb31cf`

### Turn on Downstairs Hallway Lights when Garage Door Unlocked
- **ID**: `278143dd-38fe-41db-bf51-d54369e3ae32`
- **Description**: Automatically illuminates hallway when garage door is unlocked
- **Blueprint**: `lock-light-controls.yaml`
- **Lock Entity**: `lock.garage_door_lock`
- **Light Entity**: `light.downstairs_hallway_lights`

### Turn on Downstairs Hallway Lights when Side Door Unlocked
- **ID**: `5879e67e-712b-4770-b2b6-f9b77d5b789c`
- **Description**: Automatically illuminates hallway when side door is unlocked
- **Blueprint**: `lock-light-controls.yaml`
- **Lock Entity**: `lock.side_door_lock`
- **Light Entity**: `light.downstairs_hallway_lights`

### Smoke & CO Alarm Notifications
- **ID**: `1652658055419`
- **Description**: Comprehensive emergency response for fire and carbon monoxide detection
- **Triggers**:
  - Smoke detection: `binary_sensor.fire_alarm` state change to 'on'
  - CO detection: `binary_sensor.co_alarm` state change to 'on'
- **Actions**:
  - **Emergency Dispatch**: Automatic Noonlight alarm creation for fire emergency
  - **Smoke Notification**: High-priority mobile notification with alarm channel
  - **CO Notification**: High-priority mobile notification for carbon monoxide detection
- **Mode**: Single execution to prevent notification spam

### Downstairs Ring Keypad Automations
- **ID**: `1737078956167`
- **Description**: Synchronizes downstairs Ring keypad with Alarmo alarm system
- **Blueprint**: `synchronize-ring-alarm-keypad-v2-with-alarmo.yaml`
- **Keypad**: `f6f70b9f94a10a9d13e034c9a38d033e`
- **Alarm Panel**: `alarm_control_panel.alarmo`

### Control Glass Break Sensors
- **ID**: `1737111319493`
- **Description**: Battery-saving automation that enables glass break sensors only when armed
- **Trigger**: Changes to `alarm_control_panel.alarmo` state
- **Actions**:
  - **When Armed**: Enables glass break sensors for security monitoring
  - **When Disarmed**: Disables glass break sensors to conserve battery power
- **Mode**: Restart to handle multiple state changes
- **Wait Template**: Ensures Ring keypad automation is ready before proceeding

## Dependencies
- **FFmpeg**: Video processing and streaming capabilities
- **Z-Wave JS**: For Z-Wave device communication and control
- **Alarmo**: Advanced alarm system integration
- **Noonlight**: Emergency response service integration
- **Ring Integration**: Ring alarm system and keypad synchronization
- **Custom Blueprints**: Multiple Inovelli and lock control blueprints

## Usage
The security package provides several interaction methods:
- **Visual Indicators**: LED status lights on Z-Wave switches for lock states
- **Automated Response**: Automatic emergency dispatch and notifications
- **Battery Management**: Intelligent glass break sensor power management
- **Integrated Control**: Unified alarm system with Ring keypad synchronization
- **Emergency Services**: Professional monitoring and response integration

## Related Files
- `packages/security.yaml`: Main security package configuration
- `blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-lock-notifications.yaml`: Front door lock status blueprint
- `blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml`: Side door lock status blueprint
- `blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml`: Garage door lock status blueprint
- `blueprints/automation/rohankapoorcom/lock-light-controls.yaml`: Lock and light coordination blueprint
- `blueprints/automation/ImSorryButWho/synchronize-ring-alarm-keypad-v2-with-alarmo.yaml`: Ring keypad synchronization blueprint

## Notes
- Glass break sensors are automatically enabled/disabled based on alarm state to conserve battery power
- Emergency notifications use high-priority channels with maximum importance for critical alerts
- Lock status is visually displayed using Z-Wave switch LED rings for quick status checking
- The system integrates with professional emergency response services for enhanced security
- Multiple door locks are monitored with coordinated lighting responses for entry/exit scenarios
