"""Shared platform-setup helpers for the InvisOutlet integration."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any, Protocol, TypeVar

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_EFFECTS, DOMAIN, SUBENTRY_AURA_EFFECT, SUBENTRY_OUTLET
from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator


def outlet_added_signal(entry_id: str) -> str:
    """Dispatcher signal fired (with the new coordinator) when an outlet is added."""
    return f"{DOMAIN}_outlet_added_{entry_id}"


def effect_data(entry: InvisOutletConfigEntry, effect_id: str) -> dict[str, Any]:
    """Return one effect's stored template data (its name + per-pixel/mode state).

    The shared Aura Effects subentry is the template's home, so the virtual
    entities read/write here instead of RestoreEntity — surviving the frequent
    reloads and any entity-id churn.
    """
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        if effect_id in (effects := subentry.data.get(CONF_EFFECTS, {})):
            return effects[effect_id]
    return {}


@callback
def async_update_effect_data(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    effect_id: str,
    updates: dict[str, Any],
) -> None:
    """Merge ``updates`` into one effect's stored template data."""
    for subentry in entry.get_subentries_of_type(SUBENTRY_AURA_EFFECT):
        effects = subentry.data.get(CONF_EFFECTS, {})
        if effect_id not in effects:
            continue
        merged = {**effects[effect_id], **updates}
        hass.config_entries.async_update_subentry(
            entry,
            subentry,
            data={**subentry.data, CONF_EFFECTS: {**effects, effect_id: merged}},
        )
        return


def effect_mode_signal(effect_id: str) -> str:
    """Dispatcher signal fired when an effect device's mode select changes.

    Lets that effect's virtual pixels re-render (e.g. switch HSV vs. temperature)
    without each pixel having to resolve and track the sibling select entity.
    """
    return f"{DOMAIN}_effect_mode_{effect_id}"


@callback
def async_add_outlet_entities(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
    build: Callable[[InvisOutletCoordinator], Iterable[Entity]],
) -> None:
    """Add ``build(coordinator)`` for every outlet, now and as new ones arrive.

    Each platform passes a ``build`` that returns its entities for one outlet.
    Existing outlets are added immediately; later additions arrive via the
    dispatcher signal, so adding an outlet never reloads the others.
    """

    # All outlet devices group under the single "InvisOutlet" subentry.
    subentries = entry.get_subentries_of_type(SUBENTRY_OUTLET)
    subentry_id = subentries[0].subentry_id if subentries else None

    @callback
    def _add(coordinator: InvisOutletCoordinator) -> None:
        async_add_entities(build(coordinator), config_subentry_id=subentry_id)

    for coordinator in entry.runtime_data.values():
        _add(coordinator)
    entry.async_on_unload(
        async_dispatcher_connect(hass, outlet_added_signal(entry.entry_id), _add)
    )


_DataT_contra = TypeVar("_DataT_contra", contravariant=True)


class _FieldDescription(Protocol[_DataT_contra]):
    """An entity description that reads its value from a device-data object."""

    key: str
    value_fn: Callable[[_DataT_contra], object]


def supported_for_faceplate[DescriptionT: _FieldDescription[Any]](
    hass: HomeAssistant,
    coordinator: InvisOutletCoordinator,
    domain: str,
    descriptions: Sequence[DescriptionT],
    data: object | None,
) -> Sequence[DescriptionT]:
    """Keep only the descriptions the device currently reports, pruning the rest.

    The device omits fields that don't apply to the attached faceplate
    (``value_fn`` -> ``None``) — true for both the sensor stream and the config
    blob — so create only the ones with data and remove any registry entries left
    from a different faceplate. With no data yet (``data is None``) we can't tell,
    so keep them all and prune nothing.
    """
    if data is None:
        return descriptions
    supported = [d for d in descriptions if d.value_fn(data) is not None]
    keys = {d.key for d in supported}
    registry = er.async_get(hass)
    serial = coordinator.device_info.serial_number
    for description in descriptions:
        if description.key in keys:
            continue
        unique_id = f"{serial}_{description.key}"
        if entity_id := registry.async_get_entity_id(domain, DOMAIN, unique_id):
            registry.async_remove(entity_id)
    return supported
