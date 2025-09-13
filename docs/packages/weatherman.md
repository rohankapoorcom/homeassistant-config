# Weatherman Package Documentation

## Overview
The weatherman package manages advanced weather forecasting and data aggregation for ESPHome Weatherman dashboard devices. This package provides comprehensive weather data processing, forecast aggregation, and data formatting for weather display devices with sophisticated day/night condition logic and multi-timeframe forecasting.

## Configuration Files
- `packages/weatherman.yaml`: Main weatherman configuration

## Functionality
The weatherman package provides:
- **Advanced Weather Forecasting**: Hourly and daily weather forecast processing
- **ESPHome Integration**: Weather data formatting for ESPHome Weatherman devices
- **Multi-Source Data**: Integration of local weather station and PirateWeather data
- **Day/Night Logic**: Intelligent day/night condition detection and mapping
- **Data Aggregation**: Comprehensive weather data aggregation and processing
- **Real-Time Updates**: Minute-by-minute weather data updates

## Key Components

### Weather Data Processing
- **PirateWeather Integration**: Primary weather data source integration
- **Local Weather Station**: Local weather station data integration
- **Forecast Processing**: Hourly and daily forecast data processing
- **Data Aggregation**: Multi-source weather data aggregation

### ESPHome Weatherman Integration
- **Weather Entity**: Comprehensive weather entity for ESPHome devices
- **Data Formatting**: Weather data formatting for ESPHome compatibility
- **Template Processing**: Advanced template processing for weather data
- **Device Communication**: Weather data communication to ESPHome devices

### Day/Night Condition Logic
- **Sun Position**: Sun position-based condition detection
- **Condition Mapping**: Intelligent weather condition mapping
- **Time-Based Logic**: Time-based condition logic for day/night transitions
- **Forecast Processing**: Forecast condition processing with day/night logic

## Entities

### Weather Entity
- `weather.local_weather`: Local weather entity for ESPHome integration
  - **Unique ID**: `33b0c094-0824-4cb6-9104-4d7cacfb7d78`
  - **Temperature**: Local weather station temperature
  - **Apparent Temperature**: Feels-like temperature
  - **Dew Point**: Dew point temperature
  - **Humidity**: Local weather station humidity
  - **Condition**: PirateWeather condition with day/night logic
  - **Forecasts**: Hourly and daily forecast data
  - **Wind Data**: Wind speed, bearing, and gust data
  - **Pressure**: Barometric pressure data
  - **Visibility**: Visibility data
  - **Ozone**: Ozone level data
  - **Cloud Coverage**: Cloud coverage percentage

### Remote Weather Forecast Sensor
- `sensor.local_weather_forecast`: Aggregated weather data for remote Home Assistant instances
  - **State**: Current weather condition from PirateWeather
  - **Daily Forecast**: Daily forecast data from PirateWeather
  - **Hourly Forecast**: Hourly forecast data from PirateWeather
  - **Temperature**: Local weather station outdoor temperature
  - **Humidity**: Local weather station humidity

### Weather Data Sensor
- `sensor.weatherman_data`: Weatherman data aggregation sensor
  - **Unique ID**: `d52ad688-880d-47d2-a30e-5dae145ac073`
  - **State**: "OK" status indicator
  - **Current Conditions**: Current weather condition with day/night logic
  - **Hourly Forecasts**: Multiple hourly forecast data points
  - **Temperature Data**: Temperature data for multiple timeframes
  - **Humidity Data**: Humidity data for multiple timeframes
  - **Precipitation Data**: Precipitation data for multiple timeframes
  - **Timestamp Data**: Formatted timestamp data for multiple timeframes

### Data Sources
- `weather.pirateweather`: PirateWeather weather data source
- `sensor.weather_station_outdoor_temperature`: Local weather station temperature
- `sensor.weather_station_feels_like_temperature`: Local feels-like temperature
- `sensor.weather_station_dewpoint`: Local dew point temperature
- `sensor.weather_station_humidity`: Local humidity data
- `sensor.weather_station_absolute_pressure`: Local barometric pressure

## Template Processing

### Trigger System
- **Time Pattern**: Minute-by-minute updates
- **Home Assistant Start**: Initial data loading on startup
- **Template Reload**: Template reload event handling

### Weather Data Processing
- **Forecast Retrieval**: Hourly and daily forecast data retrieval
- **Variable Processing**: Weather data variable processing
- **Template Logic**: Advanced template logic for data processing

### Day/Night Condition Logic
```yaml
{% if states('sun.sun') == 'below_horizon' %}
    {% if cond_now == 'sunny' %} night {% elif cond_now == 'partlycloudy' %} night-partly-cloudy {% else %} {{ cond_now }} {% endif %}
{% else %}
    {{ cond_now }}
{% endif %}
```

## Dependencies
- **PirateWeather**: Weather data provider integration
- **Local Weather Station**: Local weather station integration
- **ESPHome**: ESPHome Weatherman device integration
- **Template Processing**: Advanced template processing system
- **Sun Integration**: Sun position and astronomical data

## Usage
The weatherman package provides several interaction methods:
- **ESPHome Integration**: Weather data for ESPHome Weatherman devices
- **Dashboard Display**: Weather data on Home Assistant dashboard
- **Forecast Access**: Hourly and daily forecast data access
- **Data Analysis**: Weather data analysis and processing
- **Automation Integration**: Weather-based automation triggers

## Configuration

### Weather Data Sources
- **PirateWeather Setup**: PirateWeather integration configuration
- **Local Weather Station**: Local weather station integration
- **Data Validation**: Weather data validation and error handling
- **Forecast Processing**: Forecast data processing and formatting

### ESPHome Integration
- **Weather Entity**: Weather entity configuration for ESPHome
- **Data Formatting**: Weather data formatting for ESPHome compatibility
- **Template Processing**: Template processing for weather data
- **Device Communication**: Weather data communication configuration

### Day/Night Logic
- **Sun Position**: Sun position detection and processing
- **Condition Mapping**: Weather condition mapping logic
- **Time Processing**: Time-based condition processing
- **Forecast Logic**: Forecast condition processing logic

## Related Files
- `packages/weatherman.yaml`: Main weatherman package configuration
- `packages/weather.yaml`: Basic weather package integration
- `dashboards/home.yaml`: Weather dashboard display

## Notes
- Weather data updates occur every minute for real-time accuracy
- Day/night logic provides intelligent condition mapping
- ESPHome integration enables weather data display on dedicated devices
- Multi-source data integration provides comprehensive weather coverage
- Template processing enables sophisticated weather data manipulation
- The package integrates with ESPHome Weatherman dashboard devices
- Custom attributes store package information for consistent operation
