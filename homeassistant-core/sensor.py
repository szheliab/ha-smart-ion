from __future__ import annotations
        return self._definition.address
    def native_value(self) -> StateType:
    @property

        self._attr_unique_id = definition.unique_id
        self._attr_name = definition.name
        self._definition = definition
    def __init__(self, definition) -> None:
class SmartIonSensor(SensorEntity):


    async_add_entities([SmartIonSensor(entity) for entity in library.profile.sensors])
    library = load_default_library()
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:


from device_library.src.smart_ion.registry import load_default_library
from .const import DOMAIN

from homeassistant.helpers.typing import StateType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity


