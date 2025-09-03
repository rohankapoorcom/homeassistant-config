# Weather Package Documentation

## Overview
The weather package manages weather-related entities and automation, providing comprehensive weather monitoring, display, and alert functionality. This package integrates with PirateWeather for weather data and includes e-paper display automation for real-time weather information at exterior doors.

## Configuration Files
- `packages/weather.yaml`: Main weather configuration

## Functionality
The weather package provides:
- **Weather Data Integration**: PirateWeather integration for accurate weather information
- **Template Sensors**: Processed weather data with proper formatting and units
- **E-Paper Display**: Automated weather display on e-paper devices at exterior doors
- **Real-Time Updates**: Regular weather information updates throughout the day
- **Condition Mapping**: Intelligent weather condition mapping for display icons
- **Time-Based Automation**: Weather display automation with time-based conditions

## Key Components

### Weather Data Source
- **PirateWeather Integration**: Primary weather data provider
- **Weather Conditions**: Current weather condition monitoring
- **Temperature Data**: Exterior temperature with precision formatting
- **Humidity Data**: Exterior humidity with percentage formatting

### Template Sensors
- **Exterior Temperature**: Processed temperature data with rounding and units
- **Exterior Humidity**: Processed humidity data with rounding and units
- **Data Processing**: Template-based data processing for consistent formatting

### E-Paper Display System
- **Display Automation**: Automated weather display on e-paper devices
- **Icon Mapping**: Intelligent weather condition to icon mapping
- **Time-Based Updates**: Regular display updates during active hours
- **Formatting**: Professional weather display with temperature and timestamp

### Weather Condition Logic
- **Condition Mapping**: Complex condition mapping for display icons
- **Day/Night Logic**: Automatic day/night condition detection
- **Icon Selection**: Appropriate icon selection based on conditions and time

## Entities

### Sensors
- `sensor.exterior_temperature`: Template sensor for exterior temperature
  - **Source**: `weather.pirateweather` temperature attribute
  - **Formatting**: Rounded to 1 decimal place
  - **Unit**: °F
  - **Device Class**: temperature

- `sensor.exterior_humidity`: Template sensor for exterior humidity
  - **Source**: `weather.pirateweather` humidity attribute
  - **Formatting**: Rounded to 1 decimal place
  - **Unit**: %
  - **Device Class**: humidity

### Weather Integration
- `weather.pirateweather`: Primary weather data source
  - **Provider**: PirateWeather service
  - **Data**: Current conditions, temperature, humidity
  - **Updates**: Real-time weather information

## Automations

### Update ePaper Weather Displays
- **ID**: `1702712886222`
- **Description**: Display external weather on the epaper displays by the exterior doors
- **Trigger**: Time pattern every 15 minutes
- **Conditions**: Active between 7:00 AM and 2:00 AM
- **Actions**:
  - **Display Configuration**: White background, no rotation, 5-minute TTL
  - **Weather Icon**: Dynamic icon selection based on conditions and time
  - **Temperature Display**: Current temperature in red with °F units
  - **Timestamp**: Update time display in black text
  - **Target**: E-paper devices at exterior doors

### Weather Condition Logic
The automation includes sophisticated weather condition mapping:
- **Partly Cloudy**: Maps to 'partly-cloudy' icon
- **Clear Night**: Maps to 'night' icon
- **Day/Night Detection**: Uses sun position for appropriate icon selection
- **Condition Fallback**: Default condition display for unmapped conditions

### Display Features
- **Icon Positioning**: Weather icon positioned at coordinates (42, 5)
- **Temperature Display**: Temperature shown in red at coordinates (76, 105)
- **Timestamp**: Update time shown in black at coordinates (76, 135)
- **Font**: Uses ppb.ttf font for consistent typography
- **Color Scheme**: Black and red color scheme for readability

## Dependencies
- **PirateWeather**: Weather data provider integration
- **E-Paper Integration**: E-paper display device integration
- **Template Sensors**: For weather data processing and formatting
- **Sun Integration**: For day/night condition detection
- **Time Pattern**: For regular automation triggers

## Usage
The weather package provides several interaction methods:
- **Dashboard Display**: Weather information available on Lovelace dashboard
- **E-Paper Displays**: Real-time weather display at exterior doors
- **Template Sensors**: Processed weather data for other automations
- **Voice Commands**: Weather information available through voice assistants
- **Automation Integration**: Weather data available for other automation packages

## Related Files
- `packages/weather.yaml`: Main weather package configuration
- `packages/weatherman.yaml`: Advanced weather forecasting package
- `dashboards/home.yaml`: Main dashboard configuration

## Notes
- Weather updates occur every 15 minutes during active hours (7:00 AM - 2:00 AM)
- E-paper displays use a 5-minute TTL for efficient power management
- Weather condition mapping includes sophisticated day/night logic
- Temperature and humidity data is processed for consistent formatting
- The package integrates with other weather-dependent automations
- Custom attributes store package information for consistent operation
