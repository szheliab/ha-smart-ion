"""Diagnostic sensors for Smart iON CS-8."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import EntityCategory

from .entity import SmartIonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from .coordinator import SmartIonCoordinator
    from .data import SmartIonConfigEntry


@dataclass(frozen=True, kw_only=True)
class SmartIonSensorDescription(SensorEntityDescription):
    """Describe one Smart iON sensor value."""

    field: str
    source: str
    value_map: dict[int, int | str] | None = None


DESCRIPTIONS: tuple[SmartIonSensorDescription, ...] = (
    SmartIonSensorDescription(
        key="module_name",
        name="Module name",
        field="module_name",
        source="diagnostics",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="serial_number",
        name="Serial number",
        field="serial_number",
        source="diagnostics",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="firmware_version",
        name="Firmware version",
        field="firmware_version",
        source="diagnostics",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="uptime",
        name="Uptime",
        field="uptime",
        source="diagnostics",
        native_unit_of_measurement="s",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="request_count",
        name="Request count",
        field="request_count",
        source="diagnostics",
    ),
    SmartIonSensorDescription(
        key="no_response_count",
        name="No-response count",
        field="no_response_count",
        source="diagnostics",
    ),
    SmartIonSensorDescription(
        key="error_count",
        name="Error count",
        field="error_count",
        source="diagnostics",
    ),
    SmartIonSensorDescription(
        key="crc_error_count",
        name="CRC error count",
        field="crc_error_count",
        source="diagnostics",
    ),
    SmartIonSensorDescription(
        key="address",
        name="Module address",
        field="address",
        source="settings",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="baud_rate_code",
        name="Baud rate",
        field="baud_rate_code",
        source="settings",
        native_unit_of_measurement="baud",
        value_map={
            1: 2400,
            2: 4800,
            3: 9600,
            4: 14400,
            5: 19200,
            6: 28800,
            7: 38400,
            8: 57600,
            9: 115200,
        },
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="data_format_code",
        name="Data format",
        field="data_format_code",
        source="settings",
        value_map={
            1: "8N1",
            2: "8N2",
            3: "8E1",
            4: "8O1",
        },
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="debounce_duration_ms",
        name="Debounce duration",
        field="debounce_duration_ms",
        source="settings",
        native_unit_of_measurement="ms",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SmartIonSensorDescription(
        key="long_press_threshold_ms",
        name="Long press threshold",
        field="long_press_threshold_ms",
        source="settings",
        native_unit_of_measurement="ms",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    *(
        SmartIonSensorDescription(
            key=f"autooff_relay_{index}_raw",
            name=f"AutoOff Relay {index} Raw",
            field=f"autooff_relay_{index}_raw",
            source="autooff_timers",
            entity_category=EntityCategory.DIAGNOSTIC,
        )
        for index in range(1, 9)
    ),
    *(
        SmartIonSensorDescription(
            key=f"delay_relay_{index}_raw",
            name=f"Delay Relay {index} Raw",
            field=f"delay_relay_{index}_raw",
            source="delay_timers",
            entity_category=EntityCategory.DIAGNOSTIC,
        )
        for index in range(1, 9)
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: SmartIonConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up diagnostic sensor entities."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(
        SmartIonSensor(coordinator, description) for description in DESCRIPTIONS
    )


class SmartIonSensor(SmartIonEntity, SensorEntity):
    """A read-only Smart iON CS-8 configuration register."""

    entity_description: SmartIonSensorDescription

    def __init__(
        self, coordinator: SmartIonCoordinator, description: SmartIonSensorDescription
    ) -> None:
        """Initialize the diagnostic sensor entity."""
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def native_value(self) -> str | int | float | None:
        """Return the current register value."""
        source = getattr(self.coordinator.device, self.entity_description.source)
        value = getattr(source, self.entity_description.field)
        value_map = self.entity_description.value_map
        if value_map is not None and isinstance(value, int):
            return value_map.get(value, value)
        return value
