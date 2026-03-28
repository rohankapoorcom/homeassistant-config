---
name: generate-homeassistant-blueprint
description: >-
  Guides creation of reusable Home Assistant automation blueprints from similar
  automations: analysis, design, YAML implementation (metadata, variables,
  triggers, conditions, choose/actions), yamllint and functional checks, replacing
  instances while preserving IDs/aliases, and documentation. Use when consolidating
  automations into blueprints, writing blueprint YAML, or refactoring automations
  to blueprint instances.
---

# Generate Home Assistant automation blueprints

## Overview

Create a Home Assistant automation blueprint that consolidates similar automations into a reusable template: analyze existing automations, design inputs and structure, implement correct YAML, validate, replace originals with blueprint instances, and document.

**More examples:** See [`examples.md`](examples.md) in this skill folder (consolidation table, full motion-light blueprint, `use_blueprint` instance, `variables:` for templates, `sequence: !input`, condensed sun/contact cover, pitfalls, validation flow).

## Process steps

### Step 1: Analysis

- Search the codebase for automations with similar patterns, triggers, or actions
- Document common elements and variations
- Decide which inputs are configurable vs fixed; optional vs required

### Step 2: Blueprint design

- Generic input names (avoid room-specific terms)
- Appropriate selectors per input type; sensible defaults for optional inputs
- Clear descriptions; plan triggers and action logic (e.g. `choose` for scenarios)

### Step 3: Implementation

- Correct blueprint metadata and YAML structure
- Triggers with correct platform / `trigger:` syntax
- `variables:` only for inputs used inside templates; `!input` directly for simple values (entity_id, delay, offset)
- Optional inputs safe in templates
- Use `action:` (not `service:`) for service calls
- Action inputs: `sequence: !input` pattern

### Step 4: Testing and validation

- Run yamllint
- Test with sample inputs; verify triggers, conditions, optional inputs, custom actions

### Step 5: Replacement and documentation

- Replace each original automation with a blueprint instance; preserve IDs, aliases, descriptions
- Commit each replacement independently when practical
- Document per project standards (see RULES.md / documentation prompt); update README or index if the repo uses them

## Blueprint template

### Metadata structure

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

### Variables section

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
    to: "off"

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

## Best practices

### Naming

- Generic names (e.g. `cover_entity`, not `living_room_curtains`)
- Self-explanatory input names; avoid room- or device-specific jargon

### Inputs

- Required inputs: no defaults
- Optional: defaults such as `""` for entities, `[]` for actions
- Match selectors to types; short, clear descriptions

### Syntax

- `variables:` only for templated inputs; `!input` elsewhere for simple values
- `action:` not `service:` for service calls
- Optional inputs: `|default('')` and `states()` where needed
- Action lists: `sequence: !input`

### Templates

- Guard optional inputs
- Use `states()` for safe entity checks
- Prefer short-circuiting conditionals over heavy `iif()` where readability matters
- Extract complex expressions to template variables when helpful

### Structure

- `choose` for branches; group related conditions
- Meaningful sequence aliases; set `mode` and `max_exceeded` appropriately

## Common patterns

### Sun-based automation

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

### State-based automation

**Triggers:**

```yaml
- trigger: state
  entity_id: !input sensor_entity
  to: "off"
```

**Conditions** (prefer `condition: state` when the entity is a required input):

```yaml
- condition: state
  entity_id: !input sensor_entity
  state: "off"
```

### Optional sensor in templates

```yaml
{% set sensor = optional_input | default('') %}
{{ true if sensor == '' or states(sensor) == 'unknown' else is_state(sensor, 'off') }}
```

### Action inputs

```yaml
- sequence: !input custom_action
```

## Validation checklist

### Syntax

- [ ] yamllint clean
- [ ] Every `!input` defined in `blueprint.input`
- [ ] `variables:` covers all templated inputs
- [ ] `action:` used instead of `service:`

### Functionality

- [ ] Sample configuration tested
- [ ] Triggers and conditions behave as intended
- [ ] Optional inputs safe when empty
- [ ] Custom actions run

### Replacement

- [ ] Original automation IDs, aliases, descriptions preserved
- [ ] Commits scoped per replacement when practical

### Documentation

- [ ] Blueprint documented per repo standards (see RULES.md)
- [ ] Usage examples with concrete values (not bare `!input` in prose)

## Example: sun-based cover control

- Opens after sunrise (offset); closes after sunset or when window/door closes
- Optional presence check; optional extra actions

**Typical inputs:** `cover_entity`, `open_status_sensor`, `sunrise_offset`, `close_delay`, `presence_sensor` (optional), `custom_action` (optional)

## Troubleshooting

| Issue | Approach |
|-------|----------|
| Missing input | Default optional inputs |
| "expected dictionary" on action input | Use `sequence: !input`, not bare `- !input` |
| Template fails on optional entity | `|default('')` and `states()` |
| LEGACY_SYNTAX from yamllint | `!input` for simple values; `variables` only where templates need them |

## Documentation

After the blueprint is in the tree, document it using the same standards as other automations (see `.ai/prompts/homeassistant-documentation.md` and RULES.md). Cover purpose, inputs, triggers, actions, examples, and configuration; use concrete values in examples.

## Key learnings

1. Optional inputs: `|default('')` + `states()` avoids template failures
2. Action inputs: `sequence: !input` for list-shaped actions
3. `variables:` only for template-referenced inputs
4. Prefer `action:` over `service:` in modern YAML
5. Folded descriptions `>-`; wrap long lines (~120 chars)
6. Preserve automation metadata when swapping to blueprint instances
7. Incremental commits for replacements
8. Validate with yamllint and real test configs before calling it done
