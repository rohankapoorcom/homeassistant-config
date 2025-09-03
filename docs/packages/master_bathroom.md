# Master Bathroom Package Documentation

## Overview
The master bathroom package manages comprehensive bathroom automation including lighting control, fan management, humidity monitoring, and scene controls. This package provides intelligent bathroom lighting, humidity-based fan control, motion-activated automation, and Inovelli switch integration for enhanced bathroom comfort and functionality.

## Configuration Files
- `packages/master_bathroom.yaml`: Main master bathroom configuration

## Functionality
The master bathroom package provides:
- **Motion-Activated Lighting**: Intelligent lighting control based on motion detection
- **Humidity-Based Fan Control**: Humidity-based fan automation for moisture control
- **Relative Humidity Monitoring**: Relative humidity monitoring and calculation
- **Scene Controls**: Inovelli switch-based scene control automation
- **Comfort Optimization**: Enhanced bathroom comfort and functionality
- **Energy Management**: Energy-efficient lighting and fan control

## Key Components

### Motion Detection System
- **Motion Sensor**: Master bathroom motion detection
- **Motion-Activated Lighting**: Motion-based lighting automation
- **Timed Control**: Automatic lighting control with timing
- **Energy Efficiency**: Energy-efficient motion-based control

### Humidity Management System
- **Relative Humidity**: Relative humidity calculation and monitoring
- **Humidity-Based Fan Control**: Humidity-based fan automation
- **Moisture Control**: Automated moisture control for bathroom
- **Environmental Monitoring**: Environmental condition monitoring

### Fan Control System
- **Motion-Based Control**: Motion-based fan control
- **Humidity-Based Control**: Humidity-based fan control
- **Timed Operation**: Timed fan operation for moisture control
- **Energy Optimization**: Energy-efficient fan operation

### Scene Control System
- **Inovelli Switch**: VZM31-SN Blue Series switch integration
- **Button Mapping**: Multiple button mapping for different functions
- **Scene Management**: Scene-based automation management
- **Multi-Function Control**: Multiple functions per button

## Entities

### Sensors
- `sensor.master_bathroom_relative_humidity`: Master bathroom relative humidity
  - **Unit**: %
  - **Calculation**: Master bathroom humidity minus upstairs humidity
  - **Function**: Relative humidity monitoring for fan control

### Motion Sensors
- `binary_sensor.master_bathroom_motion`: Master bathroom motion detection
  - **Function**: Motion detection for lighting and fan control
  - **Integration**: Motion-based automation integration
  - **Control**: Motion-activated control system

### Humidity Sensors
- `sensor.master_bathroom_humidity`: Master bathroom humidity
  - **Function**: Absolute humidity monitoring
  - **Integration**: Humidity-based automation integration
  - **Calculation**: Used for relative humidity calculation

- `sensor.upstairs_humidity`: Upstairs humidity
  - **Function**: Upstairs humidity monitoring
  - **Integration**: Relative humidity calculation
  - **Reference**: Reference for relative humidity calculation

### Fan Control
- `fan.master_bathroom_fan`: Master bathroom fan control
  - **Function**: Bathroom fan control
  - **Automation**: Motion and humidity-based automation
  - **Energy**: Energy-efficient fan operation

### Inovelli Switch
- **Device ID**: `d80e98e0621de0822a33348e7e141e8b`
- **Model**: VZM31-SN Blue Series switch
- **Function**: Scene control and bathroom automation
- **Integration**: Multi-function control integration

## Automations

### Control the Master Bathroom Lights
- **ID**: `c9bf0f4b-2f8a-4e9d-a87e-32da42f33608`
- **Description**: Motion-activated bathroom lighting control
- **Blueprint**: `motion_light.yaml`
- **Motion Entity**: `binary_sensor.master_bathroom_motion`
- **Light Target**: `light.master_bathroom_lights`
- **No Motion Wait**: 300 seconds (5 minutes)

### Control the Master Bathroom Fan
- **ID**: `b281c2da-67a2-44b3-a11f-11d763a4ba46`
- **Description**: Motion and humidity-based fan control
- **Mode**: Restart with silent error handling
- **Triggers**:
  - Home Assistant start event
  - Automation reload event
  - Motion sensor activation (off to on)
  - Relative humidity above 20%
- **Actions**:
  - **Condition**: Motion detected OR relative humidity above 20%
  - **Sequence**:
    1. Turn on master bathroom fan
    2. Wait for humidity ≤ 10% AND no motion
    3. 5-minute delay
    4. Turn off master bathroom fan
  - **Default**: Turn off master bathroom fan

### Master Bathroom Light Switch Scene Controls
- **ID**: `e42f4721-966d-4209-b761-b53dcc737935`
- **Description**: Inovelli switch-based scene control
- **Blueprint**: `inovelli-vzm31-sn-blue-series-switch.yaml`
- **Inovelli Switch**: `d80e98e0621de0822a33348e7e141e8b`
- **Button Mapping**: Scene control configuration

### Automation Features
- **Motion Integration**: Motion-based lighting and fan control
- **Humidity Monitoring**: Real-time humidity monitoring and control
- **Timed Operation**: Timed operation for optimal control
- **Energy Optimization**: Energy-efficient operation
- **Multi-Trigger Logic**: Multiple trigger conditions for comprehensive control

## Dependencies
- **Inovelli Switch**: VZM31-SN Blue Series switch integration
- **Custom Blueprints**: Motion light and scene control blueprints
- **Motion Sensors**: Motion detection integration
- **Humidity Sensors**: Humidity monitoring integration
- **Fan Control**: Bathroom fan control integration

## Usage
The master bathroom package provides several interaction methods:
- **Motion Activation**: Automatic lighting and fan activation based on motion
- **Humidity Control**: Automatic fan control based on humidity levels
- **Inovelli Switch**: Physical switch control for bathroom functions
- **Dashboard Control**: Direct control via Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Motion Sensor Setup
- **Motion Detection**: Motion sensor configuration
- **Motion Integration**: Motion-based automation integration
- **Trigger Logic**: Motion activation triggers
- **Response Timing**: Immediate response to motion detection

### Humidity Monitoring Setup
- **Relative Humidity**: Relative humidity calculation configuration
- **Humidity Thresholds**: Humidity threshold configuration
- **Environmental Monitoring**: Environmental condition monitoring
- **Fan Control**: Humidity-based fan control configuration

### Fan Control Setup
- **Motion-Based Control**: Motion-based fan control
- **Humidity-Based Control**: Humidity-based fan control
- **Timed Operation**: Timed fan operation configuration
- **Energy Management**: Energy-efficient fan operation

### Scene Control Setup
- **Inovelli Switch**: VZM31-SN Blue Series switch configuration
- **Button Mapping**: Individual button mapping for different functions
- **Scene Management**: Scene-based automation management
- **Multi-Function Control**: Multiple functions per button

## Related Files
- `packages/master_bathroom.yaml`: Main master bathroom package configuration
- `blueprints/automation/rohankapoorcom/motion_light.yaml`: Motion light blueprint
- `blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`: Inovelli switch blueprint
- `dashboards/home.yaml`: Master bathroom dashboard display

## Notes
- Motion-activated lighting provides 5-minute delay for bathroom use
- Humidity-based fan control ensures proper moisture control
- Relative humidity calculation provides accurate moisture monitoring
- Inovelli switch provides comprehensive bathroom control
- 20% relative humidity threshold triggers fan operation
- 10% relative humidity threshold with no motion stops fan operation
- 5-minute delay ensures adequate moisture control
- The package integrates with other automation packages
- Custom attributes store package information for consistent operation
