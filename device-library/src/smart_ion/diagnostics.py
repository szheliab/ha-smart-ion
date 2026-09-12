"""Input-register diagnostics of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, string, uint32


class Diagnostics(Component):
    """Read-only diagnostic values exposed in input registers."""

    register_space = "input"

    module_name = string(0x00C0, 10)
    serial_number = string(0x00BB, 5)
    firmware_version = string(0x00CC, 2)

    uptime = uint32(0x0205, unit="s")
    request_count = uint32(0x020A)
    no_response_count = uint32(0x020C)
    error_count = uint32(0x020E)
    crc_error_count = uint32(0x0210)
