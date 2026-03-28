# Examples: generate-homeassistant-blueprint

End-to-end patterns for authoring and wiring Home Assistant **automation** blueprints: consolidation reasoning, full YAML files, `use_blueprint` instances, optional inputs, and common mistakes. Use alongside [`SKILL.md`](SKILL.md).

---

## 1. From duplicate automations to blueprint inputs

**Scenario:** You have two package automations that only differ by entity IDs and delays.

| Automation A (living room) | Automation B (bedroom) | Blueprint input |
|----------------------------|--------------------------|-----------------|
| `cover.living_room_curtains` | `cover.bedroom_shades` | `cover_entity` (selector `entity` / `domain: cover`) |
| `binary_sensor.lr_windows` | `binary_sensor.bed_windows` | `open_status_sensor` |
| Delay `5` s before close | Delay `15` s | `close_delay` (number selector, default `0`) |
| No presence check | `binary_sensor.bedroom_motion` as gate | `presence_sensor` (optional, default `""`) |

**Design takeaway:** Names are **generic** (`cover_entity`, not `living_room_curtains`). Room-specific strings live only in each **instance** under `use_blueprint` → `input:`.

---

## 2. Full minimal blueprint — motion-activated light (modern syntax)

Illustrates: required entities, numeric default, `mode: restart`, `triggers` / `actions`, `action:` + `target.entity_id`, `wait_for_trigger` as a **list** of triggers, `!input` for simple values (no `variables:` — nothing is referenced inside Jinja). Matches patterns in `blueprints/automation/rohankapoorcom/motion_light.yaml` (simplified — no reload triggers or optional `turn_on_condition`).

```yaml
blueprint:
  name: Motion-activated Light (example)
  description: >-
    Turn on a light when motion starts; turn off after motion ends and a wait.
  domain: automation
  input:
    motion_entity:
      name: Motion Sensor
      description: Binary motion sensor
      selector:
        entity:
          filter:
            domain: binary_sensor
            device_class:
              - motion
              - occupancy
    light_target:
      name: Light
      selector:
        entity:
          filter:
            domain: light
    no_motion_wait:
      name: Wait time after last motion
      description: Seconds to keep the light on after motion goes off.
      default: 120
      selector:
        number:
          min: 0
          max: 3600
          unit_of_measurement: seconds

mode: restart
max_exceeded: silent

triggers:
  - trigger: state
    entity_id: !input motion_entity
    from: "off"
    to: "on"

actions:
  - action: light.turn_on
    target:
      entity_id: !input light_target
  - wait_for_trigger:
      - trigger: state
        entity_id: !input motion_entity
        from: "on"
        to: "off"
  - delay: !input no_motion_wait
  - action: light.turn_off
    target:
      entity_id: !input light_target
```

---

## 3. Matching automation instance (`use_blueprint`)

Assume the blueprint file lives at `blueprints/automation/myfolder/motion_light_example.yaml`.

```yaml
automation:
  - id: "1710000000001"
    alias: "Living room — motion light (blueprint)"
    description: "Motion-controlled ceiling light"
    use_blueprint:
      path: blueprints/automation/myfolder/motion_light_example.yaml
      input:
        motion_entity: binary_sensor.living_room_motion
        light_target: light.living_room_ceiling
        no_motion_wait: 180
```

**Takeaway:** Preserve stable `id`, human `alias`, and `description` when replacing a hand-written automation with a blueprint instance.

---

## 4. When to use `variables:` — optional entity in templates

Use **`variables:`** only for inputs that appear inside **Jinja** (`value_template`, `wait_template`, template `condition`, etc.). Expose each such input as `name: !input name` so templates use a simple variable (e.g. `presence_sensor`), not `states('!input …')` mistakes.

**Blueprint fragment:**

```yaml
blueprint:
  name: Optional gate example
  description: Run an action only if an optional sensor is off or unset.
  domain: automation
  input:
    switch_entity:
      name: Switch to control
      selector:
        entity:
          domain: switch
    gate_sensor:
      name: Optional gate (binary)
      description: If empty, gate is skipped (always proceed).
      default: ""
      selector:
        entity:
          domain: binary_sensor

variables:
  gate_sensor: !input gate_sensor

triggers:
  - trigger: state
    entity_id: !input switch_entity
    to: "on"

actions:
  - condition: template
    value_template: >-
      {% set s = gate_sensor | default('') %}
      {{ true if s == '' or states(s) == 'unknown' else is_state(s, 'off') }}
  - action: switch.turn_off
    target:
      entity_id: !input switch_entity
```

**Takeaway:** `switch_entity` uses `!input` directly in `entity_id:` (not inside Jinja). `gate_sensor` is copied into `variables` because the template references it by name.

---

## 5. Action selector — use `sequence: !input`

Action-type inputs return a **list** of actions. Invoke them with **`sequence: !input`**, not a bare list item.

**Correct (parallel with hard-coded + custom steps):**

```yaml
blueprint:
  name: Action input example
  description: Demonstrates sequence !input for optional user-defined actions.
  domain: automation
  input:
    light_entity:
      name: Light
      selector:
        entity:
          domain: light
    extra_actions:
      name: Extra actions
      description: Optional steps (notifications, scripts, etc.)
      default: []
      selector:
        action: {}

triggers:
  - trigger: state
    entity_id: !input light_entity
    to: "on"

actions:
  - parallel:
      - action: light.turn_on
        target:
          entity_id: !input light_entity
      - sequence: !input extra_actions
```

**Wrong (often yields “expected dictionary” or parse errors):**

```yaml
actions:
  - !input extra_actions
```

---

## 6. `choose` with sun + state (condensed cover-style blueprint)

Same ideas as a multi-branch cover automation: sun windows, state trigger on a contact sensor, optional delay, `action:` for services. Optional presence uses `variables` + safe template (pattern from real consolidations).

```yaml
blueprint:
  name: Sun and contact cover (condensed example)
  description: >-
    Close cover after sunset or when contact opens; open after sunrise offset.
    Optional presence must be “off” or unset before opening.
  domain: automation
  input:
    cover_entity:
      name: Cover
      selector:
        entity:
          domain: cover
    contact_sensor:
      name: Window/door (on = open)
      selector:
        entity:
          domain: binary_sensor
    sunrise_offset:
      name: Delay after sunrise before opening
      default: "01:30:00"
      selector:
        time:
    close_delay:
      name: Delay before close
      default: 0
      selector:
        number:
          min: 0
          max: 300
          unit_of_measurement: seconds
    presence_sensor:
      name: Optional presence (off = away)
      default: ""
      selector:
        entity:
          domain: binary_sensor
    notify_action:
      name: Optional notify action
      default: []
      selector:
        action: {}

variables:
  contact_sensor: !input contact_sensor
  presence_sensor: !input presence_sensor

mode: single
max_exceeded: silent

triggers:
  - platform: sun
    event: sunset
  - platform: sun
    event: sunrise
    offset: !input sunrise_offset
  - trigger: state
    entity_id: !input contact_sensor
    to: "on"

actions:
  - choose:
      - alias: Close after dark or when opened
        conditions:
          - condition: or
            conditions:
              - condition: sun
                after: sunset
              - condition: state
                entity_id: !input contact_sensor
                state: "on"
        sequence:
          - delay: !input close_delay
          - parallel:
              - action: cover.close_cover
                target:
                  entity_id: !input cover_entity
              - sequence: !input notify_action
      - alias: Open after sunrise offset
        conditions:
          - condition: sun
            after: sunrise
            after_offset: !input sunrise_offset
        sequence:
          - wait_template: >-
              {% set s = presence_sensor | default('') %}
              {{ true if s == '' or states(s) == 'unknown' else is_state(s, 'off') }}
          - parallel:
              - action: cover.open_cover
                target:
                  entity_id: !input cover_entity
              - sequence: !input notify_action
```

---

## 7. Production reference in this repository

A full, battle-tested variant (parallel branches, `open_status_sensor` semantics, `notification_action`) lives at:

`blueprints/automation/rohankapoorcom/sun-based-cover-control.yaml`

Use it when you want a complete file with real selectors and aliases rather than the condensed teaching version above.

---

## 8. Template pitfalls (quick reference)

| Pitfall | Bad | Better |
|--------|-----|--------|
| Literal `!input` inside Jinja | `{{ is_state('!input sensor_entity', 'off') }}` | Add `variables:` / `sensor_entity: !input sensor_entity` and use `{{ is_state(sensor_entity, 'off') }}`, or use `condition: state` with `entity_id: !input sensor_entity` |
| Optional entity not guarded | `{{ is_state(optional_sensor, 'off') }}` when input may be empty | `{% set s = optional_sensor \| default('') %}` then check `s == ''` or `states(s) == 'unknown'` before `is_state` |
| Legacy service call in new YAML | `service: light.turn_on` at top level of a step | `action: light.turn_on` with `target:` / `data:` as needed |

---

## 9. Validation flow (checklist execution)

1. Save blueprint under `blueprints/automation/<namespace>/your_blueprint.yaml`.
2. Run yamllint (and any project CI) on the file.
3. In Developer Tools → YAML, reload automations or restart as required; confirm the blueprint appears in **Settings → Automations & scenes → Blueprints**.
4. Create a **test** automation from the blueprint with throwaway entities; trigger each branch (sun/state/timer if applicable).
5. Replace production automations one at a time with `use_blueprint` instances; keep `id` / `alias` / `description` aligned with the old entries.
