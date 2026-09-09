"""Coordinator for Smart iON CS-8."""

import logging

from modbus_connection import ModbusError
from smart_ion import SmartIonCS8

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)
type SmartIonConfigEntry = ConfigEntry[SmartIonCoordinator]


class SmartIonCoordinator(DataUpdateCoordinator[SmartIonCS8]):
    """Poll the fast-changing relay and input state."""

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
            await self.device.async_update_fast()
        except ModbusError as err:
            raise UpdateFailed(f"Error communicating with Smart iON CS-8: {err}") from err
        return self.device
