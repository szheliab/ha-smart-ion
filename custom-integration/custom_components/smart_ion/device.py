"""
Vendorized Smart iON CS-8 device model.

This mirrors ``device-library/src/smart_ion`` so the custom integration is
self-contained and can be installed via HACS without a separate PyPI release.
Keep this file in sync with the device library if the register map changes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from modbus_connection.model import (
    Component,
    ComponentGroup,
    coil,
    discrete_input,
    integer,
    string,
    uint32,
)

if TYPE_CHECKING:
    from modbus_connection import ModbusUnit

RELAY_COUNT = 8
INPUT_COUNT = 8


class Relays(Component):
    """The eight switched relay outputs of one Smart iON CS-8 board."""

    relay_1 = coil(0x000, writable=True)
    relay_2 = coil(0x001, writable=True)
    relay_3 = coil(0x002, writable=True)
    relay_4 = coil(0x003, writable=True)
    relay_5 = coil(0x004, writable=True)
    relay_6 = coil(0x005, writable=True)
    relay_7 = coil(0x006, writable=True)
    relay_8 = coil(0x007, writable=True)


class Inputs(Component):
    """The eight read-only discrete inputs of one Smart iON CS-8 board."""

    di_1 = discrete_input(0x000)
    di_2 = discrete_input(0x001)
    di_3 = discrete_input(0x002)
    di_4 = discrete_input(0x003)
    di_5 = discrete_input(0x004)
    di_6 = discrete_input(0x005)
    di_7 = discrete_input(0x006)
    di_8 = discrete_input(0x007)


class Diagnostics(Component):
    """Read-only diagnostic values exposed in input registers."""

    register_space = "input"

    module_name = string(0x00C0, 10)
    serial_number = string(0x00BB, 5)
    firmware_version = string(0x00CC, 2)

    uptime = uint32(0x0205, unit="s")
    request_count = uint32(0x020A)
    no_response_count = uint32(0x020C)
    error_count = uint32(0x020E)
    crc_error_count = uint32(0x0210)


class Settings(Component):
    """Read-only holding-register configuration values."""

    address = integer(0x0100, signed=False)
    baud_rate_code = integer(0x0101, signed=False)
    data_format_code = integer(0x0102, signed=False)
    debounce_duration_ms = integer(0x0103, signed=False, unit="ms", writable=True)
    long_press_threshold_ms = integer(0x0104, signed=False, unit="ms", writable=True)


class AutoOffTimers(Component):
    """Raw packed AutoOff timers in holding registers 0x0421-0x0428."""

    autooff_relay_1_raw = integer(0x0421, signed=False)
    autooff_relay_2_raw = integer(0x0422, signed=False)
    autooff_relay_3_raw = integer(0x0423, signed=False)
    autooff_relay_4_raw = integer(0x0424, signed=False)
    autooff_relay_5_raw = integer(0x0425, signed=False)
    autooff_relay_6_raw = integer(0x0426, signed=False)
    autooff_relay_7_raw = integer(0x0427, signed=False)
    autooff_relay_8_raw = integer(0x0428, signed=False)


class DelayTimers(Component):
    """Raw packed delay timers in holding registers 0x0431-0x0438."""

    delay_relay_1_raw = integer(0x0431, signed=False)
    delay_relay_2_raw = integer(0x0432, signed=False)
    delay_relay_3_raw = integer(0x0433, signed=False)
    delay_relay_4_raw = integer(0x0434, signed=False)
    delay_relay_5_raw = integer(0x0435, signed=False)
    delay_relay_6_raw = integer(0x0436, signed=False)
    delay_relay_7_raw = integer(0x0437, signed=False)
    delay_relay_8_raw = integer(0x0438, signed=False)


class SmartIonCS8:
    """An 8-channel Smart iON CS-8 Modbus relay/contactor board."""

    def __init__(self, unit: ModbusUnit) -> None:
        """Build the device model over the given unit; performs no I/O."""
        self.relays = Relays(unit)
        self.inputs = Inputs(unit)
        self.diagnostics = Diagnostics(unit)
        self.settings = Settings(unit)
        self.autooff_timers = AutoOffTimers(unit)
        self.delay_timers = DelayTimers(unit)
        self._components = ComponentGroup(
            unit,
            (
                self.relays,
                self.inputs,
                self.diagnostics,
                self.settings,
                self.autooff_timers,
                self.delay_timers,
            ),
        )

    async def async_update(self) -> None:
        """Refresh relay and settings state with as-few-as-possible reads."""
        await self._components.async_update()

    async def async_set_relay(self, index: int, *, value: bool) -> None:
        """Turn one relay (1-8) on or off."""
        if not 1 <= index <= RELAY_COUNT:
            msg = f"relay index must be 1-{RELAY_COUNT}, got {index}"
            raise ValueError(msg)
        await self.relays.write(f"relay_{index}", value=value)

    def relay_state(self, index: int) -> bool | None:
        """Return the last-known state of one relay (1-8)."""
        if not 1 <= index <= RELAY_COUNT:
            msg = f"relay index must be 1-{RELAY_COUNT}, got {index}"
            raise ValueError(msg)
        return getattr(self.relays, f"relay_{index}")

    def input_state(self, index: int) -> bool | None:
        """Return the last-known state of one discrete input (1-8)."""
        if not 1 <= index <= INPUT_COUNT:
            msg = f"input index must be 1-{INPUT_COUNT}, got {index}"
            raise ValueError(msg)
        return getattr(self.inputs, f"di_{index}")
