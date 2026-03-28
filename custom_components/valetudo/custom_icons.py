from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .file_utils import VERSION, BASE_PATH


# Adapted from https://github.com/hacs/integration/blob/7d46a52de0df2466aa65e446458b952150398f4c/custom_components/hacs/frontend.py#L58
try:
    from homeassistant.components.frontend import add_extra_js_url
except ImportError:
    def add_extra_js_url(hass: HomeAssistant, url: str, es5: bool = False) -> None:
        if "frontend_extra_module_url" not in hass.data:
            hass.data["frontend_extra_module_url"] = set()
        hass.data["frontend_extra_module_url"].add(url)


async def async_setup_icons(hass: HomeAssistant) -> None:
    static_paths = [
        StaticPathConfig(
            f'/assets/{DOMAIN}/icons.js',
            hass.config.path(f'{BASE_PATH}/res/icons.js'),
            cache_headers=False
        )
    ]

    await hass.http.async_register_static_paths(static_paths)
    
    add_extra_js_url(hass, f"/assets/{DOMAIN}/icons.js?v={VERSION}")
