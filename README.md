# Home Assistant Configuration
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![GitHub Actions][actions-shield]][actions]
[![GitHub Activity][commits-shield]][commits]
[![GitHub Last Commit][last-commit-shield]][commits]

## About

My comprehensive Home Assistant configuration for a smart home with extensive automation, security monitoring, and entertainment systems. The setup focuses on reliability, user experience, and integration across multiple protocols (Z-Wave, Zigbee, IP, Bluetooth). This configuration serves as a showcase of advanced Home Assistant capabilities and custom automation solutions.

## Architecture Overview

**Hardware Infrastructure:**
- Lenovo Tiny P330 Cluster running Home Assistant (Container) in a VM (4 CPU cores, 4GB RAM, 50GB disk)
- Multiple tablets and mobile devices for interface access
- Distributed radio connectivity via IP network

**Software Stack:**
- [Home Assistant](https://home-assistant.io) with package-based configuration
- [ZWaveJS2MQTT](https://zwave-js.github.io/zwavejs2mqtt/) for Z-Wave device management
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/) for Zigbee device management
- [Valetudo](https://valetudo.cloud/) for robot vacuums
- [Mosquitto](https://mosquitto.org/) MQTT broker for device communication
- Custom integrations for specialized functionality

**Network Topology:**
- Centralized server-based architecture
- Distributed radio connectivity via IP network
- Multi-protocol support (Z-Wave, Zigbee, IP, Bluetooth)
- Centralized authentication with LDAP integration

## Custom Integrations

### Security & Monitoring
- **[alarmo](https://github.com/nielsfaber/alarmo)**: Advanced alarm system with multiple zones and automation triggers
- **[frigate](https://github.com/blakeblackshear/frigate)**: AI-powered video surveillance with object detection
- **[noonlight](https://github.com/konnected-io/noonlight-hass)**: Emergency response integration for enhanced security

### Climate & Environment
- **[adaptive_lighting](https://github.com/basnijholt/adaptive-lighting)**: Automatic lighting adjustments based on time and natural light
- **[air_quality](https://github.com/rohankapoorcom/homeassistant-config/tree/master/custom_components/air_quality)**: Comprehensive air quality monitoring and alerts
- **[battery_notes](https://github.com/andrew-codechicken/battery-notes)**: Battery level tracking with smart notifications
- **[enphase_envoy](https://github.com/briancmpbll/home_assistant_custom_envoy)**: Solar panel monitoring and energy production tracking

### Media & Entertainment
- **[huesyncbox](https://github.com/mvdwetering/huesyncbox)**: Philips Hue Sync Box control for TV lighting synchronization
- **[spotcast](https://github.com/fondberg/spotcast)**: Spotify casting integration for whole-home audio
- **[vaddio_conferenceshot](https://github.com/rohankapoorcom/vaddio_conferenceshot)**: Professional video conferencing camera control
- **[webrtc](https://github.com/AlexxIT/WebRTC)**: WebRTC camera integration for real-time video streaming

### Smart Home Control
- **[ecoflow](https://github.com/lwsrbrts/hassio-ecoflow)**: Portable power station monitoring and control
- **[ecoflow_cloud](https://github.com/tolwi/hassio-ecoflow-cloud)**: Cloud-based EcoFlow device management
- **[keymaster](https://github.com/FutureTense/keymaster)**: Advanced lock management with access codes and scheduling
- **[smartir](https://github.com/smartHomeHub/SmartIR)**: Infrared remote control for legacy devices

### Utilities & Tools
- **[browser_mod](https://github.com/thomasloven/hass-browser_mod)**: Browser-based automations and popups
- **[lovelace_gen](https://github.com/thomasloven/hass-lovelace_gen)**: Dynamic Lovelace dashboard generation
- **[mqtt_discoverystream](https://github.com/koying/mqtt_discoverystream_ha)**: MQTT device discovery and management
- **[mqtt_vacuum_camera](https://github.com/sca075/mqtt_vacuum_camera)**: Robot vacuum camera integration
- **[open_epaper_link](https://github.com/OpenEPaperLink/Home_Assistant_Integration)**: E-paper display integration
- **[pirateweather](https://github.com/alexander0042/pirate-weather-hass)**: Alternative weather data provider
- **[qr_generator](https://github.com/DeerMaximum/QR-Code-Generator)**: QR code generation for device setup
- **[simpleicons](https://github.com/vigonotion/hass-simpleicons)**: Custom icon integration for enhanced UI
- **[smartthinq_sensors](https://github.com/ollo69/ha-smartthinq-sensors)**: LG ThinQ sensor integration
- **[spook](https://spook.boo/)**: Enhanced entity management and automation

## Custom Lovelace Cards

### Data Visualization
- **[apexcharts-card](https://github.com/RomRider/apexcharts-card)**: Advanced charting and graphs for sensor data
- **[bar-card](https://github.com/custom-cards/bar-card)**: Bar chart visualizations for comparative data
- **[mini-graph-card](https://github.com/kalkih/mini-graph-card)**: Compact data graphs for quick monitoring
- **[power-flow-card](https://github.com/ulic75/power-flow-card)**: Energy flow visualization for solar systems
- **[weather-card](https://github.com/bramkragten/weather-card)**: Comprehensive weather display and forecasting

### Home Automation
- **[button-card](https://github.com/custom-cards/button-card)**: Customizable button interface for device control
- **[light-entity-card](https://github.com/ljmerza/light-entity-card)**: Specialized lighting controls with color picker
- **[numberbox-card](https://github.com/junkfix/numberbox-card)**: Numeric input controls for devices
- **[simple-thermostat](https://github.com/nervetattoo/simple-thermostat)**: Thermostat interface with scheduling
- **[slider-button-card](https://github.com/mattieha/slider-button-card)**: Slider controls with button actions

### Layout & Navigation
- **[hass-swipe-navigation](https://github.com/zanna-37/hass-swipe-navigation)**: Swipe-based navigation for mobile interfaces
- **[kiosk-mode](https://github.com/NemesisRE/kiosk-mode)**: Kiosk interface mode for wall-mounted tablets
- **[lovelace-layout-card](https://github.com/thomasloven/lovelace-layout-card)**: Advanced layout management with conditional displays
- **[stack-in-card](https://github.com/custom-cards/stack-in-card)**: Nested card layouts for complex interfaces
- **[vertical-stack-in-card](https://github.com/ofekashery/vertical-stack-in-card)**: Vertical stacking for organized layouts

### Media & Entertainment
- **[lovelace-valetudo-map-card](https://github.com/Hypfer/lovelace-valetudo-map-card)**: Valetudo robot vacuum mapping
- **[lovelace-xiaomi-vacuum-map-card](https://github.com/PiotrMachowski/lovelace-xiaomi-vacuum-map-card)**: Robot vacuum mapping interface
- **[mini-media-player](https://github.com/kalkih/mini-media-player)**: Compact media controls for audio/video
- **[roku-card](https://github.com/custom-cards/roku-card)**: Roku device control and status
- **[spotify-card](https://github.com/custom-cards/spotify-card)**: Spotify integration with playlist controls

### Utilities
- **[config-template-card](https://github.com/iantrich/config-template-card)**: Template-based card configuration
- **[decluttering-card](https://github.com/custom-cards/decluttering-card)**: UI simplification and conditional displays
- **[lovelace-auto-entities](https://github.com/thomasloven/lovelace-auto-entities)**: Dynamic entity lists based on device states
- **[lovelace-card-mod](https://github.com/thomasloven/lovelace-card-mod)**: CSS styling and modifications for custom appearance
- **[lovelace-digital-clock](https://github.com/wassy92x/lovelace-digital-clock)**: Digital clock display
- **[lovelace-fold-entity-row](https://github.com/thomasloven/lovelace-fold-entity-row)**: Collapsible entity rows
- **[lovelace-multiple-entity-row](https://github.com/benct/lovelace-multiple-entity-row)**: Multiple entities in single row
- **[lovelace-slider-entity-row](https://github.com/thomasloven/lovelace-slider-entity-row)**: Slider controls in entity rows
- **[lovelace-state-switch](https://github.com/thomasloven/lovelace-state-switch)**: State-based card switching
- **[lovelace-template-entity-row](https://github.com/thomasloven/lovelace-template-entity-row)**: Template-based entity rows

## Custom Blueprints

Comprehensive list of all custom blueprints created by the repository owner:

### Device-Specific Automations
- **[emulated-roku](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/emulated-roku.yaml)**: Emulated Roku device automation
- **[solum-m3-epaper-tag-buttons](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml)**: Solum M3 e-paper tag button controls
- **[tuya-ts0044-4-button-remote](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tuya-ts0044-4-button-remote.yaml)**: Tuya 4-button remote control automation

#### Inovelli Device Automations
- **[inovelli-lzw30-black-series-lock-notifications](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-black-series-lock-notifications.yaml)**: Lock notification automation
- **[inovelli-lzw30-red-series-switch](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw30-red-series-switch.yaml)**: Red series switch automation
- **[inovelli-lzw31-red-series-switch](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw31-red-series-switch.yaml)**: LZW31 red series switch automation
- **[inovelli-lzw31-sn-red-series-lock-notifications](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-lzw31-sn-red-series-lock-notifications.yaml)**: Lock notifications for LZW31
- **[inovelli-red-series-night-mode](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-red-series-night-mode.yaml)**: Night mode automation for red series devices
- **[inovelli-vzm31-sn-blue-series-lock-notifications](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-lock-notifications.yaml)**: Blue series lock notifications
- **[inovelli-vzm31-sn-blue-series-switch](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml)**: Blue series switch automation
- **[inovelli-vzw31-sn-red-series-lock-notifications](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-lock-notifications.yaml)**: VZW31 lock notifications
- **[inovelli-vzw31-sn-red-series-switch](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/inovelli-vzw31-sn-red-series-switch.yaml)**: VZW31 red series switch automation

#### Zooz Device Automations
- **[zooz-zen32-scene-controller-status-lights](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controller-status-lights.yaml)**: Scene controller status light automation
- **[zooz-zen32-scene-controls](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/zooz-zen32-scene-controls.yaml)**: Scene controller automation

### General Automation
- **[adaptive-lighting-sleep-mode](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/adaptive-lighting-sleep-mode.yaml)**: Adaptive lighting sleep mode automation
- **[lock-light-controls](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/lock-light-controls.yaml)**: Lock and light control automation
- **[low-battery-level-detection-notification](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml)**: Battery level monitoring and notifications
- **[motion_light](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml)**: Motion-activated lighting automation
- **[tablet-battery-charging](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/tablet-battery-charging.yaml)**: Tablet battery charging automation

## Package Organization

The configuration uses a package-based organization system for modular and maintainable code:

### Feature-based Packages
- **air_quality.yaml**: Air quality monitoring and alerts
- **appliances.yaml**: Appliance control and monitoring
- **assistant.yaml**: Voice assistant integration
- **default_config.yaml**: Default configuration settings
- **media_music.yaml**: Whole-home audio and entertainment
- **notifications.yaml**: Notification management
- **presence.yaml**: Presence detection and automation
- **security.yaml**: Cross-room security and monitoring
- **tablets.yaml**: Tablet interface management
- **weather.yaml**: Weather monitoring and alerts
- **weatherman.yaml**: Advanced weather forecasting

### Room-based Packages
- **downstairs_bathroom.yaml**: Bathroom automation
- **downstairs_hallway.yaml**: Hallway lighting and motion control
- **front_door.yaml**: Entry door security and access control
- **garage.yaml**: Garage door control and monitoring
- **guest_room.yaml**: Guest room automation
- **gym.yaml**: Home gym automation
- **hallway.yaml**: Main hallway controls
- **hallway_bathroom.yaml**: Bathroom-specific features
- **kitchen/**: Kitchen automation and appliance control
- **living_room/**: Entertainment and living space management
- **master_bathroom.yaml**: Master bathroom automation
- **master_bedroom.yaml**: Master bedroom comfort and security
- **office.yaml**: Office automation and productivity features
- **server_rack.yaml**: Server infrastructure monitoring
- **stairway.yaml**: Stairway lighting and safety features

## Dashboard Structure

Single responsive Lovelace dashboard (`dashboards/home.yaml`) that adapts to different screen sizes:

- **Large screens (10"+ tablets)**: Two-column layout with left navigation
- **Medium screens**: Top navigation bar with responsive grid
- **Small screens (phones)**: Single-column layout with stacked cards

Custom cards provide specialized interfaces for different device types and automation scenarios. The dashboard includes sections for:
- Appliances and utilities
- Climate and environment
- Home overview and status
- Lighting controls
- Media and entertainment
- Robot vacuums and cleaning
- Security and monitoring

### Screenshots

<p align="center">
    <img alt="Home" src="./docs/img/1.png" width="200"/>
    &nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="Lights" src="./docs/img/2.png" width="200"/>
</p>
<p align="center">
    <img alt="Vacuums" src="./docs/img/5.png" width="200"/>
    &nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="Appliances" src="./docs/img/6.png" width="200"/>
</p>
<p align="center">
    <img alt="Music" src="./docs/img/7.png" width="200"/>
    &nbsp; &nbsp; &nbsp; &nbsp;
    <img alt="TV Remote" src="./docs/img/8.png" width="200"/>
</p>

\* Screenshots use a template from [Design Bolts](https://www.designbolts.com/2020/05/06/free-oneplus-8-pro-mockup-ai-psd-format/).

## Contributing

I treat my Home Assistant configuration as an active open source project but don't always follow the best practices (with issues and PRs). If there's something you'd like to improve or contribute to it, please feel free to make a PR.

## License

The MIT License (MIT)

Copyright (c) 2025 Rohan Kapoor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[commits-shield]: https://img.shields.io/github/commit-activity/y/rohankapoorcom/homeassistant-config.svg
[commits]: https://github.com/rohankapoorcom/homeassistant-config/commits/master
[actions-shield]: https://github.com/rohankapoorcom/homeassistant-config/actions/workflows/check-config.yml/badge.svg
[actions]: https://github.com/rohankapoorcom/homeassistant-config/actions
[home-assistant]: https://home-assistant.io
[issue]: https://github.com/rohankapoorcom/homeassistant-config/issues
[license-shield]: https://img.shields.io/github/license/rohankapoorcom/homeassistant-config.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/rohankapoorcom/homeassistant-config.svg
