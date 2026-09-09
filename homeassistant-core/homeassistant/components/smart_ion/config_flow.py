"""Config flow for Smart iON CS-8."""

from typing import Any

import voluptuous as vol
from homeassistant.components.modbus_connection import (
    ConnectionNotReady,
    async_get_unit,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import (
    ConfigEntrySelector,
    ConfigEntrySelectorConfig,
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
)
from modbus_connection import ModbusError

from .const import CONF_CONNECTION, CONF_UNIT_ID, DEFAULT_UNIT_ID, DOMAIN

STEP_USER = vol.Schema(
    {
        vol.Required(CONF_CONNECTION): ConfigEntrySelector(
            ConfigEntrySelectorConfig(integration="modbus_connection"),
        ),
        vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): NumberSelector(
            NumberSelectorConfig(min=1, max=247, step=1, mode=NumberSelectorMode.BOX),
        ),
    },
)


class SmartIonConfigFlow(ConfigFlow, domain=DOMAIN):
    """Configure a CS-8 through a shared Modbus Connection."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Let the user pick a Modbus Connection entry and unit address."""
        errors: dict[str, str] = {}
        if user_input is not None:
            unit_id = int(user_input[CONF_UNIT_ID])
            await self.async_set_unique_id(f"{user_input[CONF_CONNECTION]}_{unit_id}")
            self._abort_if_unique_id_configured()
            try:
                unit = async_get_unit(self.hass, user_input[CONF_CONNECTION], unit_id)
                await unit.read_coils(0, 1)
            except (ConnectionNotReady, ModbusError, OSError, ValueError):
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Smart iON CS-8 ({unit_id})",
                    data=user_input,
                )
        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER,
            errors=errors,
        )
