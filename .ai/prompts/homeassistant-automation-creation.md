# Home Assistant Automation Creation

**Description:** A comprehensive prompt for creating Home Assistant automations following established patterns, conventions, and best practices. This prompt ensures automations are properly structured, documented, and integrated into the package-based organization system.

## Context

You are creating Home Assistant automations for a well-organized configuration repository that uses:
- Package-based organization in the packages/ directory
- Comprehensive documentation following established patterns
- Consistent naming conventions and structure
- Integration with existing blueprints and custom components
- Proper entity management and customization

The goal is to create automations that:
1. Follow established patterns and conventions
2. Are properly documented using the documentation prompt
3. Integrate seamlessly with existing packages
4. Use appropriate triggers, conditions, and actions
5. Include proper error handling and edge cases
6. Maintain consistency with the overall system architecture

## Instructions

When creating Home Assistant automations, follow these comprehensive guidelines:

### 1. **Package Organization**
- **CRITICAL**: Determine the appropriate package for the automation based on functionality
- **Feature-based packages**: Cross-room functionality (security, notifications, weather, etc.)
- **Room-based packages**: Single room functionality (office, kitchen, bedroom, etc.)
- **Integration packages**: Third-party service configurations (assistant, presence, tablets, etc.)
- **CRITICAL**: Use existing package files when possible, create new packages only when necessary
- **CRITICAL**: Follow the established package naming convention (snake_case)

### 2. **Automation Structure**
- **CRITICAL**: Always include a unique ID using proper GUID format (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
- **CRITICAL**: Generate GUIDs using reliable tools (see GUID Generation Tools section below)
- **CRITICAL**: Use descriptive alias names that clearly indicate the automation's purpose
- **CRITICAL**: Include concise descriptions explaining what the automation does (2-3 lines maximum)
- **CRITICAL**: Use proper mode settings (single, restart, queued, parallel)
- **CRITICAL**: Structure triggers, conditions, and actions logically and clearly

### 3. **Blueprint Integration**
- **CRITICAL**: Check if an existing blueprint can be used before creating custom automations
- **CRITICAL**: Use blueprints from the repository owner (rohankapoorcom) when applicable
- **CRITICAL**: Reference blueprints using the correct path format (rohankapoorcom/blueprint-name.yaml)
- **CRITICAL**: Provide all required blueprint inputs with appropriate entity IDs
- **CRITICAL**: Document blueprint usage in automation descriptions

### 4. **Entity Management**
- **CRITICAL**: Use existing entities when possible, create new ones only when necessary
- **CRITICAL**: Follow established entity naming conventions (domain.entity_name format)
- **CRITICAL**: Use proper entity IDs that match the device/functionality
- **CRITICAL**: Include entity validation and error handling
- **CRITICAL**: Reference entities using their full entity_id format

### 5. **Trigger Design**
- **CRITICAL**: Use appropriate trigger types (state, time, event, device, etc.)
- **CRITICAL**: Include proper trigger conditions and filters
- **CRITICAL**: Consider edge cases and multiple trigger scenarios
- **CRITICAL**: Use time-based triggers with appropriate patterns
- **CRITICAL**: Include proper trigger validation and error handling

### 6. **Condition Logic**
- **CRITICAL**: Use logical conditions to prevent unwanted automation execution
- **CRITICAL**: Include time-based conditions when appropriate
- **CRITICAL**: Use state conditions to validate entity states
- **CRITICAL**: Include presence detection conditions when relevant
- **CRITICAL**: Use template conditions for complex logic
- **CRITICAL**: Use alias field for condition documentation instead of Jinja2 comments
- **CRITICAL**: Include safety checks when using time-based delays (for: minutes: X)

### 7. **Action Implementation**
- **CRITICAL**: Use appropriate action types (service calls, scripts, delays, etc.)
- **CRITICAL**: Include proper error handling and fallback actions
- **CRITICAL**: Use service calls with correct target entities
- **CRITICAL**: Include appropriate delays and timeouts
- **CRITICAL**: Use template actions for dynamic behavior

### 8. **Documentation Requirements**
- **CRITICAL**: Create comprehensive documentation using the homeassistant-documentation.md prompt
- **CRITICAL**: Document the automation's purpose, triggers, conditions, and actions
- **CRITICAL**: Include entity references and dependencies
- **CRITICAL**: Document integration with other automations and packages
- **CRITICAL**: Include troubleshooting information and edge cases
- **CRITICAL**: Update the appropriate documentation index files

### 9. **Integration Standards**
- **CRITICAL**: Ensure compatibility with existing custom integrations
- **CRITICAL**: Use proper MQTT topics and payloads when applicable
- **CRITICAL**: Follow established notification patterns
- **CRITICAL**: Integrate with existing presence detection systems
- **CRITICAL**: Use established security and access control patterns

### 10. **Testing and Validation**
- **CRITICAL**: Run `./tests/test-config.sh` before committing any changes
- **CRITICAL**: Fix all yamllint errors before pushing to repository
- **CRITICAL**: Test against current HA version (2025.1.1) and other versions
- **CRITICAL**: Verify GUID uniqueness across all entities
- **CRITICAL**: Include proper error handling and edge case management
- **CRITICAL**: Test automation logic with various entity states
- **CRITICAL**: Validate trigger conditions and action sequences
- **CRITICAL**: Ensure automation doesn't conflict with existing automations
- **CRITICAL**: Include proper logging and debugging information
- **CRITICAL**: Test automations in safe environment before deployment
- **CRITICAL**: Verify integration compatibility and dependencies

### 11. **Package File Structure**
- **CRITICAL**: Follow the established package header format with author, date, package name, and description
- **CRITICAL**: Include proper YAML structure with homeassistant.customize section
- **CRITICAL**: Use package.node_anchors for consistent customization
- **CRITICAL**: Organize sections logically (sensors, binary_sensors, scripts, automations, etc.)
- **CRITICAL**: Include proper comments and section dividers

### 12. **Customization Integration**
- **CRITICAL**: Include proper entity customization in the package
- **CRITICAL**: Use package-specific customization anchors
- **CRITICAL**: Set appropriate entity attributes (friendly_name, icon, etc.)
- **CRITICAL**: Include proper device_class and state_class settings
- **CRITICAL**: Use consistent naming patterns for customizations

## Condition Documentation Standards

### Use Alias Instead of Comments
- **CRITICAL**: Use the `alias` field for condition documentation instead of Jinja2 comments
- **CRITICAL**: Keep alias descriptions concise but descriptive (under 120 characters for yamllint compliance)
- **CRITICAL**: Explain the purpose and safety checks performed by conditions
- **CRITICAL**: Avoid cluttering templates with `{# #}` comment syntax

### Example:
```yaml
conditions:
  - alias: "Safety check: Verify at least one sensor is on battery power to prevent false notifications"
    condition: template
    value_template: >-
      {% set sensor1 = is_state('sensor.example_1', 'target_state') %}
      {% set sensor2 = is_state('sensor.example_2', 'target_state') %}
      {{ sensor1 or sensor2 }}
```

## Trigger Type Selection Guidelines

### State Triggers (Use When)
- **CRITICAL**: Use `state` triggers for "any change detection" scenarios
- **CRITICAL**: Use `state` triggers when you need dynamic threshold logic
- **CRITICAL**: Use `state` triggers for complex calculations involving multiple entities
- **CRITICAL**: Use `state` triggers when the threshold is calculated dynamically (e.g., temperature differences)

### Numeric State Triggers (Use When)
- **CRITICAL**: Use `numeric_state` triggers for "static threshold monitoring"
- **CRITICAL**: Use `numeric_state` triggers when you have a fixed threshold value
- **CRITICAL**: Use `numeric_state` triggers for simple above/below comparisons
- **CRITICAL**: Use `numeric_state` triggers when the threshold doesn't change based on other entities

### Example Decision Tree:
```yaml
# Use state trigger for dynamic calculations
triggers:
  - trigger: state
    entity_id: sensor.temperature
    # Logic: Calculate difference with another sensor dynamically

# Use numeric_state trigger for fixed thresholds  
triggers:
  - trigger: numeric_state
    entity_id: sensor.temperature
    above: 25
    # Logic: Simple above/below comparison
```

## Safety Check Condition Patterns

### Entity Availability Checks
- **CRITICAL**: Always check entity availability before using in calculations
- **CRITICAL**: Use `states('entity_id') != 'unavailable'` for sensor states
- **CRITICAL**: Use `state_attr('entity_id', 'attribute') is not none` for attributes
- **CRITICAL**: Never assume entities are available without verification

### False Notification Prevention
- **CRITICAL**: Always include safety checks when using time-based delays (`for: minutes: X`)
- **CRITICAL**: Verify current state at execution time, not just trigger time
- **CRITICAL**: Use template conditions to validate that the triggering condition still exists

### Common Safety Check Patterns:
```yaml
# For sensor states
conditions:
  - alias: "Safety check: Verify sensor is available"
    condition: template
    value_template: "{{ states('sensor.example') != 'unavailable' }}"

# For entity attributes  
conditions:
  - alias: "Safety check: Verify attribute is available"
    condition: template
    value_template: "{{ state_attr('climate.example', 'temperature') is not none }}"

# For multiple entities
conditions:
  - alias: "Safety check: Verify all required entities are available"
    condition: template
    value_template: >-
      {{ states('sensor.temp1') != 'unavailable' and 
         state_attr('climate.thermostat', 'temperature') is not none }}

# Time-based safety check
triggers:
  - trigger: state
    entity_id: sensor.example_sensor
    to: 'target_state'
    for:
      minutes: 10
conditions:
  - alias: "Safety check: Verify sensor is still in target state to prevent false notifications"
    condition: template
    value_template: "{{ is_state('sensor.example_sensor', 'target_state') }}"

# Multi-Sensor Safety Check Pattern:
conditions:
  - alias: "Safety check: Verify at least one sensor is in target state to prevent false notifications"
    condition: template
    value_template: >-
      {% set sensor1 = is_state('sensor.sensor1', 'target_state') %}
      {% set sensor2 = is_state('sensor.sensor2', 'target_state') %}
      {{ sensor1 or sensor2 }}
```

## Notification Message Best Practices

### Message Structure
- **CRITICAL**: Use dynamic alert messages that clearly identify which system triggered the alert
- **CRITICAL**: Group related information logically (e.g., battery capacity and runtime together)
- **CRITICAL**: Use visual separators (blank lines) between different information sections
- **CRITICAL**: Include comprehensive status information for troubleshooting
- **CRITICAL**: Provide clear action requests

### Template Logic for Dynamic Messages
```yaml
message: >-
  {% set system1_battery = is_state('sensor.system1', 'Battery') %}
  {% set system2_battery = is_state('sensor.system2', 'Battery') %}
  {% if system1_battery and system2_battery %}
    ⚠️ BOTH System1 AND System2 are on battery power for 10+ minutes!
  {% elif system1_battery %}
    ⚠️ System1 switched to battery for 10+ minutes!
  {% elif system2_battery %}
    ⚠️ System2 switched to battery for 10+ minutes!
  {% endif %}
  
  Current Status:
  • System1: {{ states('sensor.system1') }}
  • System2: {{ states('sensor.system2') }}
  
  Detailed Information:
  • System1 Battery: {{ states('sensor.system1_battery') }}%
  • System1 Runtime: {{ states('sensor.system1_runtime') }} minutes
  
  • System2 Battery: {{ states('sensor.system2_battery') }}%
  • System2 Runtime: {{ states('sensor.system2_runtime') }} minutes
  
  Time: {{ now().strftime('%m/%d/%Y at %I:%M %p') }}
  
  Please check status and take appropriate action.
```

## Automation Description Best Practices

### Concise Descriptions
- **CRITICAL**: Keep descriptions concise but informative (2-3 lines maximum)
- **CRITICAL**: Focus on what the automation does, not who it notifies (unless critical)
- **CRITICAL**: Include key timing information (e.g., "for more than 10 minutes")
- **CRITICAL**: Mention which sensors/entities are monitored

### Good Examples:
```yaml
description: >-
  Notifies when server rack switches to battery power for more than 10 minutes.
  Monitors server rack backup and UPS power source sensors.
```

### Avoid:
- Redundant information already covered by alias
- Overly verbose descriptions
- Information that doesn't add value

## Eventual Consistency Patterns

### Startup Triggers (CRITICAL)
- **CRITICAL**: Always include `homeassistant.start` trigger for eventual consistency
- **CRITICAL**: Always include `automation_reloaded` trigger for configuration changes
- **CRITICAL**: These triggers ensure automation state is correct after restarts/reloads
- **CRITICAL**: Place startup triggers FIRST in the trigger list

### Standard Pattern:
```yaml
triggers:
  - trigger: homeassistant
    event: start
  - trigger: event
    event_type: automation_reloaded
  - trigger: state
    entity_id: sensor.example
    # ... other triggers
```

### When to Use:
- **ALWAYS**: For automations that maintain state or perform calculations
- **ALWAYS**: For automations that depend on current entity states
- **ALWAYS**: For automations that need to be "caught up" after restarts
- **NEVER**: For purely reactive automations that don't need state consistency

## YAML Formatting Requirements

### Line Length Compliance
- **CRITICAL**: Keep all lines under 120 characters for yamllint compliance
- **CRITICAL**: Break long template expressions across multiple lines when needed
- **CRITICAL**: Use proper indentation (2 spaces) consistently
- **CRITICAL**: When breaking lines, maintain logical grouping of related expressions

### Trailing Spaces
- **CRITICAL**: Never include trailing spaces in YAML files
- **CRITICAL**: Run yamllint after making changes to catch formatting issues
- **CRITICAL**: Use proper blank line formatting (no trailing spaces on empty lines)
- **CRITICAL**: Check for trailing spaces after line length fixes

### Template Formatting Best Practices
```yaml
# Good: Logical grouping and proper line breaks
value_template: >-
  {% set current_temp = states('sensor.temp1') | float(0) %}
  {% set target_temp = state_attr('climate.thermostat', 'temperature') | float(0) %}
  {% set temp_diff = current_temp - target_temp %}
  {{ temp_diff > 8 }}

# Avoid: Unnecessary line breaks that hurt readability
value_template: >-
  {% set current_temp = states('sensor.temp1') | 
    float(0) %}
```

## GUID Generation Tools

### Recommended Tools for Generating GUIDs

#### Command Line Tools
- **uuidgen** (Linux/macOS): `uuidgen` - Generates standard UUIDs
- **PowerShell** (Windows): `[System.Guid]::NewGuid()` - Generates .NET GUIDs
- **Python**: `python -c "import uuid; print(uuid.uuid4())"` - Generates UUID4

#### Online Tools
- **UUID Generator**: https://www.uuidgenerator.net/
- **Online UUID Generator**: https://www.uuidgenerator.net/version4
- **GUID Generator**: https://www.guidgenerator.com/

#### IDE Extensions
- **VS Code**: "UUID Generator" extension
- **IntelliJ/PyCharm**: Built-in UUID generator
- **Sublime Text**: "UUID Generator" package

#### Programming Languages
- **JavaScript**: `crypto.randomUUID()` (modern browsers/Node.js)
- **Python**: `import uuid; uuid.uuid4()`
- **C#**: `System.Guid.NewGuid()`
- **Java**: `java.util.UUID.randomUUID()`

### GUID Format Requirements
- **Format**: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (8-4-4-4-12 hexadecimal digits)
- **Version**: Use UUID4 (random) for automation IDs
- **Uniqueness**: Ensure each automation has a globally unique identifier
- **Consistency**: Use lowercase letters (a-f) and numbers (0-9)

### Example GUID Generation Commands
```bash
# Linux/macOS
uuidgen

# Windows PowerShell
[System.Guid]::NewGuid()

# Python
python -c "import uuid; print(str(uuid.uuid4()))"

# Node.js
node -e "console.log(require('crypto').randomUUID())"
```

## Automation Template

```yaml
###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  {current_date}
#  @package      :  {package_name}
#  @description  :  {package_description}
###############################################################################
---
homeassistant:
  customize:
    ################################################
    ## Node Anchors
    ################################################

    package.node_anchors:
      customize: &customize
        package: '{package_name}'

# Additional package configurations (sensors, scripts, etc.)

automation:
  - id: {unique_guid}  # Generate using: uuidgen, [System.Guid]::NewGuid(), or online tools
    alias: '{automation_alias}'
    description: >-
      {automation_description}
    mode: {automation_mode}
    triggers:
      - trigger: {trigger_type}
        {trigger_configuration}
    conditions:
      - condition: {condition_type}
        {condition_configuration}
    actions:
      - action: {action_type}
        {action_configuration}
```

## Package Selection Guidelines

### Feature-based Packages (Cross-room functionality)
- **security.yaml**: Security systems, locks, cameras, access control
- **notifications.yaml**: Notification management, alerts, messaging
- **weather.yaml**: Weather monitoring, alerts, forecasting
- **weatherman.yaml**: Advanced weather data processing
- **air_quality.yaml**: Air quality monitoring and alerts
- **media_music.yaml**: Whole-home audio, entertainment systems
- **appliances.yaml**: Appliance control and monitoring
- **assistant.yaml**: Voice assistant integration
- **presence.yaml**: Presence detection and automation
- **tablets.yaml**: Tablet interface management

### Room-based Packages (Single room functionality)
- **office.yaml**: Office automation, productivity features
- **kitchen/**: Kitchen automation, appliance control
- **living_room/**: Living room entertainment, lighting
- **master_bedroom.yaml**: Bedroom comfort, lighting
- **master_bathroom.yaml**: Bathroom automation
- **downstairs_bathroom.yaml**: Downstairs bathroom features
- **hallway_bathroom.yaml**: Hallway bathroom automation
- **hallway.yaml**: Hallway lighting, motion control
- **downstairs_hallway.yaml**: Downstairs hallway automation
- **stairway.yaml**: Stairway lighting, safety features
- **garage.yaml**: Garage door control, monitoring
- **front_door.yaml**: Entry door security, access control
- **guest_room.yaml**: Guest room automation
- **gym.yaml**: Home gym automation

### Integration Packages (Third-party services)
- **default_config.yaml**: Default configuration settings
- **server_rack.yaml**: Server infrastructure monitoring

## Common Automation Patterns

### Motion-activated Lighting
```yaml
- id: {guid}
  alias: '{room} Motion Light'
  description: 'Turns on {room} lights when motion is detected'
  mode: restart
  triggers:
    - trigger: state
      entity_id: binary_sensor.{room}_motion
      to: 'on'
  conditions:
    - condition: state
      entity_id: light.{room}_lights
      state: 'off'
    - condition: time
      after: '06:00:00'
      before: '23:00:00'
  actions:
    - action: light.turn_on
      target:
        entity_id: light.{room}_lights
      data:
        brightness: 128
        transition: 2
    - action: delay
      duration: '00:05:00'
    - action: light.turn_off
      target:
        entity_id: light.{room}_lights
      data:
        transition: 2
```

### Time-based Automation with Safety Check
```yaml
- id: {guid}
  alias: '{automation_name}'
  description: '{automation_description}'
  mode: single
  triggers:
    - trigger: state
      entity_id: {entity_id}
      to: '{target_state}'
      for:
        minutes: 10
  conditions:
    - alias: "Safety check: Verify entity is still in target state to prevent false notifications"
      condition: template
      value_template: "{{ is_state('{entity_id}', '{target_state}') }}"
  actions:
    - action: {service}
      target:
        entity_id: {target_entity}
      data:
        {service_data}
```

### Multi-Sensor Notification with Dynamic Messages
```yaml
- id: {guid}
  alias: '{automation_name}'
  description: '{automation_description}'
  mode: single
  triggers:
    - trigger: state
      entity_id: sensor.sensor1
      to: 'Battery'
      for:
        minutes: 10
    - trigger: state
      entity_id: sensor.sensor2
      to: 'Battery'
      for:
        minutes: 10
  conditions:
    - alias: "Safety check: Verify at least one sensor is on battery power to prevent false notifications"
      condition: template
      value_template: >-
        {% set sensor1_battery = is_state('sensor.sensor1', 'Battery') %}
        {% set sensor2_battery = is_state('sensor.sensor2', 'Battery') %}
        {{ sensor1_battery or sensor2_battery }}
  actions:
    - action: notify.rohan_kapoor
      data:
        title: '{notification_title}'
        message: >-
          {% set sensor1_battery = is_state('sensor.sensor1', 'Battery') %}
          {% set sensor2_battery = is_state('sensor.sensor2', 'Battery') %}
          {% if sensor1_battery and sensor2_battery %}
            ⚠️ BOTH Sensor1 AND Sensor2 are on battery power for 10+ minutes!
          {% elif sensor1_battery %}
            ⚠️ Sensor1 switched to battery for 10+ minutes!
          {% elif sensor2_battery %}
            ⚠️ Sensor2 switched to battery for 10+ minutes!
          {% endif %}
          
          Current Status:
          • Sensor1: {{ states('sensor.sensor1') }}
          • Sensor2: {{ states('sensor.sensor2') }}
          
          Time: {{ now().strftime('%m/%d/%Y at %I:%M %p') }}
          
          Please check status and take appropriate action.
```

### Blueprint Usage
```yaml
- id: {guid}
  alias: '{automation_name}'
  description: 'Uses blueprint for {device_type} automation'
  use_blueprint:
    path: rohankapoorcom/{blueprint_name}.yaml
    input:
      {blueprint_input_1}: {entity_id_1}
      {blueprint_input_2}: {entity_id_2}
```

## Documentation Integration Requirements

### Automation Documentation Structure
- **CRITICAL**: Document automations ONLY in package documentation files (docs/packages/)
- **CRITICAL**: Do NOT create separate individual automation files unless explicitly requested
- **CRITICAL**: Follow established patterns - automations are documented within their package context
- **CRITICAL**: Update package documentation to include new automation details
- **CRITICAL**: Maintain consistency with existing documentation structure
- **CRITICAL**: Use the homeassistant-documentation.md prompt for documentation
- **CRITICAL**: Include automation purpose, triggers, conditions, and actions
- **CRITICAL**: Document entity dependencies and integration points
- **CRITICAL**: Include troubleshooting information and edge cases

### Package Documentation
- **CRITICAL**: Update package documentation in docs/packages/
- **CRITICAL**: Include new automation in package documentation
- **CRITICAL**: Update package functionality descriptions
- **CRITICAL**: Include automation in package entity listings

### Index Updates
- **CRITICAL**: Update docs/automations/README.md with new automation (if individual files are created)
- **CRITICAL**: Update docs/packages/README.md with package changes
- **CRITICAL**: Maintain alphabetical ordering in all lists
- **CRITICAL**: Include proper cross-references between documentation files

## Testing Requirements and Validation

### Pre-Commit Testing (CRITICAL)
- **CRITICAL**: Run `./tests/test-config.sh` before committing any changes
- **CRITICAL**: Fix all yamllint errors before pushing to repository
- **CRITICAL**: Test against current HA version (2025.1.1) and other versions
- **CRITICAL**: Verify GUID uniqueness across all entities
- **CRITICAL**: Ensure no secrets are committed to repository

### Automation Testing (CRITICAL)
- **CRITICAL**: Test automation logic with various entity states
- **CRITICAL**: Validate trigger conditions and action sequences
- **CRITICAL**: Ensure automation doesn't conflict with existing automations
- **CRITICAL**: Test automations in safe environment before deployment
- **CRITICAL**: Verify integration compatibility and dependencies
- **CRITICAL**: Include proper error handling and edge case management
- **CRITICAL**: Test automation with different entity states and conditions

### Configuration Testing (CRITICAL)
- **CRITICAL**: Validate YAML syntax and formatting
- **CRITICAL**: Test package structure and organization
- **CRITICAL**: Verify entity references and dependencies
- **CRITICAL**: Test blueprint integration and inputs
- **CRITICAL**: Validate service calls and data structures

### Documentation Testing (CRITICAL)
- **CRITICAL**: Update all relevant documentation files
- **CRITICAL**: Test documentation links for proper resolution
- **CRITICAL**: Verify cross-references between documentation files
- **CRITICAL**: Ensure documentation follows established patterns

### Testing Commands
```bash
# Full validation (CRITICAL - run before every commit)
./tests/test-config.sh

# YAML linting only
yamllint .

# Home Assistant configuration check only
docker run --rm \
  -v "$(pwd):/config" \
  -v "$(pwd)/tests/travis_secrets.yaml:/config/secrets.yaml:ro" \
  "ghcr.io/home-assistant/home-assistant:stable" \
  python -m homeassistant --config /config --script check_config

# Documentation link validation
./tests/check-docs-links.sh
```

### Testing Checklist (CRITICAL - verify before committing)
- [ ] **Local testing passes** (`./tests/test-config.sh`)
- [ ] **yamllint passes** without errors
- [ ] **No secrets** committed to repository
- [ ] **Documentation updated** following established standards
- [ ] **Automations tested** in safe environment
- [ ] **Integration compatibility** verified
- [ ] **GUIDs used** for all ID fields and verified as unique
- [ ] **Entity references** validated and working
- [ ] **Blueprint inputs** tested and validated
- [ ] **Service calls** tested with proper data structures

## Quality Standards

- **CRITICAL**: Follow established package organization patterns
- **CRITICAL**: Use consistent naming conventions throughout
- **CRITICAL**: Include proper error handling and edge cases
- **CRITICAL**: Document all automations comprehensively
- **CRITICAL**: Test automation logic and integration points
- **CRITICAL**: Ensure compatibility with existing systems
- **CRITICAL**: Use appropriate trigger, condition, and action types
- **CRITICAL**: Include proper entity validation and management
- **CRITICAL**: Follow established blueprint usage patterns
- **CRITICAL**: Maintain consistency with existing automation styles
- **CRITICAL**: Include proper logging and debugging information
- **CRITICAL**: Validate automation doesn't conflict with existing automations
- **CRITICAL**: Use appropriate automation modes and settings
- **CRITICAL**: Include proper service calls and data structures
- **CRITICAL**: Follow established customization patterns
- **CRITICAL**: Update all relevant documentation files
- **CRITICAL**: Maintain proper YAML formatting and structure
- **CRITICAL**: Use consistent comment and section organization
- **CRITICAL**: Include proper package headers and metadata
- **CRITICAL**: Follow established entity naming conventions
- **CRITICAL**: Use appropriate device classes and state classes
- **CRITICAL**: Run comprehensive testing before committing changes
- **CRITICAL**: Fix all linting issues before pushing to repository
- **CRITICAL**: Verify GUID uniqueness across all entities
- **CRITICAL**: Test against multiple Home Assistant versions
- **CRITICAL**: Ensure no secrets are committed to repository

## Examples

### Motion Light Automation
```yaml
###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  12/15/2024
#  @package      :  hallway
#  @description  :  Manages functionality within the hallway
###############################################################################
---
homeassistant:
  customize:
    ################################################
    ## Node Anchors
    ################################################

    package.node_anchors:
      customize: &customize
        package: 'hallway'

automation:
  - id: a1b2c3d4-e5f6-7890-abcd-ef1234567890  # Generated using: uuidgen
    alias: 'Hallway Motion Light'
    description: >-
      Turns on hallway lights when motion is detected and automatically
      turns them off after 5 minutes of no motion
    mode: restart
    triggers:
      - trigger: state
        entity_id: binary_sensor.hallway_motion
        to: 'on'
    conditions:
      - condition: state
        entity_id: light.hallway_lights
        state: 'off'
      - condition: time
        after: '06:00:00'
        before: '23:00:00'
    actions:
      - action: light.turn_on
        target:
          entity_id: light.hallway_lights
        data:
          brightness: 128
          transition: 2
      - action: delay
        duration: '00:05:00'
      - action: light.turn_off
        target:
          entity_id: light.hallway_lights
        data:
          transition: 2
```

### Blueprint-based Automation
```yaml
###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  12/15/2024
#  @package      :  security
#  @description  :  Controls cameras, locks and other security devices
###############################################################################
---
homeassistant:
  customize:
    ################################################
    ## Node Anchors
    ################################################

    package.node_anchors:
      customize: &customize
        package: 'security'

automation:
  - id: b2c3d4e5-f6g7-8901-bcde-f23456789012  # Generated using: [System.Guid]::NewGuid()
    alias: 'Show Front Door Lock Status'
    description: >-
      Utilizes a blueprint to show the Front Door Lock Status on an
      Inovelli LZW30 Switch with LED indicators
    use_blueprint:
      path: rohankapoorcom/inovelli-vzw31-sn-red-series-lock-notifications.yaml
      input:
        lock_entity: lock.front_door_lock
        zwave_device: 64a4dd14224033fa4119a7b1cb66d888
```

### Time-based Automation
```yaml
###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  12/15/2024
#  @package      :  office
#  @description  :  Manages functionality within the office
###############################################################################
---
homeassistant:
  customize:
    ################################################
    ## Node Anchors
    ################################################

    package.node_anchors:
      customize: &customize
        package: 'office'

automation:
  - id: c3d4e5f6-g7h8-9012-cdef-345678901234  # Generated using: python -c "import uuid; print(uuid.uuid4())"
    alias: 'Office Morning Routine'
    description: >-
      Automates the office morning routine by turning on lights,
      adjusting fan speed, and setting desk height for work
    mode: single
    triggers:
      - trigger: time
        at: '08:00:00'
    conditions:
      - condition: time
        weekday:
          - mon
          - tue
          - wed
          - thu
          - fri
      - condition: state
        entity_id: binary_sensor.office_occupancy
        state: 'on'
    actions:
      - action: light.turn_on
        target:
          entity_id: light.office_lights
        data:
          brightness: 255
          transition: 30
      - action: fan.set_percentage
        target:
          entity_id: fan.office_fan
        data:
          percentage: 50
      - action: button.press
        target:
          entity_id: button.standing_desk_preset_2
```

### Multi-Sensor Battery Alert with Safety Check
```yaml
###############################################################################
#  @author       :  Rohan Kapoor
#  @date         :  12/15/2024
#  @package      :  server_rack
#  @description  :  Manages functionality within the Server Rack
###############################################################################
---
homeassistant:
  customize:
    ################################################
    ## Node Anchors
    ################################################

    package.node_anchors:
      customize: &customize
        package: 'server_rack'

automation:
  - id: 2c8ca4d5-b0e5-48c9-9a6d-a3cd60d2a449  # Generated using: uuidgen
    alias: 'Server Rack Battery Power Alert'
    description: >-
      Notifies when server rack switches to battery power for more than 10 minutes.
      Monitors server rack backup and UPS power source sensors.
    mode: single
    triggers:
      - trigger: state
        entity_id: sensor.server_rack_backup_power_source
        to: 'Battery'
        for:
          minutes: 10
      - trigger: state
        entity_id: sensor.ups_source
        to: 'Battery'
        for:
          minutes: 10
    conditions:
      - alias: "Safety check: Verify at least one sensor is on battery power to prevent false notifications"
        condition: template
        value_template: >-
          {% set server_rack_battery = is_state('sensor.server_rack_backup_power_source', 'Battery') %}
          {% set ups_battery = is_state('sensor.ups_source', 'Battery') %}
          {{ server_rack_battery or ups_battery }}
    actions:
      - action: notify.rohan_kapoor
        data:
          title: 'Server Rack Battery Power Alert'
          message: >-
            {% set server_rack_battery = is_state('sensor.server_rack_backup_power_source', 'Battery') %}
            {% set ups_battery = is_state('sensor.ups_source', 'Battery') %}
            {% if server_rack_battery and ups_battery %}
              ⚠️ BOTH Server Rack Backup AND UPS are on battery power for 10+ minutes!
            {% elif server_rack_battery %}
              ⚠️ Server Rack Backup Power Source switched to battery for 10+ minutes!
            {% elif ups_battery %}
              ⚠️ UPS switched to battery power for 10+ minutes!
            {% endif %}

            Current Status:
            • Server Rack Backup: {{ states('sensor.server_rack_backup_power_source') }}
            • UPS Source: {{ states('sensor.ups_source') }}

            Battery Information:
            • UPS Battery Capacity: {{ states('sensor.ups_battery_capacity') }}%
            • UPS Runtime Remaining: {{ states('sensor.ups_runtime_remaining') }} minutes

            • Server Rack Backup Time Remaining: {{ states('sensor.server_rack_backup_time_remaining') }} minutes
            • Server Rack Main Battery: {{ states('sensor.server_rack_backup_main_battery') }}%
            • Server Rack Extra1 Battery: {{ states('sensor.server_rack_backup_extra1_battery') }}%
            • Server Rack Extra2 Battery: {{ states('sensor.server_rack_backup_extra2_battery') }}%

            Time: {{ now().strftime('%m/%d/%Y at %I:%M %p') }}

            Please check power status and take appropriate action.
```

## Integration with Testing Workflow

### Before Creating Automations
1. **Run validation**: Execute `./tests/test-config.sh` to ensure current state works
2. **Check dependencies**: Verify all required integrations and components are available
3. **Create feature branch**: Use `git checkout -b feature/descriptive-name` for significant changes

### During Automation Development
1. **Follow naming conventions**: Use snake_case for files, descriptive names for packages
2. **Use proper YAML formatting**: 2-space indentation, consistent spacing, quote strings when needed
3. **Generate GUIDs**: Use recommended tools for all ID fields
4. **Document changes**: Add comments explaining complex logic or non-standard configurations
5. **Test incrementally**: Validate automation logic as you build it

### Before Committing Automation Changes
1. **Run full validation**: Execute `./tests/test-config.sh`
2. **Check yamllint**: Execute `yamllint .` and fix any errors
3. **Verify GUIDs**: Ensure all ID fields use proper GUIDs and are unique
4. **Test automations**: Verify automations work in safe environment
5. **Update documentation**: Follow documentation standards
6. **Verify no secrets**: Ensure no sensitive data is committed

### Git Workflow Commands
```bash
# Create feature branch
git checkout -b feature/new-automation

# Test before committing
./tests/test-config.sh

# Commit with description
git commit -m "Add new automation with proper testing"

# Push and create PR
git push origin feature/new-automation
```

## Output Format

Use YAML formatting with:
- Proper indentation (2 spaces)
- Clear section organization
- Consistent naming conventions
- Comprehensive comments
- Proper package structure
- Complete automation definitions
- Appropriate entity references
- Proper service calls and data structures
- Include testing validation comments
- Reference testing requirements in documentation
