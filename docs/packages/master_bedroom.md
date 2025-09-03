# Master Bedroom Package Documentation

## Overview
The master bedroom package manages comprehensive automation and configuration for the master bedroom, including lighting, climate control, entertainment systems, and comfort features. This package provides a complete bedroom automation solution with intelligent lighting, fan control, TV automation, and sleep environment optimization.

## Configuration Files
- `packages/master_bedroom.yaml`: Main master bedroom configuration

## Functionality
The master bedroom package provides:
- **Intelligent Lighting**: Multi-zone lighting with adaptive brightness and color temperature control
- **Climate Control**: Ceiling fan with percentage-based speed control and temperature monitoring
- **Entertainment Automation**: TV and audio system control with multiple source options
- **Sleep Environment**: Optimized lighting and climate for sleep quality
- **Occupancy-Based Control**: Intelligent automation based on room occupancy
- **Comfort Features**: Automated comfort adjustments based on time and conditions

## Key Components

### Lighting System
- **Main Bedroom Lights**: Primary lighting with adaptive brightness control
- **Fan Light**: Integrated fan light with template-based fan control
- **Adaptive Lighting**: Automatic color temperature and brightness adjustments
- **Occupancy Control**: Motion-based lighting automation

### Climate Control
- **Ceiling Fan**: Template-based fan with percentage control (0-100%)
- **Temperature Monitoring**: Real-time temperature tracking
- **Speed Control**: 3-speed fan operation with precise percentage control
- **Comfort Optimization**: Automated climate adjustments for sleep

### Entertainment System
- **TV Control**: Master bedroom TV with multiple source options
- **Audio System**: Denon AVR Zone 2 integration
- **Source Management**: HDMI source switching and audio routing
- **Media Devices**: Shield TV and Apple TV integration

### Sleep Environment
- **Sleep Mode**: Optimized lighting and climate for sleep
- **Wake Mode**: Gradual lighting and climate adjustments for waking
- **Comfort Automation**: Automated comfort adjustments based on conditions

## Entities

### Fans
- `fan.master_bedroom_fan`: Template fan with percentage-based control
  - **Speed Count**: 3 speeds
  - **Percentage Template**: Converts brightness to fan percentage (0-100%)
  - **Control**: On/off and percentage-based speed control

### Scripts
- `script.turn_on_watch_master_bedroom_tv`: Activates TV with Shield TV source
- `script.turn_on_watch_master_bedroom_apple_tv`: Activates TV with Apple TV source

### Custom Attributes
- **Master Bedroom Light Switch Device ID**: Z-Wave device identifier for lighting control
- **Package Identification**: Custom attributes for package management

## Automations

### Lighting Control
- **Adaptive Lighting Integration**: Automatic color temperature and brightness adjustments
- **Occupancy-Based Control**: Motion-activated lighting with intelligent timing
- **Sleep Mode Lighting**: Optimized lighting for sleep environment
- **Wake Mode Lighting**: Gradual lighting adjustments for morning routine

### Fan Control
- **Percentage-Based Speed**: Precise fan speed control (0-100%)
- **Temperature-Based Operation**: Automatic fan operation based on temperature
- **Comfort Optimization**: Automated fan adjustments for optimal comfort
- **Sleep Mode Fan**: Reduced fan operation during sleep hours

### Entertainment Automation
- **TV Source Switching**: Automatic source selection for different media devices
- **Audio Routing**: Coordinated audio system control
- **Device Synchronization**: Synchronized operation of TV, audio, and media devices
- **Activity-Based Control**: Entertainment system activation based on activities

### Sleep Environment
- **Sleep Mode Activation**: Automatic sleep environment optimization
- **Wake Mode Activation**: Gradual environment adjustments for waking
- **Comfort Monitoring**: Continuous comfort optimization based on conditions
- **Occupancy Integration**: Sleep environment adjustments based on occupancy

## Dependencies
- **Template Fan**: For ceiling fan control and percentage-based operation
- **Adaptive Lighting**: For automatic lighting adjustments
- **Denon AVR**: For audio system control and source switching
- **Android TV**: For Shield TV integration and control
- **Apple TV**: For Apple TV integration and media control
- **Z-Wave JS**: For Z-Wave device communication and control

## Usage
The master bedroom package provides several interaction methods:
- **Dashboard Controls**: Direct control via Lovelace dashboard
- **Voice Commands**: Integration with voice assistants for hands-free control
- **Automation Triggers**: Occupancy and time-based automatic control
- **Manual Controls**: Physical switches and remote controls
- **Script Execution**: Direct script execution for entertainment system control

## Related Files
- `packages/master_bedroom.yaml`: Main master bedroom package configuration
- `dashboards/home.yaml`: Main dashboard configuration
- `blueprints/automation/rohankapoorcom/`: Custom automation blueprints

## Notes
- The fan control uses a template-based approach with percentage conversion from brightness
- Entertainment automation includes multiple source options for different media preferences
- Sleep environment optimization considers both lighting and climate factors
- Occupancy-based control includes intelligent timing to prevent rapid on/off cycling
- The package integrates with adaptive lighting for optimal color temperature and brightness
- Custom attributes store device IDs and package information for consistent operation
