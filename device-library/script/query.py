#!/usr/bin/env python3

"""Query (and optionally toggle) a Smart iON CS-8 board over Modbus.

Connects over Modbus TCP/RTU-over-TCP (a network gateway) or a serial/USB
port, reads all eight relay states and the board's configured address, and
prints them to the terminal. Pass ``--set N on|off`` to also toggle one
relay. Handy for checking a real board without any home automation platform.

The library only needs the connection protocol; this script selects the
pymodbus backend, so install the ``cli`` extra first.
"""

from __future__ import annotations

import argparse
import asyncio
import sys

from modbus_connection import (
    ModbusConnection,
    ModbusError,
    ModbusSerialParams,
    ModbusTcpParams,
)

from smart_ion import RELAY_COUNT, SmartIonCS8


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="transport", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--unit",
        type=int,
        default=1,
        help="Modbus unit/station address (default: 1)",
    )
    common.add_argument(
        "--set",
        nargs=2,
        metavar=("RELAY", "STATE"),
        help="toggle one relay (1-8) 'on' or 'off' before printing state",
    )

    tcp = sub.add_parser(
        "tcp",
        parents=[common],
        help="connect over Modbus TCP (network gateway)",
    )
    tcp.add_argument("host", help="hostname or IP of the gateway/board")
    tcp.add_argument("--port", type=int, default=502, help="TCP port (default: 502)")
    tcp.add_argument(
        "--framer",
        choices=("rtu", "socket"),
        default="rtu",
        help=(
            "wire framing: 'rtu' for RTU-over-TCP (transparent serial "
            "gateways) or 'socket' for native Modbus TCP (default: rtu)"
        ),
    )

    serial = sub.add_parser(
        "serial",
        parents=[common],
        help="connect over a serial/USB port",
    )
    serial.add_argument("device", help="serial device, e.g. /dev/ttyUSB0")
    serial.add_argument("--baudrate", type=int, default=9600, help="default: 9600")
    serial.add_argument("--parity", choices=("N", "E", "O"), default="N")
    serial.add_argument("--stopbits", type=int, choices=(1, 2), default=1)
    serial.add_argument("--bytesize", type=int, choices=(7, 8), default=8)
    return parser.parse_args(argv)


def _connection(args: argparse.Namespace) -> ModbusConnection:
    """Build the connection described by the arguments. Performs no I/O."""
    from modbus_connection.pymodbus import PymodbusConnection

    if args.transport == "serial":
        return PymodbusConnection(
            ModbusSerialParams(
                device=args.device,
                baudrate=args.baudrate,
                parity=args.parity,
                stopbits=args.stopbits,
                bytesize=args.bytesize,
            )
        )
    return PymodbusConnection(
        ModbusTcpParams(host=args.host, port=args.port, framer=args.framer)
    )


def _print(board: SmartIonCS8) -> None:
    print(f"Address register: {board.settings.address}")
    for index in range(1, RELAY_COUNT + 1):
        state = board.relay_state(index)
        label = "unknown" if state is None else ("on" if state else "off")
        print(f"Relay {index}: {label}")


async def _run(args: argparse.Namespace) -> int:
    connection = _connection(args)
    try:
        await connection.connect()
    except ModbusError as err:
        print(f"Could not connect: {err}", file=sys.stderr)
        return 1

    board = SmartIonCS8(connection.for_unit(args.unit))
    try:
        if args.set:
            relay, state = args.set
            await board.async_set_relay(int(relay), state.strip().lower() == "on")
        await board.async_update()
    except ModbusError as err:
        print(f"Error reading board: {err}", file=sys.stderr)
        return 1
    finally:
        await connection.close()

    _print(board)
    return 0


def main() -> int:
    return asyncio.run(_run(_parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
