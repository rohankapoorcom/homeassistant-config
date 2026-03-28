---
name: extract-homeassistant-dashboard-entities
description: >-
  Extracts unique Home Assistant entity IDs from Lovelace dashboard YAML (entity:,
  entity_id:, script: lines, grid/solar, template variable values, states['…'] in JS).
  Produces alphabetized entities: (non-script only), separate scripts: list, counts,
  and satellite scripts.yaml stubs that call script.remote_<name> for dual-instance
  remote_homeassistant setups. Omits camera.*, replaces weather.local_weather with
  sensor.local_weather_forecast, excludes template/user placeholders. Decluttering
  templates are only scanned when reachable from active (non-comment) YAML. Use when auditing
  dashboard entities, building remote allowlists, inventorying dashboards/decluttering
  templates, or generating script forwarding stubs for a UI satellite instance.
---

# Extract Home Assistant entities from dashboard YAML

## Instructions

Extract all Home Assistant entities referenced in dashboard YAML files and produce a deduplicated list **excluding the `script` domain** in the main `entities:` block (scripts are listed and forwarded separately per steps 15–16). When the inventory includes `script.*` entities, also produce the `scripts:` inventory (step 15) and secondary-instance `scripts.yaml` forwarding stubs (step 16).

**Default scope** for this repository: the `dashboards/` directory tree (including `dashboards/home.yaml`, `components/panels/`, `components/decluttering_templates/`, and related YAML). Adjust the path if the user specifies another folder. **Do not** treat every file under `decluttering_templates/` as in-use; see step 2.

**More examples:** See [`examples.md`](examples.md) in this skill folder (template variables, cameras/weather, `grid`/`solar`, `states['…']`, dedupe, `remote_` edge case).

## Process steps

**CRITICAL WARNING**: When extracting entities from template variables, ONLY extract the actual entity values (right side of colon), NOT the template variable names (left side of colon). Template variable names like `apple_tv_media_player_entity` are NOT entities—they are variable names used in templates.

1. **Comment-aware YAML text**: For discovery and extraction, treat `#` as starting an end-of-line comment (strip from `#` to EOL). Ignore matches that would come only from commented-out text—e.g. archived Lovelace in `# …` blocks must not add templates or entities.

2. **Reachable decluttering templates only** (before scanning `decluttering_templates/` for entity IDs):
   - Start from the dashboard entry YAML (here: `dashboards/home.yaml`). Recursively follow `!include` targets to collect all **panel and layout** files that are part of the live dashboard.
   - In those files (comment-aware), find `template: <name>` on `custom:decluttering-card` (and equivalent decluttering usage). That seeds a set of **used** template names.
   - For each used template, open `dashboards/components/decluttering_templates/<name>.yaml` (root key is typically `<name>:`). Inside that file, add any **nested** `template: <other>` names (e.g. a group template that instantiates a row template). Repeat until the set stops growing.
   - **Extract entities from decluttering YAML only for templates in this reachable set.** Omit entities that appear exclusively in decluttering files that are never referenced from active (non-comment) dashboard YAML—e.g. templates kept for archival alongside commented-out views.

3. **Identify target files for extraction**:
   - Always include: reachable panel/layout YAML from step 2, plus reachable decluttering template files.
   - Optionally include other YAML under `dashboards/` that is clearly part of the active UI (e.g. `kiosk_mode.yaml` if included from the entry file). Do **not** blindly grep all of `decluttering_templates/` without applying step 2.

4. **Extract direct entity references**: Find lines containing `entity:` across the **target** YAML files from step 3.
   - **CRITICAL**: Use high `head_limit` (1000+) to avoid truncation.
   - **CRITICAL**: If truncation occurs, search each file individually.
   - **CRITICAL**: Use `files_with_matches` first to get the complete file list.

5. **Extract script references**: Find lines containing `script:`.
   - Look for both `script: script_name` and `script: script.script_name`.
   - Convert to `script.script_name` (add `script.` prefix if missing).
   - **CRITICAL**: Use high `head_limit` to avoid truncation.

6. **Extract alternative patterns**: Lines that may reference entities without `entity:`:
   - `grid:`, `solar:`, `battery:`, `power:`, `voltage:`, `current:`, `load:`, `status:`, `source:`, `temperature:`, `capacity:`, `runtime:`, `charge:`, `level:`, `mode:`, `water:` (filter to values that look like `domain.object_id` where appropriate).

7. **Extract templated references**: `entity_id:` (e.g. lovelace_gen), `{{ … }}` entity contexts, template definitions.

8. **Extract template variable assignments**: `entity_id: entity_name`, lists in lovelace_gen `!include` variables, `*_entity: domain.entity`.
   - **CRITICAL**: Only extract VALUES, not names like `apple_tv_media_player_entity`.

9. **Parse entity names** from lines such as:
   - `entity: sensor.temperature`
   - `entity_id: camera.front_door` (camera values are still parsed for completeness but removed in filter step)
   - `script: script_name` → `script.script_name`

10. **Filter out non-entities**:
   - `entity: template`, `entity: user` (state-switch cards)
   - Placeholders: `[[entity]]`, `{{ camera.entity_id }}` as literals (resolve cameras via parent definitions when listing real IDs; still exclude `camera.*` from output)
   - **Template variable names**: not entities
   - **Camera entities**: exclude all `camera.*` from final outputs (remote_homeassistant proxy limitation)
   - **Weather**: replace `weather.local_weather` with `sensor.local_weather_forecast`
   - Other non-entity config values

11. **Deduplicate** (including scripts until partitioned in step 12).

12. **Partition scripts**: Split into non-script vs `script.*`. Only non-script entities go in `entities:`. Scripts feed steps 15–16 only.

13. **Alphabetize** each partition separately.

14. **Format `entities:`** (non-script only):

    ```yaml
    entities:
      - binary_sensor.example_sensor
      - light.example_light
      - sensor.example_temperature
    ```

15. **Format `scripts:`** (if any):

    ```yaml
    scripts:
      - script.turn_on_lights
    ```

16. **Satellite `scripts.yaml`**: For each `script.<name>` from dashboards, emit a wrapper on the **secondary** instance with key `<name>` whose single step calls `script.remote_<name>` on the primary. If `<name>` already starts with `remote_`, do not double-prefix. Prefer `sequence` + `action: script.remote_<name>` (HA 2025.x); fall back to `service:` or `script.turn_on` + `target.entity_id` if needed. Include readable `alias` text. Output the `scripts:` list from step 15 near this block.

17. **Verification**: Confirm all relevant YAML was searched, truncation did not drop matches, and unreachable decluttering templates were excluded per step 2.

## Commands to use

Use repository search tools (grep, glob, read_file) analogously to:

```bash
# After computing reachable files (see process step 2–3), grep within those paths only;
# do not use path="dashboards" alone if that would pull in unreachable decluttering_templates.
grep pattern="entity:" path="<reachable-file-or-dir>" output_mode="content"
# …per-file passes if results truncate
```

Also search for `states['domain.entity']` in dashboard YAML when present.

## Output requirements

- Alphabetized **`entities:`** with every `script.*` omitted
- **Count** of non-script entities
- If scripts exist: **count**, **`scripts:`** list, and copy-pasteable **`scripts.yaml`** for the satellite (step 16)
- Valid `domain.entity_name` entries

## Example usage

When scanning `dashboards/`:

1. Extract `entity:`, `entity_id:`, `script:`, alternate keys, template values
2. Apply filters (no cameras in output, weather replacement, no template/user)
3. Dedupe → partition scripts → sort
4. Emit `entities:`, `scripts:`, counts, and satellite `scripts.yaml` stubs

## Minimal output example

See [`examples.md`](examples.md) for many input→output cases. End-to-end shape:

```yaml
entities:
  - binary_sensor.downstairs_motion
  - light.kitchen_lights
  - sensor.local_weather_forecast
  - sensor.temperature
  - switch.example_switch
```

```yaml
scripts:
  - script.turn_on_lights
```

**Total non-script entities**: 5 · **Total scripts**: 1

**Satellite `scripts.yaml`** (secondary only; primary implements `script.remote_turn_on_lights`):

```yaml
turn_on_lights:
  alias: "Turn on lights (forward to primary)"
  mode: single
  sequence:
    - action: script.remote_turn_on_lights
```

## Capabilities summary

- Static and templated Lovelace references; **reachable** decluttering templates only; lovelace_gen includes
- Comment-aware parsing so archived/commented YAML does not expand the entity list
- Truncation-aware search (per-file if needed)
- Camera exclusion, weather → sensor forecast, scripts split + `remote_*` forwarding stubs for dual-instance setups
