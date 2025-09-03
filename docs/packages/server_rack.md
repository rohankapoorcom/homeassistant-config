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

### SNMP Configuration
- **Host**: SNMP UPS host (configured in secrets)
- **Version**: SNMP version 2c
- **Community**: SNMP community string (configured in secrets)
- **Base OID**: Various OIDs for different UPS parameters

## Automations

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
