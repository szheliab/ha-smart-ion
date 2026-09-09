"""Relay switch entities."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonCoordinator
    from .data import SmartIonConfigEntry


@dataclass(frozen=True, kw_only=True)
class SmartIonSwitchDescription(SwitchEntityDescription):
    """Describe a relay coil."""

    field: str


DESCRIPTIONS = tuple(
    SmartIonSwitchDescription(
        key=f"relay_{index}", name=f"Relay {index}", field=f"relay_{index}"
    )
    for index in range(1, 9)
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up relay entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SmartIonSwitch(coordinator, description) for description in DESCRIPTIONS
    )


class SmartIonSwitch(SmartIonEntity, SwitchEntity):
    """One writable relay coil."""

    entity_description: SmartIonSwitchDescription

    def __init__(
        self, coordinator: SmartIonCoordinator, description: SmartIonSwitchDescription
    ) -> None:
        """Initialize the relay switch entity."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        """Return true if the relay is energized."""
        return getattr(self.coordinator.device.relays, self.entity_description.field)

    async def async_turn_on(self, **kwargs: object) -> None:
        """Energize the relay."""
        del kwargs
        await self.coordinator.device.relays.write(
            self.entity_description.field, value=True
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: object) -> None:
        """De-energize the relay."""
        del kwargs
        await self.coordinator.device.relays.write(
            self.entity_description.field, value=False
        )
        await self.coordinator.async_request_refresh()
