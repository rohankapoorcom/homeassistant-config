# Stairway Package Documentation

## Overview
The stairway package manages comprehensive stairway automation including lighting control, area-based lighting monitoring, and safety features. This package provides intelligent stairway lighting, multi-area lighting state monitoring, and automated lighting control for enhanced stairway safety and convenience.

## Configuration Files
- `packages/stairway.yaml`: Main stairway configuration

## Functionality
The stairway package provides:
- **Area-Based Lighting Monitoring**: Comprehensive lighting state monitoring across multiple areas
- **Stairway Safety**: Enhanced stairway safety through intelligent lighting
- **Multi-Area Integration**: Integration with downstairs and upstairs areas
- **Lighting State Tracking**: Real-time lighting state tracking and monitoring
- **Safety Automation**: Automated safety features for stairway use
- **Energy Management**: Energy-efficient lighting control and monitoring

## Key Components

### Area-Based Lighting Monitoring
- **Downstairs Monitoring**: Comprehensive downstairs area lighting monitoring
- **Upstairs Monitoring**: Comprehensive upstairs area lighting monitoring
- **Multi-Area Integration**: Integration with multiple home areas
- **State Tracking**: Real-time lighting state tracking

### Stairway Safety System
- **Safety Lighting**: Enhanced stairway safety through intelligent lighting
- **Area Integration**: Integration with all home areas for comprehensive monitoring
- **State Detection**: Intelligent state detection for lighting conditions
- **Safety Automation**: Automated safety features

### Multi-Area Integration
- **Downstairs Areas**: Downstairs bathroom, hallway, garage, guest room, gym
- **Upstairs Areas**: Hallway, hallway bathroom, living room, kitchen
- **Comprehensive Coverage**: Complete home area coverage
- **State Aggregation**: Aggregated lighting state monitoring

### Lighting State Tracking
- **Real-Time Monitoring**: Real-time lighting state monitoring
- **State Aggregation**: Aggregated state tracking across areas
- **Condition Detection**: Intelligent condition detection
- **State Reporting**: Comprehensive state reporting

## Entities

### Binary Sensors
- `binary_sensor.downstairs_lights_on`: Downstairs lights on detection
  - **Function**: Detects when stairway and downstairs hallway lights are on
  - **Logic**: Both stairway and downstairs hallway lights must be on
  - **Integration**: Stairway safety integration

- `binary_sensor.downstairs_lights_off`: Downstairs lights off detection
  - **Function**: Detects when all downstairs area lights are off
  - **Areas**: Downstairs bathroom, hallway, garage, guest room, gym
  - **Logic**: Counts all lights in downstairs areas and detects when count is 0

- `binary_sensor.upstairs_lights_on`: Upstairs lights on detection
  - **Function**: Detects when hallway and kitchen cabinet lights are on
  - **Logic**: Both hallway and kitchen cabinet lights must be on
  - **Integration**: Stairway safety integration

- `binary_sensor.upstairs_lights_off`: Upstairs lights off detection
  - **Function**: Detects when all upstairs area lights are off
  - **Areas**: Hallway, hallway bathroom, living room, kitchen
  - **Logic**: Counts all lights in upstairs areas and detects when count is 0

### Template Logic
The package uses sophisticated template logic for area-based monitoring:
- **Area Entity Expansion**: Expands all entities in specific areas
- **State Filtering**: Filters entities by state (on/off)
- **Count Aggregation**: Counts filtered entities
- **Condition Detection**: Detects specific lighting conditions

## Automations

### Stairway Safety Features
The package provides comprehensive stairway safety through:
- **Area Monitoring**: Real-time monitoring of all home areas
- **State Detection**: Intelligent detection of lighting states
- **Safety Integration**: Integration with stairway safety features
- **Condition Reporting**: Comprehensive condition reporting

### Multi-Area Integration
- **Downstairs Integration**: Integration with all downstairs areas
- **Upstairs Integration**: Integration with all upstairs areas
- **Comprehensive Coverage**: Complete home area coverage
- **State Aggregation**: Aggregated state monitoring

### Lighting State Tracking
- **Real-Time Monitoring**: Real-time lighting state monitoring
- **State Aggregation**: Aggregated state tracking across areas
- **Condition Detection**: Intelligent condition detection
- **State Reporting**: Comprehensive state reporting

## Dependencies
- **Area Integration**: Home Assistant area system integration
- **Template Sensors**: Complex template sensor logic
- **State Monitoring**: Real-time state monitoring system
- **Multi-Area Logic**: Multi-area lighting state logic
- **Safety Integration**: Stairway safety system integration

## Usage
The stairway package provides several interaction methods:
- **Area Monitoring**: Real-time monitoring of all home areas
- **Safety Integration**: Integration with stairway safety features
- **State Tracking**: Comprehensive lighting state tracking
- **Dashboard Integration**: Stairway status on Home Assistant dashboard
- **Automation Integration**: Integration with other automation packages
- **Safety Features**: Enhanced stairway safety features

## Configuration

### Area Monitoring Setup
- **Area Definition**: Definition of downstairs and upstairs areas
- **Entity Integration**: Integration with all area entities
- **State Monitoring**: Real-time state monitoring configuration
- **Condition Detection**: Intelligent condition detection setup

### Safety Integration Setup
- **Safety Features**: Stairway safety feature configuration
- **Area Integration**: Integration with all home areas
- **State Detection**: Intelligent state detection configuration
- **Safety Automation**: Automated safety feature setup

### Multi-Area Logic Setup
- **Area Coverage**: Complete home area coverage configuration
- **State Aggregation**: Aggregated state monitoring setup
- **Condition Detection**: Intelligent condition detection configuration
- **State Reporting**: Comprehensive state reporting setup

## Related Files
- `packages/stairway.yaml`: Main stairway package configuration
- `packages/`: Other packages for area integration
- `dashboards/home.yaml`: Stairway dashboard display

## Notes
- Area-based monitoring provides comprehensive home lighting state tracking
- Template logic enables sophisticated state detection across multiple areas
- Multi-area integration ensures complete home coverage
- Safety features enhance stairway safety through intelligent lighting
- State aggregation provides comprehensive lighting condition reporting
- The package integrates with all other area-based automation packages
- Custom attributes store package information for consistent operation
