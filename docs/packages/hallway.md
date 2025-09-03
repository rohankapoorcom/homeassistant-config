# Hallway Package Documentation

## Overview
The hallway package manages comprehensive hallway automation including lighting control, tablet management, scene controls, and closet lighting. This package provides intelligent hallway lighting, automated tablet charging, Zooz scene controller integration, and motion-activated closet lighting for enhanced hallway functionality and convenience.

## Configuration Files
- `packages/hallway.yaml`: Main hallway configuration

## Functionality
The hallway package provides:
- **Tablet Management**: Automated tablet charging and power management
- **Scene Controls**: Zooz ZEN32 scene controller integration
- **Status Lights**: LED status indicators for lighting states
- **Closet Lighting**: Motion-activated closet lighting automation
- **Multi-Room Control**: Control of multiple rooms from hallway
- **Energy Optimization**: Energy-efficient lighting and power management

## Key Components

### Tablet Management System
- **Battery Monitoring**: Real-time tablet battery monitoring
- **Automated Charging**: Intelligent tablet charging automation
- **Power Optimization**: Energy-efficient tablet power management
- **Charging Control**: Automated charging control system

### Scene Control System
- **Zooz ZEN32**: ZEN32 scene controller integration
- **Multi-Room Control**: Control of dining room, kitchen, and hallway
- **Scene Mapping**: Multiple scene configurations
- **Toggle Functionality**: Toggle control for various lighting zones

### Status Light System
- **LED Indicators**: Visual status indicators for lighting states
- **State Mapping**: Real-time lighting state mapping
- **Visual Feedback**: Visual feedback for lighting states
- **Status Synchronization**: Synchronized status indicators

### Closet Lighting System
- **Motion Activation**: Motion-activated closet lighting
- **Door Integration**: Door state integration for lighting control
- **Immediate Response**: Immediate lighting response
- **Energy Efficiency**: Energy-efficient closet lighting

## Entities

### Tablet Management
- `sensor.upstairs_hallway_tablet_battery`: Upstairs hallway tablet battery
  - **Function**: Tablet battery monitoring
  - **Integration**: Automated charging control
  - **Monitoring**: Real-time battery level tracking

- `switch.upstairs_hallway_tablet_charger`: Upstairs hallway tablet charger
  - **Function**: Tablet charging control
  - **Automation**: Automated charging management
  - **Power**: Power management for tablet

### Scene Control
- **Zooz ZEN32 Device ID**: `4418d1607160e581af11597ef65ef295`
- **Model**: Zooz ZEN32 scene controller
- **Function**: Multi-room scene control
- **Integration**: Z-Wave scene controller integration

### Lighting Control
- `light.hallway_lights`: Hallway lighting control
  - **Function**: Main hallway lighting
  - **Control**: Scene controller integration
  - **Status**: LED status indicator

- `light.dining_room_lights`: Dining room lighting control
  - **Function**: Dining room lighting
  - **Control**: Scene controller integration
  - **Status**: LED status indicator

- `light.dining_room_accent_lights`: Dining room accent lighting
  - **Function**: Dining room accent lighting
  - **Control**: Scene controller integration
  - **Status**: LED status indicator

- `light.kitchen_lights`: Kitchen lighting control
  - **Function**: Kitchen lighting
  - **Control**: Scene controller integration
  - **Status**: LED status indicator

- `light.kitchen_cabinet_lights`: Kitchen cabinet lighting
  - **Function**: Kitchen cabinet lighting
  - **Control**: Scene controller integration
  - **Status**: LED status indicator

### Closet Lighting
- `light.upstairs_hallway_closet_lights`: Upstairs hallway closet lighting
  - **Function**: Closet lighting control
  - **Motion**: Motion-activated control
  - **Door**: Door state integration

- `binary_sensor.upstairs_hallway_closet_door_window_door_is_open`: Closet door sensor
  - **Function**: Closet door state monitoring
  - **Integration**: Motion light automation
  - **Control**: Door-based lighting control

## Automations

### Control the Upstairs Hallway Tablet Charger
- **ID**: `0de6a925-9ceb-42fb-b7be-f6621be3ed09`
- **Description**: Automated tablet charging management
- **Blueprint**: `tablet-battery-charging.yaml`
- **Battery Entity**: `sensor.upstairs_hallway_tablet_battery`
- **Switch Entity**: `switch.upstairs_hallway_tablet_charger`
- **Function**: Intelligent tablet charging automation

### Upstairs Hallway Scene Controls
- **ID**: `1643337826040`
- **Description**: Zooz ZEN32 scene controller automation
- **Blueprint**: `ZoozZen32forZwaveJs.yaml`
- **Zooz Switch**: `4418d1607160e581af11597ef65ef295`
- **Scene Mapping**:
  - **Scene 1**: Toggle dining room lights
  - **Scene 2**: Toggle dining room accent lights
  - **Scene 3**: Toggle kitchen lights
  - **Scene 4**: Toggle kitchen cabinet lights (with brightness and color temp)
  - **Scene 5**: Toggle hallway lights

### Upstairs Hallway Scene Controller Status Lights
- **ID**: `1643339651442`
- **Description**: LED status indicators for lighting states
- **Blueprint**: `zooz-zen32-scene-controller-status-lights.yaml`
- **Zooz Switch**: `4418d1607160e581af11597ef65ef295`
- **Status Mapping**:
  - **Large Button**: Hallway lights status
  - **Small Button 1**: Dining room lights status
  - **Small Button 2**: Dining room accent lights status
  - **Small Button 3**: Kitchen lights status
  - **Small Button 4**: Kitchen cabinet lights status

### Control the Hallway Closet Lights
- **ID**: `56be5167-15a8-4243-ae8d-c4b8b82b3e9e`
- **Description**: Motion-activated closet lighting
- **Blueprint**: `motion_light.yaml`
- **Motion Entity**: `binary_sensor.upstairs_hallway_closet_door_window_door_is_open`
- **Light Target**: `light.upstairs_hallway_closet_lights`
- **No Motion Wait**: 0 seconds (immediate response)

### Automation Features
- **Multi-Room Control**: Control of multiple rooms from hallway
- **Scene Management**: Comprehensive scene management
- **Status Synchronization**: Real-time status synchronization
- **Motion Integration**: Motion-activated closet lighting
- **Energy Optimization**: Energy-efficient lighting control

## Dependencies
- **Zooz ZEN32**: ZEN32 scene controller integration
- **Custom Blueprints**: Tablet charging and scene control blueprints
- **Z-Wave JS**: Z-Wave device communication and control
- **Motion Sensors**: Motion detection integration
- **Lighting Control**: Multi-room lighting control integration

## Usage
The hallway package provides several interaction methods:
- **Zooz Scene Controller**: Physical scene controller for multi-room control
- **Automated Charging**: Automatic tablet charging management
- **Motion Activation**: Motion-activated closet lighting
- **Dashboard Control**: Direct control via Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Tablet Management Setup
- **Battery Monitoring**: Tablet battery level monitoring
- **Charging Automation**: Automated charging control
- **Power Optimization**: Energy-efficient power management
- **Charging Control**: Automated charging management

### Scene Control Setup
- **Zooz ZEN32**: ZEN32 scene controller configuration
- **Scene Mapping**: Individual scene mapping for different functions
- **Multi-Room Control**: Control of multiple rooms from hallway
- **Status Integration**: LED status indicator integration

### Status Light Setup
- **LED Mapping**: LED status indicator mapping
- **State Synchronization**: Real-time state synchronization
- **Visual Feedback**: Visual feedback for lighting states
- **Status Control**: Status indicator control

### Closet Lighting Setup
- **Motion Integration**: Motion sensor integration
- **Door Integration**: Door state integration
- **Immediate Response**: Immediate lighting response
- **Energy Efficiency**: Energy-efficient lighting control

## Related Files
- `packages/hallway.yaml`: Main hallway package configuration
- `blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml`: Tablet charging blueprint
- `blueprints/automation/Matt-PMCT/ZoozZen32forZwaveJs.yaml`: Zooz scene controller blueprint
- `blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml`: Status lights blueprint
- `blueprints/automation/rohankapoorcom/motion_light.yaml`: Motion light blueprint
- `dashboards/home.yaml`: Hallway dashboard display

## Notes
- Tablet charging automation optimizes battery life and ensures availability
- Zooz ZEN32 provides comprehensive multi-room control from hallway
- LED status indicators provide real-time lighting state feedback
- Motion-activated closet lighting provides immediate response
- Scene 4 includes brightness and color temperature control for kitchen cabinets
- The package integrates with dining room and kitchen automation packages
- Custom attributes store package information for consistent operation
