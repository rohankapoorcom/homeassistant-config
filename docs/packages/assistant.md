# Assistant Package Documentation

## Overview
The assistant package manages Google Assistant integration and voice control capabilities for the Home Assistant system. This package provides comprehensive voice control over lighting, climate, entertainment, and other home automation systems with intelligent entity exposure and alias management.

## Configuration Files
- `packages/assistant.yaml`: Main assistant configuration

## Functionality
The assistant package provides:
- **Google Assistant Integration**: Full Google Assistant voice control integration
- **Entity Exposure Management**: Selective entity exposure for voice control
- **Alias Configuration**: Multiple voice command aliases for entities
- **State Reporting**: Real-time state reporting to Google Assistant
- **Voice Commands**: Natural language voice control for home automation
- **Device Synchronization**: Bidirectional state synchronization

## Key Components

### Google Assistant Integration
- **Project ID**: Google Cloud project configuration
- **Service Account**: Secure service account authentication
- **State Reporting**: Real-time state updates to Google Assistant
- **Entity Configuration**: Selective device exposure and control

### Voice Control Categories
- **Lighting Control**: Comprehensive lighting system voice control
- **Climate Management**: Fan and climate system voice commands
- **Entertainment**: Media and entertainment system control
- **Security**: Security system voice commands
- **Appliances**: Appliance and device control
- **Climate Systems**: HVAC and climate control

### Entity Exposure Strategy
- **Selective Exposure**: Only specific entities exposed for voice control
- **Alias Management**: Multiple voice command aliases per entity
- **Room-Based Organization**: Logical grouping by room and function
- **Security Considerations**: Sensitive devices excluded from voice control

## Entities

### Lighting Control
- `light.master_bedroom_lights`: Master bedroom lighting
- `light.hallway_lights`: Hallway lighting
- `light.kitchen_lights`: Kitchen lighting
- `light.kitchen_cabinet_lights`: Kitchen cabinet lighting
  - **Aliases**: Cabinet Lights, Cabinet Lighting, Cabinets
- `light.sink_accent_lights`: Sink accent lighting
  - **Aliases**: Sink Lights, Sink Lighting
- `light.dining_room_lights`: Dining room lighting
  - **Aliases**: Dining Table Lights, Dining Lights
- `light.living_room_lights`: Living room lighting
- `light.office_lights`: Office lighting
  - **Aliases**: Study Lights
- `light.master_bathroom_lights`: Master bathroom lighting
- `light.backyard_lights`: Backyard lighting
  - **Aliases**: Outdoor Lights, Patio Lights, Balcony Lights
- `light.stairway_lights`: Stairway lighting
  - **Aliases**: Staircase Lights, Stairs
- `light.downstairs_hallway_lights`: Downstairs hallway lighting
  - **Aliases**: Downstairs, Downstairs Lights, Downstairs Hallway Lights
- `light.guest_room_lights`: Guest room lighting
  - **Aliases**: Guest Lights
- `light.gym_lights`: Gym lighting
- `light.garage_lights`: Garage lighting

### Climate Control
- `fan.master_bedroom_fan`: Master bedroom fan
- `fan.living_room_fan`: Living room fan
- `fan.office_fan`: Office fan
  - **Aliases**: Study Fan
- `fan.master_bathroom_fan`: Master bathroom fan
- `fan.gym_fan`: Gym fan
- `climate.downstairs`: Downstairs climate control
- `climate.upstairs`: Upstairs climate control

### Sensors
- `sensor.master_bedroom_temperature`: Master bedroom temperature
- `sensor.office_temperature`: Office temperature

### Window Coverings
- `cover.living_room_curtains`: Living room curtains
- `cover.living_room_sheers`: Living room sheers

### Appliances
- `switch.master_bathroom_towel_warmer`: Master bathroom towel warmer
- `button.standing_desk_preset_1`: Standing desk preset position

### Cleaning
- `vacuum.valetudo_upstairs_vacuum`: Upstairs robot vacuum
- `vacuum.valetudo_downstairs_vacuum`: Downstairs robot vacuum

## Voice Commands

### Lighting Commands
- **Room Lighting**: "Turn on/off [room] lights"
- **Specific Lights**: "Turn on/off cabinet lights", "Turn on/off sink lights"
- **Brightness Control**: "Set [room] lights to [percentage]"
- **Color Control**: "Set [room] lights to [color]"

### Climate Commands
- **Fan Control**: "Turn on/off [room] fan"
- **Fan Speed**: "Set [room] fan to [speed]"
- **Temperature Control**: "Set [room] temperature to [degrees]"
- **Climate Mode**: "Set [room] to [mode]"

### Entertainment Commands
- **Vacuum Control**: "Start/stop upstairs/downstairs vacuum"
- **Vacuum Status**: "What's the status of the vacuum"

### Appliance Commands
- **Towel Warmer**: "Turn on/off towel warmer"
- **Desk Control**: "Activate standing desk preset 1"

## Dependencies
- **Google Assistant**: Google Assistant integration service
- **Google Cloud**: Google Cloud project and service account
- **Secrets Management**: Secure credential storage
- **Entity Integration**: Integration with all exposed entities

## Usage
The assistant package provides several interaction methods:
- **Voice Commands**: Natural language voice control
- **Google Assistant App**: Mobile app voice control
- **Smart Speakers**: Google Home/Nest speaker integration
- **Mobile Devices**: Google Assistant on mobile devices
- **Automation Integration**: Voice commands as automation triggers

## Configuration

### Google Assistant Setup
- **Project ID**: Google Cloud project identifier
- **Service Account**: Secure service account credentials
- **State Reporting**: Real-time state synchronization
- **Entity Configuration**: Selective device exposure

### Entity Exposure
- **Selective Control**: Only specific entities exposed for voice control
- **Alias Management**: Multiple voice command aliases per entity
- **Room Organization**: Logical grouping by room and function
- **Security**: Sensitive devices excluded from voice control

### Voice Command Optimization
- **Natural Language**: Intuitive voice command structure
- **Alias Variety**: Multiple ways to reference the same device
- **Room Context**: Room-based command organization
- **Function Grouping**: Logical grouping of related devices

## Related Files
- `packages/assistant.yaml`: Main assistant package configuration
- `secrets.yaml`: Secure credential storage
- `packages/`: Other packages for entity integration

## Notes
- Google Assistant credentials are stored securely in secrets.yaml
- Only specific entities are exposed for voice control security
- Multiple aliases provide flexible voice command options
- State reporting ensures Google Assistant has current device states
- Voice commands integrate with all other automation packages
- Custom attributes store package information for consistent operation
