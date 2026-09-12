"""Tests for packed AutoOff/Delay timer registers."""

from __future__ import annotations

import pytest

from smart_ion import AutoOffTimers, DelayTimers

pytestmark = pytest.mark.asyncio


async def test_autooff_timer_reads(mock_modbus_unit) -> None:
    """AutoOff raw register values are decoded from 0x0421-0x0428."""
    mock_modbus_unit.load_raw({"holding": {0x0421: 258, 0x0428: 772}})
    timers = AutoOffTimers(mock_modbus_unit)
    await timers.async_update()
    assert timers.autooff_relay_1_raw == 258
    assert timers.autooff_relay_8_raw == 772


async def test_delay_timer_reads(mock_modbus_unit) -> None:
    """Delay raw register values are decoded from 0x0431-0x0438."""
    mock_modbus_unit.load_raw({"holding": {0x0431: 515, 0x0438: 1029}})
    timers = DelayTimers(mock_modbus_unit)
    await timers.async_update()
    assert timers.delay_relay_1_raw == 515
    assert timers.delay_relay_8_raw == 1029
