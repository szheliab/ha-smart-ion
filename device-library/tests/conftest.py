"""Shared fixtures for the smart-ion-modbus test suite.

``mock_modbus_connection`` / ``mock_modbus_unit`` come from the
``modbus_connection`` library's pytest plugin (registered as a ``pytest11``
entry point once the package is installed) and provide an in-memory,
backend-free ``ModbusUnit`` seeded with whatever register/coil values a test
needs.
"""
