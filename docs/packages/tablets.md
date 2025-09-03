# Tablets Package Documentation

## Overview
The tablets package manages kiosk tablet interfaces and automation for wall-mounted and mobile tablet devices. This package provides automated tablet maintenance, browser management, and interface optimization for Home Assistant dashboard access.

## Configuration Files
- `packages/tablets.yaml`: Main tablets configuration

## Functionality
The tablets package provides:
- **Kiosk Tablet Management**: Automated management of Fully Kiosk browser instances
- **Browser Maintenance**: Daily browser restart automation for reliability
- **Tablet Optimization**: Interface optimization for wall-mounted tablets
- **Dashboard Access**: Optimized Home Assistant dashboard access
- **Automated Maintenance**: Scheduled maintenance tasks for tablet reliability
- **Interface Management**: Kiosk mode and interface optimization

## Key Components

### Fully Kiosk Integration
- **Browser Management**: Automated browser instance management
- **Restart Automation**: Daily browser restart for reliability
- **Interface Optimization**: Kiosk mode and interface settings
- **Multi-Tablet Support**: Support for multiple tablet devices

### Tablet Maintenance
- **Daily Restart**: Automated daily browser restart at 3:00 AM
- **Reliability Optimization**: Prevents browser freezing and issues
- **Automated Recovery**: Automatic recovery from browser issues
- **Performance Monitoring**: Tablet performance and reliability monitoring

### Interface Optimization
- **Kiosk Mode**: Optimized interface for wall-mounted tablets
- **Dashboard Access**: Streamlined Home Assistant dashboard access
- **Touch Interface**: Optimized touch interface for tablet use
- **Display Management**: Display optimization for different tablet types

## Entities

### Fully Kiosk Entities
- **Browser Restart Buttons**: Fully Kiosk browser restart buttons
  - **Entity Pattern**: `*_restart_browser` entities
  - **Integration**: Fully Kiosk integration entities
  - **Function**: Browser restart functionality

### Tablet Devices
- **Wall-Mounted Tablets**: Fixed position tablet interfaces
- **Mobile Tablets**: Portable tablet devices
- **Kiosk Tablets**: Dedicated kiosk interface tablets

## Automations

### Restart Fully Kiosk Browsers
- **ID**: `f126138c-bb79-4a9c-957a-a727ab53f95f`
- **Description**: Restart all tablets once a day to ensure they don't get stuck
- **Trigger**: Daily at 3:00 AM
- **Actions**:
  - **Entity Selection**: Dynamically selects all Fully Kiosk restart browser entities
  - **Button Press**: Executes restart browser button press for all tablets
  - **Template Logic**: Uses template to find all restart browser entities
- **Mode**: Single execution to prevent multiple restarts

### Automation Logic
The automation uses sophisticated template logic:
- **Integration Entities**: Finds all Fully Kiosk integration entities
- **Entity Filtering**: Filters for entities with `_restart_browser` in entity ID
- **Dynamic Selection**: Automatically adapts to new tablet additions
- **Batch Operation**: Restarts all tablets simultaneously

## Dependencies
- **Fully Kiosk**: Kiosk browser integration
- **Template Logic**: Dynamic entity selection and filtering
- **Time Triggers**: Scheduled automation triggers
- **Button Integration**: Button press automation support

## Usage
The tablets package provides several interaction methods:
- **Automated Maintenance**: Daily browser restart automation
- **Manual Control**: Manual tablet restart capabilities
- **Dashboard Access**: Optimized Home Assistant dashboard access
- **Interface Management**: Kiosk mode and interface optimization
- **Performance Monitoring**: Tablet performance and reliability monitoring

## Configuration

### Fully Kiosk Setup
- **Browser Configuration**: Fully Kiosk browser settings
- **Interface Optimization**: Kiosk mode and display settings
- **Restart Automation**: Automated browser restart configuration
- **Multi-Tablet Support**: Support for multiple tablet devices

### Tablet Optimization
- **Display Settings**: Optimized display settings for different tablet types
- **Touch Interface**: Touch interface optimization
- **Dashboard Access**: Streamlined dashboard access configuration
- **Performance Settings**: Performance optimization settings

### Automation Configuration
- **Restart Schedule**: Daily restart timing configuration
- **Entity Selection**: Dynamic entity selection logic
- **Error Handling**: Error handling and recovery procedures
- **Performance Monitoring**: Performance monitoring and optimization

## Related Files
- `packages/tablets.yaml`: Main tablets package configuration
- `dashboards/home.yaml`: Main dashboard configuration
- `packages/`: Other packages for tablet integration

## Notes
- Daily browser restart occurs at 3:00 AM to minimize disruption
- Automation uses dynamic entity selection to adapt to new tablets
- Fully Kiosk integration provides reliable kiosk browser functionality
- Tablet optimization includes kiosk mode and interface settings
- The package integrates with Home Assistant dashboard system
- Custom attributes store package information for consistent operation
