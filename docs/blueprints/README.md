# Blueprint Documentation

This directory contains documentation for custom blueprints created by the repository owner (rohankapoorcom) for various Home Assistant automation scenarios.

## Blueprint Types

### [Automation Blueprints](automation/README.md)
Comprehensive collection of automation blueprints covering device-specific controls, lighting automation, battery management, and general home automation.

### [Script Blueprints](script/README.md)
Script blueprints for creating reusable scripts for device control and status updates.

### [Template Blueprints](template/README.md)
Template blueprints for creating custom sensors and calculations.

## Quick Reference

| Blueprint | Type | File | Key Features | Device Support |
|-----------|------|------|--------------|----------------|
| Adaptive Lighting Sleep Mode | automation | [adaptive-lighting-sleep-mode-blueprint.md](automation/adaptive-lighting-sleep-mode-blueprint.md) | Sleep mode automation | Adaptive Lighting integration |
| Emulated Roku | automation | [emulated-roku-blueprint.md](automation/emulated-roku-blueprint.md) | Roku device emulation | Media devices |
| Inovelli LZW30 Black Series Lock Notifications | automation | [inovelli-lzw30-black-series-lock-notifications-blueprint.md](automation/inovelli-lzw30-black-series-lock-notifications-blueprint.md) | Lock status notifications | Inovelli LZW30 locks |
| Inovelli LZW30 Red Series Switch | automation | [inovelli-lzw30-red-series-switch-blueprint.md](automation/inovelli-lzw30-red-series-switch-blueprint.md) | Switch automation | Inovelli LZW30 switches |
| Inovelli LZW31 Red Series Switch | automation | [inovelli-lzw31-red-series-switch-blueprint.md](automation/inovelli-lzw31-red-series-switch-blueprint.md) | Switch automation | Inovelli LZW31 switches |
| Inovelli LZW31-SN Red Series Lock Notifications | automation | [inovelli-lzw31-sn-red-series-lock-notifications-blueprint.md](automation/inovelli-lzw31-sn-red-series-lock-notifications-blueprint.md) | Lock status notifications | Inovelli LZW31-SN locks |
| Inovelli Red Series Night Mode | automation | [inovelli-red-series-night-mode-blueprint.md](automation/inovelli-red-series-night-mode-blueprint.md) | Night mode automation | Inovelli red series devices |
| Inovelli VZM31-SN Blue Series Lock Notifications | automation | [inovelli-vzm31-sn-blue-series-lock-notifications-blueprint.md](automation/inovelli-vzm31-sn-blue-series-lock-notifications-blueprint.md) | Lock status notifications | Inovelli VZM31-SN locks |
| Inovelli VZM31-SN Blue Series Switch | automation | [inovelli-vzm31-sn-blue-series-switch-blueprint.md](automation/inovelli-vzm31-sn-blue-series-switch-blueprint.md) | Switch automation | Inovelli VZM31-SN switches |
| Inovelli VZW31-SN Red Series Lock Notifications | automation | [inovelli-vzw31-sn-red-series-lock-notifications-blueprint.md](automation/inovelli-vzw31-sn-red-series-lock-notifications-blueprint.md) | Lock status notifications | Inovelli VZW31-SN locks |
| Inovelli VZW31-SN Red Series Switch | automation | [inovelli-vzw31-sn-red-series-switch-blueprint.md](automation/inovelli-vzw31-sn-red-series-switch-blueprint.md) | Switch automation | Inovelli VZW31-SN switches |
| Lock Light Controls | automation | [lock-light-controls-blueprint.md](automation/lock-light-controls-blueprint.md) | Lock and light coordination | Locks and lights |
| Low Battery Level Detection Notification | automation | [low-battery-level-detection-notification-blueprint.md](automation/low-battery-level-detection-notification-blueprint.md) | Battery monitoring | All battery sensors |
| Motion Light | automation | [motion-light-blueprint.md](automation/motion-light-blueprint.md) | Motion-activated lighting | Motion sensors and lights |
| Solum M3 E-Paper Tag Buttons | automation | [solum-m3-epaper-tag-buttons-blueprint.md](automation/solum-m3-epaper-tag-buttons-blueprint.md) | E-paper tag controls | Solum M3 tags |
| Sun-Based Cover Control | automation | [sun-based-cover-control-blueprint.md](automation/sun-based-cover-control-blueprint.md) | Sun-based automation, window/door integration | Cover entities, binary sensors |
| Tablet Battery Charging | automation | [tablet-battery-charging-blueprint.md](automation/tablet-battery-charging-blueprint.md) | Tablet charging automation | Tablets |
| Tuya TS0044 4-Button Remote | automation | [tuya-ts0044-4-button-remote-blueprint.md](automation/tuya-ts0044-4-button-remote-blueprint.md) | Remote control automation | Tuya TS0044 remotes |
| Update Dishwasher E-Paper Display | script | [update-dishwasher-epaper-display-blueprint.md](script/update-dishwasher-epaper-display-blueprint.md) | Status display, timestamp, icons | OpenEPaperLink displays |
| US AQI | template | [us-aqi-blueprint.md](template/us-aqi-blueprint.md) | EPA-compliant AQI calculation | Any PM2.5 sensor |
| Zooz ZEN32 Scene Controller Status Lights | automation | [zooz-zen32-scene-controller-status-lights-blueprint.md](automation/zooz-zen32-scene-controller-status-lights-blueprint.md) | Status light automation | Zooz ZEN32 controllers |
| Zooz ZEN32 Scene Controls | automation | [zooz-zen32-scene-controls-blueprint.md](automation/zooz-zen32-scene-controls-blueprint.md) | Scene control automation | Zooz ZEN32 controllers |

## Blueprint Categories

### Device-Specific Automations
- **Emulated Roku**: Roku device emulation for media control
- **Solum M3 E-Paper Tag Buttons**: E-paper display button controls
- **Tuya TS0044 4-Button Remote**: Tuya remote control automation

### Z-Wave Device Automations
- **Inovelli Devices**: Comprehensive automation for Inovelli switches, dimmers, and locks
- **Zooz Devices**: Scene controller automation for Zooz ZEN32 devices

### General Automation
- **Adaptive Lighting Sleep Mode**: Sleep mode integration with adaptive lighting
- **Lock Light Controls**: Coordinated lock and lighting automation
- **Low Battery Level Detection**: Battery monitoring and notifications
- **Motion Light**: Motion-activated lighting automation
- **Sun-Based Cover Control**: Intelligent window covering automation based on sun position and window status
- **Tablet Battery Charging**: Tablet charging management

### Script Blueprints
- **Update Dishwasher E-Paper Display**: Script for updating e-paper displays with dishwasher status

### Template Sensors
- **US AQI**: EPA-compliant air quality index calculation from PM2.5 sensors

## Importing Blueprints

Each blueprint documentation includes a one-click import button that will open your Home Assistant instance and pre-fill the blueprint import dialog. Simply click the "Import Blueprint" button in any blueprint's documentation to get started.

## Related Documentation

- [Main Configuration README](../../README.md): Overview of the entire Home Assistant configuration
- [Custom Integrations](../../README.md#custom-integrations): List of custom integrations used
- [Custom Lovelace Cards](../../README.md#custom-lovelace-cards): List of custom UI components

---

*This documentation is part of the [Home Assistant Configuration](https://github.com/rohankapoorcom/homeassistant-config) project.*
