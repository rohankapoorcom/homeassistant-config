# Home Assistant Configuration
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![GitHub Actions][actions-shield]][actions]
[![GitHub Activity][commits-shield]][commits]
[![GitHub Last Commit][last-commit-shield]][commits]

## About

My configuration files for [Home Assistant](https://home-assistant.io), which runs all of my home automations.

I run Home Assistant (Core) as a virtual machine (VM) on my Dell R720 host machine. It's allocated 2 CPU cores and 2GB of RAM and 50GB of Disk. I also run [ZWavejs2Mqtt](https://zwave-js.github.io/zwavejs2mqtt/#/) on the same VM.

Since Home Assistant is running as a VM in my server rack, I have a Raspberry Pi (original) running [ser2net](https://linux.die.net/man/8/ser2net#) located on top of my Kitchen cabinets to connect my Z-Wave and Zigbee radios.

## Devices
This section still needs to be written...
<!-- * HUSBZB-1 for Z-Wave and Zigbee control
*  -->

## Dashboards
I have a single [Lovelace dashboard](dashboards/home.yaml) that I use for all different screen sizes. On large screens like 10" tablets (or larger), it's a two column layout with a navigation bar on the left side. On smaller tablets, the navigation bar switches to the top. On smaller screens (like phones), it becomes a single column layout. Some screenshots below show the view from my phone. For privacy reasons any screens showing camera views have been omitted.

I use many [custom Lovelace cards](www/community) to build my dashboard.

<img alt="Home" src="./docs/img/1.png" width="200"/> <img alt="Lights" src="./docs/img/2.png" width="200"/>
<img alt="Vacuums" src="./docs/img/5.png" width="200"/> <img alt="Appliances" src="./docs/img/6.png" width="200"/>
<img alt="Music" src="./docs/img/7.png" width="200"/> <img alt="TV Remote" src="./docs/img/8.png" width="200"/>

## Contributing

I treat my Home Assistant configuration as an active open source project but don't always follow the best practices (with issues and PRs). If there's something you'd like to improve or contribute to it, please feel free to make a PR.

## License

The MIT License (MIT)

Copyright (c) 2018-2022 Rohan Kapoor

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
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/rohankapoorcom/homeassistant-config.svg