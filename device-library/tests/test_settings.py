"""Tests for the configuration/settings registers."""

from __future__ import annotations

import pytest

from smart_ion import Settings

pytestmark = pytest.mark.asyncio


async def test_settings_reads_configured_address(mock_modbus_unit) -> None:
    """The board settings are read from holding registers 0x0100-0x0104."""
    mock_modbus_unit.load_raw(
        {"holding": {0x0100: 7, 0x0101: 3, 0x0102: 2, 0x0103: 25, 0x0104: 1000}}
    )
    settings = Settings(mock_modbus_unit)
    await settings.async_update()
    assert settings.address == 7
    assert settings.baud_rate_code == 3
    assert settings.data_format_code == 2
    assert settings.debounce_duration_ms == 25
    assert settings.long_press_threshold_ms == 1000


async def test_settings_unread_is_none(mock_modbus_unit) -> None:
    """Before the first update, the address is unknown."""
    settings = Settings(mock_modbus_unit)
    assert settings.address is None
