from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
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
    async_add_entities([SmartIonSensor(entity) for entity in library.sensor_entities])


class SmartIonSensor(SensorEntity):
    def __init__(self, definition) -> None:
        self._definition = definition
        self._attr_name = definition.name
        self._attr_unique_id = definition.unique_id
        self._attr_has_entity_name = True
        self._attr_device_info = {
            "identifiers": {DEVICE_IDENTIFIER},
            "name": "Smart iOn CS-8",
            "manufacturer": "Smart iOn",
            "model": "CS-8",
        }

    @property
    def native_value(self):
        return self._definition.address

    @property
    def extra_state_attributes(self):
        return {
            "address": self._definition.address,
            "slave": self._definition.slave,
            "domain": self._definition.domain,
            "input_type": self._definition.input_type,
        }
