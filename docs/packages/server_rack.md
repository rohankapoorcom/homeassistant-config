# Server Rack Package Documentation

## Overview
The server rack package manages comprehensive server infrastructure monitoring and automation including UPS monitoring, environmental monitoring, and infrastructure management. This package provides real-time UPS monitoring, environmental monitoring, and automated infrastructure management for enhanced server rack reliability and performance.

## Configuration Files
- `packages/server_rack.yaml`: Main server rack configuration

## Functionality
The server rack package provides:
- **UPS Monitoring**: Comprehensive UPS monitoring and management
- **Environmental Monitoring**: Temperature and humidity monitoring
- **Infrastructure Management**: Automated infrastructure management
- **SNMP Integration**: SNMP-based device monitoring
- **Real-Time Monitoring**: Real-time infrastructure monitoring
- **Alert System**: Automated alert system for infrastructure issues

## Key Components

### UPS Monitoring System
- **Battery Monitoring**: Real-time UPS battery monitoring
- **Temperature Monitoring**: UPS battery and environmental temperature
- **Voltage Monitoring**: UPS battery and output voltage monitoring
- **Load Monitoring**: UPS load monitoring and management
- **Runtime Monitoring**: UPS runtime remaining monitoring

### Environmental Monitoring
- **Temperature Monitoring**: UPS EnviroSense temperature monitoring
- **Humidity Monitoring**: UPS EnviroSense humidity monitoring
- **Environmental Alerts**: Environmental condition alerts
- **Climate Control**: Automated climate control for server rack

### SNMP Integration
- **SNMP Monitoring**: SNMP-based device monitoring
- **OID Management**: SNMP OID management and monitoring
- **Data Collection**: Real-time data collection via SNMP
- **Device Communication**: SNMP device communication

### Infrastructure Management
- **Server Monitoring**: Server infrastructure monitoring
- **Performance Tracking**: Performance tracking and optimization
- **Alert Management**: Automated alert management
- **Maintenance Tracking**: Infrastructure maintenance tracking

## Entities

### UPS Sensors
- `sensor.ups_battery_temperature`: UPS battery temperature
  - **Unit**: °F
  - **OID**: .1.3.6.1.4.1.850.1.1.3.1.2.1.1.8.1
  - **Function**: Battery temperature monitoring

- `sensor.ups_envirosense_temperature`: UPS EnviroSense temperature
  - **Unit**: °F
  - **OID**: .1.3.6.1.4.1.850.1.1.3.3.3.1.1.2.2
  - **Function**: Environmental temperature monitoring

- `sensor.ups_envirosense_humidity`: UPS EnviroSense humidity
  - **Unit**: %
  - **OID**: .1.3.6.1.4.1.850.1.1.3.3.3.2.1.1.2
  - **Function**: Environmental humidity monitoring

- `sensor.ups_battery_voltage`: UPS battery voltage
  - **Unit**: V
  - **OID**: .1.3.6.1.2.1.33.1.2.5.0
  - **Function**: Battery voltage monitoring

- `sensor.ups_battery_capacity`: UPS battery capacity
  - **Unit**: %
  - **OID**: .1.3.6.1.2.1.33.1.2.4.0
  - **Function**: Battery capacity monitoring

- `sensor.ups_runtime_remaining`: UPS runtime remaining
  - **Unit**: minutes
  - **OID**: .1.3.6.1.2.1.33.1.2.3.0
  - **Function**: Runtime remaining monitoring

- `sensor.ups_ac_input_voltage`: UPS AC input voltage
  - **Unit**: V
  - **OID**: .1.3.6.1.2.1.33.1.3.3.1.3.1
  - **Function**: AC input voltage monitoring

- `sensor.ups_output_voltage`: UPS output voltage
  - **Unit**: V
  - **OID**: .1.3.6.1.2.1.33.1.4.4.1.2.1
  - **Function**: Output voltage monitoring

- `sensor.ups_load`: UPS load
  - **Unit**: %
  - **OID**: .1.3.6.1.4.1.850.1.1.3.1.3.3.2.1.5.1.1
  - **Function**: Load monitoring

### Template Sensors
- `sensor.server_rack_backup_time_remaining`: Server rack backup time remaining
  - **Unit**: minutes
  - **Function**: Calculated runtime based on charging/discharging state
  - **Dynamic Attributes**: Friendly name changes based on charging state

- `sensor.server_rack_backup_power_source`: Server rack backup power source
  - **Function**: Dynamic power source detection
  - **States**: AC/DC Input, AC Input, DC Input, Battery
  - **Logic**: Determines power source based on AC and DC input states

### SNMP Configuration
- **Host**: SNMP UPS host (configured in secrets)
- **Version**: SNMP version 2c
- **Community**: SNMP community string (configured in secrets)
- **Base OID**: Various OIDs for different UPS parameters

## Automations

### Update Server Rack Status Display
- **ID**: `1701157132714`
- **Description**: Display server rack climate controls status on the epaper displays
- **Functionality**:
  - Updates e-paper display with current temperature and humidity
  - Shows target temperature and fan speed settings
  - Displays climate control status with visual indicators
  - Includes timestamp for status reference
- **Trigger**: Time pattern (every 10 minutes)
- **Mode**: Restart

### Server Rack Battery Power Alert
- **ID**: `2c8ca4d5-b0e5-48c9-9a6d-a3cd60d2a449`
- **Description**: Notifies when server rack switches to battery power for more than 10 minutes. Monitors server rack backup and UPS power source sensors.
- **Functionality**:
  - Monitors both server rack backup and UPS power source sensors
  - Sends dynamic alert messages identifying which system(s) are on battery power
  - Provides comprehensive battery status information
  - Includes safety checks to prevent false notifications
- **Triggers**:
  - Server rack backup power source switches to 'Battery' for 10+ minutes
  - UPS source switches to 'Battery' for 10+ minutes
- **Conditions**:
  - Safety check: Verify at least one sensor is on battery power to prevent false notifications
- **Actions**:
  - Sends notification via `notify.rohan_kapoor` service
  - Dynamic alert message with comprehensive battery information
- **Mode**: Single

### Server Rack Exhaust Fan Max Speed Control
- **ID**: `319350f9-c4b6-4030-ba68-e975b926828f`
- **Description**: Automatically adjusts the max fan speed based on temperature difference. Sets max speed to 100% when temperature difference exceeds 8°F, otherwise 85%.
- **Functionality**:
  - Monitors current temperature and target temperature from thermostat
  - Calculates temperature difference dynamically
  - Adjusts fan max speed based on temperature conditions
  - Provides immediate response to temperature changes
  - Ensures eventual consistency with startup triggers
- **Triggers**:
  - Home Assistant startup (`homeassistant.start`)
  - Automation reload (`automation_reloaded`)
  - Current temperature sensor state changes
  - Thermostat target temperature attribute changes
- **Conditions**:
  - Safety check: Verify both temperature sensors are available before adjusting fan speed
- **Actions**:
  - Calculates temperature difference (current - target)
  - Sets max fan speed to 100% if difference > 8°F
  - Sets max fan speed to 85% if difference ≤ 8°F
- **Mode**: Restart
- **Entities Used**:
  - `sensor.server_rack_exhaust_fan_temperature_1`: Current temperature reading
  - `climate.server_rack_exhaust_fan_fan_1_thermostat`: Thermostat with target temperature
  - `number.server_rack_exhaust_fan_fan_1_max_fan_speed`: Fan max speed control

### Infrastructure Monitoring
The package provides comprehensive infrastructure monitoring through:
- **Real-Time Monitoring**: Real-time UPS and environmental monitoring
- **Alert Management**: Automated alert management for infrastructure issues
- **Performance Tracking**: Performance tracking and optimization
- **Maintenance Tracking**: Infrastructure maintenance tracking

### Environmental Management
- **Temperature Monitoring**: Real-time temperature monitoring
- **Humidity Monitoring**: Real-time humidity monitoring
- **Environmental Alerts**: Environmental condition alerts
- **Climate Control**: Automated climate control for server rack

### UPS Management
- **Battery Monitoring**: Real-time battery monitoring
- **Load Monitoring**: Real-time load monitoring
- **Runtime Monitoring**: Runtime remaining monitoring
- **Voltage Monitoring**: Voltage monitoring and alerts

## Dependencies
- **SNMP Integration**: SNMP-based device monitoring
- **UPS Integration**: UPS device integration
- **Environmental Monitoring**: Environmental monitoring system
- **Alert System**: Automated alert system
- **Infrastructure Management**: Infrastructure management system

## Usage
The server rack package provides several interaction methods:
- **Real-Time Monitoring**: Real-time infrastructure monitoring
- **Alert Management**: Automated alert management
- **Dashboard Integration**: Server rack status on Home Assistant dashboard
- **Performance Tracking**: Performance tracking and optimization
- **Maintenance Tracking**: Infrastructure maintenance tracking
- **Environmental Control**: Environmental monitoring and control

## Configuration

### SNMP Setup
- **Host Configuration**: SNMP host configuration in secrets
- **Community String**: SNMP community string configuration
- **OID Management**: SNMP OID management and monitoring
- **Data Collection**: Real-time data collection configuration

### UPS Monitoring Setup
- **Battery Monitoring**: Battery monitoring configuration
- **Temperature Monitoring**: Temperature monitoring configuration
- **Voltage Monitoring**: Voltage monitoring configuration
- **Load Monitoring**: Load monitoring configuration

### Environmental Monitoring Setup
- **Temperature Monitoring**: Environmental temperature monitoring
- **Humidity Monitoring**: Environmental humidity monitoring
- **Alert Configuration**: Environmental alert configuration
- **Climate Control**: Automated climate control configuration

### Infrastructure Management Setup
- **Server Monitoring**: Server infrastructure monitoring
- **Performance Tracking**: Performance tracking configuration
- **Alert Management**: Automated alert management configuration
- **Maintenance Tracking**: Infrastructure maintenance tracking

## Related Files
- `packages/server_rack.yaml`: Main server rack package configuration
- `secrets.yaml`: SNMP credentials and configuration
- `dashboards/home.yaml`: Server rack dashboard display

## Notes
- SNMP integration provides comprehensive UPS monitoring
- Real-time monitoring ensures infrastructure reliability
- Environmental monitoring protects server infrastructure
- Automated alerts provide early warning of infrastructure issues
- Performance tracking enables infrastructure optimization
- The package integrates with notification system for alerts
- Custom attributes store package information for consistent operation
