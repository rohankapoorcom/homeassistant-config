"""Frontend hack, isolated: serve and globally load commission_bridge.js.

commission_bridge.js is the frontend half of commissioning (it launches the
phone's native Matter flow and relays the finish message back). This module is
only the plumbing that loads that script into the main frontend app; nothing
else depends on it, and removing this file plus commission_bridge.js removes the
frontend hack entirely.
"""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_URL = f"/{DOMAIN}/commission_bridge.js"
_FILE = Path(__file__).parent / "commission_bridge.js"


async def async_setup_commission_bridge(hass: HomeAssistant) -> None:
    """Serve commission_bridge.js and register it as a global frontend module.

    No-ops when the frontend isn't loaded (e.g. under tests); the bridge only
    matters when the UI is present. after_dependencies orders us after frontend
    in production, so it is loaded by the time this runs there.
    """
    if "frontend" not in hass.config.components:
        return
    await hass.http.async_register_static_paths(
        [StaticPathConfig(_URL, str(_FILE), cache_headers=False)]
    )
    # Bust the webview's aggressive ES-module cache when the file changes.
    version = int(_FILE.stat().st_mtime)
    add_extra_js_url(hass, f"{_URL}?v={version}")
