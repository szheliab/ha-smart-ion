"""Coordinator for Smart iON CS-8 live state."""

import logging

from modbus_connection import ModbusError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, FAST_SCAN_INTERVAL
from .device import SmartIonCS8

_LOGGER = logging.getLogger(__name__)
type SmartIonConfigEntry = ConfigEntry[SmartIonCoordinator]


class SmartIonCoordinator(DataUpdateCoordinator[SmartIonCS8]):
    """Poll relay and discrete input state."""

    def __init__(
        self, hass: HomeAssistant, entry: SmartIonConfigEntry, device: SmartIonCS8
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=FAST_SCAN_INTERVAL,
        )
        self.device = device

    async def _async_update_data(self) -> SmartIonCS8:
        try:
            await self.device.async_update()
        except ModbusError as err:
            raise UpdateFailed(f"Error communicating with Smart iON CS-8: {err}") from err
        return self.device
