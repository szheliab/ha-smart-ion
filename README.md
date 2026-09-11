# ha-smart-ion

[![hacs][hacs-shield]][hacs]

Home Assistant Modbus support for **Smart iON CS-8** 8-channel relay/contactor
boards, built on the [new Modbus Connection framework](https://developers.home-assistant.io/docs/modbus/introduction).

Each Smart iON CS-8 board exposes:

- 8 switched relay coils (`0x000`-`0x007`),
- 8 discrete inputs (`0x000`-`0x007` via function `0x02`),
- input-register diagnostics (module name, serial, firmware, uptime, request/error counters),
- holding-register settings (`0x0100`-`0x0104`).

This repository has three independent deliverables:

## Project structure

```
ha-smart-ion/
├── custom_components/smart_ion/  # HACS-installable custom integration (installable today)
├── device-library/                # standalone smart-ion-modbus Python package
│   ├── src/smart_ion/              # device/component model (relays, inputs, diagnostics, settings, timers)
│   ├── tests/                      # pytest suite
│   └── script/                     # format/check/query helper scripts
├── homeassistant-core/            # home-assistant/core contribution candidate
│   └── homeassistant/components/smart_ion/
├── config/                        # devcontainer HA config for local testing of custom_components/
├── scripts/                       # setup/develop/lint scripts (integration_blueprint-style)
├── hacs.json                      # HACS manifest (repo root, required for HACS install)
└── README.md                      # this file
```

## [`custom_components/smart_ion/`](custom_components/smart_ion) — HACS custom integration

A HACS-installable custom integration, based on the
[`ludeeus/integration_blueprint`](https://github.com/ludeeus/integration_blueprint)
template. It lives at the repository root (as required for a standard HACS
install) and vendorizes the device model and owns its Modbus connection
directly, so it can be installed and tested today without depending on any
unreleased Home Assistant core changes.

### Install via HACS

1. Click **Open HACS repository**, or add
   `https://github.com/szheliab/ha-smart-ion` manually in HACS as a custom
   repository (category: Integration), then install "Smart iON CS-8" and
   restart Home Assistant.
   
   [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=szheliab&repository=ha-smart-ion&category=Integration)
2. Click **Add integration**, or go to **Settings → Devices & Services
   → Add Integration** and search for "Smart iON CS-8", to start the config
   flow.
   
   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=smart_ion)

### Manual install

Copy `custom_components/smart_ion` into your Home Assistant
`config/custom_components` directory and restart Home Assistant.

### Features

- Config flow supporting both TCP / RTU-over-TCP gateways (e.g. Waveshare
  RS485-to-Ethernet adapters) and direct serial (RS-485/USB) connections, plus
  a reconfigure flow to change connection/timeout settings after setup.
- 8 `switch` entities per board — one per relay coil.
- 8 `binary_sensor` entities per board — one per discrete input.
- diagnostic/runtime/settings `sensor` entities for module identity, firmware,
  uptime, request/error counters, and settings registers (`0x0100`-`0x0104`).
- 2 writable `number` entities for debounce duration and long-press threshold.
- One config entry per physical CS-8 board, so multiple boards behind the
  same gateway (different Modbus unit addresses) are each configured
  independently.

### Configuration

All configuration is done through the UI. Pick a transport:

- **TCP / RTU-over-TCP** — host, port (default `502`), framer (`rtu` for
  RTU-over-TCP gateways, `socket` for native Modbus TCP), unit address
  (default `7`), timeout, and connect delay.
- **Serial** — device path, baud rate, data bits, parity, stop bits, unit
  address, timeout, and connect delay.

### Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the devcontainer-based development
workflow (based on [`ludeeus/integration_blueprint`](https://github.com/ludeeus/integration_blueprint)).

## [`device-library/`](device-library)

A standalone Python device-modeling library (`smart-ion-modbus`), built on
[`modbus-connection`](https://pypi.org/project/modbus-connection/) and modeled
after [`Tom-Bom-badil/trovis-modbus`](https://github.com/Tom-Bom-badil/trovis-modbus).
It has no Home Assistant dependency and can be used standalone (including a
`smart-ion-query` CLI) or as a dependency of the two integrations above/below.

## [`homeassistant-core/`](homeassistant-core)

A `smart_ion` integration in the shape expected for contribution to
[`home-assistant/core`](https://github.com/home-assistant/core), following the
[`trovis557x`](https://github.com/home-assistant/core/tree/trovis557x-integration/homeassistant/components/trovis557x)
pattern. It depends on the device library as a PyPI package and borrows a
shared Modbus unit from a `modbus_connection` config entry.

## Supported device map

- 8 relay coils at `0x000`-`0x007`
- 8 discrete inputs at `0x000`-`0x007`
- input-register diagnostics: `0x00BB`, `0x00C0`, `0x00CC`, `0x0205`, `0x020A`,
  `0x020C`, `0x020E`, `0x0210`
- holding-register settings: `0x0100`-`0x0104`, `0x0421`-`0x0428`, `0x0431`-`0x0438`

This matches the reference Modbus RTU-over-TCP setup of 3 physical Smart iON
CS-8 boards (Modbus unit addresses 2, 3, and 7) behind a single Waveshare
RTU-over-TCP gateway.
