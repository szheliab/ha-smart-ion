"""Test Smart iON CS-8 setup and unload."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


async def test_setup_and_unload(
    hass: HomeAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Setting up borrows a unit and reads it once; unloading tears it down cleanly."""
    unit = AsyncMock()
    unit.read_coils = AsyncMock(return_value=[False] * 8)
    unit.read_holding_registers = AsyncMock(return_value=[7])
    unit.on_connection_lost = AsyncMock(return_value=lambda: None)

    with patch("homeassistant.components.smart_ion.async_get_unit", return_value=unit):
        assert await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED
