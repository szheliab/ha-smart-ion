"""
The Smart iON CS-8 custom integration.

Vendorizes the ``smart_ion`` device model (see ``device.py``) so this
integration is self-contained and testable via HACS today, without depending
on Home Assistant's not-yet-released shared ``modbus_connection`` integration.
It owns its Modbus connection directly and closes it on unload.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.const import CONF_HOST, CONF_PORT, Platform
from modbus_connection import ModbusSerialParams, ModbusTcpParams
from modbus_connection.pymodbus import PymodbusConnection

from .const import (
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_DELAY,
    CONF_DEVICE,
    CONF_FRAMER,
    CONF_PARITY,
    CONF_STOPBITS,
    CONF_TIMEOUT,
    CONF_TRANSPORT,
    CONF_UNIT_ID,
    TRANSPORT_SERIAL,
)
from .coordinator import SmartIonCoordinator
from .data import SmartIonConfigEntry, SmartIonRuntimeData
from .device import SmartIonCS8

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

PLATFORMS = [Platform.BINARY_SENSOR, Platform.NUMBER, Platform.SENSOR, Platform.SWITCH]


def _build_connection(data: dict[str, Any]) -> PymodbusConnection:
    """Build the Modbus connection described by a config entry (no I/O yet)."""
    if data[CONF_TRANSPORT] == TRANSPORT_SERIAL:
        params: ModbusSerialParams | ModbusTcpParams = ModbusSerialParams(
            device=data[CONF_DEVICE],
            baudrate=data[CONF_BAUDRATE],
            bytesize=data[CONF_BYTESIZE],
            parity=data[CONF_PARITY],
            stopbits=data[CONF_STOPBITS],
        )
    else:
        params = ModbusTcpParams(
            host=data[CONF_HOST], port=data[CONF_PORT], framer=data[CONF_FRAMER]
        )
    return PymodbusConnection(
        params, timeout=data[CONF_TIMEOUT], connect_delay=data[CONF_DELAY]
    )


async def async_setup_entry(hass: HomeAssistant, entry: SmartIonConfigEntry) -> bool:
    """Set up a Smart iON CS-8 board from a config entry."""
    connection = _build_connection(entry.data)
    await connection.connect()
    unit = connection.for_unit(int(entry.data[CONF_UNIT_ID]))
    device = SmartIonCS8(unit)
    coordinator = SmartIonCoordinator(hass, entry, device)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = SmartIonRuntimeData(
        connection=connection, coordinator=coordinator
    )
    entry.async_on_unload(
        connection.on_connection_lost(
            lambda: hass.config_entries.async_schedule_reload(entry.entry_id)
        )
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: SmartIonConfigEntry) -> bool:
    """Unload a config entry and close its owned Modbus connection."""
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        await entry.runtime_data.connection.close()
    return unloaded
