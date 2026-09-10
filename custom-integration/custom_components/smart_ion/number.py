"""Writable number entities for Smart iON CS-8 settings."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.const import EntityCategory

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonCoordinator
    from .data import SmartIonConfigEntry


@dataclass(frozen=True, kw_only=True)
class SmartIonNumberDescription(NumberEntityDescription):
    """Describe one writable setting register."""

    field: str


DESCRIPTIONS = (
    SmartIonNumberDescription(
        key="debounce_duration_ms",
        name="Debounce duration",
        field="debounce_duration_ms",
        native_unit_of_measurement="ms",
        native_min_value=1,
        native_max_value=500,
        native_step=5,
        entity_category=EntityCategory.CONFIG,
    ),
    SmartIonNumberDescription(
        key="long_press_threshold_ms",
        name="Long press threshold",
        field="long_press_threshold_ms",
        native_unit_of_measurement="ms",
        native_min_value=500,
        native_max_value=5000,
        native_step=50,
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up writable number entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SmartIonNumber(coordinator, description) for description in DESCRIPTIONS
    )


class SmartIonNumber(SmartIonEntity, NumberEntity):
    """One writable Smart iON holding-register value."""

    entity_description: SmartIonNumberDescription

    def __init__(
        self,
        coordinator: SmartIonCoordinator,
        description: SmartIonNumberDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> float | None:
        """Return the current register value as a number."""
        value = getattr(self.coordinator.device.settings, self.entity_description.field)
        if value is None:
            return None
        return float(value)

    async def async_set_native_value(self, value: float) -> None:
        """Write a new register value."""
        await self.coordinator.device.settings.write(
            self.entity_description.field,
            int(value),
        )
        await self.coordinator.async_request_refresh()
