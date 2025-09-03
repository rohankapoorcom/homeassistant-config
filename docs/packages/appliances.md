# Appliances Package Documentation

## Overview
The appliances package manages household appliances and their automation, providing intelligent control and monitoring for various home appliances. This package includes motion-activated appliance control, energy management, and automated appliance operation based on occupancy and usage patterns.

## Configuration Files
- `packages/appliances.yaml`: Main appliances configuration

## Functionality
The appliances package provides:
- **Motion-Activated Control**: Appliance activation based on motion detection
- **Energy Management**: Intelligent energy usage optimization
- **Occupancy-Based Operation**: Appliance operation based on room occupancy
- **Hot Water Management**: Automated hot water pump control
- **Appliance Monitoring**: Real-time appliance status monitoring
- **Efficiency Optimization**: Automated efficiency improvements

## Key Components

### Hot Water System
- **Hot Water Pump**: Automated hot water pump control
- **Motion Activation**: Motion-based pump activation
- **Bathroom Integration**: Integration with bathroom motion sensors
- **Kitchen Integration**: Kitchen motion sensor integration
- **Energy Efficiency**: Optimized hot water delivery

### Motion Detection Integration
- **Multi-Room Motion**: Motion sensors across multiple rooms
- **Bathroom Motion**: Master bathroom, hallway bathroom, downstairs bathroom
- **Kitchen Motion**: Kitchen motion sensor integration
- **Occupancy Logic**: Intelligent occupancy-based appliance control

### Appliance Management
- **Switch Control**: Automated appliance switch control
- **Status Monitoring**: Real-time appliance status monitoring
- **Energy Optimization**: Energy usage optimization
- **Maintenance Alerts**: Appliance maintenance and status alerts

## Entities

### Switches
- `switch.hot_water_pump`: Hot water pump control
  - **Function**: Hot water circulation pump
  - **Control**: Automated on/off control
  - **Integration**: Motion sensor integration

### Motion Sensors
- `binary_sensor.master_bathroom_motion`: Master bathroom motion detection
- `binary_sensor.hallway_bathroom_motion`: Hallway bathroom motion detection
- `binary_sensor.downstairs_bathroom_motion`: Downstairs bathroom motion detection
- `binary_sensor.kitchen_motion`: Kitchen motion detection

### Custom Attributes
- **Package Identification**: Custom attributes for package management
- **Appliance Metadata**: Appliance-specific configuration and identification

## Automations

### Turn on the Hot Water Pump when there is motion in any of the bathrooms
- **ID**: `22220e6d-5b70-4718-8a3c-7080f270f928`
- **Description**: Activates hot water pump when motion is detected in bathrooms or kitchen
- **Triggers**: Motion sensor state changes from 'off' to 'on'
- **Motion Sensors**:
  - Master bathroom motion sensor
  - Hallway bathroom motion sensor
  - Downstairs bathroom motion sensor
  - Kitchen motion sensor
- **Actions**: Turns on hot water pump switch
- **Logic**: Any motion in bathrooms or kitchen activates hot water pump

### Automation Features
- **Multi-Sensor Integration**: Monitors multiple motion sensors simultaneously
- **State Change Detection**: Triggers on motion sensor activation
- **Immediate Response**: Instant hot water pump activation
- **Energy Efficiency**: Provides hot water only when needed

## Dependencies
- **Motion Sensors**: Motion detection sensor integration
- **Switch Control**: Appliance switch control integration
- **Multi-Room Integration**: Integration with bathroom and kitchen packages
- **Energy Management**: Energy optimization and monitoring

## Usage
The appliances package provides several interaction methods:
- **Motion Activation**: Automatic appliance activation based on motion
- **Manual Control**: Direct appliance control via switches
- **Dashboard Integration**: Appliance status on Home Assistant dashboard
- **Voice Commands**: Voice control integration via assistant package
- **Automation Integration**: Integration with other automation packages

## Configuration

### Motion Sensor Setup
- **Multi-Room Coverage**: Motion sensors in bathrooms and kitchen
- **Sensor Integration**: Integration with motion detection system
- **Trigger Logic**: Motion activation triggers appliance control
- **Response Timing**: Immediate response to motion detection

### Appliance Control
- **Switch Integration**: Direct switch control for appliances
- **Status Monitoring**: Real-time appliance status monitoring
- **Energy Management**: Energy usage optimization
- **Maintenance Alerts**: Appliance maintenance notifications

### Automation Configuration
- **Motion Triggers**: Motion sensor state change triggers
- **Multi-Sensor Logic**: Logic for multiple sensor integration
- **Response Actions**: Automated appliance activation
- **Energy Optimization**: Energy efficiency considerations

## Related Files
- `packages/appliances.yaml`: Main appliances package configuration
- `packages/master_bathroom.yaml`: Master bathroom integration
- `packages/hallway_bathroom.yaml`: Hallway bathroom integration
- `packages/downstairs_bathroom.yaml`: Downstairs bathroom integration
- `packages/kitchen/`: Kitchen integration

## Notes
- Hot water pump activation is based on motion detection for energy efficiency
- Multiple motion sensors provide comprehensive coverage
- Appliance control integrates with motion detection system
- Energy optimization reduces unnecessary appliance operation
- The package integrates with bathroom and kitchen automation packages
- Custom attributes store package information for consistent operation
