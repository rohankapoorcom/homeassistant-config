# Air Quality Package Documentation

## Overview
The air quality package manages comprehensive air quality monitoring and US Air Quality Index (AQI) calculations across multiple rooms. This package provides real-time air quality monitoring, AQI calculations based on PM2.5 levels, and multi-room air quality tracking for health and comfort optimization.

## Configuration Files
- `packages/air_quality.yaml`: Main air quality configuration

## Functionality
The air quality package provides:
- **US AQI Calculation**: Real-time US Air Quality Index calculations
- **Multi-Room Monitoring**: Air quality monitoring across multiple rooms
- **PM2.5 Integration**: PM2.5 sensor integration for air quality assessment
- **Health Monitoring**: Air quality health impact monitoring
- **Alert System**: Air quality alerts and notifications
- **Data Processing**: Complex AQI calculation algorithms

## Key Components

### US AQI Calculation System
- **PM2.5 Integration**: PM2.5 sensor data integration
- **AQI Algorithm**: US EPA AQI calculation algorithm
- **Range Classification**: AQI range classification and categorization
- **Invalid Data Handling**: Invalid data detection and handling

### Multi-Room Air Quality Monitoring
- **Master Bedroom**: Master bedroom air quality monitoring
- **Living Room**: Living room air quality monitoring
- **Guest Room**: Guest room air quality monitoring
- **Downstairs Hallway**: Downstairs hallway air quality monitoring
- **Comprehensive Coverage**: Full home air quality coverage

### AQI Calculation Algorithm
- **EPA Standards**: US Environmental Protection Agency standards
- **Range-Based Calculation**: AQI calculation based on PM2.5 ranges
- **Macro Functions**: Reusable calculation macro functions
- **Precision Handling**: Precise AQI calculation with rounding

## Entities

### Air Quality Sensors
- `sensor.master_bedroom_us_air_quality_index`: Master bedroom US AQI
  - **Unique ID**: `e940b6f3-da35-4600-8fd6-8016debd5218`
  - **Device Class**: aqi
  - **Source**: `sensor.master_bedroom_air_quality_pm2_5`

- `sensor.living_room_us_air_quality_index`: Living room US AQI
  - **Unique ID**: `e232af2c-99c4-480d-a5cf-79ab5e4b8e1d`
  - **Device Class**: aqi
  - **Source**: `sensor.living_room_air_quality_pm2_5`

- `sensor.guest_room_us_air_quality_index`: Guest room US AQI
  - **Unique ID**: `dcaca7bf-568b-42ba-b9c6-4edb3fdd8cdd`
  - **Device Class**: aqi
  - **Source**: `sensor.guest_room_air_quality_pm2_5`

- `sensor.downstairs_hallway_us_air_quality_index`: Downstairs hallway US AQI
  - **Unique ID**: `f9695676-bdbf-48e7-ba93-feadf9ec54eb`
  - **Device Class**: aqi
  - **Source**: `sensor.downstairs_hallway_air_quality_pm2_5`

### Source PM2.5 Sensors
- `sensor.master_bedroom_air_quality_pm2_5`: Master bedroom PM2.5
- `sensor.living_room_air_quality_pm2_5`: Living room PM2.5
- `sensor.guest_room_air_quality_pm2_5`: Guest room PM2.5
- `sensor.downstairs_hallway_air_quality_pm2_5`: Downstairs hallway PM2.5

## AQI Calculation Algorithm

### AQI Ranges and Categories
The package implements the US EPA AQI calculation with the following ranges:

| PM2.5 Range (μg/m³) | AQI Range | Category | Health Impact |
|---------------------|-----------|----------|---------------|
| 0.0 - 12.0 | 0 - 50 | Good | Minimal impact |
| 12.1 - 35.4 | 51 - 100 | Moderate | Some concern for sensitive groups |
| 35.5 - 55.4 | 101 - 150 | Unhealthy for Sensitive Groups | Increased concern for sensitive groups |
| 55.5 - 150.4 | 151 - 200 | Unhealthy | Everyone may experience health effects |
| 150.5 - 250.4 | 201 - 300 | Very Unhealthy | Health warnings for everyone |
| 250.5 - 350.4 | 301 - 400 | Hazardous | Health alert for everyone |
| 350.5 - 500.0 | 401 - 500 | Hazardous | Health warning of emergency conditions |
| > 500.0 | > 500 | Hazardous | Emergency conditions |

### Calculation Macro
```yaml
{% macro calcAQI(Cp, Ih, Il, BPh, BPl) -%}
  {{ (((Ih - Il)/(BPh - BPl)) * (Cp - BPl) + Il) | round }}
{%- endmacro %}
```

## Dependencies
- **PM2.5 Sensors**: Air quality PM2.5 sensor integration
- **Template Sensors**: Complex AQI calculation templates
- **US EPA Standards**: US Environmental Protection Agency AQI standards
- **Multi-Room Integration**: Integration with room-specific packages

## Usage
The air quality package provides several interaction methods:
- **Real-Time Monitoring**: Live air quality monitoring across rooms
- **Dashboard Display**: Air quality data on Home Assistant dashboard
- **Health Alerts**: Air quality health impact notifications
- **Data Analysis**: Historical air quality data analysis
- **Automation Integration**: Air quality-based automation triggers

## Configuration

### PM2.5 Sensor Setup
- **Sensor Integration**: PM2.5 sensor integration and calibration
- **Data Validation**: PM2.5 data validation and error handling
- **Range Monitoring**: PM2.5 range monitoring and alerts
- **Calibration**: Sensor calibration and accuracy verification

### AQI Calculation
- **Algorithm Implementation**: US EPA AQI calculation algorithm
- **Range Classification**: AQI range classification and categorization
- **Invalid Data Handling**: Invalid data detection and handling
- **Precision Management**: AQI calculation precision and rounding

### Multi-Room Monitoring
- **Room Coverage**: Comprehensive room coverage for air quality
- **Data Aggregation**: Multi-room air quality data aggregation
- **Health Monitoring**: Health impact monitoring and alerts
- **Trend Analysis**: Air quality trend analysis and reporting

## Related Files
- `packages/air_quality.yaml`: Main air quality package configuration
- `packages/notifications.yaml`: Air quality alert integration
- `dashboards/home.yaml`: Air quality dashboard display

## Notes
- AQI calculations follow US EPA standards and guidelines
- Invalid PM2.5 readings (>1000 μg/m³) are marked as "invalid"
- AQI calculations use precise mathematical formulas with rounding
- Multi-room monitoring provides comprehensive air quality coverage
- The package integrates with notification system for air quality alerts
- Custom attributes store package information for consistent operation
