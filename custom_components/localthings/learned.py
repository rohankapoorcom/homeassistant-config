"""Modes a device reports itself in but never advertises as supported.

Some firmwares report a current mode that is missing from the same
resource's own supported list (issue #327: an ARTIK051 air conditioner
sitting in 'Quiet' with supportedModes [Off, Sleep, Speed, Nano,
NanoSleep]). The mode is real -- the remote and the SmartThings app select
it, and the unit accepts it written back -- so once the device has been
seen in it, it is remembered and offered alongside the advertised ones.

Learning is deliberately not global. A current value that isn't a
selectable option is common across this corpus -- an oven idling in
'NoOperation', a fridge's /mode/vs/0 carrying capability tokens like
'WATERFILTER_DISABLE' -- and remembering one of those permanently would
put an option in the UI that the device can only reject. LEARNABLE names
the canonical hrefs where a reported mode is known to be genuinely
selectable, and the coordinator narrows it further to the hrefs this
device actually binds a climate entity to (see _refresh_learnable_hrefs):
the same href is declared explicitly unmodeled on a dehumidifier and
empty on an air purifier, and learning for those would persist a code
nothing ever offers.

This module also owns the entry key the store persists under, so the
shape lives in exactly one place.
"""

from __future__ import annotations

import threading

from .const import CONF_LEARNED_MODES
from .registry.capabilities.airconditioner import HREF_CONVENIENT

MODES_FIELD = "x.com.samsung.da.modes"
SUPPORTED_FIELD = "x.com.samsung.da.supportedModes"

# Convenient (preset) mode: firmware omits an active preset (e.g. Quiet)
# from its own supportedModes -- a reporting gap, not a capability
# difference (issue #327).
LEARNABLE: frozenset[str] = frozenset({HREF_CONVENIENT})


def _codes(value) -> list[str]:
    """Mode codes from a `modes`-style field, which some firmwares send as
    a bare string rather than an array."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, (list, tuple)):
        return [v for v in value if isinstance(v, str)]
    return []


def _coerce(stored) -> dict[str, list[str]]:
    """Restore the persisted map, dropping anything that isn't the shape
    this module writes. It round-trips through the config entry as plain
    JSON, and a hand-edited .storage file shouldn't be able to crash
    setup."""
    if not isinstance(stored, dict):
        return {}
    restored = {}
    for href, codes in stored.items():
        if isinstance(href, str) and (valid := [c for c in _codes(codes) if c]):
            restored[href] = valid
    return restored


def stored(entry) -> dict[str, list[str]]:
    """What `entry` has persisted, coerced -- for a reader that can't go
    through a coordinator (the options flow, on an unloaded entry)."""
    return _coerce(entry.data.get(CONF_LEARNED_MODES))


def persist(hass, entry, codes: dict[str, list[str]]) -> None:
    """Write `codes` onto the entry. Runs on the event loop, which
    async_update_entry requires."""
    hass.config_entries.async_update_entry(entry, data={**entry.data, CONF_LEARNED_MODES: codes})


class LearnedModes:
    """Per-device store of learned codes, keyed by actual (on-the-wire)
    href so two subdevices of one composite appliance learn separately.

    Mutated from whichever thread applied the update (the DTLS reader for
    an OBSERVE notify, an executor thread for a poll -- see
    ObserveManager.apply), so every access takes the lock; persistence is
    the caller's job, on the event loop.
    """

    def __init__(self, stored=None) -> None:
        self._lock = threading.Lock()
        self._learned = _coerce(stored)

    def observe(self, actual_href: str, rep: dict) -> list[str]:
        """Learn from one applied rep; returns the codes newly learned, so
        an empty list means there is nothing to persist.

        A rep that carries no supported list teaches nothing: "missing from
        the list" is only meaningful against a list that exists, and
        inventing one for a device that publishes none would offer options
        nothing ever said were selectable. `rep` is the merged rep
        ObserveManager.apply stores, so a partial notify carrying `modes`
        alone (issue #27) still sees the supported list from the last full
        poll.
        """
        supported = _codes(rep.get(SUPPORTED_FIELD))
        if not supported:
            return []
        with self._lock:
            known = self._learned.get(actual_href, [])
            new = [
                code
                for code in _codes(rep.get(MODES_FIELD))
                if code and code not in supported and code not in known
            ]
            if new:
                self._learned[actual_href] = [*known, *new]
        return new

    def codes(self, actual_href: str) -> list[str]:
        with self._lock:
            return list(self._learned.get(actual_href, ()))

    def snapshot(self) -> dict[str, list[str]]:
        with self._lock:
            return {href: list(codes) for href, codes in self._learned.items()}

    def clear(self) -> None:
        with self._lock:
            self._learned = {}
