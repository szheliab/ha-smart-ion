"""Configuration registers of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, integer


class Settings(Component):
    """Read-only configuration registers, starting at holding register 0x100."""

    address = integer(0x100, signed=False)
    """The board's own configured Modbus station (unit) address."""
