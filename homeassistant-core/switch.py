from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from device_library.src.smart_ion.registry import load_default_library


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    library = load_default_library()
    async_add_entities([SmartIonSwitch(entity) for entity in library.profile.switches])


class SmartIonSwitch(SwitchEntity):
    def __init__(self, definition) -> None:
        self._definition = definition
        self._attr_name = definition.name
        self._attr_unique_id = definition.unique_id
        self._state = False

    async def async_turn_on(self, **kwargs) -> None:
        self._state = True

    async def async_turn_off(self, **kwargs) -> None:
        self._state = False

    @property
    def is_on(self) -> bool:
        return self._state

