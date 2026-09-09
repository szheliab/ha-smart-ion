"""The Smart iON CS-8 relay board, reached through a ``ModbusUnit``."""

from __future__ import annotations

from modbus_connection import ModbusUnit
from modbus_connection.model import ComponentGroup

from .relays import RELAY_COUNT, Relays
from .settings import Settings


class SmartIonCS8:
    """An 8-channel Smart iON CS-8 Modbus relay/contactor board.

    One board answers on one Modbus unit (station) address. Several boards on
    the same RS-485 line or RTU-over-TCP gateway are modelled as one
    ``SmartIonCS8`` instance per unit address, each built from its own
    ``ModbusUnit`` (``connection.for_unit(unit_id)``).
    """

    def __init__(self, unit: ModbusUnit) -> None:
        """Build the device model over the given unit; performs no I/O."""
        self._unit = unit
        self.relays = Relays(unit)
        self.settings = Settings(unit)
        self._components = ComponentGroup(unit, (self.relays, self.settings))

    async def async_update(self) -> None:
        """Refresh every sub-system in as few Modbus requests as possible."""
        await self._components.async_update()

    async def async_set_relay(self, index: int, value: bool) -> None:
        """Turn one relay (1-8) on or off."""
        if not 1 <= index <= RELAY_COUNT:
            raise ValueError(f"relay index must be 1-{RELAY_COUNT}, got {index}")
        await self.relays.write(f"relay_{index}", value)

    def relay_state(self, index: int) -> bool | None:
        """Current known state of one relay (1-8), or ``None`` if not yet read."""
        if not 1 <= index <= RELAY_COUNT:
            raise ValueError(f"relay index must be 1-{RELAY_COUNT}, got {index}")
        return getattr(self.relays, f"relay_{index}")
