"""Smart iON CS-8 integration."""

from smart_ion import SmartIonCS8

from homeassistant.components.modbus_connection import async_get_unit
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_CONNECTION, CONF_UNIT_ID
from .coordinator import SmartIonConfigEntry, SmartIonCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: SmartIonConfigEntry) -> bool:
    """Set up a CS-8 from a selected Modbus Connection unit."""
    unit = async_get_unit(
        hass, entry.data[CONF_CONNECTION], int(entry.data[CONF_UNIT_ID])
    )
    coordinator = SmartIonCoordinator(hass, entry, SmartIonCS8(unit))
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    entry.async_on_unload(
        unit.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: SmartIonConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
