from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from device_library.src.smart_ion.registry import load_default_library

from .const import DOMAIN

DEVICE_IDENTIFIER = (DOMAIN, "smart_ion_cs_8")


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    library = load_default_library()
    async_add_entities([SmartIonSwitch(entity) for entity in library.switch_entities])


class SmartIonSwitch(SwitchEntity):
    def __init__(self, definition) -> None:
        self._definition = definition
        self._state = False
        self._attr_name = definition.name
        self._attr_unique_id = definition.unique_id
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {DEVICE_IDENTIFIER},
            "name": "Smart iOn CS-8",
            "manufacturer": "Smart iOn",
            "model": "CS-8",
        }

    async def async_turn_on(self, **kwargs) -> None:
        self._state = True

    async def async_turn_off(self, **kwargs) -> None:
        self._state = False

    @property
    def is_on(self) -> bool:
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, object]:
        return {
            "address": self._definition.address,
            "slave": self._definition.slave,
            "unique_id": self._definition.unique_id,
            "write_type": self._definition.write_type,
        }
