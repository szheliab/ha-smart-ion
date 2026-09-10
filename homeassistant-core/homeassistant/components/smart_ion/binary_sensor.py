"""Binary sensor entities for Smart iON CS-8 discrete inputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonConfigEntry, SmartIonCoordinator


@dataclass(frozen=True, kw_only=True)
class SmartIonBinarySensorDescription(BinarySensorEntityDescription):
    """Describe one discrete input."""

    field: str


DESCRIPTIONS = tuple(
    SmartIonBinarySensorDescription(
        key=f"di_{index}",
        name=f"DI {index}",
        field=f"di_{index}",
    )
    for index in range(1, 9)
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DI entities."""
    async_add_entities(
        SmartIonBinarySensor(entry.runtime_data, description)
        for description in DESCRIPTIONS
    )


class SmartIonBinarySensor(SmartIonEntity, BinarySensorEntity):
    """One discrete input state."""

    entity_description: SmartIonBinarySensorDescription

    def __init__(
        self,
        coordinator: SmartIonCoordinator,
        description: SmartIonBinarySensorDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return true when the input is active."""
        return getattr(self.coordinator.device.inputs, self.entity_description.field)
