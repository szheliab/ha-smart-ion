"""Configuration registers of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, integer


class Settings(Component):
    """Holding-register configuration values."""

    address = integer(0x0100, signed=False)
    """The board's own configured Modbus station (unit) address."""

    baud_rate_code = integer(0x0101, signed=False)
    """Protocol-specific baud-rate code."""

    data_format_code = integer(0x0102, signed=False)
    """Protocol-specific serial data-format code."""

    debounce_duration_ms = integer(0x0103, signed=False, unit="ms", writable=True)
    """Input debounce duration in milliseconds."""

    long_press_threshold_ms = integer(0x0104, signed=False, unit="ms", writable=True)
    """Long-press threshold in milliseconds."""
