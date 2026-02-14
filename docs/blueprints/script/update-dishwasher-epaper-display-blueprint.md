# Update Dishwasher E-Paper Display Script Blueprint

## Overview

A customizable script blueprint for updating OpenEPaperLink e-paper displays with dishwasher status information. This blueprint creates a script that displays the current state of a dishwasher (Clean, Dirty, or Running) with visual indicators and timestamp on an e-paper tag.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/script/rohankapoorcom/update-dishwasher-epaper-display.yaml)

## Blueprint Information

- **Name**: Update Dishwasher E-Paper Display
- **Domain**: script
- **Source URL**: [GitHub](https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/script/rohankapoorcom/update-dishwasher-epaper-display.yaml)
- **Author**: rohankapoorcom

## Input Parameters

### Blueprint Configuration
- `epaper_tag`: The OpenEPaperLink e-paper tag device to update (required)
  - Selector: Device filtered by `open_epaper_link` integration

### Script Fields
- `state`: The current state of the dishwasher (required)
  - Expected values: "Clean", "Dirty", or "Running"
  - Example: "Running"
  - Type: Text

## Functionality

This script blueprint creates a reusable script that:
- Updates an e-paper display with the current dishwasher status
- Shows the state prominently in large red text (70pt)
- Displays a timestamp showing when the status was last updated
- Shows a silverware icon to indicate dishwasher context
- Provides visual indicators (arrows) for both Clean and Dirty states
- Uses white background with black and red text for clarity
- Sets a 5-minute TTL (time-to-live) for the display update

## Display Layout

The e-paper display shows:
- **Top Center**: Large state text (Clean/Dirty/Running) in red
- **Left Side**: Silverware icon
- **Bottom Left**: "Dirty" label with down arrow indicator
- **Bottom Center-Left**: "Clean" label with down arrow indicator
- **Bottom Right**: Timestamp showing "As of MM/DD/YYYY at HH:MM AM/PM"

## Usage Examples

### Creating the Script

```yaml
# Example: Create a script using this blueprint
script:
  update_kitchen_dishwasher_display:
    use_blueprint:
      path: rohankapoorcom/update-dishwasher-epaper-display.yaml
      input:
        epaper_tag: 1234567890abcdef  # Your e-paper tag device ID
```

### Calling the Script

```yaml
# Call the script with a state value
- action: script.update_kitchen_dishwasher_display
  data:
    state: "Clean"
```

### Integration with Automation

```yaml
# Example: Update display when dishwasher finishes
- alias: "Dishwasher Complete"
  trigger:
    - platform: state
      entity_id: sensor.dishwasher_state
      to: "off"
  action:
    - action: script.update_kitchen_dishwasher_display
      data:
        state: "Clean"
```

## Display Configuration

The script uses the `open_epaper_link.drawcustom` action with the following parameters:
- **background**: white
- **rotate**: 0 (no rotation)
- **ttl**: 300 seconds (5 minutes)
- **dither**: false (no dithering)

## Visual Elements

### Text Elements
1. **State Display**
   - Font: ppb.ttf, Size: 70pt, Color: red
   - Position: Center-top (x: 220, y: 64)
   - Anchor: Middle-middle

2. **Timestamp**
   - Font: ppb.ttf, Size: 15pt, Color: black
   - Position: Bottom-right (x: 375, y: 160)
   - Anchor: Right-south
   - Format: "As of MM/DD/YYYY at HH:MM AM/PM"

3. **State Labels**
   - "Dirty" label: 15pt, left-bottom (x: 15, y: 130)
   - "Clean" label: 15pt, left-bottom (x: 100, y: 130)

### Icon Elements
1. **Silverware Icon**
   - Icon: silverware-clean
   - Position: Left side (x: 40, y: 64)
   - Size: 60pt, Color: black

2. **Arrow Indicators**
   - Down arrows below Dirty and Clean labels
   - Size: 25pt, Color: red
   - Positions: (x: 33, y: 160) and (x: 125, y: 160)

## Dependencies

- **OpenEPaperLink Integration**: Required for e-paper display control
  - Installation: Available through HACS
  - GitHub: [OpenEPaperLink/Home_Assistant_Integration](https://github.com/OpenEPaperLink/Home_Assistant_Integration)

- **E-Paper Display Hardware**: Compatible OpenEPaperLink e-paper tag
  - Hardware: 2.9" or larger e-paper display recommended
  - Display resolution: 400x300 or similar

## Related Files

- `packages/appliances.yaml`: Dishwasher sensor and automation configuration
- `blueprints/automation/rohankapoorcom/solum-m3-epaper-tag-buttons.yaml`: E-paper button automation blueprint

## Notes

- The display layout is optimized for 2.9" e-paper displays with 400x300 resolution
- The TTL (time-to-live) of 300 seconds means the display will refresh every 5 minutes if the script is called frequently
- The timestamp uses local time formatting (12-hour format with AM/PM)
- The script supports three common dishwasher states: Clean, Dirty, and Running
- The ppb.ttf font should be installed on the OpenEPaperLink hub
- Display updates may take a few seconds to appear on the e-paper tag due to e-paper refresh rates
- The white background with black/red text provides good contrast and readability
- Arrow indicators help users quickly identify which state button corresponds to which action

## Best Practices

1. **State Management**: Maintain a dishwasher state sensor to track current status
2. **Automation Integration**: Trigger the script when dishwasher state changes
3. **Manual Controls**: Create automations with e-paper tag buttons to manually update state
4. **Error Handling**: Implement fallback logic if the e-paper tag is unavailable
5. **Display Refresh**: Consider the 5-minute TTL when planning update frequency

---
*This documentation is part of the [Blueprint Documentation Index](../README.md)*
