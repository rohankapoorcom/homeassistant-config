# Generate Home Assistant Blueprint

**Description:** Create a reusable Home Assistant automation blueprint based on similar automations  
**Version:** 1.0

## Overview

You are tasked with creating a Home Assistant automation blueprint that consolidates similar automations into a reusable template. This prompt guides you through the process of analyzing existing automations, designing a flexible blueprint, and implementing it correctly.

## Process Steps

### Step 1: Analysis Phase
**Goal:** Identify similar automations that can be consolidated

**Tasks:**
- Search the codebase for automations with similar patterns, triggers, or actions
- Document the common elements and variations between automations
- Identify which inputs should be configurable vs. fixed
- Note any optional vs. required components

### Step 2: Blueprint Design
**Goal:** Design the blueprint structure and inputs

**Tasks:**
- Define clear, generic input names (avoid room-specific terms)
- Use appropriate selectors for each input type
- Set sensible defaults for optional inputs
- Write clear descriptions for each input
- Plan the trigger structure
- Design the action logic with choose blocks for different scenarios

### Step 3: Implementation
**Goal:** Implement the blueprint with correct syntax

**Tasks:**
- Use proper YAML structure with blueprint metadata
- Implement triggers using correct platform syntax
- Use variables section for inputs referenced in templates
- Use `!input` directly for simple values (entity_id, delay, offset)
- Handle optional inputs safely in templates
- Use `action:` syntax instead of `service:` for service calls
- Implement action inputs using `sequence: !input` pattern

### Step 4: Testing and Validation
**Goal:** Ensure the blueprint works correctly

**Tasks:**
- Run yamllint to check syntax
- Test blueprint with sample inputs
- Verify all triggers and conditions work
- Check that optional inputs are handled safely
- Ensure custom actions execute correctly

### Step 5: Replacement and Documentation
**Goal:** Replace original automations and document the blueprint

**Tasks:**
- Replace each original automation with blueprint instance
- Preserve original IDs, aliases, and descriptions
- Commit each replacement independently
- Generate comprehensive documentation using the documentation prompt
- Update README files with new blueprint information

## Blueprint Template

### Metadata Structure
```yaml
blueprint:
  name: "Blueprint Name"
  description: >-
    Comprehensive description of what the blueprint does,
    its features, and use cases. Keep under 120 characters per line.
  domain: automation
  input:
    # Required inputs first
    entity_input:
      name: "Entity Input Name"
      description: "Clear description of what this input does"
      selector:
        entity:
          domain: "appropriate_domain"
    
    # Optional inputs with defaults
    optional_input:
      name: "Optional Input Name"
      description: "Description of optional functionality"
      selector:
        entity:
          domain: "appropriate_domain"
      default: ""
    
    # Action inputs for custom actions/callbacks
    custom_action:
      name: "Custom Action"
      description: "Action to run for custom behavior (optional)"
      default: []
      selector:
        action: {}
```

### Variables Section
```yaml
variables:
  # Only include inputs that are used in templates
  optional_input: !input optional_input
```

### Triggers
```yaml
triggers:
  # Sun-based triggers
  - platform: sun
    event: sunset
  - platform: sun
    event: sunrise
    offset: !input sunrise_offset
  
  # State triggers
  - trigger: state
    entity_id: !input state_sensor
    to: 'off'
  
  # System triggers
  - trigger: homeassistant
    event: start
  - trigger: event
    event_type: automation_reloaded
```

### Conditions
```yaml
conditions:
  # Sun conditions
  - condition: sun
    after: sunset
  - condition: sun
    after: sunrise
    after_offset: !input sunrise_offset
  
  # State conditions with safe template handling
  - condition: template
    value_template: >-
      {% set sensor = optional_input | default('') %}
      {{ true if sensor == '' or states(sensor) == 'unknown' else is_state(sensor, 'off') }}
```

### Actions
```yaml
actions:
  - choose:
      # Close action branch
      - conditions:
          - condition: template
            value_template: "{{ is_state(state_sensor, 'off') }}"
        sequence:
          - delay: !input close_delay
          - action: service_name.service_action
            target:
              entity_id: !input entity_input
          - sequence: !input custom_action
      
      # Open action branch
      - conditions:
          - condition: sun
            after: sunrise
            after_offset: !input sunrise_offset
        sequence:
          - wait_template: >-
              {% set sensor = optional_input | default('') %}
              {{ true if sensor == '' or states(sensor) == 'unknown' else is_state(sensor, 'off') }}
          - action: service_name.service_action
            target:
              entity_id: !input entity_input
          - sequence: !input custom_action
  mode: single
  max_exceeded: silent
```

## Best Practices

### Naming
- Use generic, descriptive names for inputs (e.g., `cover_entity` not `living_room_curtains`)
- Make input names self-explanatory
- Avoid room-specific or device-specific terminology

### Inputs
- Required inputs should not have defaults
- Optional inputs should have appropriate defaults (`""` for entities, `[]` for actions)
- Use appropriate selectors for each input type
- Write clear, concise descriptions for each input

### Syntax
- Use variables section only for inputs referenced in templates
- Use `!input` directly for simple values (entity_id, delay, offset)
- Use `action:` syntax instead of `service:` for service calls
- Handle optional inputs safely with `|default('')` and `states()` checks
- Use `sequence: !input` for action inputs that return lists of actions

### Templates
- Always guard optional inputs in templates
- Use `states()` function to safely check entity states
- Prefer short-circuiting conditionals over `iif()` filter
- Use template variables for complex expressions

### Structure
- Use choose blocks for different action scenarios
- Group related conditions together
- Use meaningful aliases for action sequences
- Set appropriate mode and max_exceeded values

## Common Patterns

### Sun-Based Automation
**Description:** For automations that respond to sun events

**Triggers:**
```yaml
- platform: sun
  event: sunset
- platform: sun
  event: sunrise
  offset: !input sunrise_offset
```

**Conditions:**
```yaml
- condition: sun
  after: sunset
- condition: sun
  after: sunrise
  after_offset: !input sunrise_offset
```

### State-Based Automation
**Description:** For automations that respond to entity state changes

**Triggers:**
```yaml
- trigger: state
  entity_id: !input sensor_entity
  to: 'off'
```

**Conditions:**
```yaml
- condition: template
  value_template: "{{ is_state('!input sensor_entity', 'off') }}"
```

### Optional Sensor Handling
**Description:** Safe handling of optional sensors in templates

**Pattern:**
```yaml
{% set sensor = optional_input | default('') %}
{{ true if sensor == '' or states(sensor) == 'unknown' else is_state(sensor, 'off') }}
```

### Action Inputs
**Description:** Proper handling of action inputs that return lists

**Pattern:**
```yaml
- sequence: !input custom_action
```

## Validation Checklist

### Syntax
- [ ] Run yamllint to check for syntax errors
- [ ] Verify all `!input` references are valid
- [ ] Check that variables section includes all templated inputs
- [ ] Ensure `action:` syntax is used instead of `service:`

### Functionality
- [ ] Test blueprint with sample inputs
- [ ] Verify all triggers fire correctly
- [ ] Check that conditions evaluate properly
- [ ] Ensure optional inputs are handled safely
- [ ] Test custom actions execute correctly

### Replacement
- [ ] Preserve original automation IDs
- [ ] Preserve original automation aliases
- [ ] Preserve original automation descriptions
- [ ] Commit each replacement independently

### Documentation
- [ ] Use the documentation prompt to generate comprehensive blueprint documentation
- [ ] Update README files with new blueprint
- [ ] Include usage examples
- [ ] Document all inputs and their purposes

## Examples

### Sun-Based Cover Control
**Description:** Blueprint for sun-based curtain/shade control

**Key Features:**
- Opens covers after sunrise (configurable offset)
- Closes covers after sunset or when windows/doors close
- Optional presence sensor check before opening
- Customizable action callbacks
- Window/door status integration

**Inputs:**
- `cover_entity`: Cover entity to control
- `open_status_sensor`: Binary sensor for window/door status
- `sunrise_offset`: Time offset after sunrise to open
- `close_delay`: Delay before closing
- `presence_sensor`: Optional presence sensor
- `custom_action`: Optional custom actions

## Troubleshooting

### Common Issues

**Problem:** "Missing input" error  
**Solution:** Add default value to optional inputs

**Problem:** "expected dictionary" error with action inputs  
**Solution:** Use `sequence: !input` instead of `- !input` for action lists

**Problem:** Template rendering failure with optional inputs  
**Solution:** Use `|default('')` and `states()` function for safe evaluation

**Problem:** LEGACY_SYNTAX yamllint warnings  
**Solution:** Use `!input` directly for simple values, variables section for templated inputs

## Documentation Generation

After creating your blueprint, use the documentation prompt to generate comprehensive documentation:

1. **Use the Documentation Prompt:** Reference `@homeassistant-documentation.xml` to generate blueprint documentation
2. **Include All Details:** Ensure documentation covers:
   - Blueprint purpose and functionality
   - All input parameters with descriptions
   - Trigger explanations
   - Action sequences
   - Usage examples
   - Configuration options
3. **Update Documentation Files:** Add the new blueprint to relevant README files and index pages
4. **Verify Examples:** Ensure all examples use concrete values, not `!input` tags

## Key Learnings from Implementation

Based on real-world blueprint development experience:

1. **Safe Optional Input Handling:** Always use `|default('')` and `states()` function to prevent template rendering failures
2. **Action Input Lists:** Use `sequence: !input` pattern for action inputs that return lists of actions
3. **Variables Section:** Only include inputs that are referenced in templates, use `!input` directly for simple values
4. **Syntax Choices:** Use `action:` instead of `service:` for service calls in blueprints
5. **YAML Formatting:** Keep lines under 120 characters, use folded style (`>-`) for long descriptions
6. **Metadata Preservation:** Always preserve original automation IDs, aliases, and descriptions when replacing
7. **Incremental Commits:** Commit each automation replacement independently for better change tracking
8. **Comprehensive Testing:** Run yamllint, test with sample inputs, and verify all functionality before considering complete
