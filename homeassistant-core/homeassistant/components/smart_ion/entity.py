"""Shared Smart iON entity behavior."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SmartIonCoordinator


class SmartIonEntity(CoordinatorEntity[SmartIonCoordinator]):
    """Entity belonging to one CS-8 module."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: SmartIonCoordinator, key: str) -> None:
        """Initialize the shared entity attributes for one Smart iON CS-8."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer="Smart iON",
            model="CS-8",
            name="Smart iON CS-8",
        )
