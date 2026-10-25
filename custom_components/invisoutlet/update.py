"""Update platform: firmware for the outlet and the attached InvisDeco."""

from __future__ import annotations

from typing import Any

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from invisoutlet import FirmwareRelease, OtaTarget

from .coordinator import InvisOutletConfigEntry, InvisOutletCoordinator
from .entity import InvisOutletEntity
from .helpers import async_add_outlet_entities

# OTA phase device_type reported during an outlet update: 3 = the WWW (web UI)
# partition, which precedes the main firmware phase.
_OTA_PHASE_WWW = 3


async def async_setup_entry(
    hass: HomeAssistant,
    entry: InvisOutletConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the firmware update entities for a config entry."""

    def build(coordinator: InvisOutletCoordinator) -> list[UpdateEntity]:
        entities = [InvisOutletUpdate(coordinator, OtaTarget.INVISOUTLET)]
        if coordinator.device_info.sub_device is not None:
            entities.append(InvisOutletUpdate(coordinator, OtaTarget.INVISDECO))
        return entities

    async_add_outlet_entities(hass, entry, async_add_entities, build)


class InvisOutletUpdate(InvisOutletEntity, UpdateEntity):
    """Firmware update for a single module (the outlet or the InvisDeco)."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_supported_features = (
        UpdateEntityFeature.INSTALL
        | UpdateEntityFeature.PROGRESS
        | UpdateEntityFeature.RELEASE_NOTES
    )

    def __init__(
        self,
        coordinator: InvisOutletCoordinator,
        target: OtaTarget,
    ) -> None:
        """Initialize the update entity."""
        super().__init__(coordinator)
        self._target = target
        self._attr_name = coordinator.model_name(target)
        self._attr_unique_id = (
            f"{coordinator.device_info.serial_number}_update_{target.name.lower()}"
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Refresh the name when device data changes (e.g. model repopulates)."""
        self._attr_name = self.coordinator.model_name(self._target)
        super()._handle_coordinator_update()

    @property
    def entity_picture(self) -> str | None:
        """Use the device-class icon, not the (missing) brands image."""
        return None

    @property
    def _release(self) -> FirmwareRelease | None:
        """Return the latest-firmware info for this module, if known."""
        return self.coordinator.firmware.get(self._target)

    @property
    def installed_version(self) -> str | None:
        """Return the installed firmware revision, or None if not known."""
        return self.coordinator.installed_version(self._target) or None

    @property
    def latest_version(self) -> str | None:
        """Return the latest available revision, or None if not known.

        Returning None (rather than guessing) leaves HA showing "Unknown"
        instead of a false "Up-to-date"/"Update available" — we only ever assert
        a verdict when both the installed and available versions are known.
        """
        release = self._release
        if release is None:
            return None
        return release.available_fw_rev or None

    @property
    def available(self) -> bool:
        """Stay available through the brief socket drop while installing.

        The outlet goes silent as it starts the OTA, so our heartbeat drops and
        reconnects the socket — every entity blips unavailable, which is honest
        for the rest of them. But an install is knowingly in progress, so the
        update dialog shouldn't flash unavailable; the install survives the
        reconnect (stall timer + result come back on their own).
        """
        if self._target in self.coordinator.ota_progress:
            return True
        return super().available

    @property
    def in_progress(self) -> bool:
        """Return whether an update is currently being installed."""
        return self._target in self.coordinator.ota_progress

    @property
    def update_percentage(self) -> int | None:
        """Return the install progress percentage, if updating."""
        return self.coordinator.ota_progress.get(self._target)

    @property
    def release_summary(self) -> str | None:
        """While installing, name the current phase (the outlet has two)."""
        if self._target not in self.coordinator.ota_progress:
            return None
        if self.coordinator.ota_phase.get(self._target) == _OTA_PHASE_WWW:
            return "Updating web UI partition…"
        return "Updating firmware…"

    async def async_release_notes(self) -> str | None:
        """Return the release notes as a markdown bullet list (one per line)."""
        release = self._release
        if release is None or not release.message:
            return None
        lines = [line.strip() for line in release.message.splitlines()]
        return "\n".join(f"- {line}" for line in lines if line)

    async def async_install(
        self, version: str | None, backup: bool, **kwargs: Any
    ) -> None:
        """Start the firmware update."""
        await self.coordinator.async_install_firmware(self._target)
