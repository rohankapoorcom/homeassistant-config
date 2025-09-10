# US AQI Template Blueprint Documentation

## Overview
A template blueprint that creates a sensor to compute the U.S. Air Quality Index (AQI) from a reference PM2.5 sensor. This blueprint follows the U.S. EPA AQI calculation algorithm to provide accurate air quality measurements.

## Blueprint Information
- **Name**: Calculate US AQI
- **Domain**: template
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/template/rohankapoorcom/us_aqi.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `reference_entity`: The PM2.5 sensor entity to be used for computing the US AQI

## Functionality
This blueprint creates a template sensor that:
- Takes a PM2.5 sensor value as input
- Applies the U.S. EPA AQI calculation algorithm
- Returns a standardized AQI value (0-500)
- Handles invalid readings (>1000 or negative values)
- Provides proper device class and state class for AQI sensors

## AQI Calculation Algorithm
The blueprint implements the EPA's AQI calculation using breakpoints for different PM2.5 concentration ranges:

- **Good (0-50)**: PM2.5 0.0-12.0 μg/m³
- **Moderate (51-100)**: PM2.5 12.1-35.4 μg/m³
- **Unhealthy for Sensitive Groups (101-150)**: PM2.5 35.5-55.4 μg/m³
- **Unhealthy (151-200)**: PM2.5 55.5-150.4 μg/m³
- **Very Unhealthy (201-300)**: PM2.5 150.5-250.4 μg/m³
- **Hazardous (301-400)**: PM2.5 250.5-350.4 μg/m³
- **Hazardous (401-500)**: PM2.5 350.5-500.0 μg/m³

## Usage Examples
```yaml
# Example: Create AQI sensor from PurpleAir PM2.5 sensor
template:
  - use_blueprint:
      path: rohankapoorcom/us_aqi.yaml
      input:
        reference_entity: sensor.purpleair_pm2_5
    name: living_room_us_air_quality_index
    unique_id: living_room_aqi_sensor
```

## Dependencies
- **PM2.5 Sensor**: Any sensor providing PM2.5 concentration values in μg/m³
- **Template Integration**: Built-in Home Assistant template sensor support

## Related Files
- `packages/air_quality.yaml`: Package using this blueprint for multiple rooms
- `blueprints/template/rohankapoorcom/us_aqi.yaml`: The blueprint source file

## Notes
- Based on the U.S. EPA AQI calculation formula
- Reference: https://community.home-assistant.io/t/purpleair-air-quality-sensor/146588
- Handles edge cases for invalid readings
- Provides proper availability tracking based on reference sensor state
- Uses device_class: aqi for proper integration with air quality cards

---
*This documentation is part of the [Blueprint Documentation Index](../README.md)*
