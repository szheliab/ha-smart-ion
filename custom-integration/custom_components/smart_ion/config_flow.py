"""Config flow for the Smart iON CS-8 custom integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PORT
from modbus_connection import ModbusError, ModbusSerialParams, ModbusTcpParams
from modbus_connection.pymodbus import PymodbusConnection

from .const import (
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_DELAY,
    CONF_DEVICE,
    CONF_FRAMER,
    CONF_PARITY,
    CONF_STOPBITS,
    CONF_TIMEOUT,
    CONF_TRANSPORT,
    CONF_UNIT_ID,
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_DELAY,
    DEFAULT_FRAMER,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TCP_PORT,
    DEFAULT_TIMEOUT,
    DEFAULT_UNIT_ID,
    DOMAIN,
    TRANSPORT_SERIAL,
    TRANSPORT_TCP,
)

STEP_TCP = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_TCP_PORT): int,
        vol.Required(CONF_FRAMER, default=DEFAULT_FRAMER): vol.In(["rtu", "socket"]),
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): vol.All(
            int, vol.Range(min=1, max=247)
        ),
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
        vol.Optional(CONF_DELAY, default=DEFAULT_DELAY): int,
    }
)

STEP_SERIAL = vol.Schema(
    {
        vol.Required(CONF_DEVICE): str,
        vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): int,
        vol.Required(CONF_BYTESIZE, default=DEFAULT_BYTESIZE): vol.In([7, 8]),
        vol.Required(CONF_PARITY, default=DEFAULT_PARITY): vol.In(["N", "E", "O"]),
        vol.Required(CONF_STOPBITS, default=DEFAULT_STOPBITS): vol.In([1, 2]),
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): vol.All(
            int, vol.Range(min=1, max=247)
        ),
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
        vol.Optional(CONF_DELAY, default=DEFAULT_DELAY): int,
    }
)


def _build_connection(transport: str, data: dict[str, Any]) -> PymodbusConnection:
    """Build a throwaway connection to probe a candidate board."""
    if transport == TRANSPORT_SERIAL:
        params: ModbusSerialParams | ModbusTcpParams = ModbusSerialParams(
            device=data[CONF_DEVICE],
            baudrate=data[CONF_BAUDRATE],
            bytesize=data[CONF_BYTESIZE],
            parity=data[CONF_PARITY],
            stopbits=data[CONF_STOPBITS],
        )
    else:
        params = ModbusTcpParams(
            host=data[CONF_HOST], port=data[CONF_PORT], framer=data[CONF_FRAMER]
        )
    return PymodbusConnection(
        params, timeout=data[CONF_TIMEOUT], connect_delay=data[CONF_DELAY]
    )


class SmartIonConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for a Smart iON CS-8 board."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Let the user choose how the board is reached."""
        return self.async_show_menu(step_id="user", menu_options=["tcp", "serial"])

    async def _async_step_transport(
        self,
        transport: str,
        schema: vol.Schema,
        user_input: dict[str, Any] | None,
    ) -> ConfigFlowResult:
        """Validate and create an entry for a given transport."""
        errors: dict[str, str] = {}
        if user_input is not None:
            unit_id = int(user_input[CONF_UNIT_ID])
            endpoint = user_input.get(CONF_HOST) or user_input.get(CONF_DEVICE)
            await self.async_set_unique_id(f"{transport}_{endpoint}_{unit_id}")
            self._abort_if_unique_id_configured()

            connection = _build_connection(transport, user_input)
            try:
                await connection.for_unit(unit_id).read_coils(0, 1)
            except (ModbusError, OSError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Smart iON CS-8 ({unit_id})",
                    data={**user_input, CONF_TRANSPORT: transport},
                )
            finally:
                await connection.close()
        return self.async_show_form(
            step_id=transport, data_schema=schema, errors=errors
        )

    async def async_step_tcp(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure a board reached over TCP / RTU-over-TCP."""
        return await self._async_step_transport(TRANSPORT_TCP, STEP_TCP, user_input)

    async def async_step_serial(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure a board reached over a serial/USB port."""
        return await self._async_step_transport(
            TRANSPORT_SERIAL, STEP_SERIAL, user_input
        )
