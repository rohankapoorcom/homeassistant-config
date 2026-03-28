# Examples: extract-homeassistant-dashboard-entities

Illustrative dashboard YAML fragments and the **expected extraction behavior**. Use these to sanity-check parsing, filtering, partitioning, and satellite stub generation.

---

## 1. Direct `entity:` and glance-style lists

**Input (fragment):**

```yaml
type: glance
entities:
  - entity: sensor.living_room_temperature
  - entity: light.kitchen_lights
```

**Extracted (before partition):** `sensor.living_room_temperature`, `light.kitchen_lights`

**`entities:` (sorted):**

```yaml
entities:
  - light.kitchen_lights
  - sensor.living_room_temperature
```

**`scripts:`:** *(none)*

---

## 2. `script:` lines — normalize and partition

**Input:**

```yaml
type: custom:button-card
variables:
  script: turn_on_the_lights
- type: custom:button-card
  variables:
    script: script.turn_off_the_tv
```

**Extracted:** `script.turn_on_the_lights`, `script.turn_off_the_tv`

**`entities:`:** *(empty — scripts never appear here)*

**`scripts:`:**

```yaml
scripts:
  - script.turn_off_the_tv
  - script.turn_on_the_lights
```

**Satellite `scripts.yaml` (excerpt):**

```yaml
turn_on_the_lights:
  alias: "Turn on the lights (forward to primary)"
  mode: single
  sequence:
    - action: script.remote_turn_on_the_lights

turn_off_the_tv:
  alias: "Turn off the tv (forward to primary)"
  mode: single
  sequence:
    - action: script.remote_turn_off_the_tv
```

---

## 3. Template variable **names** vs **values**

**Input:**

```yaml
variables:
  - apple_tv_media_player_entity: media_player.living_room_apple_tv
  - apple_tv_remote_entity: remote.living_room_apple_tv
  - volume_media_player_entity: media_player.denon_avr_x4300h
```

**Extract (values only):**

- `media_player.living_room_apple_tv`
- `remote.living_room_apple_tv`
- `media_player.denon_avr_x4300h`

**Do not extract:** `apple_tv_media_player_entity`, `volume_media_player_entity` (those are keys, not entity IDs).

**`entities:` (sorted excerpt):**

```yaml
entities:
  - media_player.denon_avr_x4300h
  - media_player.living_room_apple_tv
  - remote.living_room_apple_tv
```

---

## 4. Excluded: `entity: template`, `entity: user`, placeholders

**Input:**

```yaml
type: custom:state-switch
entity: template
template: "{{ states('sensor.x') }}"
states:
  "On":
    type: picture-entity
    entity: user

type: custom:decluttering-card
template: slider_button_card
variables:
  - entity: '[[entity]]'
```

**Extracted usable entities:** only what appears inside real `entity:` / `entity_id:` / variable **values** that are `domain.object_id`. Here, `entity: template`, `entity: user`, and `'[[entity]]'` contribute **no** entity IDs. Strings inside Jinja (`{{ … }}`) are not scraped unless the user explicitly asks for deep template resolution.

---

## 5. Cameras omitted; weather replaced

**Input:**

```yaml
entity: weather.local_weather
cards:
  - entity_id: camera.front_door
```

**Rules:**

- `camera.front_door` → **omit** from `entities:` (and from `scripts:` — not a script).
- `weather.local_weather` → **replace** with `sensor.local_weather_forecast` in `entities:`.

**`entities:`:**

```yaml
entities:
  - sensor.local_weather_forecast
```

---

## 6. `grid:` / `solar:` entity-style values

**Input:**

```yaml
type: energy
grid: sensor.eagle_200_meter_power_demand
solar: sensor.envoy_current_power_production
```

**Extract:** `sensor.eagle_200_meter_power_demand`, `sensor.envoy_current_power_production`

**Note:** Many `source: Netflix` lines are **app names**, not entities — only treat a value as an entity when it matches `domain.object_id` (e.g. `sensor.*`, `switch.*`).

---

## 7. `states['domain.entity']` in JavaScript templates

**Input:**

```yaml
state:
  - operator: template
    value: >
      [[[
        return states['switch.living_room_sync_box_light_sync'].state === 'on'
      ]]]
```

**Extract:** `switch.living_room_sync_box_light_sync`

Include in **`entities:`** (sorted with other non-script entities).

---

## 8. Deduplication

**Input:** Three cards all use `entity: light.hallway_lights`.

**Output:** A single line in `entities:`:

```yaml
entities:
  - light.hallway_lights
```

---

## 9. Script object_id already starts with `remote_`

**Input:**

```yaml
script: remote_run_scene_kitchen
```

**Normalized:** `script.remote_run_scene_kitchen`

**Satellite stub:** **Do not** emit `action: script.remote_remote_run_scene_kitchen`. Either skip generating a wrapper for this entry or document that the dashboard already targets a remote-prefixed script on the primary.

---

## 10. Full deliverable shape (checklist)

For a typical run, the user-facing answer should include:

1. **`entities:`** — alphabetized, **no** `script.*`, **no** `camera.*`, weather already substituted.
2. **Count** — `Total non-script entities: N`
3. **`scripts:`** — alphabetized `script.*` only (if any).
4. **Count** — `Total scripts: M`
5. **`scripts.yaml`** — one wrapper per dashboard script (subject to §9), for paste into the **secondary** instance.

---

## Repository default path

For this config repo, start from **`dashboards/`** (including `dashboards/home.yaml` and everything under `dashboards/components/`) unless the user names a different directory.
