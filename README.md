# Home Assistant Configuration
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![GitHub Actions][actions-shield]][actions]
[![GitHub Activity][commits-shield]][commits]
[![GitHub Last Commit][last-commit-shield]][commits]

## About

My comprehensive Home Assistant configuration for a smart home with extensive automation, security monitoring, and entertainment systems. The setup focuses on reliability, user experience, and integration across multiple protocols (Z-Wave, Zigbee, IP, Bluetooth).

## Architecture Overview

**Hardware Infrastructure:**
- Lenovo Tiny P330 Cluster running Home Assistant (Container) in a VM (4 CPU cores, 4GB RAM, 50GB disk)
- Multiple tablets and mobile devices for interface access

**Software Stack:**
- Home Assistant with package-based configuration
- ZWaveJS2MQTT for Z-Wave device management
- Zigbee2MQTT for Zigbee device management
- Valetudo for robot vacuums
- Mosquitto MQTT broker for device communication
- Custom integrations for specialized functionality

**Network Topology:**
- Centralized server-based architecture
- Distributed radio connectivity via IP network
- Multi-protocol support (Z-Wave, Zigbee, IP, Bluetooth)
- Centralized authentication with LDAP integration

## Custom Integrations

### Security & Monitoring
- **alarmo**: Advanced alarm system with multiple zones and automation triggers
- **frigate**: AI-powered video surveillance with object detection
- **noonlight**: Emergency response integration for enhanced security

### Climate & Environment
- **adaptive_lighting**: Automatic lighting adjustments based on time and natural light
- **battery_notes**: Battery level tracking with smart notifications
- **enphase_envoy**: Solar panel monitoring and energy production tracking
- **air_quality**: Comprehensive air quality monitoring and alerts

### Media & Entertainment
- **spotcast**: Spotify casting integration for whole-home audio
- **huesyncbox**: Philips Hue Sync Box control for TV lighting synchronization
- **vaddio_conferenceshot**: Professional video conferencing camera control
- **webrtc**: WebRTC camera integration for real-time video streaming

### Smart Home Control
- **smartir**: Infrared remote control for legacy devices
- **keymaster**: Advanced lock management with access codes and scheduling
- **ecoflow**: Portable power station monitoring and control
- **ecoflow_cloud**: Cloud-based EcoFlow device management

### Utilities & Tools
- **browser_mod**: Browser-based automations and popups
- **lovelace_gen**: Dynamic Lovelace dashboard generation
- **mqtt_discoverystream**: MQTT device discovery and management
- **qr_generator**: QR code generation for device setup
- **simpleicons**: Custom icon integration for enhanced UI
- **smartthinq_sensors**: LG ThinQ sensor integration
- **open_epaper_link**: E-paper display integration
- **pirateweather**: Alternative weather data provider
- **spook**: Enhanced entity management and automation
- **mqtt_vacuum_camera**: Robot vacuum camera integration

## Custom Lovelace Cards

### Layout & Navigation
- **lovelace-layout-card**: Advanced layout management with conditional displays
- **hass-swipe-navigation**: Swipe-based navigation for mobile interfaces
- **kiosk-mode**: Kiosk interface mode for wall-mounted tablets
- **stack-in-card**: Nested card layouts for complex interfaces
- **vertical-stack-in-card**: Vertical stacking for organized layouts

### Data Visualization
- **apexcharts-card**: Advanced charting and graphs for sensor data
- **mini-graph-card**: Compact data graphs for quick monitoring
- **bar-card**: Bar chart visualizations for comparative data
- **power-flow-card**: Energy flow visualization for solar systems
- **weather-card**: Comprehensive weather display and forecasting

### Media & Entertainment
- **mini-media-player**: Compact media controls for audio/video
- **spotify-card**: Spotify integration with playlist controls
- **roku-card**: Roku device control and status
- **lovelace-xiaomi-vacuum-map-card**: Robot vacuum mapping interface
- **lovelace-valetudo-map-card**: Valetudo robot vacuum mapping

### Home Automation
- **button-card**: Customizable button interface for device control
- **light-entity-card**: Specialized lighting controls with color picker
- **simple-thermostat**: Thermostat interface with scheduling
- **slider-button-card**: Slider controls with button actions
- **numberbox-card**: Numeric input controls for devices

### Utilities
- **lovelace-card-mod**: CSS styling and modifications for custom appearance
- **lovelace-auto-entities**: Dynamic entity lists based on device states
- **decluttering-card**: UI simplification and conditional displays
- **config-template-card**: Template-based card configuration
- **lovelace-multiple-entity-row**: Multiple entities in single row
- **lovelace-slider-entity-row**: Slider controls in entity rows
- **lovelace-template-entity-row**: Template-based entity rows
- **lovelace-fold-entity-row**: Collapsible entity rows
- **lovelace-state-switch**: State-based card switching
- **lovelace-digital-clock**: Digital clock display

## Package Organization

The configuration uses a package-based organization system for modular and maintainable code:

### Room-based Packages
- **office.yaml**: Office automation and productivity features
- **master_bedroom.yaml**: Master bedroom comfort and security
- **kitchen/**: Kitchen automation and appliance control
- **living_room/**: Entertainment and living space management
- **garage.yaml**: Garage door control and monitoring
- **guest_room.yaml**: Guest room automation
- **downstairs_hallway.yaml**: Hallway lighting and motion control
- **stairway.yaml**: Stairway lighting and safety features
- **server_rack.yaml**: Server infrastructure monitoring
- **downstairs_bathroom.yaml**: Bathroom automation
- **hallway.yaml**: Main hallway controls
- **hallway_bathroom.yaml**: Bathroom-specific features
- **master_bathroom.yaml**: Master bathroom automation
- **front_door.yaml**: Entry door security and access control
- **gym.yaml**: Home gym automation

### Feature-based Packages
- **security.yaml**: Cross-room security and monitoring
- **media_music.yaml**: Whole-home audio and entertainment
- **weather.yaml**: Weather monitoring and alerts
- **weatherman.yaml**: Advanced weather forecasting
- **notifications.yaml**: Notification management
- **air_quality.yaml**: Air quality monitoring and alerts
- **appliances.yaml**: Appliance control and monitoring
- **assistant.yaml**: Voice assistant integration
- **presence.yaml**: Presence detection and automation
- **tablets.yaml**: Tablet interface management
- **default_config.yaml**: Default configuration settings

## Dashboard Structure

Single responsive Lovelace dashboard (`dashboards/home.yaml`) that adapts to different screen sizes:

- **Large screens (10"+ tablets)**: Two-column layout with left navigation
- **Medium screens**: Top navigation bar with responsive grid
- **Small screens (phones)**: Single-column layout with stacked cards

Custom cards provide specialized interfaces for different device types and automation scenarios. The dashboard includes sections for:
- Home overview and status
- Lighting controls
- Climate and environment
- Security and monitoring
- Media and entertainment
- Appliances and utilities
- Robot vacuums and cleaning

## Screenshots

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
