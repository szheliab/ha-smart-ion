"""Smart iON CS-8 device library.

An asynchronous, transport-independent Python library for the **Smart iON
CS-8** 8-channel Modbus relay/contactor board, built on top of
``modbus_connection``'s device-modelling framework.
"""

from .device import SmartIonCS8
from .relays import RELAY_COUNT, Relays
from .settings import Settings

__all__ = ["RELAY_COUNT", "Relays", "Settings", "SmartIonCS8"]
