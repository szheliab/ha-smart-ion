"""Tests for the configuration/settings registers."""

from __future__ import annotations

import pytest

from smart_ion import Settings

pytestmark = pytest.mark.asyncio


async def test_settings_reads_configured_address(mock_modbus_unit) -> None:
    """The board's configured address is read from holding register 0x100."""
    mock_modbus_unit.load_raw({"holding": {0x100: 7}})
    settings = Settings(mock_modbus_unit)
    await settings.async_update()
    assert settings.address == 7


async def test_settings_unread_is_none(mock_modbus_unit) -> None:
    """Before the first update, the address is unknown."""
    settings = Settings(mock_modbus_unit)
    assert settings.address is None
