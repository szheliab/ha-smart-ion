"""The relay outputs of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, coil

RELAY_COUNT = 8


class Relays(Component):
    """The eight switched relay outputs of one Smart iON CS-8 board.

    Each output is a single coil, written with function code 0x05 (write
    single coil) and read back with function code 0x01 (read coils).
    """

    relay_1 = coil(0x000, writable=True)
    relay_2 = coil(0x001, writable=True)
    relay_3 = coil(0x002, writable=True)
    relay_4 = coil(0x003, writable=True)
    relay_5 = coil(0x004, writable=True)
    relay_6 = coil(0x005, writable=True)
    relay_7 = coil(0x006, writable=True)
    relay_8 = coil(0x007, writable=True)
