"""Custom types for the Smart iON CS-8 custom integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from modbus_connection.pymodbus import PymodbusConnection

    from .coordinator import SmartIonCoordinator


type SmartIonConfigEntry = ConfigEntry[SmartIonRuntimeData]


@dataclass
class SmartIonRuntimeData:
    """Runtime data for one Smart iON CS-8 config entry."""

    connection: PymodbusConnection
    coordinator: SmartIonCoordinator
