# Front Door Package Documentation

## Overview
The front door package manages front door automation and security features, providing intelligent lighting control, motion detection, and entry management. This package includes motion-activated lighting, illuminance-based control, and automated entry lighting for enhanced security and convenience.

## Configuration Files
- `packages/front_door.yaml`: Main front door configuration

## Functionality
The front door package provides:
- **Motion-Activated Lighting**: Intelligent lighting control based on motion detection
- **Illuminance-Based Control**: Lighting control based on ambient light levels
- **Entry Management**: Automated entry lighting and security features
- **Darkness Detection**: Automatic lighting when ambient light is low
- **Timed Lighting**: Automatic lighting shutdown after motion ceases
- **Security Enhancement**: Enhanced security through automated lighting

## Key Components

### Motion Detection System
- **Front Door Motion Sensor**: Primary motion detection for front door area
- **Motion Triggers**: Motion-based automation triggers
- **Entry Detection**: Entry and exit detection via motion sensors
- **Security Monitoring**: Security monitoring through motion detection

### Lighting Control System
- **Front Door Lights**: Front door area lighting control
- **Illuminance Monitoring**: Ambient light level monitoring
- **Darkness Detection**: Automatic darkness detection for lighting activation
- **Timed Control**: Automatic lighting control with timing

### Entry Management
- **Entry Lighting**: Automatic lighting for entry and exit
- **Security Enhancement**: Enhanced security through automated lighting
- **Convenience Features**: Convenient lighting for entry and exit
- **Energy Efficiency**: Energy-efficient lighting control

## Entities

### Motion Sensors
- `binary_sensor.front_door_motion_sensor`: Front door motion detection
  - **Function**: Primary motion detection for front door area
  - **Triggers**: Motion-based automation triggers
  - **Security**: Security monitoring and entry detection

### Illuminance Sensors
- `sensor.garage_entry_motion_sensor_illuminance`: Garage entry illuminance
  - **Function**: Ambient light level monitoring
  - **Threshold**: 100 lux threshold for darkness detection
  - **Integration**: Illuminance-based lighting control

### Lights
- `light.front_door_lights`: Front door lighting control
  - **Function**: Front door area lighting
  - **Control**: Automated on/off control
  - **Integration**: Motion and illuminance-based control

### Custom Attributes
- **Package Identification**: Custom attributes for package management
- **Front Door Metadata**: Front door-specific configuration and identification

## Automations

### Control the Front Door Lights
- **ID**: `304cad1d-c405-4479-9177-2beb93c46cae`
- **Description**: Intelligent front door lighting control based on motion and illuminance
- **Mode**: Restart with silent error handling
- **Triggers**:
  - Home Assistant start event
  - Automation reload event
  - Front door motion sensor activation (off to on)
- **Actions**:
  - **Condition**: Motion detected AND illuminance below 100 lux
  - **Sequence**:
    1. Turn on front door lights
    2. Wait for motion to cease
    3. 1-minute delay
    4. Turn off front door lights
  - **Default**: Turn off front door lights

### Automation Logic
The automation includes sophisticated logic:
- **Motion Detection**: Triggers on motion sensor activation
- **Darkness Detection**: Only activates when ambient light is below 100 lux
- **Timed Control**: Automatic shutdown after motion ceases and delay
- **Error Handling**: Silent error handling for maximum exceeded scenarios
- **Restart Mode**: Restart mode for reliable operation

## Dependencies
- **Motion Sensors**: Motion detection sensor integration
- **Illuminance Sensors**: Ambient light level monitoring
- **Lighting Control**: Front door lighting control integration
- **Template Logic**: Motion and illuminance-based logic
- **Timing Control**: Automatic timing and delay control

## Usage
The front door package provides several interaction methods:
- **Motion Activation**: Automatic lighting activation based on motion
- **Manual Control**: Direct lighting control via switches
- **Dashboard Integration**: Front door status on Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Motion Sensor Setup
- **Front Door Motion**: Front door motion sensor configuration
- **Motion Integration**: Motion detection system integration
- **Trigger Logic**: Motion activation triggers lighting control
- **Response Timing**: Immediate response to motion detection

### Illuminance Monitoring
- **Ambient Light**: Ambient light level monitoring
- **Threshold Configuration**: Darkness detection threshold (100 lux)
- **Integration**: Illuminance-based lighting control
- **Calibration**: Illuminance sensor calibration

### Lighting Control
- **Front Door Lights**: Front door lighting configuration
- **Timing Control**: Automatic timing and delay control
- **Energy Management**: Energy-efficient lighting control
- **Security Integration**: Security enhancement through lighting

## Related Files
- `packages/front_door.yaml`: Main front door package configuration
- `packages/security.yaml`: Security system integration
- `dashboards/home.yaml`: Front door dashboard display

## Notes
- Front door lighting activates only when motion is detected and ambient light is low
- 1-minute delay after motion ceases ensures adequate lighting duration
- Illuminance threshold of 100 lux provides optimal darkness detection
- Restart mode with silent error handling ensures reliable operation
- The package integrates with security system for enhanced security
- Custom attributes store package information for consistent operation
