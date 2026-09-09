"""Tests for the top-level ``SmartIonCS8`` device object."""

from __future__ import annotations

import pytest

from smart_ion import SmartIonCS8

pytestmark = pytest.mark.asyncio


async def test_device_update_reads_relays_and_settings(mock_modbus_unit) -> None:
    """A single update refreshes both the relays and the settings component."""
    mock_modbus_unit.load_raw({"coil": {2: True}, "holding": {0x100: 3}})
    board = SmartIonCS8(mock_modbus_unit)
    await board.async_update()
    assert board.relay_state(3) is True
    assert board.settings.address == 3


async def test_set_relay_writes_and_reads_back(mock_modbus_unit) -> None:
    """Setting a relay writes the coil; a following update reflects it."""
    board = SmartIonCS8(mock_modbus_unit)
    await board.async_set_relay(5, True)
    await board.async_update()
    assert board.relay_state(5) is True


@pytest.mark.parametrize("index", [0, 9, -1])
async def test_set_relay_validates_index(mock_modbus_unit, index: int) -> None:
    """An out-of-range relay index is rejected before touching the wire."""
    board = SmartIonCS8(mock_modbus_unit)
    with pytest.raises(ValueError):
        await board.async_set_relay(index, True)
