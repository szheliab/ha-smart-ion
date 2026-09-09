"""Digital input entities."""

from dataclasses import dataclass

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import SmartIonConfigEntry, SmartIonCoordinator
from .entity import SmartIonEntity


@dataclass(frozen=True, kw_only=True)
class SmartIonBinaryDescription(BinarySensorEntityDescription):
    """Describe one packed input-register bit."""

    field: str


DESCRIPTIONS = (
    *tuple(SmartIonBinaryDescription(key=f"input_{index}", name=f"Input {index}", field=f"input_{index}") for index in range(1, 9)),
    *tuple(SmartIonBinaryDescription(key=f"input_status_{index}", name=f"Input {index} status", field=f"input_status_{index}", entity_category=EntityCategory.DIAGNOSTIC, entity_registry_enabled_default=False) for index in range(1, 9)),
    SmartIonBinaryDescription(key="auxiliary_input", name="Auxiliary input", field="auxiliary_input"),
    SmartIonBinaryDescription(key="auxiliary_input_status", name="Auxiliary input status", field="auxiliary_input_status", entity_category=EntityCategory.DIAGNOSTIC, entity_registry_enabled_default=False),
)


async def async_setup_entry(hass: HomeAssistant, entry: SmartIonConfigEntry, async_add_entities: AddConfigEntryEntitiesCallback) -> None:
    """Set up input entities."""
    async_add_entities(SmartIonBinarySensor(entry.runtime_data, description) for description in DESCRIPTIONS)


class SmartIonBinarySensor(SmartIonEntity, BinarySensorEntity):
    """One read-only input bit."""

    entity_description: SmartIonBinaryDescription

    def __init__(self, coordinator: SmartIonCoordinator, description: SmartIonBinaryDescription) -> None:
        super().__init__(coordinator, description.key)
        self.entity_description = description

    @property
    def is_on(self) -> bool | None:
        return getattr(self.coordinator.device.input_status, self.entity_description.field)
