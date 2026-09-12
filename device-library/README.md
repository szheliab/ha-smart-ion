# `smart-ion-modbus` Python library

[![CI](https://github.com/szheliab/ha-smart-ion/actions/workflows/ci.yml/badge.svg?branch=develop&event=push)](https://github.com/szheliab/ha-smart-ion/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/smart-ion-modbus.svg)](https://pypi.org/project/smart-ion-modbus/)
[![Python](https://img.shields.io/pypi/pyversions/smart-ion-modbus.svg)](https://pypi.org/project/smart-ion-modbus/)
[![License](https://img.shields.io/github/license/szheliab/ha-smart-ion.svg)](LICENSE)

`smart-ion-modbus` is an asynchronous, transport-independent Python library for
communicating with **Smart iON CS-8** 8-channel relay/contactor boards over
Modbus.

The library is kept independent of any home automation platform, so it can be
used by any Python application or project that needs to read or drive one or
more Smart iON CS-8 boards.

## Purpose and scope

`smart-ion-modbus` models exactly what a Smart iON CS-8 board exposes over
Modbus:

* the eight switched relay outputs (coils `0x000`-`0x007`), read and written
  with function codes 0x01/0x05,
* the eight discrete inputs (`0x000`-`0x007`) via function code 0x02,
* input-register diagnostics (`0x00BB`, `0x00C0`, `0x00CC`, `0x0205`, `0x020A`,
  `0x020C`, `0x020E`, `0x0210`) via function code 0x04,
* holding-register settings (`0x0100`-`0x0104`) and packed timer registers
  (`0x0421`-`0x0428`, `0x0431`-`0x0438`) via function code 0x03.

It does **not** create or own the Modbus transport. Applications using the
library provide a
[`modbus_connection.ModbusUnit`](https://home-assistant-libs.github.io/modbus-connection/)
and may use any backend supported by `modbus-connection` (pymodbus, tmodbus,
...). Several boards on the same RS-485 line or RTU-over-TCP gateway are
modelled as one `SmartIonCS8` instance per unit (station) address, sharing one
underlying connection.

An example script `script/query.py` shows how to build an application that
connects to a board over Modbus/TCP, Modbus RTU-over-TCP, or a direct serial
port, prints relay/input/settings state, and can toggle a relay.

## Supported boards

| Board             | Outputs | Inputs | Register map                                                                 |
| :---------------- | :-----: | :----: | :---------------------------------------------------------------------------- |
| Smart iON CS-8    |    8    |   8    | Coils `0x000`-`0x007`, DI `0x000`-`0x007`, input `0x00BB/0x00C0/0x00CC/0x0205-0x0211`, holding `0x0100`-`0x0104`, `0x0421`-`0x0428`, `0x0431`-`0x0438` |

## Data provided by the library

`smart-ion-modbus` provides, per board:

* the on/off state of each of the eight relay outputs,
* the on/off state of each of the eight discrete inputs,
* module identity/firmware and runtime counters from input registers,
* configuration values from holding registers (address, serial format and timing settings),
* raw packed timer values for AutoOff and delay behavior,
* validated writes to turn any relay output on or off.

## Installation

```bash
pip install smart-ion-modbus
# or, to also pull in a concrete Modbus backend for the CLI script:
pip install "smart-ion-modbus[cli]"
```

## Usage

```python
from modbus_connection import ModbusTcpParams
from modbus_connection.tmodbus import ModbusConnection

from smart_ion import SmartIonCS8

connection = ModbusConnection(ModbusTcpParams(host="192.168.0.171", port=4196, framer="rtu"))
board = SmartIonCS8(connection.for_unit(7))  # unit/station address 7

await board.async_update()
print(board.relay_state(1), board.input_state(1), board.settings.address)
await board.async_set_relay(1, True)
```

## Development

```bash
script/run_checks.sh   # install deps, lint, type-compile, test, build
script/format_code.sh   # format + auto-fix with ruff
```

Tests run against the in-memory mock backend shipped with `modbus-connection`;
no real board or server is required.

## Branching and releases

`develop` is the integration branch; `main` is release-only and only accepts
pull requests from the local `develop` branch. Releasing a GitHub Release
publishes the package to PyPI with the release tag as the version.

## License

Apache License 2.0, see [`LICENSE`](LICENSE).
