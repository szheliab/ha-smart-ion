from __future__ import annotations

from .const import (
    CONF_BAUDRATE,
    CONF_CONNECTION_TYPE,
    CONF_DELAY,
    CONF_HOST,
    CONF_PARITY,
    CONF_PORT,
    CONF_SERIAL_PORT,
    CONF_SLAVE,
    CONF_STOPBITS,
    CONF_TIMEOUT,
    CONNECTION_TYPE_SERIAL,
    CONNECTION_TYPE_TCP,
    DEFAULT_BAUDRATE,
    DEFAULT_DELAY,
    DEFAULT_NAME,
    DEFAULT_PARITY,
    DEFAULT_PORT,
    DEFAULT_SLAVE,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
)


class SmartIonConfigFlow:
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return {"type": "create_entry", "title": DEFAULT_NAME, "data": user_input}
        return {
            "type": "form",
            "step_id": "user",
            "data_schema": {
                CONF_CONNECTION_TYPE: [CONNECTION_TYPE_TCP, CONNECTION_TYPE_SERIAL],
                CONF_HOST: "string",
                CONF_PORT: DEFAULT_PORT,
                CONF_SERIAL_PORT: "/dev/ttyUSB0",
                CONF_BAUDRATE: DEFAULT_BAUDRATE,
                CONF_PARITY: DEFAULT_PARITY,
                CONF_STOPBITS: DEFAULT_STOPBITS,
                CONF_TIMEOUT: DEFAULT_TIMEOUT,
                CONF_DELAY: DEFAULT_DELAY,
                CONF_SLAVE: DEFAULT_SLAVE,
            },
        }
