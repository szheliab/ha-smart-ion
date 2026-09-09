"""Constants for Smart iON CS-8."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "smart_ion"
CONF_CONNECTION: Final = "connection_entry_id"
CONF_UNIT_ID: Final = "unit_id"
DEFAULT_UNIT_ID: Final = 7
FAST_SCAN_INTERVAL: Final = timedelta(seconds=1)
