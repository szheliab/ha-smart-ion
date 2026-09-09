from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from .models import DeviceProfile, RegisterEntity, load_device_profile

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_REGISTRY_PATH = ROOT / "docs" / "smart-ion-registers.yaml"


@dataclass(frozen=True, slots=True)
class SmartIonDeviceLibrary:
    profile: DeviceProfile

    @property
    def name(self) -> str:
        return self.profile.device_name

    @property
    def all_entities(self) -> tuple[RegisterEntity, ...]:
        return self.profile.all_entities

    @property
    def switch_entities(self) -> tuple[RegisterEntity, ...]:
        return self.profile.switches

    @property
    def sensor_entities(self) -> tuple[RegisterEntity, ...]:
        return self.profile.sensors

    def as_summary(self) -> dict[str, object]:
        return {
            "device_name": self.name,
            "connection": {
                "name": self.profile.connection.name,
                "type": self.profile.connection.type,
                "host": self.profile.connection.host,
                "port": self.profile.connection.port,
                "delay": self.profile.connection.delay,
                "timeout": self.profile.connection.timeout,
            },
            "switches": [
                {
                    "name": entity.name,
                    "address": entity.address_hex,
                    "unique_id": entity.unique_id,
                }
                for entity in self.switch_entities
            ],
            "sensors": [
                {
                    "name": entity.name,
                    "address": entity.address_hex,
                    "unique_id": entity.unique_id,
                }
                for entity in self.sensor_entities
            ],
        }


@lru_cache(maxsize=1)
def load_default_library(path: str | Path = DEFAULT_REGISTRY_PATH) -> SmartIonDeviceLibrary:
    return SmartIonDeviceLibrary(profile=load_device_profile(path))


def entity_lookup(path: str | Path = DEFAULT_REGISTRY_PATH) -> dict[str, RegisterEntity]:
    library = load_default_library(path)
    return {entity.unique_id: entity for entity in library.all_entities}
