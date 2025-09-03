# Presence Package Documentation

## Overview
The presence package manages presence detection and location tracking using a combination of motion sensors, door/window sensors, and GPS-based zone tracking. This package provides comprehensive presence detection for home automation triggers and occupancy-based control systems.

## Configuration Files
- `packages/presence.yaml`: Main presence configuration

## Functionality
The presence package provides:
- **Zone-Based Presence**: GPS-based location tracking with defined zones
- **Motion Detection**: Motion sensor integration for indoor presence detection
- **Door/Window Monitoring**: Entry/exit detection via door and window sensors
- **Multi-Zone Support**: Home and work zone definitions
- **Presence Triggers**: Automation triggers based on presence state changes
- **Occupancy Logic**: Intelligent occupancy detection for automation

## Key Components

### Zone Definitions
- **Home Zone**: Primary residence zone with configurable radius
- **Work Zone**: Secondary location zone for work presence
- **GPS Tracking**: Location-based presence detection
- **Radius Configuration**: Customizable zone boundaries

### Presence Detection Methods
- **GPS Location**: Mobile device GPS tracking for zone-based presence
- **Motion Sensors**: Indoor motion detection for room-level presence
- **Door Sensors**: Entry/exit detection via door state monitoring
- **Window Sensors**: Additional entry point monitoring

### Zone Configuration
- **Home Zone**: 12-meter radius around home location
- **Work Zone**: 250-meter radius around work location
- **Coordinate Storage**: Secure latitude/longitude storage
- **Custom Attributes**: Package identification and zone metadata

## Entities

### Zones
- `zone.home`: Primary residence zone
  - **Radius**: 12 meters
  - **Location**: Home coordinates (latitude/longitude)
  - **Purpose**: Home presence detection

- `zone.work`: Work location zone
  - **Radius**: 250 meters
  - **Location**: Work coordinates (latitude/longitude)
  - **Purpose**: Work presence detection

### Custom Attributes
- **Package Identification**: Custom attributes for package management
- **Zone Metadata**: Zone-specific configuration and identification
- **Coordinate Storage**: Secure location coordinate storage

## Automations

### Presence-Based Triggers
The presence package provides foundation for various presence-based automations:
- **Home Arrival**: Triggers when entering home zone
- **Home Departure**: Triggers when leaving home zone
- **Work Arrival**: Triggers when entering work zone
- **Work Departure**: Triggers when leaving work zone
- **Occupancy Changes**: Room-level occupancy detection

### Integration with Other Packages
- **Security Package**: Presence-based security system activation
- **Lighting Packages**: Occupancy-based lighting control
- **Climate Control**: Presence-based climate adjustments
- **Entertainment**: Presence-based entertainment system control

## Dependencies
- **GPS Tracking**: Mobile device GPS integration
- **Motion Sensors**: Indoor motion detection sensors
- **Door/Window Sensors**: Entry point monitoring sensors
- **Secrets Management**: Secure coordinate storage
- **Zone Integration**: Home Assistant zone system

## Usage
The presence package provides several interaction methods:
- **Zone Tracking**: GPS-based location tracking
- **Motion Detection**: Indoor presence via motion sensors
- **Entry Detection**: Door/window sensor monitoring
- **Automation Triggers**: Presence-based automation activation
- **Occupancy Logic**: Intelligent occupancy detection

## Configuration

### Zone Setup
- **Home Coordinates**: Secure storage of home latitude/longitude
- **Work Coordinates**: Secure storage of work latitude/longitude
- **Zone Radii**: Configurable zone boundary definitions
- **Custom Attributes**: Package-specific configuration

### GPS Integration
- **Mobile App**: Home Assistant mobile app GPS tracking
- **Location Updates**: Regular location update intervals
- **Zone Detection**: Automatic zone entry/exit detection
- **Battery Optimization**: GPS power management

### Sensor Integration
- **Motion Sensors**: Indoor motion detection integration
- **Door Sensors**: Entry point monitoring
- **Window Sensors**: Additional entry point detection
- **Sensor Logic**: Multi-sensor presence detection algorithms

## Related Files
- `packages/presence.yaml`: Main presence package configuration
- `secrets.yaml`: Secure coordinate storage
- `packages/security.yaml`: Security system integration
- `packages/office.yaml`: Office automation integration

## Notes
- Zone coordinates are stored securely in secrets.yaml
- Presence detection uses multiple methods for reliability
- Zone radii are optimized for typical usage patterns
- The package integrates with other automation packages
- GPS tracking includes battery optimization features
- Custom attributes store package information for consistent operation
