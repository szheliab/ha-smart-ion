# ha-smart-ion

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=szheliab&repository=ha-smart-ion&category=Integration)
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=smart_ion)

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
├── device-library/          # standalone smart-ion-modbus Python package
│   ├── src/smart_ion/        # device/component model (relays, inputs, diagnostics, settings, timers)
│   ├── tests/                # pytest suite
│   └── script/                # format/check/query helper scripts
├── homeassistant-core/       # home-assistant/core contribution candidate
│   └── homeassistant/components/smart_ion/
├── custom-integration/       # HACS-installable custom integration
│   ├── custom_components/smart_ion/   # config flow, coordinator, platforms (vendorized device model)
│   ├── config/                          # devcontainer HA config for local testing
│   └── scripts/                         # setup/develop/lint scripts (integration_blueprint-style)
└── README.md                 # this file
```

## [`device-library/`](device-library)

A standalone Python device-modeling library (`smart-ion-modbus`), built on
[`modbus-connection`](https://pypi.org/project/modbus-connection/) and modeled
after [`Tom-Bom-badil/trovis-modbus`](https://github.com/Tom-Bom-badil/trovis-modbus).
It has no Home Assistant dependency and can be used standalone (including a
`smart-ion-query` CLI) or as a dependency of the two integrations below.

## [`homeassistant-core/`](homeassistant-core)

A `smart_ion` integration in the shape expected for contribution to
[`home-assistant/core`](https://github.com/home-assistant/core), following the
[`trovis557x`](https://github.com/home-assistant/core/tree/trovis557x-integration/homeassistant/components/trovis557x)
pattern. It depends on the device library as a PyPI package and borrows a
shared Modbus unit from a `modbus_connection` config entry.

## [`custom-integration/`](custom-integration)

A HACS-installable custom integration, based on the
[`ludeeus/integration_blueprint`](https://github.com/ludeeus/integration_blueprint)
template. It vendorizes the device model and owns its Modbus connection
directly, so it can be installed and tested today without depending on any
unreleased Home Assistant core changes.

### Quick install (HACS)

1. Click **Add HACS repository** above, or add
   `https://github.com/szheliab/ha-smart-ion` manually in HACS as a custom
   repository (category: Integration), then install "Smart iON CS-8" and
   restart Home Assistant.
2. Click **Add integration** above, or go to **Settings → Devices & Services
   → Add Integration** and search for "Smart iON CS-8", to start the config
   flow.

See [`custom-integration/README.md`](custom-integration/README.md) for full
installation and configuration details.

## Supported device map

- 8 relay coils at `0x000`-`0x007`
- 8 discrete inputs at `0x000`-`0x007`
- input-register diagnostics: `0x00BB`, `0x00C0`, `0x00CC`, `0x0205`, `0x020A`,
  `0x020C`, `0x020E`, `0x0210`
- holding-register settings: `0x0100`-`0x0104`, `0x0421`-`0x0428`, `0x0431`-`0x0438`

This matches the reference Modbus RTU-over-TCP setup of 3 physical Smart iON
CS-8 boards (Modbus unit addresses 2, 3, and 7) behind a single Waveshare
RTU-over-TCP gateway.
