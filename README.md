# ha-smart-ion

Home Assistant Modbus support for **Smart iON CS-8** 8-channel relay/contactor
boards, built on the [new Modbus Connection framework](https://developers.home-assistant.io/docs/modbus/introduction).

Each Smart iON CS-8 board exposes:

- 8 switched relay coils (`0x000`-`0x007`),
- 8 discrete inputs (`0x000`-`0x007` via function `0x02`),
- input-register diagnostics (module name, serial, firmware, uptime, request/error counters),
- holding-register settings (`0x0100`-`0x0104`).

This repository has three independent deliverables:

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

## Supported device map

- 8 relay coils at `0x000`-`0x007`
- 8 discrete inputs at `0x000`-`0x007`
- input-register diagnostics: `0x00BB`, `0x00C0`, `0x00CC`, `0x0205`, `0x020A`,
  `0x020C`, `0x020E`, `0x0210`
- holding-register settings: `0x0100`-`0x0104`

This matches the reference Modbus RTU-over-TCP setup of 3 physical Smart iON
CS-8 boards (Modbus unit addresses 2, 3, and 7) behind a single Waveshare
RTU-over-TCP gateway.
