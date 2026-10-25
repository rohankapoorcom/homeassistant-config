"""Move an entry's registry entries from one device key to another.

The key (registry.identity.resolve_device_key) is permanent in three
places, so changing it means rewriting the registries rather than storing
a new value -- anything left behind is orphaned. Rewriting rather than
recreating is what keeps an entity's entity_id, and with it its history,
area and automations.

Its own module because both callers need it: the v1 -> v2 migration in
__init__.py and the coordinator's first-poll adoption (issue #381).
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN
from .devices import find_entry_device

_LOGGER = logging.getLogger(__name__)


@callback
def rekey_entry(hass: HomeAssistant, entry: ConfigEntry, old_key: str, new_key: str) -> None:
    """Rewrite everything this entry registered under `old_key` to `new_key`.

    All three permanent places move together: entity unique_ids
    (f"{DOMAIN}_{key}_{state_key}"), device identifiers ((DOMAIN, key), plus
    (DOMAIN, f"{key}_{subdevice}") per subdevice -- see device_info_for),
    and the entry's own unique_id. Leaving that last one behind would let
    the config flow's duplicate check wave through a re-add of this very
    appliance.

    Idempotent, so it is safe to attempt on every poll rather than tracking
    whether it has run. Where both keys already exist the `old_key` copy is
    the dead one, so it is removed rather than rewritten over the live entry.

    Must run on the event loop; the registry helpers require it.
    """
    if old_key == new_key:
        return

    new_entry_unique_id = f"{DOMAIN}_{new_key}"
    if entry.unique_id != new_entry_unique_id:
        hass.config_entries.async_update_entry(entry, unique_id=new_entry_unique_id)

    ent_reg = er.async_get(hass)
    stale_prefix = f"{DOMAIN}_{old_key}_"
    for entity in list(er.async_entries_for_config_entry(ent_reg, entry.entry_id)):
        if not entity.unique_id.startswith(stale_prefix):
            continue
        new_unique_id = f"{DOMAIN}_{new_key}_{entity.unique_id[len(stale_prefix) :]}"
        if ent_reg.async_get_entity_id(entity.domain, DOMAIN, new_unique_id):
            _LOGGER.debug("removing orphaned entity %s", entity.entity_id)
            ent_reg.async_remove(entity.entity_id)
        else:
            _LOGGER.debug("re-keying entity %s to %s", entity.entity_id, new_unique_id)
            ent_reg.async_update_entity(entity.entity_id, new_unique_id=new_unique_id)

    dev_reg = dr.async_get(hass)
    for device in list(dr.async_entries_for_config_entry(dev_reg, entry.entry_id)):
        stale = {
            ident
            for ident in device.identifiers
            if ident[0] == DOMAIN and (ident[1] == old_key or ident[1].startswith(f"{old_key}_"))
        }
        if not stale:
            continue
        fresh = {(DOMAIN, f"{new_key}{ident[1][len(old_key) :]}") for ident in stale}
        existing = find_entry_device(hass, entry.entry_id, fresh)
        if existing is not None and existing.id != device.id:
            # Removing a device takes its entities with it. Anything still
            # attached here was re-keyed rather than removed above -- the
            # surviving copy, not a duplicate -- so move it onto the device
            # it now belongs to before the removal destroys it too.
            for entity in er.async_entries_for_device(
                ent_reg, device.id, include_disabled_entities=True
            ):
                ent_reg.async_update_entity(entity.entity_id, device_id=existing.id)
            _LOGGER.debug("removing orphaned device %s", device.id)
            dev_reg.async_remove_device(device.id)
        else:
            _LOGGER.debug("re-keying device %s to %s", device.id, fresh)
            dev_reg.async_update_device(
                device.id, new_identifiers=(device.identifiers - stale) | fresh
            )
