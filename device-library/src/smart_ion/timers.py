"""Packed timer registers of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, integer


class AutoOffTimers(Component):
    """Raw packed AutoOff timers in holding registers 0x0421-0x0428."""

    autooff_relay_1_raw = integer(0x0421, signed=False)
    autooff_relay_2_raw = integer(0x0422, signed=False)
    autooff_relay_3_raw = integer(0x0423, signed=False)
    autooff_relay_4_raw = integer(0x0424, signed=False)
    autooff_relay_5_raw = integer(0x0425, signed=False)
    autooff_relay_6_raw = integer(0x0426, signed=False)
    autooff_relay_7_raw = integer(0x0427, signed=False)
    autooff_relay_8_raw = integer(0x0428, signed=False)


class DelayTimers(Component):
    """Raw packed delay timers in holding registers 0x0431-0x0438."""

    delay_relay_1_raw = integer(0x0431, signed=False)
    delay_relay_2_raw = integer(0x0432, signed=False)
    delay_relay_3_raw = integer(0x0433, signed=False)
    delay_relay_4_raw = integer(0x0434, signed=False)
    delay_relay_5_raw = integer(0x0435, signed=False)
    delay_relay_6_raw = integer(0x0436, signed=False)
    delay_relay_7_raw = integer(0x0437, signed=False)
    delay_relay_8_raw = integer(0x0438, signed=False)
