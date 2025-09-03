# Guest Room Package Documentation

## Overview
The guest room package manages guest room automation and lighting control, providing intelligent lighting management and remote control capabilities. This package includes Tuya remote control integration, multi-zone lighting control, and scene-based automation for enhanced guest comfort and convenience.

## Configuration Files
- `packages/guest_room.yaml`: Main guest room configuration

## Functionality
The guest room package provides:
- **Tuya Remote Control**: 4-button Tuya remote control integration
- **Multi-Zone Lighting**: Multiple lighting zones for guest comfort
- **Scene Controls**: Scene-based lighting control automation
- **Guest Comfort**: Enhanced guest room comfort and convenience
- **Remote Management**: Remote control capabilities for guests
- **Lighting Automation**: Intelligent lighting automation for guest use

## Key Components

### Tuya Remote Control System
- **4-Button Remote**: Tuya TS0044 4-button remote control
- **Button Mapping**: Individual button mapping for different functions
- **Scene Control**: Scene-based control automation
- **Remote Integration**: Seamless remote control integration

### Multi-Zone Lighting System
- **Main Room Lights**: Primary guest room lighting
- **Key Light**: Key lighting for specific tasks
- **Desk Lower Lights**: Under-desk lighting for workspace
- **Zone Control**: Individual zone control capabilities

### Scene Control Automation
- **Button 1**: Main room lights toggle
- **Button 2**: Key light toggle
- **Button 3**: Desk lower lights toggle
- **Button 4**: *(Not configured)*
- **Toggle Functionality**: Simple on/off toggle for each zone

## Entities

### Lights
- `light.guest_room_lights`: Guest room main lighting
  - **Function**: Primary guest room lighting
  - **Control**: Remote control via Tuya remote
  - **Toggle**: Simple on/off toggle functionality

- `light.guest_room_key_light`: Guest room key light
  - **Function**: Key lighting for specific tasks
  - **Control**: Remote control via Tuya remote
  - **Toggle**: Simple on/off toggle functionality

- `light.guest_room_desk_lower_lights`: Guest room desk lower lights
  - **Function**: Under-desk lighting for workspace
  - **Control**: Remote control via Tuya remote
  - **Toggle**: Simple on/off toggle functionality

### Tuya Remote Control
- **Device ID**: `2283e3981bf8a11408a1f1c1cc2ec21e`
- **Model**: Tuya TS0044 4-button remote
- **Integration**: Tuya integration for remote control
- **Function**: Scene control automation

## Automations

### Guest Room Desk Remote Scene Controls
- **ID**: `9131cc74-27b4-4794-98fb-700530d11ce2`
- **Description**: Tuya remote control automation for guest room lighting
- **Blueprint**: `tuya-ts0044-4-button-remote.yaml`
- **Tuya Switch**: `2283e3981bf8a11408a1f1c1cc2ec21e`
- **Button Mapping**:
  - **Button 1**: Toggle guest room main lights
  - **Button 2**: Toggle guest room key light
  - **Button 3**: Toggle guest room desk lower lights
  - **Button 4**: *(Not configured)*

### Automation Features
- **Blueprint Integration**: Uses custom Tuya remote blueprint
- **Toggle Functionality**: Simple on/off toggle for each lighting zone
- **Individual Control**: Independent control of each lighting zone
- **Guest-Friendly**: Simple and intuitive control for guests

## Dependencies
- **Tuya Integration**: Tuya device integration for remote control
- **Custom Blueprint**: Tuya TS0044 4-button remote blueprint
- **Lighting Control**: Guest room lighting control integration
- **Scene Management**: Scene-based automation system

## Usage
The guest room package provides several interaction methods:
- **Tuya Remote**: Physical remote control for guest convenience
- **Dashboard Control**: Direct control via Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages
- **Guest Access**: Simple remote control for guest use

## Configuration

### Tuya Remote Setup
- **Device Registration**: Tuya device registration and configuration
- **Button Mapping**: Individual button mapping for different functions
- **Blueprint Integration**: Custom blueprint integration for remote control
- **Scene Configuration**: Scene-based automation configuration

### Lighting Control
- **Multi-Zone Setup**: Multiple lighting zones for comprehensive control
- **Toggle Functionality**: Simple on/off toggle for each zone
- **Guest Optimization**: Guest-friendly control interface
- **Energy Management**: Energy-efficient lighting control

### Automation Configuration
- **Blueprint Usage**: Custom blueprint for Tuya remote control
- **Button Logic**: Individual button logic and mapping
- **Scene Management**: Scene-based automation management
- **Integration**: Integration with lighting control system

## Related Files
- `packages/guest_room.yaml`: Main guest room package configuration
- `blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml`: Tuya remote control blueprint
- `dashboards/home.yaml`: Guest room dashboard display

## Notes
- Tuya remote provides simple and intuitive control for guests
- Three lighting zones provide comprehensive guest room lighting
- Toggle functionality ensures simple on/off control
- Blueprint integration provides reliable remote control automation
- Guest-friendly design ensures easy use for visitors
- The package integrates with other automation packages
- Custom attributes store package information for consistent operation
