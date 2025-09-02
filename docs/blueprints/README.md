# Blueprint Documentation

This directory contains comprehensive documentation for all blueprints created by the repository owner (rohankapoorcom). These blueprints provide reusable automation templates for various Home Assistant scenarios.

## Overview

The blueprints in this repository are organized into several categories based on their functionality and target devices. Each blueprint includes detailed documentation with input parameters, usage examples, and dependencies.

## Blueprint Categories

### [Device-Specific Automations](device-specific/README.md)
Blueprints designed for specific device types and protocols:
- **Emulated Roku**: Control automations via emulated Roku device keypresses
- **Solum M3 E-Paper Tag Buttons**: Automations triggered by e-paper tag button presses
- **Tuya TS0044 4-Button Remote**: Control automations via Tuya remote buttons

### [Inovelli Device Automations](inovelli/README.md)
Comprehensive blueprints for Inovelli Z-Wave switches and dimmers:
- **Lock Notifications**: Various Inovelli lock notification blueprints
- **Switch Controls**: Complete button mapping for all Inovelli switch models
- **Night Mode**: Automatic lighting adjustments for Inovelli Red Series devices

### [Zooz Device Automations](zooz/README.md)
Blueprints for Zooz Z-Wave devices:
- **ZEN32 Scene Controller Status Lights**: Synchronize status lights with Home Assistant entities
- **ZEN32 Scene Controls**: Complete scene control mapping for the ZEN32 controller

### [General Automations](general/README.md)
General-purpose automation blueprints:
- **Adaptive Lighting Sleep Mode**: Time-based adaptive lighting control
- **Motion Light**: Motion-activated lighting with automatic shutoff
- **Tablet Battery Charging**: Intelligent battery management for tablets

## Blueprint Statistics

- **Total Blueprints**: 19
- **Automation Blueprints**: 19
- **Script Blueprints**: 0 (none created by repository owner)
- **Template Blueprints**: 0 (none created by repository owner)

## Device Support

### Z-Wave Devices
- **Inovelli**: LZW30, LZW31, VZM31, VZW31 series (Red and Blue)
- **Zooz**: ZEN32 Scene Controller

### Other Protocols
- **Tuya**: TS0044 4-button remote
- **Emulated Roku**: Software-based Roku device
- **Open E-Paper Link**: Solum M3 e-paper tags

### General Integrations
- **Adaptive Lighting**: Sleep mode control
- **Motion Sensors**: Binary sensors with motion device class
- **Battery Sensors**: All sensors with battery device class
- **Locks**: All lock entities
- **Lights**: All light entities
- **Switches**: Charger and control switches

## Usage Guidelines

1. **Installation**: Copy the desired blueprint YAML file to your `blueprints/automation/` directory
2. **Configuration**: Use the blueprint in your `automations.yaml` file with the `use_blueprint` directive
3. **Customization**: Modify the input parameters to match your specific devices and requirements
4. **Testing**: Test each automation thoroughly before deploying to production

## Contributing

These blueprints are maintained as part of the Home Assistant configuration repository. Contributions are welcome through pull requests and issue reports.

## License

All blueprints are provided under the MIT License as part of the main repository.

## Related Documentation

- [Main README](../README.md): Overview of the entire Home Assistant configuration
- [Package Documentation](../packages/): Documentation for package-based configurations
- [Custom Components](../custom_components/): Documentation for custom integrations

---
*This documentation follows the updated Home Assistant documentation prompt guidelines*
