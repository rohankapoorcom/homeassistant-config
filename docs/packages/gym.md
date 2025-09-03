# Gym Package Documentation

## Overview
The gym package manages comprehensive gym automation including equipment control, tablet management, lighting control, climate management, and automated shade control. This package provides intelligent gym equipment management, automated tablet charging, scene controls, and sun-based shade automation for optimal workout environment.

## Configuration Files
- `packages/gym.yaml`: Main gym configuration

## Functionality
The gym package provides:
- **Tablet Management**: Automated tablet charging and browser management
- **Scene Controls**: Inovelli switch-based scene control automation
- **Shade Automation**: Sun-based automated shade control
- **Climate Control**: Fan control for workout environment
- **Equipment Integration**: Gym equipment automation and control
- **LED Effects**: Custom LED effects for gym atmosphere

## Key Components

### Tablet Management System
- **Battery Monitoring**: Real-time tablet battery monitoring
- **Automated Charging**: Intelligent tablet charging automation
- **Browser Management**: Automated browser restart functionality
- **Power Optimization**: Energy-efficient tablet power management

### Scene Control System
- **Inovelli Switch**: VZW31-SN Red Series switch integration
- **Button Mapping**: Multiple button mapping for different functions
- **LED Effects**: Custom LED effects and animations
- **Multi-Function Control**: Multiple functions per button

### Shade Automation System
- **Sun-Based Control**: Sun position-based shade automation
- **Door Integration**: Sliding door integration for shade control
- **Time-Based Logic**: Time-based shade control logic
- **Environmental Optimization**: Optimal workout environment control

### Climate Control
- **Fan Management**: Gym fan control for workout environment
- **Temperature Optimization**: Temperature optimization for workouts
- **Air Circulation**: Automated air circulation control
- **Comfort Management**: Workout comfort optimization

## Entities

### Tablet Management
- `sensor.gym_tablet_battery`: Gym tablet battery level
  - **Function**: Tablet battery monitoring
  - **Integration**: Automated charging control
  - **Monitoring**: Real-time battery level tracking

- `switch.gym_tablet_charger`: Gym tablet charger control
  - **Function**: Tablet charging control
  - **Automation**: Automated charging management
  - **Power**: Power management for tablet

- `button.gym_tablet_restart_browser`: Gym tablet browser restart
  - **Function**: Browser restart functionality
  - **Automation**: Automated browser management
  - **Integration**: Tablet integration

### Climate Control
- `fan.gym_fan`: Gym fan control
  - **Function**: Gym climate control
  - **Automation**: Automated fan control
  - **Comfort**: Workout comfort optimization

### Shade Control
- `cover.gym_shades`: Gym shade control
  - **Function**: Automated shade control
  - **Sun Integration**: Sun-based automation
  - **Environment**: Workout environment optimization

- `binary_sensor.gym_sliding_door_window_door_is_open`: Gym sliding door sensor
  - **Function**: Door state monitoring
  - **Integration**: Shade control integration
  - **Automation**: Door-based automation

### Inovelli Switch
- **Device ID**: `4ef91ee5285ec4ad43cb3dbf25b3faf7`
- **Model**: VZW31-SN Red Series switch
- **Function**: Scene control and LED effects
- **Integration**: Multi-function control

## Automations

### Control the Gym Tablet Charger
- **ID**: `dd25ecc8-aaee-4a32-8b38-90b13db78b09`
- **Description**: Automated tablet charging management
- **Blueprint**: `tablet-battery-charging.yaml`
- **Battery Entity**: `sensor.gym_tablet_battery`
- **Switch Entity**: `switch.gym_tablet_charger`
- **Function**: Intelligent tablet charging automation

### Gym Scene Controls
- **ID**: `1667032908768`
- **Description**: Inovelli switch-based scene control
- **Blueprint**: `inovelli-vzw31-sn-red-series-switch.yaml`
- **Z-Wave Device**: `4ef91ee5285ec4ad43cb3dbf25b3faf7`
- **Button Mapping**:
  - **Config Button**: Toggle gym shades with LED effects
  - **Config Button 2**: Restart gym tablet browser
  - **Button A2**: Turn on gym fan
  - **Button B2**: Turn off gym fan

### Manage the Gym Shades
- **ID**: `067c456d-a3fa-4ee2-9969-b2a48445e369`
- **Description**: Sun-based automated shade control
- **Triggers**:
  - Sunset event
  - Sunrise event (with 1:30 offset)
  - Gym sliding door state change
  - Home Assistant start
  - Automation reload
- **Actions**:
  - **After Sunset**: Close shades (if door is closed)
  - **90 Minutes After Sunrise**: Open shades
  - **Door Integration**: Shade control based on door state

### Automation Features
- **Sun Integration**: Sun position-based automation
- **Time Offsets**: Customizable time offsets for shade control
- **Door Integration**: Sliding door state integration
- **LED Effects**: Custom LED effects for gym atmosphere
- **Multi-Function Control**: Multiple functions per button

## Dependencies
- **Inovelli Switch**: VZW31-SN Red Series switch integration
- **Custom Blueprints**: Tablet charging and scene control blueprints
- **Sun Integration**: Sun position and astronomical data
- **Z-Wave JS**: Z-Wave device communication and control
- **Cover Control**: Shade control integration
- **Fan Control**: Climate control integration

## Usage
The gym package provides several interaction methods:
- **Inovelli Switch**: Physical switch control for gym functions
- **Automated Charging**: Automatic tablet charging management
- **Sun-Based Automation**: Automatic shade control based on sun position
- **Dashboard Control**: Direct control via Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Tablet Management Setup
- **Battery Monitoring**: Tablet battery level monitoring
- **Charging Automation**: Automated charging control
- **Browser Management**: Automated browser restart
- **Power Optimization**: Energy-efficient power management

### Scene Control Setup
- **Inovelli Switch**: VZW31-SN Red Series switch configuration
- **Button Mapping**: Individual button mapping for different functions
- **LED Effects**: Custom LED effects configuration
- **Multi-Function Control**: Multiple functions per button

### Shade Automation Setup
- **Sun Integration**: Sun position-based automation
- **Time Offsets**: Customizable time offsets
- **Door Integration**: Sliding door state integration
- **Environmental Control**: Workout environment optimization

### Climate Control Setup
- **Fan Control**: Gym fan automation
- **Temperature Management**: Temperature optimization
- **Air Circulation**: Automated air circulation
- **Comfort Optimization**: Workout comfort management

## Related Files
- `packages/gym.yaml`: Main gym package configuration
- `blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml`: Tablet charging blueprint
- `blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml`: Inovelli switch blueprint
- `dashboards/home.yaml`: Gym dashboard display

## Notes
- Tablet charging automation optimizes battery life and ensures availability
- Sun-based shade automation provides optimal workout environment
- Inovelli switch provides comprehensive gym control with LED effects
- 90-minute sunrise offset ensures adequate daylight for workouts
- Door integration prevents shade operation when door is open
- LED effects enhance gym atmosphere and provide visual feedback
- The package integrates with other automation packages
- Custom attributes store package information for consistent operation
