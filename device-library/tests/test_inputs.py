"""Tests for the discrete input states."""

from __future__ import annotations

import pytest

from smart_ion import INPUT_COUNT, Inputs

pytestmark = pytest.mark.asyncio


async def test_inputs_read_all_off_by_default(mock_modbus_unit) -> None:
    """A freshly-loaded mock unit reports every DI as off."""
    inputs = Inputs(mock_modbus_unit)
    await inputs.async_update()
    for index in range(1, INPUT_COUNT + 1):
        assert getattr(inputs, f"di_{index}") is False


async def test_inputs_read_seeded_state(mock_modbus_unit) -> None:
    """Seeded discrete values are decoded onto matching DI attributes."""
    mock_modbus_unit.load_raw({"discrete": {0: True, 1: False, 7: True}})
    inputs = Inputs(mock_modbus_unit)
    await inputs.async_update()
    assert inputs.di_1 is True
    assert inputs.di_2 is False
    assert inputs.di_8 is True
