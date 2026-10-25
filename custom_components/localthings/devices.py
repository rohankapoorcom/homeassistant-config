"""Device-registry lookups and parent links, across the HA releases this
integration supports.

HA 2026.9 deprecated `DeviceInfo`'s `via_device` for `via_device_id` and
`device_registry.async_get_device` for `async_get_device_by_identifier`, both
breaking in 2027.8; neither replacement exists on hacs.json's 2025.1 floor.
The lookups here are written to need no replacement at all, and the one call
that does feature-detects at runtime -- same pattern as `__init__.py`'s
PARTICULATE_UNIT and `new_unit_class`.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, cast

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo

# Set through a plain mapping either way: whichever key this core wants, the
# other one is absent from its DeviceInfo TypedDict, so a static assignment
# could only ever type-check against one HA generation.
_HAS_VIA_DEVICE_ID = "via_device_id" in DeviceInfo.__annotations__


def find_entry_device(
    hass: HomeAssistant, entry_id: str, identifiers: Iterable[tuple[str, str]]
) -> dr.DeviceEntry | None:
    """The `entry_id` device row carrying any of `identifiers`.

    Scans the entry's own rows rather than calling `async_get_device`, which
    searches every entry and is deprecated for exactly that reason -- an
    identifier is only unique within one config entry. Every caller here means
    its own entry's row, so this is both the compatible spelling and the
    correct one; entries hold a handful of rows, so the scan is free.
    """
    wanted = set(identifiers)
    return next(
        (
            row
            for row in dr.async_entries_for_config_entry(dr.async_get(hass), entry_id)
            if row.identifiers & wanted
        ),
        None,
    )


def set_via_device(
    hass: HomeAssistant, entry_id: str, info: DeviceInfo, parent: tuple[str, str]
) -> None:
    """Link `info` under the `parent` identifier's device row, in place.

    A core new enough to want `via_device_id` needs the parent's registry id,
    and drops the entity outright if that id names no registered device -- so
    an unregistered parent leaves the link unset here, exactly as an
    unresolvable `via_device` does on an older core. Either way the next
    entity added under this device picks the link up once the parent exists.
    """
    if not _HAS_VIA_DEVICE_ID:
        cast("dict[str, Any]", info)["via_device"] = parent
        return
    if (device := find_entry_device(hass, entry_id, (parent,))) is not None:
        cast("dict[str, Any]", info)["via_device_id"] = device.id
