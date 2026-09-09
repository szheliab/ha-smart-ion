"""Coordinator for Smart iON CS-8 live state."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from modbus_connection import ModbusError

from .const import DOMAIN, SCAN_INTERVAL
from .data import SmartIonConfigEntry
from .device import SmartIonCS8

_LOGGER = logging.getLogger(__name__)


class SmartIonCoordinator(DataUpdateCoordinator[SmartIonCS8]):
    """Poll relay and settings state for one Smart iON CS-8 board."""

    def __init__(
        self, hass: HomeAssistant, entry: SmartIonConfigEntry, device: SmartIonCS8
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.device = device

    async def _async_update_data(self) -> SmartIonCS8:
        try:
            await self.device.async_update()
        except ModbusError as err:
            raise UpdateFailed(
                f"Error communicating with Smart iON CS-8: {err}"
            ) from err
        return self.device
