# Smart iON CS-8 — Home Assistant core integration

This folder contains the `smart_ion` integration in the shape expected for a
contribution to [`home-assistant/core`](https://github.com/home-assistant/core),
following the pattern used by the
[`trovis557x`](https://github.com/home-assistant/core/tree/trovis557x-integration/homeassistant/components/trovis557x)
integration.

It does not own its Modbus connection. It borrows a shared `ModbusUnit` from a
`modbus_connection` config entry (selected in this integration's config flow)
and hands it to the [`smart-ion-modbus`](../device-library) device library.
The `modbus_connection` entry owns the connection lifecycle; this integration
reloads when the connection drops so it re-borrows a unit on the rebuilt
connection.

## Layout

To land this in `home-assistant/core`, copy:

- `homeassistant/components/smart_ion/` into the core checkout's
  `homeassistant/components/smart_ion/`.
- `tests/components/smart_ion/` into the core checkout's
  `tests/components/smart_ion/`.

Then add `smart-ion-modbus` to core's `requirements_all.txt` /
`requirements_test_all.txt` via `python3 -m script.gen_requirements_all`, and
register the domain brand assets per
[Creating a new integration](https://developers.home-assistant.io/docs/creating_integration_file_structure).

## Entities

- 8 `switch` entities — one per relay coil (`relay_1`-`relay_8`).
- 8 `binary_sensor` entities — one per discrete input (`di_1`-`di_8`).
- diagnostic/runtime/settings `sensor` entities for:
  - module name, serial number, firmware version,
  - uptime and request/error counters,
  - module address, baud-rate code, data-format code, debounce and long-press settings.
- 2 `number` entities — writable debounce duration and long-press threshold.

## Config flow

Pick an existing `modbus_connection` entry and the board's Modbus unit
(station) address; the flow probes the unit with a coil read before creating
the entry.
