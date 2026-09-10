"""Tests for input-register diagnostics."""

from __future__ import annotations

import pytest

from smart_ion import Diagnostics

pytestmark = pytest.mark.asyncio


async def test_diagnostics_read_counters(mock_modbus_unit) -> None:
    """Input-register counters are decoded from uint32 register pairs."""
    mock_modbus_unit.load_raw(
        {
            "input": {
                0x0205: 0x0000,
                0x0206: 0x000A,
                0x020A: 0x0000,
                0x020B: 0x0064,
                0x020C: 0x0000,
                0x020D: 0x0003,
                0x020E: 0x0000,
                0x020F: 0x0001,
                0x0210: 0x0000,
                0x0211: 0x0002,
            }
        }
    )
    diagnostics = Diagnostics(mock_modbus_unit)
    await diagnostics.async_update()
    assert diagnostics.uptime == 10
    assert diagnostics.request_count == 100
    assert diagnostics.no_response_count == 3
    assert diagnostics.error_count == 1
    assert diagnostics.crc_error_count == 2
