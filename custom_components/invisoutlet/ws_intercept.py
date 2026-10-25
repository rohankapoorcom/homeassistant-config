"""Generic websocket-command interception.

Lets an integration wrap a websocket command that another integration owns,
handling some requests itself and delegating the rest to the original handler,
unchanged. The wrapper is registered last (last registration wins in the
websocket command registry) and can be re-asserted whenever the owning
integration reloads, so the owner re-registering its command never orphans us.

This is deliberately domain-agnostic; nothing here knows about Matter or
InvisOutlet. It could be lifted out into a shared helper or plugin as-is.
"""

from __future__ import annotations

import logging

from homeassistant.components import websocket_api
from homeassistant.components.websocket_api import const as ws_const
from homeassistant.config_entries import (
    SIGNAL_CONFIG_ENTRY_CHANGED,
    ConfigEntry,
    ConfigEntryChange,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

_LOGGER = logging.getLogger(__name__)

# hass.data key: {command: original handler tuple (or None)} we wrapped.
_DATA_DELEGATES = "ws_command_intercept_delegates"


@callback
def _install(hass: HomeAssistant, command: str, wrapper) -> None:
    """Capture the current handler as delegate and register wrapper last.

    Idempotent, and must not await: the websocket registry is a plain dict, so
    reading the current handler and registering ours has to happen in one tick
    or a concurrent (re)registration could slip between them.
    """
    handlers = hass.data.get(ws_const.DOMAIN)
    current = handlers.get(command) if handlers else None
    if current is not None and current[0] is wrapper:
        return  # already ours; delegate already captured
    hass.data.setdefault(_DATA_DELEGATES, {})[command] = current
    websocket_api.async_register_command(hass, wrapper)
    _LOGGER.debug(
        "Installed wrapper for %s (delegate=%s)",
        command,
        "present" if current else "none",
    )


@callback
def async_intercept_command(
    hass: HomeAssistant,
    command: str,
    wrapper,
    *,
    reassert_domain: str | None = None,
) -> None:
    """Wrap ``command`` with ``wrapper`` for the life of HA.

    ``wrapper`` is a decorated websocket command handler (``@websocket_command``
    et al.) whose ``type`` matches ``command``. If ``reassert_domain`` is given,
    the wrapper is re-installed whenever a config entry of that domain changes
    state (load/reload), so the owner re-registering its command can't displace
    us. Subscribe before the catch-up install so an entry loading in the same
    tick can't slip past.
    """
    if reassert_domain is not None:

        @callback
        def _on_entry_change(change: ConfigEntryChange, entry: ConfigEntry) -> None:
            if entry.domain == reassert_domain:
                _install(hass, command, wrapper)

        async_dispatcher_connect(hass, SIGNAL_CONFIG_ENTRY_CHANGED, _on_entry_change)

    _install(hass, command, wrapper)


@callback
def async_delegate(
    hass: HomeAssistant,
    command: str,
    connection: websocket_api.ActiveConnection,
    msg: dict,
) -> None:
    """Hand a request to the wrapped handler, or reply unknown-command if none."""
    delegate = hass.data.get(_DATA_DELEGATES, {}).get(command)
    if delegate is not None:
        handler, schema = delegate
        handler(hass, connection, schema(msg) if schema else msg)
    else:
        connection.send_error(
            msg["id"], ws_const.ERR_UNKNOWN_COMMAND, "Unknown command."
        )
