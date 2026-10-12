"""Select entities for Smart iON CS-8 input switch types."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory

from .device import INPUT_COUNT
from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonCoordinator
    from .data import SmartIonConfigEntry

OPTION_MOMENTARY = "momentary"
OPTION_STATE = "state"
OPTIONS = [OPTION_MOMENTARY, OPTION_STATE]


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up input switch-type select entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SmartIonInputModeSelect(coordinator, index)
        for index in range(1, INPUT_COUNT + 1)
    )


class SmartIonInputModeSelect(SmartIonEntity, SelectEntity):
    """Switch type (momentary or state) of one input."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_options = OPTIONS

    def __init__(self, coordinator: SmartIonCoordinator, index: int) -> None:
        """Initialize the select entity for input ``index`` (1-8)."""
        super().__init__(coordinator, f"input_{index}_switch_type")
        self._index = index
        self._attr_translation_key = "input_switch_type"
        self._attr_translation_placeholders = {"input": str(index)}

    @property
    def current_option(self) -> str | None:
        """Return the configured switch type of this input."""
        mask = self.coordinator.device.settings.input_mode_mask
        if mask is None:
            return None
        return OPTION_STATE if mask >> (self._index - 1) & 1 else OPTION_MOMENTARY

    async def async_select_option(self, option: str) -> None:
        """Write the switch type, preserving the other inputs' bits."""
        await self.coordinator.device.async_set_input_mode(
            self._index, state=option == OPTION_STATE
        )
        self.coordinator.request_diagnostics_refresh()
        await self.coordinator.async_request_refresh()
