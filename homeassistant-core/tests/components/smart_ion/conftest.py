"""Fixtures for the Smart iON CS-8 tests.

The ``mock_modbus_connection`` / ``mock_modbus_unit`` fixtures come from the
``modbus_connection`` library's pytest plugin (registered as a ``pytest11``
entry point). Seeding the unit's stores drives the real ``smart_ion`` library
exactly as a board would.
"""

from __future__ import annotations

from collections.abc import Generator
from unittest.mock import patch

import pytest

from homeassistant.components.smart_ion.const import DOMAIN
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry


@pytest.fixture
def mock_setup_entry() -> Generator[None]:
    """Prevent actual entry setup from running during config-flow tests."""
    with patch(
        "homeassistant.components.smart_ion.async_setup_entry", return_value=True
    ):
        yield


@pytest.fixture
def mock_config_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Return a mock config entry for a CS-8 board on unit id 7."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Smart iON CS-8 (7)",
        data={"connection_entry_id": "modbus_connection_1", "unit_id": 7},
        unique_id="modbus_connection_1_7",
    )
    entry.add_to_hass(hass)
    return entry
