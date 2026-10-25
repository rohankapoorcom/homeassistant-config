"""Button platform: restart the InvisOutlet and (if present) the InvisDeco."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from homeassistant.components.button import (
    ButtonDeviceClass,
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from invisoutlet import InvisOutletClient, InvisOutletError

from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import InvisOutletEntity
from .helpers import async_add_outlet_entities


@dataclass(frozen=True, kw_only=True)
class InvisOutletButtonDescription(ButtonEntityDescription):
    """A device button. ``press_fn`` runs the action.

    ``requires_subdevice`` both gates creation/availability on the faceplate and
    selects which model name (faceplate vs outlet) names the button.
    """

    press_fn: Callable[[InvisOutletClient], Awaitable[object]]
    requires_subdevice: bool = False


BUTTONS: tuple[InvisOutletButtonDescription, ...] = (
    InvisOutletButtonDescription(
        key="restart_outlet",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.DIAGNOSTIC,
        press_fn=lambda client: client.restart(),
    ),
    InvisOutletButtonDescription(
        key="restart_invisdeco",
        device_class=ButtonDeviceClass.RESTART,
        entity_category=EntityCategory.DIAGNOSTIC,
        press_fn=lambda client: client.restart_invisdeco(),
        requires_subdevice=True,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the restart buttons for a config entry."""

    def build(coordinator: InvisOutletCoordinator) -> list[ButtonEntity]:
        return [
            InvisOutletButton(coordinator, description)
            for description in BUTTONS
            if not description.requires_subdevice
            or coordinator.device_info.sub_device is not None
        ]

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletButton(InvisOutletEntity, ButtonEntity):
    """A device action button (restart)."""

    entity_description: InvisOutletButtonDescription

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        description: InvisOutletButtonDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_{description.key}"
        )
        self._attr_name = self._restart_name()

    def _restart_name(self) -> str:
        """Build the "Restart <model>" name from the coordinator's model name."""
        if self.entity_description.requires_subdevice:
            return f"Restart {self.coordinator.sub_device_name}"
        return f"Restart {self.coordinator.outlet_name}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Refresh the name only when device data changes, not on every render."""
        self._attr_name = self._restart_name()
        super()._handle_coordinator_update()

    @property
    def available(self) -> bool:
        """Gray out a sub-device action while that device is offline.

        Restarting an offline faceplate does nothing (the outlet can't relay to
        it), so there's no point offering the button until it's back.
        """
        if (
            self.entity_description.requires_subdevice
            and not self.coordinator.sub_device_online
        ):
            return False
        return super().available

    async def async_press(self) -> None:
        """Run the button's action."""
        try:
            await self.entity_description.press_fn(self.coordinator.client)
        except InvisOutletError as err:
            raise HomeAssistantError(f"Could not restart device: {err}") from err
