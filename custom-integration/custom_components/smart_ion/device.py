"""
Vendorized Smart iON CS-8 device model.

This mirrors ``device-library/src/smart_ion`` so the custom integration is
self-contained and can be installed via HACS without a separate PyPI release.
Keep this file in sync with the device library if the register map changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from modbus_connection.model import Component, ComponentGroup, coil, integer

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

RELAY_COUNT = 8


class Relays(Component):
    """The eight switched relay outputs of one Smart iON CS-8 board."""

    relay_1 = coil(0x000, writable=True)
    relay_2 = coil(0x001, writable=True)
    relay_3 = coil(0x002, writable=True)
    relay_4 = coil(0x003, writable=True)
    relay_5 = coil(0x004, writable=True)
    relay_6 = coil(0x005, writable=True)
    relay_7 = coil(0x006, writable=True)
    relay_8 = coil(0x007, writable=True)


class Settings(Component):
    """Read-only configuration registers, starting at holding register 0x100."""

    address = integer(0x100, signed=False)


class SmartIonCS8:
    """An 8-channel Smart iON CS-8 Modbus relay/contactor board."""

    def __init__(self, unit: ModbusUnit) -> None:
        """Build the device model over the given unit; performs no I/O."""
        self.relays = Relays(unit)
        self.settings = Settings(unit)
        self._components = ComponentGroup(unit, (self.relays, self.settings))

    async def async_update(self) -> None:
        """Refresh relay and settings state with as-few-as-possible reads."""
        await self._components.async_update()

    async def async_set_relay(self, index: int, *, value: bool) -> None:
        """Turn one relay (1-8) on or off."""
        if not 1 <= index <= RELAY_COUNT:
            msg = f"relay index must be 1-{RELAY_COUNT}, got {index}"
            raise ValueError(msg)
        await self.relays.write(f"relay_{index}", value=value)

    def relay_state(self, index: int) -> bool | None:
        """Return the last-known state of one relay (1-8)."""
        if not 1 <= index <= RELAY_COUNT:
            msg = f"relay index must be 1-{RELAY_COUNT}, got {index}"
            raise ValueError(msg)
        return getattr(self.relays, f"relay_{index}")
