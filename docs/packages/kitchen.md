# Kitchen Package

## Overview

The `kitchen` package manages lighting, automation, and utility features in the kitchen. It consists of two sub-packages: `kitchen_lights` for lighting control and automation, and `kitchen_label_printer` for label printing functionality.

## Functionality

This package provides comprehensive kitchen automation with:
- **Multi-zone lighting control** with cabinet and main lighting
- **Smart shade management** based on sun position
- **Dishwasher status display** with e-paper integration
- **Scene controls** via Inovelli switches with LED feedback
- **Label printing system** with multiple printer support
- **Energy monitoring** for appliance status detection

## Key Components

### Lighting System
- Cabinet lighting groups (upper and lower)
- Main kitchen lighting
- Inovelli switch scene controls with LED notifications
- Adaptive lighting integration

### Automation Features
- Sun-based shade control
- Dishwasher status monitoring and display
- Energy-based appliance detection
- E-paper display integration

### Utility Systems
- Label printing with multiple printer support
- Date/time integration for labels
- Shell command integration

## Entities

### Lights
- `light.kitchen_cabinet_lights` - Group of cabinet lights
- `light.kitchen_cabinet_lower_lights` - Lower cabinet lighting
- `light.kitchen_cabinet_upper_lights` - Upper cabinet lighting
- `light.kitchen_lights` - Main kitchen lighting

### Covers
- `cover.kitchen_shades` - Kitchen window shades

### Sensors
- `sensor.energy_monitor_2_dishwasher_power` - Dishwasher power consumption

### Input Entities
- `input_button.print_main_label` - Main label print trigger
- `input_button.print_tape_label` - Tape label print trigger
- `input_button.print_office_label` - Office label print trigger
- `input_text.label_text` - Label text content
- `input_boolean.print_date` - Date printing toggle
- `input_datetime.label_date` - Label date selection
- `input_number.label_copies` - Number of copies

## Automations

### Kitchen Lights Package

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `6eb0e509-5d18-401a-87e1-d05a7b3854f6` | Update Dishwasher Display | Power-based dishwasher status detection | Power sensor thresholds | E-paper display update |
| `035831df-c284-4935-93fd-a337e2890b8c` | Dishwasher Display Button Triggers | Manual dishwasher status control | E-paper button presses | Display state changes |
| `3c66912f-0aa1-469f-9b91-93bfa7c2711f` | Kitchen Light Switch Zigbee Scene Controls | Multi-function scene control | Inovelli switch buttons | Lighting and shade control |
| `ea920c86-437a-4224-8329-7cad4537dc1a` | Manage the Kitchen Shades | Sun-based shade automation | Sunrise/sunset events | Automatic shade control |

### Kitchen Label Printer Package

| ID | Name | Description | Trigger | Actions |
|---|---|---|---|---|
| `c4fdcb6b-1b34-4445-950e-122605812a25` | Print Kitchen Main Label | Main label printing | Input button press | Shell command execution |
| `cc513eb7-2912-440d-baa9-9d4fd9fd056d` | Print Kitchen Tape Label | Tape label printing | Input button press | Shell command execution |
| `925e45b5-affc-46cd-921d-227d7777306e` | Print Office Label | Office label printing | Input button press | Shell command execution |
| `828c11ac-62c2-49da-891c-7d6b99cd88c4` | Set Label Date to Today at Midnight | Date reset automation | Daily at midnight | Date input update |

### Automation Details

#### Update Dishwasher Display
- **Blueprint**: `sbyx/notify-or-do-something-when-an-appliance-like-a-dishwasher-or-washing-machine-finishes.yaml`
- **Power Sensor**: `sensor.energy_monitor_2_dishwasher_power`
- **Starting Threshold**: 25W
- **Finishing Threshold**: 15W
- **Actions**: Updates e-paper display with "Clean" status
- **Pre-actions**: Updates display with "Running" status

#### Dishwasher Display Button Triggers
- **Blueprint**: `rohankapoorcom/solum-m3-epaper-tag-buttons.yaml`
- **E-paper Tag**: `a3f2009d29c8d2526fb0ad4c94097c63`
- **Button 1**: Sets display to "Clean"
- **Button 2**: Sets display to "Dirty"

#### Kitchen Light Switch Zigbee Scene Controls
- **Blueprint**: `rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`
- **Device IDs**: `ff2b9426281125e3833ee5edf69f5ab0`, `1ba8afa3f33d85ff33d77a5a13dfd364`
- **Config Button**: Toggle shades with LED notification
- **Button A2**: Cabinet lights on (100%, 3000K)
- **Button B2**: Cabinet lights off
- **Button A3**: Cabinet + main lights on
- **Button B3**: Cabinet + main lights off
- **Button A4**: All kitchen area lights on
- **Button B4**: All kitchen area lights off

#### Manage the Kitchen Shades
- **Triggers**: Sunset, sunrise +1:30, Home Assistant start
- **Logic**: Close at sunset, open 90 minutes after sunrise
- **LED Feedback**: Open/Close effect on all switches

#### Label Printing Automations
- **Shell Commands**: `/config/shell_command/print_*.sh`
- **Content**: Label text + optional date
- **Copies**: User-defined number of copies
- **Date Reset**: Daily at midnight

## Scripts

### update_dishwasher_display
- **Purpose**: Updates e-paper display with dishwasher status
- **Parameters**: `state` (Clean, Dirty, Running)
- **Display Elements**: Status text, timestamp, icons, arrows
- **Target Device**: `a3f2009d29c8d2526fb0ad4c94097c63`

## Dependencies

### Core Integrations
- `light` - Lighting control
- `cover` - Shade control
- `sensor` - Energy monitoring
- `input_*` - User interface elements
- `shell_command` - Label printing

### Custom Integrations
- `open_epaper_link` - E-paper display integration

### Blueprints
- `sbyx/notify-or-do-something-when-an-appliance-like-a-dishwasher-or-washing-machine-finishes.yaml`
- `rohankapoorcom/solum-m3-epaper-tag-buttons.yaml`
- `rohankapoorcom/inovelli-vzm31-sn-blue-series-switch.yaml`

### Scripts
- `script.inovelli_blue_notifications` - LED notification control

### Shell Commands
- `print_kitchen_label` - Main kitchen label printing
- `print_tape_label` - Tape label printing
- `print_office_label` - Office label printing

## Usage

### Lighting Control
- **Scene Controls**: Use Inovelli switches for multi-zone control
- **LED Feedback**: Visual confirmation of actions
- **Area Control**: Control all kitchen lights as a group

### Shade Management
- **Automatic**: Sun-based opening/closing
- **Manual Override**: Config button on switches
- **Timing**: 90-minute delay after sunrise

### Dishwasher Monitoring
- **Automatic**: Power-based status detection
- **Manual Control**: E-paper button interface
- **Display**: Real-time status with timestamp

### Label Printing
- **Multiple Printers**: Kitchen main, tape, and office
- **Date Integration**: Optional date printing
- **Copy Control**: User-defined number of copies
- **Daily Reset**: Automatic date reset at midnight

## Configuration

### Lighting Groups
```yaml
light:
  - platform: group
    name: Kitchen Cabinet Lights
    entities:
      - light.kitchen_cabinet_lower_lights
      - light.kitchen_cabinet_upper_lights
```

### Device IDs
```yaml
kitchen_light_switch_device_ids: &kitchen_light_switch_device_ids
  - ff2b9426281125e3833ee5edf69f5ab0
  - 1ba8afa3f33d85ff33d77a5a13dfd364
```

### Shell Commands
```yaml
shell_command:
  print_kitchen_label: "/bin/bash /config/shell_command/print_kitchen_label.sh '{{content}}' '{{copies}}'"
  print_tape_label: "/bin/bash /config/shell_command/print_tape_label.sh '{{content}}' '{{copies}}'"
  print_office_label: "/bin/bash /config/shell_command/print_office_label.sh '{{content}}' '{{copies}}'"
```

### E-paper Display Configuration
- **Background**: White
- **Font**: ppb.ttf
- **Icons**: Silverware, arrows
- **Layout**: Status text, timestamp, icons, labels

## Notes

- The package uses YAML anchors for device ID management
- E-paper display provides both automatic and manual dishwasher status
- LED notifications provide visual feedback for all switch actions
- Label printing supports multiple printer types and locations
- Shade automation includes manual override capability
- Energy monitoring provides reliable appliance status detection
- All automations include proper error handling and restart modes
