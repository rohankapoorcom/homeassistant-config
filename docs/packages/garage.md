# Garage Package Documentation

## Overview
The garage package manages comprehensive garage automation including lighting control, motion detection, garage door control, and tablet management. This package provides intelligent garage lighting, motion-activated controls, garage door integration, and automated tablet screen management for enhanced garage functionality and security.

## Configuration Files
- `packages/garage.yaml`: Main garage configuration

## Functionality
The garage package provides:
- **Intelligent Lighting Control**: Motion and garage door-based lighting automation
- **Motion Detection**: Multi-sensor motion detection system
- **Garage Door Integration**: Garage door state-based automation
- **Tablet Management**: Automated tablet screen control
- **Multi-Trigger Automation**: Multiple trigger conditions for comprehensive control
- **Timed Shutdown**: Automatic shutdown with extended delay periods

## Key Components

### Motion Detection System
- **Garage Motion Group**: Multi-sensor motion detection group
- **Motion Sensors**: Multiple motion sensors for comprehensive coverage
- **Presence Detection**: Presence sensor integration
- **Multi-Sensor Logic**: Group-based motion detection logic

### Lighting Control System
- **Garage Lights**: Main garage lighting control
- **Garage Door Light**: Garage door area lighting
- **Motion-Activated**: Motion-based lighting activation
- **Door-Triggered**: Garage door state-based lighting

### Garage Door Integration
- **Door State Monitoring**: Real-time garage door state monitoring
- **Opening Detection**: Garage door opening detection
- **State-Based Control**: Door state-based automation control
- **Security Integration**: Security system integration

### Tablet Management
- **Tablet Screen Control**: Automated tablet screen power management
- **Power Optimization**: Energy-efficient tablet screen control
- **Integration**: Tablet integration with garage automation
- **Timed Control**: Automatic tablet screen shutdown

## Entities

### Lights
- `light.garage_lights`: Garage lighting control
  - **Platform**: Switch-based light control
  - **Entity ID**: `switch.garage_lights`
  - **Function**: Main garage area lighting

### Motion Sensors
- `binary_sensor.garage_motion`: Garage motion detection group
  - **Unique ID**: `e0fcd27b-7ca9-42c3-815e-63d15f0795ed`
  - **Device Class**: motion
  - **Entities**: Multiple motion sensors
  - **Function**: Comprehensive motion detection

### Individual Motion Sensors
- `binary_sensor.garage_lights_motion`: Garage lights area motion
- `binary_sensor.garage_multisensor_motion`: Garage multisensor motion
- `binary_sensor.garage_presence_sensor_presence`: Garage presence sensor

### Garage Door
- `cover.garage_door`: Garage door control and monitoring
  - **States**: closed, opening, open
  - **Integration**: Door state-based automation
  - **Security**: Security system integration

### Tablet Control
- `switch.garage_tablet_screen`: Garage tablet screen control
  - **Function**: Tablet screen power management
  - **Integration**: Garage automation integration
  - **Energy**: Energy-efficient power control

### Additional Lights
- `light.garage_door_light`: Garage door area lighting
  - **Function**: Door area specific lighting
  - **Integration**: Door state-based control

## Automations

### Control the Garage Lights
- **ID**: `8cbaf941-3de6-482e-9226-fbe103e7c84e`
- **Description**: Comprehensive garage lighting and tablet control
- **Mode**: Restart with silent error handling
- **Triggers**:
  - Home Assistant start event
  - Automation reload event
  - Garage motion sensor activation (off to on)
  - Garage door opening (closed to opening)
- **Actions**:
  - **Condition**: Motion detected OR garage door opening/open
  - **Sequence**:
    1. Turn on garage lights and door light
    2. Turn on garage tablet screen
    3. Wait for door closed AND no motion
    4. 10-minute delay
    5. Turn off garage lights, door light, and tablet screen
  - **Default**: Turn off all garage lights and tablet screen

### Automation Logic
The automation includes sophisticated logic:
- **Multi-Trigger**: Multiple trigger conditions for comprehensive control
- **State Monitoring**: Real-time garage door state monitoring
- **Motion Integration**: Motion detection integration
- **Extended Delay**: 10-minute delay for extended garage use
- **Comprehensive Control**: Control of lights and tablet screen
- **Error Handling**: Silent error handling for maximum exceeded scenarios

### Send Garage Vacuum Home When Garage Door Opens
- **ID**: `4c9eaa93-7d04-4e3c-94b1-bfda6e3a89b9`
- **Description**: Sends the garage vacuum back to its dock when the garage door starts opening and the garage vacuum is not currently docked.
- **Mode**: Single
- **Triggers**:
  - Garage door opening (closed to opening)
- **Conditions**:
  - Safety check to ensure the garage vacuum is available and not currently docked
- **Actions**:
  - Command the garage vacuum to return to base

## Dependencies
- **Motion Sensors**: Multiple motion sensor integration
- **Garage Door**: Garage door control and monitoring
- **Lighting Control**: Garage lighting control integration
- **Tablet Integration**: Tablet screen control integration
- **Template Logic**: Complex state and motion-based logic
- **Timing Control**: Extended timing and delay control

## Usage
The garage package provides several interaction methods:
- **Motion Activation**: Automatic lighting and tablet activation based on motion
- **Door Integration**: Garage door state-based automation
- **Manual Control**: Direct control via switches and dashboard
- **Dashboard Integration**: Garage status on Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Motion Sensor Setup
- **Multi-Sensor Group**: Multiple motion sensors for comprehensive coverage
- **Motion Integration**: Motion detection system integration
- **Trigger Logic**: Motion activation triggers comprehensive control
- **Response Timing**: Immediate response to motion detection

### Garage Door Integration
- **Door State Monitoring**: Real-time garage door state monitoring
- **State-Based Control**: Door state-based automation control
- **Security Integration**: Security system integration
- **Opening Detection**: Garage door opening detection

### Lighting Control
- **Multi-Light Control**: Control of multiple garage lights
- **Timing Control**: Extended timing and delay control
- **Energy Management**: Energy-efficient lighting control
- **Integration**: Integration with motion and door systems

### Tablet Management
- **Screen Control**: Tablet screen power management
- **Energy Optimization**: Energy-efficient tablet control
- **Integration**: Tablet integration with garage automation
- **Timed Control**: Automatic tablet screen shutdown

## Related Files
- `packages/garage.yaml`: Main garage package configuration
- `packages/security.yaml`: Security system integration
- `dashboards/home.yaml`: Garage dashboard display

## Notes
- Garage automation activates on motion detection or garage door opening
- 10-minute delay ensures adequate time for garage activities
- Multiple motion sensors provide comprehensive coverage
- Tablet screen control optimizes energy usage
- Restart mode with silent error handling ensures reliable operation
- The package integrates with security system for enhanced security
- Custom attributes store package information for consistent operation
