from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import callback

from .const import DOMAIN, CONF_ENTRY_TYPE, ENTRY_TYPE_ICONS, ENTRY_TYPE_AUGMENTATIONS


class FlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        return self.async_show_menu(
            step_id="user",
            menu_options=[ENTRY_TYPE_ICONS, ENTRY_TYPE_AUGMENTATIONS],
        )

    async def async_step_icons(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        for entry in self._async_current_entries():
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_ICONS:
                return self.async_abort(reason="icons_instance_exists")

        if user_input is not None:
            return self.async_create_entry(
                title="Valetudo Icons",
                data={CONF_ENTRY_TYPE: ENTRY_TYPE_ICONS},
            )

        return self.async_show_form(step_id="icons")

    async def async_step_augmentations(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        for entry in self._async_current_entries():
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_AUGMENTATIONS:
                return self.async_abort(reason="augmentations_instance_exists")

        if user_input is not None:
            return self.async_create_entry(
                title="Augmentations",
                data={CONF_ENTRY_TYPE: ENTRY_TYPE_AUGMENTATIONS},
            )

        return self.async_show_form(step_id="augmentations")
