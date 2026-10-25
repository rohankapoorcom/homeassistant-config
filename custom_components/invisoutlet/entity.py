"""Base entity for the InvisOutlet integration."""

from __future__ import annotations

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import InvisOutletCoordinator


def configuration_url(host: str | None, hw_rev: str | None) -> str | None:
    """The device page's "Visit device" link, or None when there's nothing to visit.

    revB hardware has no web UI.
    """
    if not host or hw_rev == "revB":
        return None
    return f"http://{host}"


class InvisOutletEntity(CoordinatorEntity[InvisOutletCoordinator]):
    """Base entity tying everything to the device registry entry."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: InvisOutletCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        info = coordinator.device_info
        connections = {(CONNECTION_NETWORK_MAC, info.mac)} if info.mac else set()
        name = " ".join(p for p in (info.device, info.serial_number) if p)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, info.serial_number)},
            connections=connections,
            manufacturer=MANUFACTURER,
            model=info.device or None,
            sw_version=info.fw_rev,
            serial_number=info.serial_number,
            name=name or MANUFACTURER,
            configuration_url=configuration_url(info.host, info.hw_rev),
        )
