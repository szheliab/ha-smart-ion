"""Diagnostic sensors for Smart iON CS-8."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonCoordinator
    from .data import SmartIonConfigEntry
    from .device import SmartIonCS8


@dataclass(frozen=True, kw_only=True)
class SmartIonSensorDescription(SensorEntityDescription):
    """Describe a Smart iON CS-8 diagnostic sensor."""

    value_fn: Callable[[SmartIonCS8], int | None]


DESCRIPTIONS: tuple[SmartIonSensorDescription, ...] = (
    SmartIonSensorDescription(
        key="address",
        translation_key="address",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda device: device.settings.address,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up diagnostic sensor entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SmartIonSensor(coordinator, description) for description in DESCRIPTIONS
    )


class SmartIonSensor(SmartIonEntity, SensorEntity):
    """A read-only Smart iON CS-8 configuration register."""

    entity_description: SmartIonSensorDescription

    def __init__(
        self, coordinator: SmartIonCoordinator, description: SmartIonSensorDescription
    ) -> None:
        """Initialize the diagnostic sensor entity."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> int | None:
        """Return the current register value."""
        return self.entity_description.value_fn(self.coordinator.device)
