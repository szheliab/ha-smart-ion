"""Vendorized typed register model for Smart iON CS-8."""

from modbus_connection import ModbusUnit
from modbus_connection.model import Component, ComponentGroup, bit, coil, integer


class RelayOutputs(Component):
    coil_ranges = ((0, 7),)
    relay_1 = coil(0, writable=True)
    relay_2 = coil(1, writable=True)
    relay_3 = coil(2, writable=True)
    relay_4 = coil(3, writable=True)
    relay_5 = coil(4, writable=True)
    relay_6 = coil(5, writable=True)
    relay_7 = coil(6, writable=True)
    relay_8 = coil(7, writable=True)


class InputStatus(Component):
    register_space = "input"
    register_ranges = ((4096, 4099),)
    input_1 = bit(4096, 0)
    input_2 = bit(4096, 1)
    input_3 = bit(4096, 2)
    input_4 = bit(4096, 3)
    input_5 = bit(4096, 4)
    input_6 = bit(4096, 5)
    input_7 = bit(4096, 6)
    input_8 = bit(4096, 7)
    input_status_1 = bit(4097, 0)
    input_status_2 = bit(4097, 1)
    input_status_3 = bit(4097, 2)
    input_status_4 = bit(4097, 3)
    input_status_5 = bit(4097, 4)
    input_status_6 = bit(4097, 5)
    input_status_7 = bit(4097, 6)
    input_status_8 = bit(4097, 7)
    auxiliary_input = bit(4098, 0)
    auxiliary_input_status = bit(4099, 0)


class ModuleSettings(Component):
    """Module-wide holding-register settings."""

    register_ranges = ((256, 260),)
    module_address = integer(256, signed=False)
    debounce_duration = integer(259, signed=False, writable=True)
    long_press_duration = integer(260, signed=False, writable=True)


class InputSettings(Component):
    """Digital-input configuration."""

    register_ranges = ((769, 770), (785, 792))
    debounce_enabled = integer(769, signed=False, writable=True)
    input_mode = integer(770, signed=False, writable=True)
    long_press_1 = integer(785, signed=False, writable=True)
    long_press_2 = integer(786, signed=False, writable=True)
    long_press_3 = integer(787, signed=False, writable=True)
    long_press_4 = integer(788, signed=False, writable=True)
    long_press_5 = integer(789, signed=False, writable=True)
    long_press_6 = integer(790, signed=False, writable=True)
    long_press_7 = integer(791, signed=False, writable=True)
    long_press_8 = integer(792, signed=False, writable=True)


class OutputSettings(Component):
    """Relay behavior and timing settings."""

    register_ranges = ((1025, 1028), (1057, 1064), (1073, 1080))
    restore_output_states = integer(1025, signed=False, writable=True)
    input_output_mapping = integer(1026, signed=False, writable=True)
    output_inversion = integer(1027, signed=False, writable=True)
    startup_output_states = integer(1028, signed=False, writable=True)
    max_on_time_1 = integer(1057, signed=False, writable=True)
    max_on_time_2 = integer(1058, signed=False, writable=True)
    max_on_time_3 = integer(1059, signed=False, writable=True)
    max_on_time_4 = integer(1060, signed=False, writable=True)
    max_on_time_5 = integer(1061, signed=False, writable=True)
    max_on_time_6 = integer(1062, signed=False, writable=True)
    max_on_time_7 = integer(1063, signed=False, writable=True)
    max_on_time_8 = integer(1064, signed=False, writable=True)
    off_delay_1 = integer(1073, signed=False, writable=True)
    off_delay_2 = integer(1074, signed=False, writable=True)
    off_delay_3 = integer(1075, signed=False, writable=True)
    off_delay_4 = integer(1076, signed=False, writable=True)
    off_delay_5 = integer(1077, signed=False, writable=True)
    off_delay_6 = integer(1078, signed=False, writable=True)
    off_delay_7 = integer(1079, signed=False, writable=True)
    off_delay_8 = integer(1080, signed=False, writable=True)


class AuxiliaryInputSettings(Component):
    """Auxiliary-input configuration."""

    register_ranges = ((1281, 1286),)
    debounce_enabled = integer(1281, signed=False, writable=True)
    input_mode = integer(1282, signed=False, writable=True)
    on_status_mapping = integer(1283, signed=False, writable=True)
    on_transition_mapping = integer(1284, signed=False, writable=True)
    off_status_mapping = integer(1285, signed=False, writable=True)
    off_transition_mapping = integer(1286, signed=False, writable=True)


class DeviceInformation(Component):
    """Read-only identification registers."""

    register_space = "input"
    register_ranges = ((187, 191),)
    serial_word_1 = integer(187, signed=False)
    serial_word_2 = integer(188, signed=False)
    serial_word_3 = integer(189, signed=False)
    serial_word_4 = integer(190, signed=False)
    serial_word_5 = integer(191, signed=False)


class SmartIonCS8:
    """Only the live, frequently-polled state needed by HA entities."""

    def __init__(self, unit: ModbusUnit) -> None:
        self.relay_outputs = RelayOutputs(unit)
        self.input_status = InputStatus(unit)
        self.module_settings = ModuleSettings(unit)
        self.input_settings = InputSettings(unit)
        self.output_settings = OutputSettings(unit)
        self.auxiliary_input_settings = AuxiliaryInputSettings(unit)
        self.info = DeviceInformation(unit)
        self._components = ComponentGroup(unit, (self.relay_outputs, self.input_status))
        self._settings = ComponentGroup(
            unit,
            (
                self.module_settings,
                self.input_settings,
                self.output_settings,
                self.auxiliary_input_settings,
                self.info,
            ),
        )

    async def async_update(self) -> None:
        await self._components.async_update()

    async def async_update_settings(self) -> None:
        """Update configuration and device-identification registers."""
        await self._settings.async_update()
