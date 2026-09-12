"""Constants for the Smart iON CS-8 custom integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "smart_ion"

CONF_TRANSPORT: Final = "transport"
CONF_FRAMER: Final = "framer"
CONF_UNIT_ID: Final = "unit_id"
CONF_TIMEOUT: Final = "timeout"
CONF_DELAY: Final = "delay"
CONF_DEVICE: Final = "device"
CONF_BAUDRATE: Final = "baudrate"
CONF_BYTESIZE: Final = "bytesize"
CONF_PARITY: Final = "parity"
CONF_STOPBITS: Final = "stopbits"

TRANSPORT_TCP: Final = "tcp"
TRANSPORT_SERIAL: Final = "serial"

DEFAULT_UNIT_ID: Final = 7
DEFAULT_TCP_PORT: Final = 502
DEFAULT_FRAMER: Final = "rtu"
DEFAULT_TIMEOUT: Final = 5
DEFAULT_DELAY: Final = 2
DEFAULT_BAUDRATE: Final = 9600
DEFAULT_BYTESIZE: Final = 8
DEFAULT_PARITY: Final = "N"
DEFAULT_STOPBITS: Final = 2

SCAN_INTERVAL: Final = timedelta(seconds=1)
DIAGNOSTIC_UPDATE_EVERY_POLLS: Final = 5
