"""Tests for the relay outputs (coils)."""

from __future__ import annotations

import pytest

from smart_ion import RELAY_COUNT, Relays

pytestmark = pytest.mark.asyncio


async def test_relays_read_all_off_by_default(mock_modbus_unit) -> None:
    """A freshly-loaded mock unit reports every coil as off."""
    relays = Relays(mock_modbus_unit)
    await relays.async_update()
    for index in range(1, RELAY_COUNT + 1):
        assert getattr(relays, f"relay_{index}") is False


async def test_relays_read_seeded_state(mock_modbus_unit) -> None:
    """Seeded coil values are decoded onto the matching attribute."""
    mock_modbus_unit.load_raw({"coil": {0: True, 1: False, 7: True}})
    relays = Relays(mock_modbus_unit)
    await relays.async_update()
    assert relays.relay_1 is True
    assert relays.relay_2 is False
    assert relays.relay_8 is True


async def test_write_relay(mock_modbus_unit) -> None:
    """Writing a relay by attribute name sends a coil write."""
    relays = Relays(mock_modbus_unit)
    await relays.write("relay_3", True)
    await relays.async_update()
    assert relays.relay_3 is True
