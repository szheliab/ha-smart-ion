# Smart iON CS-8 — Home Assistant custom integration

[![hacs][hacs-shield]][hacs]

A HACS-installable custom integration for **Smart iON CS-8** 8-channel Modbus
relay/contactor boards, ready to test today without waiting on any unreleased
Home Assistant core changes.

Unlike [`../homeassistant-core`](../homeassistant-core), this integration
vendorizes the [`smart-ion-modbus`](../device-library) device model
(`custom_components/smart_ion/device.py`) and owns its Modbus connection
directly via the [`modbus-connection`](https://pypi.org/project/modbus-connection/)
library — it does not depend on Home Assistant's shared `modbus_connection`
integration.

## Features

- Config flow supporting both TCP / RTU-over-TCP gateways (e.g. Waveshare
  RS485-to-Ethernet adapters) and direct serial (RS-485/USB) connections.
- 8 `switch` entities per board — one per relay coil.
- 8 `binary_sensor` entities per board — one per discrete input.
- diagnostic/runtime/settings `sensor` entities for module identity, firmware,
  uptime, request/error counters, and settings registers (`0x0100`-`0x0104`).
- 2 writable `number` entities for debounce duration and long-press threshold.
- One config entry per physical CS-8 board, so multiple boards behind the
  same gateway (different Modbus unit addresses) are each configured
  independently.

## Installation

### HACS (recommended)

1. Add this repository as a custom repository in HACS (category:
   integration), or open it directly if listed.
2. Install "Smart iON CS-8".
3. Restart Home Assistant.
4. Go to **Settings → Devices & Services → Add Integration** and search for
   "Smart iON CS-8".

### Manual

Copy `custom_components/smart_ion` into your Home Assistant `config/custom_components`
directory and restart Home Assistant.

## Configuration

All configuration is done through the UI. Pick a transport:

- **TCP / RTU-over-TCP** — host, port (default `502`), framer (`rtu` for
  RTU-over-TCP gateways, `socket` for native Modbus TCP), unit address
  (default `7`), timeout, and connect delay.
- **Serial** — device path, baud rate, data bits, parity, stop bits, unit
  address, timeout, and connect delay.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the devcontainer-based development
workflow (based on [`ludeeus/integration_blueprint`](https://github.com/ludeeus/integration_blueprint)).

[hacs-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://github.com/hacs/integration
