"""Coordinator for Smart iON CS-8 live state."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from modbus_connection import ModbusError

from .const import DOMAIN, SCAN_INTERVAL
from .device import SmartIonCS8

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from modbus_connection.pymodbus import PymodbusConnection

    from .data import SmartIonConfigEntry

_LOGGER = logging.getLogger(__name__)


class SmartIonCoordinator(DataUpdateCoordinator[SmartIonCS8]):
    """Poll relay and settings state for one Smart iON CS-8 board."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: SmartIonConfigEntry,
        device: SmartIonCS8,
        connection: PymodbusConnection,
    ) -> None:
        """Initialize the coordinator for one Smart iON CS-8 board."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device
        self.connection = connection

    async def _async_update_data(self) -> SmartIonCS8:
        try:
            await self.device.async_update()
        except ModbusError:
            await self.connection.connect()
            try:
                await self.device.async_update()
            except ModbusError as second_err:
                msg = f"Error communicating with Smart iON CS-8: {second_err}"
                raise UpdateFailed(msg) from second_err
        return self.device
