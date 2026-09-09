"""Sensor platform for Smart iON CS-8."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonConfigEntry, SmartIonCoordinator


@dataclass(frozen=True, kw_only=True)
class SmartIonSensorDescription(SensorEntityDescription):
    """Describe one settings register."""

    field: str


DESCRIPTIONS = (
    SmartIonSensorDescription(
        key="address",
        name="Modbus address",
        field="address",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up settings-register entities."""
    async_add_entities(
        SmartIonSensor(entry.runtime_data, description) for description in DESCRIPTIONS
    )


class SmartIonSensor(SmartIonEntity, SensorEntity):
    """One read-only settings register."""

    entity_description: SmartIonSensorDescription

    def __init__(
        self,
        coordinator: SmartIonCoordinator,
        description: SmartIonSensorDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> int | None:
        """Return the value of the settings register."""
        return getattr(self.coordinator.device.settings, self.entity_description.field)
