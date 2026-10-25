"""The InvisOutlet integration."""

from __future__ import annotations

import logging
from types import MappingProxyType
from typing import Any

from homeassistant.config_entries import ConfigSubentry
from homeassistant.const import CONF_HOST, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import (
    DeviceEntry,
    async_entries_for_config_entry,
)
from homeassistant.helpers.device_registry import (
    async_get as async_get_device_registry,
)
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.typing import ConfigType

from invisoutlet import InvisOutletClient

from .commission import async_setup_interceptor
from .commission_bridge import async_setup_commission_bridge
from .const import (
    CONF_AREA,
    CONF_EFFECTS,
    CONF_ENTRY_TYPE,
    CONF_OUTLETS,
    DOMAIN,
    ENTRY_TYPE_HUB,
    MANUFACTURER,
    PLATFORMS,
    SUBENTRY_AURA_EFFECT,
    SUBENTRY_OUTLET,
)
from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import configuration_url
from .helpers import outlet_added_signal

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the InvisOutlet integration."""
    _async_purge_orphan_rows(hass)
    async_setup_interceptor(hass)
    await async_setup_commission_bridge(hass)

    return True


async def _async_add_outlet(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    serial: str,
    outlet: dict,
    *,
    dispatch: bool,
) -> None:
    """Bring up one outlet's coordinator, optionally signalling live platforms.

    ``dispatch`` is False during initial setup (platforms add existing outlets
    themselves) and True for a later add, so its entities appear without
    reloading the others.
    """
    dev_reg = async_get_device_registry(hass)
    if dev_reg.async_get_device(identifiers={(DOMAIN, serial)}) is None:
        # Register the device before its entities so the name chosen in the
        # add flow drives the entity ids. The entities' device_info later
        # renames the device to its model + serial, so the choice goes in as
        # name_by_user, which wins and sticks. Only values actually chosen are
        # applied: a re-added outlet arrives without them (the flow skips the
        # name step), so its restored name/area/entity ids survive untouched.
        subentries = entry.get_subentries_of_type(SUBENTRY_OUTLET)
        device = dev_reg.async_get_or_create(
            config_entry_id=entry.entry_id,
            config_subentry_id=subentries[0].subentry_id if subentries else None,
            identifiers={(DOMAIN, serial)},
            manufacturer=MANUFACTURER,
            name=outlet.get(CONF_NAME, f"InvisOutlet {serial}"),
        )
        updates: dict[str, Any] = {}
        if outlet.get(CONF_NAME):
            updates["name_by_user"] = outlet[CONF_NAME]
        if outlet.get(CONF_AREA):
            updates["area_id"] = outlet[CONF_AREA]
        if updates:
            dev_reg.async_update_device(device.id, **updates)
    client = InvisOutletClient(outlet[CONF_HOST])
    coordinator = InvisOutletCoordinator(hass, entry, serial, client)
    try:
        if dispatch:
            # The entry is already loaded; first_refresh is setup-only.
            await coordinator.async_dynamic_setup()
        else:
            await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await client.close()
        _LOGGER.warning("InvisOutlet %s is unreachable; skipping it for now", serial)
        return
    entry.runtime_data[serial] = coordinator
    if dispatch:
        async_dispatcher_send(hass, outlet_added_signal(entry.entry_id), coordinator)


async def async_setup_entry(hass: HomeAssistant, entry: InvisOutletConfigEntry) -> bool:
    """Set up InvisOutlet from a config entry."""
    # The hub: one client + coordinator per stored outlet (keyed by serial).
    # Ensure the grouping subentry exists first so outlet entities can be tagged
    # to it (created before platforms are forwarded / the update listener runs).
    if not entry.get_subentries_of_type(SUBENTRY_OUTLET):
        hass.config_entries.async_add_subentry(
            entry,
            ConfigSubentry(
                data=MappingProxyType({}),
                subentry_type=SUBENTRY_OUTLET,
                title="InvisOutlet",
                unique_id=None,
            ),
        )

    entry.runtime_data = {}
    for serial, outlet in entry.data.get(CONF_OUTLETS, {}).items():
        await _async_add_outlet(hass, entry, serial, outlet, dispatch=False)

    entry.async_on_unload(entry.add_update_listener(_async_outlets_changed))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _async_reconcile_registry(hass, entry)

    return True


async def _async_outlets_changed(
    hass: HomeAssistant, entry: InvisOutletConfigEntry
) -> None:
    """React to the outlet map changing: hosts, new outlets, reload on removal."""
    dev_reg = async_get_device_registry(hass)
    outlets = entry.data.get(CONF_OUTLETS, {})
    configured = set(outlets)
    current = set(entry.runtime_data)
    if current - configured:
        # An outlet was removed — full reload to tear it down cleanly.
        await hass.config_entries.async_reload(entry.entry_id)
        return
    for serial in configured & current:
        # Zeroconf re-discovery records a new IP here when DHCP moves an outlet.
        # The coordinator's client was built with the old one and would go on
        # retrying it forever, so hand it the new address to reconnect to.
        host = outlets[serial].get(CONF_HOST)
        if not host:
            continue
        coordinator = entry.runtime_data[serial]
        if host == coordinator.client.host:
            continue
        await coordinator.client.set_host(host)
        # The "Visit device" link is built from the host, so move it too rather
        # than leaving the device page pointing at an address nothing answers on.
        device = dev_reg.async_get_device(identifiers={(DOMAIN, serial)})
        if device is not None:
            dev_reg.async_update_device(
                device.id,
                configuration_url=configuration_url(
                    host, coordinator.device_info.hw_rev
                ),
            )
    for serial in configured - current:
        await _async_add_outlet(hass, entry, serial, outlets[serial], dispatch=True)


@callback
def _async_reconcile_registry(
    hass: HomeAssistant, entry: InvisOutletConfigEntry
) -> None:
    """Drop registry entities/devices whose backing config no longer exists.

    Deleting a device only tombstones it in HA, and the next
    ``async_get_or_create`` with the same identifiers resurrects it; entity rows
    and devices can also linger (an entity keeps a dangling ``device_id``) if
    their outlet/effect was dropped from config outside the delete handler.
    Reconciling against config on every setup makes a removal stick across
    restarts no matter how it happened.
    """
    valid = set(entry.data.get(CONF_OUTLETS, {}))
    valid |= {f"{serial}_aura_effects" for serial in valid}
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        valid |= set(subentry.data.get(CONF_EFFECTS, {}))

    def _backed(unique_id: str) -> bool:
        # unique_ids are "<outlet-serial-or-effect-id>_<suffix>"; keep only those
        # whose prefix is still a configured outlet/effect.
        return any(unique_id == v or unique_id.startswith(f"{v}_") for v in valid)

    ent_reg = er.async_get(hass)
    for entity in er.async_entries_for_config_entry(ent_reg, entry.entry_id):
        if not _backed(entity.unique_id):
            ent_reg.async_remove(entity.entity_id)

    dev_reg = async_get_device_registry(hass)
    for device in async_entries_for_config_entry(dev_reg, entry.entry_id):
        domain_ids = {i[1] for i in device.identifiers if i[0] == DOMAIN}
        if domain_ids and domain_ids.isdisjoint(valid):
            dev_reg.async_remove_device(device.id)


@callback
def _async_purge_orphan_rows(hass: HomeAssistant) -> None:
    """Remove entities left tied to a config entry that no longer exists.

    Removing an entry normally cascades its rows, but stragglers can survive a
    botched removal. They can't be reconciled per-entry since no setup runs for a
    missing entry, so sweep them once when the integration loads.
    """
    known = {entry.entry_id for entry in hass.config_entries.async_entries(DOMAIN)}
    ent_reg = er.async_get(hass)
    for entity in list(ent_reg.entities.values()):
        if entity.platform == DOMAIN and entity.config_entry_id not in known:
            ent_reg.async_remove(entity.entity_id)


async def async_remove_config_entry_device(
    hass: HomeAssistant,
    config_entry: InvisOutletConfigEntry,
    device_entry: DeviceEntry,
) -> bool:
    """Allow removing an outlet, dropping it from the stored outlet map.

    It won't be recreated on reload; if it's still on the network it'll be
    rediscovered over zeroconf.
    """
    entry_type = config_entry.data.get(CONF_ENTRY_TYPE)
    ids = {i[1] for i in device_entry.identifiers if i[0] == DOMAIN}

    # An Aura effect device (its id is the subentry's effect key): drop it from
    # the shared subentry so it doesn't return on reload. The button lives on
    # the hub, so this applies there as well as the standalone Aura entry.
    for subentry in config_entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        current = subentry.data.get(CONF_EFFECTS, {})
        effects = {k: v for k, v in current.items() if k not in ids}
        if effects != current:
            hass.config_entries.async_update_subentry(
                config_entry, subentry, data={CONF_EFFECTS: effects}
            )
            # HA tombstones the device on the True return; the setup-time
            # _async_reconcile_registry clears any row that outlives its config.
            return True

    # Only the hub carries outlet coordinators in runtime_data; the device-less
    # Aura Effects entry just allows the removal.
    if entry_type != ENTRY_TYPE_HUB:
        return True

    removed = ids
    # Tear down just this outlet, then drop it from the map. Popping it from
    # runtime_data first means the update below leaves the outlet set unchanged
    # versus what's loaded, so no reload is triggered.
    for serial in removed:
        coordinator = config_entry.runtime_data.pop(serial, None)
        if coordinator is not None:
            await coordinator.async_teardown()

    outlets = config_entry.data.get(CONF_OUTLETS, {})
    remaining = {s: o for s, o in outlets.items() if s not in removed}
    if remaining != outlets:
        hass.config_entries.async_update_entry(
            config_entry, data={**config_entry.data, CONF_OUTLETS: remaining}
        )

    # HA tombstones the device on the True return; the setup-time
    # _async_reconcile_registry clears any row that outlives its config. If the
    # outlet is still on the network it can be rediscovered over zeroconf afresh.
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: InvisOutletConfigEntry
) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        for coordinator in entry.runtime_data.values():
            await coordinator.async_teardown()
    return unload_ok
