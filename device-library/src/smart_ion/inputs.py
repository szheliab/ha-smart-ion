"""Discrete input states of a Smart iON CS-8 board."""

from __future__ import annotations

from modbus_connection.model import Component, bit, discrete_input

INPUT_COUNT = 8


class Inputs(Component):
    """The eight read-only discrete inputs of one Smart iON CS-8 board."""

    di_1 = discrete_input(0x000)
    di_2 = discrete_input(0x001)
    di_3 = discrete_input(0x002)
    di_4 = discrete_input(0x003)
    di_5 = discrete_input(0x004)
    di_6 = discrete_input(0x005)
    di_7 = discrete_input(0x006)
    di_8 = discrete_input(0x007)

    # Input status (holding 0x1001): equals the contact state for state-type
    # switches and toggles on each press for momentary ones.
    di_1_status = bit(0x1001, 0)
    di_2_status = bit(0x1001, 1)
    di_3_status = bit(0x1001, 2)
    di_4_status = bit(0x1001, 3)
    di_5_status = bit(0x1001, 4)
    di_6_status = bit(0x1001, 5)
    di_7_status = bit(0x1001, 6)
    di_8_status = bit(0x1001, 7)
