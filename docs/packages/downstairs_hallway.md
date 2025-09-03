# Downstairs Hallway Package Documentation

## Overview
The downstairs hallway package manages comprehensive downstairs hallway automation including tablet management, scene controls, TV control, and water heater monitoring. This package provides intelligent tablet charging, Inovelli switch-based scene control, Roku TV automation, and e-paper display integration for enhanced downstairs hallway functionality.

## Configuration Files
- `packages/downstairs_hallway.yaml`: Main downstairs hallway configuration

## Functionality
The downstairs hallway package provides:
- **Tablet Management**: Automated tablet charging and browser management
- **Scene Controls**: Inovelli VZM31-SN Blue Series switch integration
- **TV Automation**: Roku TV state-based automation
- **Water Heater Monitoring**: E-paper display for water heater status
- **Multi-Device Control**: Control of multiple devices from hallway
- **Energy Optimization**: Energy-efficient device management

## Key Components

### Tablet Management System
- **Battery Monitoring**: Combined tablet battery monitoring
- **Automated Charging**: Intelligent tablet charging automation
- **Browser Management**: Automated browser restart functionality
- **Power Optimization**: Energy-efficient tablet power management

### Scene Control System
- **Inovelli Switch**: VZM31-SN Blue Series switch integration
- **Button Mapping**: Multiple button mapping for different functions
- **Multi-Device Control**: Control of tablet charger and TV
- **Browser Management**: Browser restart functionality

### TV Automation System
- **Roku Integration**: Roku Streambar integration
- **State-Based Control**: Roku state-based TV control
- **Idle Detection**: Automatic TV shutdown on idle
- **Power Management**: Energy-efficient TV power management

### Water Heater Monitoring
- **E-Paper Display**: E-paper display for water heater status
- **Cleaning Tracking**: Water heater cleaning status tracking
- **Visual Display**: Visual status display on e-paper
- **Maintenance Tracking**: Maintenance schedule tracking

## Entities

### Tablet Management
- `sensor.downstairs_hallway_tablets_battery_combined`: Combined tablet battery
  - **Function**: Combined tablet battery monitoring
  - **Integration**: Automated charging control
  - **Monitoring**: Real-time battery level tracking

- `switch.downstairs_hallway_tablet_charger`: Downstairs hallway tablet charger
  - **Function**: Tablet charging control
  - **Automation**: Automated charging management
  - **Power**: Power management for tablets

- `button.downstairs_hallway_tablet_restart_browser`: Tablet browser restart
  - **Function**: Browser restart functionality
  - **Automation**: Automated browser management
  - **Integration**: Tablet integration

### TV Control
- `switch.downstairs_hallway_tv`: Downstairs hallway TV control
  - **Function**: TV power control
  - **Automation**: Roku state-based automation
  - **Power**: Energy-efficient TV power management

- `media_player.roku_streambar`: Roku Streambar media player
  - **Function**: Roku media control
  - **States**: on, idle, playing
  - **Integration**: TV automation integration

### Water Heater Monitoring
- `input_datetime.water_heater_last_cleaning`: Water heater cleaning date
  - **Function**: Cleaning date tracking
  - **Display**: E-paper display integration
  - **Maintenance**: Maintenance schedule tracking

### Inovelli Switch
- **Device ID**: `1b083dd3571388e94041b98699fb31cf`
- **Model**: VZM31-SN Blue Series switch
- **Function**: Scene control and device management
- **Integration**: Multi-device control

## Automations

### Control the Downstairs Hallway Tablet Charger
- **ID**: `049cbddb-1796-4df9-be5b-7a6e0335015d`
- **Description**: Automated tablet charging management
- **Blueprint**: `tablet-battery-charging.yaml`
- **Battery Entity**: `sensor.downstairs_hallway_tablets_battery_combined`
- **Switch Entity**: `switch.downstairs_hallway_tablet_charger`
- **Function**: Intelligent tablet charging automation

### Downstairs Hallway Scene Controls
- **ID**: `1667032713651`
- **Description**: Inovelli switch-based scene control
- **Blueprint**: `inovelli-vzm31-sn-blue-series-switch.yaml`
- **Inovelli Switch**: `1b083dd3571388e94041b98699fb31cf`
- **Button Mapping**:
  - **Config Button**: Restart downstairs hallway tablet browser
  - **Button A2**: Toggle downstairs hallway tablet charger
  - **Button B2**: Toggle downstairs hallway TV

### Control the Downstairs Hallway TV
- **ID**: `60f9f9b9-ef6e-494d-af89-fd43cdc92d9e`
- **Description**: Roku state-based TV control
- **Triggers**:
  - Home Assistant start event
  - Automation reload event
  - Roku Streambar state change to 'on'
  - Roku Streambar state change to 'idle' for 10 minutes
- **Actions**:
  - **Roku Idle**: Turn off downstairs hallway TV
  - **Roku On**: Turn on downstairs hallway TV

### Update Water Heater Cleaning Status
- **ID**: `825c80a1-794c-4f3c-95a9-077ebee85d58`
- **Description**: E-paper display for water heater cleaning status
- **Triggers**:
  - Home Assistant start event
  - Automation reload event
  - Water heater cleaning date change
- **Actions**: Update e-paper display with cleaning status

### Automation Features
- **Multi-Device Control**: Control of multiple devices from hallway
- **State-Based Automation**: Roku state-based TV control
- **Idle Detection**: Automatic TV shutdown on idle
- **E-Paper Integration**: Visual status display on e-paper
- **Energy Optimization**: Energy-efficient device management

## Dependencies
- **Inovelli Switch**: VZM31-SN Blue Series switch integration
- **Custom Blueprints**: Tablet charging and scene control blueprints
- **Roku Integration**: Roku Streambar integration
- **E-Paper Integration**: E-paper display integration
- **Z-Wave JS**: Z-Wave device communication and control

## Usage
The downstairs hallway package provides several interaction methods:
- **Inovelli Switch**: Physical switch control for hallway functions
- **Automated Charging**: Automatic tablet charging management
- **Roku Integration**: Roku state-based TV automation
- **E-Paper Display**: Visual water heater status display
- **Dashboard Control**: Direct control via Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Tablet Management Setup
- **Battery Monitoring**: Combined tablet battery monitoring
- **Charging Automation**: Automated charging control
- **Browser Management**: Automated browser restart
- **Power Optimization**: Energy-efficient power management

### Scene Control Setup
- **Inovelli Switch**: VZM31-SN Blue Series switch configuration
- **Button Mapping**: Individual button mapping for different functions
- **Multi-Device Control**: Control of tablet charger and TV
- **Browser Management**: Browser restart functionality

### TV Automation Setup
- **Roku Integration**: Roku Streambar integration
- **State Monitoring**: Roku state monitoring
- **Idle Detection**: Automatic idle detection
- **Power Management**: Energy-efficient TV power management

### Water Heater Monitoring Setup
- **E-Paper Display**: E-paper display configuration
- **Cleaning Tracking**: Water heater cleaning tracking
- **Visual Display**: Visual status display configuration
- **Maintenance Tracking**: Maintenance schedule tracking

## Related Files
- `packages/downstairs_hallway.yaml`: Main downstairs hallway package configuration
- `blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml`: Tablet charging blueprint
- `blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`: Inovelli switch blueprint
- `dashboards/home.yaml`: Downstairs hallway dashboard display

## Notes
- Tablet charging automation optimizes battery life and ensures availability
- Inovelli switch provides comprehensive downstairs hallway control
- Roku state-based TV automation provides energy-efficient TV control
- 10-minute idle detection prevents premature TV shutdown
- E-paper display provides visual water heater maintenance tracking
- Combined tablet battery monitoring manages multiple tablets
- The package integrates with other automation packages
- Custom attributes store package information for consistent operation
