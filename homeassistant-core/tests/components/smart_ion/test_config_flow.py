"""Test the Smart iON CS-8 config flow."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from modbus_connection import ModbusError

from homeassistant.components.smart_ion.const import DOMAIN
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType


async def test_user_flow_creates_entry(
    hass: HomeAssistant, mock_setup_entry: None
) -> None:
    """A reachable unit creates a config entry."""
    unit = AsyncMock()
    unit.read_coils = AsyncMock(return_value=[False])
    with patch(
        "homeassistant.components.smart_ion.config_flow.async_get_unit",
        return_value=unit,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"connection_entry_id": "modbus_connection_1", "unit_id": 7},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Smart iON CS-8 (7)"
    assert result["data"] == {
        "connection_entry_id": "modbus_connection_1",
        "unit_id": 7,
    }


@pytest.mark.parametrize("error", [ModbusError("timed out"), OSError("no route")])
async def test_user_flow_cannot_connect(
    hass: HomeAssistant, mock_setup_entry: None, error: Exception
) -> None:
    """An unreachable unit shows a form with an error instead of aborting."""
    unit = AsyncMock()
    unit.read_coils = AsyncMock(side_effect=error)
    with patch(
        "homeassistant.components.smart_ion.config_flow.async_get_unit",
        return_value=unit,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {"connection_entry_id": "modbus_connection_1", "unit_id": 7},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
