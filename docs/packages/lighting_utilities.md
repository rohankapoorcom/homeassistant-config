# Lighting Utilities Package

## Overview

The `lighting_utilities` package provides centralized lighting utility scripts for efficient light management across the home.

## Purpose

This utility package provides optimized lighting control scripts that improve performance by reducing unnecessary device communication and improving automation efficiency.

## Package Details

- **Package Name**: `lighting_utilities`
- **Location**: `packages/utilities/lighting_utilities.yaml`
- **Description**: Centralized lighting utility scripts

## Scripts

### Turn Off Lights in Areas

**Script Name**: `turn_off_lights_in_areas`

Turns off only lights that are currently "on" in specified areas, rather than sending turn-off commands to all lights regardless of their state.

#### Features
- **Efficiency**: Only turns off lights that are actually on
- **Reduced Traffic**: Minimizes unnecessary device communication
- **Device Longevity**: Reduces wear on smart switches/devices
- **Parallel Execution**: Supports concurrent execution (max 100 instances)
- **Template Logic**: Uses optimized template patterns from `stairway.yaml`

#### Usage
```yaml
- action: script.turn_off_lights_in_areas
  data:
    areas:
      - kitchen
      - living_room
      - office
```

#### Input Parameters
| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `areas` | List | List of area IDs to turn off lights in | `["kitchen", "living_room", "office"]` |


## Template Logic Optimization

The lighting scripts use optimized template patterns based on the sophisticated logic found in `stairway.yaml`:

### Pattern Used
```yaml
expand(states.light)
| selectattr('entity_id', 'in', area_entities(area))
| selectattr('state', 'eq', 'on')
| map(attribute='entity_id')
| list
```

### Benefits
- **Efficient Filtering**: Uses Home Assistant's native template functions
- **State-Aware**: Only processes lights that are currently "on"
- **Area-Based**: Leverages `area_entities()` for efficient area targeting
- **Performance**: Optimized for minimal processing overhead

## Integration

### Updated Packages

The following packages have been updated to use the efficient lighting scripts:

- `packages/stairway.yaml` - Scene controls
- `packages/garage.yaml` - Relay controls  
- `packages/office.yaml` - Button controls
- `packages/kitchen/kitchen_lights.yaml` - Button controls

### Migration from Direct Area Targeting

#### Before (Inefficient)
```yaml
- action: light.turn_off
  target:
    area_id:
      - kitchen
      - living_room
      - office
```

#### After (Efficient)
```yaml
- action: script.turn_off_lights_in_areas
  data:
    areas:
      - kitchen
      - living_room
      - office
```

## Performance Benefits

### Efficiency Improvements
- **Reduced Network Traffic**: Only sends commands to lights that need them
- **Device Longevity**: Minimizes unnecessary device communication
- **Faster Execution**: Parallel processing with configurable limits
- **Resource Optimization**: Uses Home Assistant's native template functions

### Scalability
- **Parallel Execution**: Supports up to 100 concurrent instances
- **Template Optimization**: Efficient state filtering and entity selection
- **Area-Based Logic**: Leverages Home Assistant's area management

## Testing

The lighting package has been tested with:
- Various area combinations
- Mixed on/off light states
- Unavailable entities
- Empty area lists
- Configuration validation across Home Assistant versions
- Parallel execution scenarios

## Related Documentation

- [Home Assistant Scripts Documentation](https://www.home-assistant.io/docs/scripts/)
- [Home Assistant Templating Documentation](https://www.home-assistant.io/docs/configuration/templating/)
- [Area Entities Function](https://www.home-assistant.io/docs/configuration/templating/#area_entities)

## Maintenance

### Adding New Lighting Scripts
1. Add script definition to `packages/utilities/lighting_utilities.yaml`
2. Follow existing template patterns for efficiency
3. Use parallel mode with appropriate max limits
4. Update this documentation
5. Test across multiple Home Assistant versions

### Updating Existing Scripts
1. Test changes in development environment
2. Validate template logic efficiency
3. Update documentation as needed
4. Run full configuration tests
5. Verify backward compatibility
