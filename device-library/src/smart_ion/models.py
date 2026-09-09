from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class ModbusConnection:
    name: str
    type: str
    host: str | None = None
    port: int | None = None
    delay: int = 0
    timeout: int = 5

    @property
    def is_tcp(self) -> bool:
        return self.type == "rtuovertcp"


@dataclass(frozen=True, slots=True)
class RegisterEntity:
    name: str
    address: int
    unique_id: str
    slave: int
    domain: str
    input_type: str | None = None
    write_type: str | None = None
    scan_interval: int | None = None
    data_type: str | None = None

    @property
    def entity_key(self) -> str:
        return self.unique_id.replace("-", "_")

    @property
    def address_hex(self) -> str:
        return f"0x{self.address:03x}"


@dataclass(frozen=True, slots=True)
class DeviceProfile:
    connection: ModbusConnection
    switches: tuple[RegisterEntity, ...] = field(default_factory=tuple)
    sensors: tuple[RegisterEntity, ...] = field(default_factory=tuple)

    @property
    def device_name(self) -> str:
        return "Smart iOn CS-8"

    @property
    def all_entities(self) -> tuple[RegisterEntity, ...]:
        return (*self.switches, *self.sensors)

    @property
    def unique_ids(self) -> tuple[str, ...]:
        return tuple(entity.unique_id for entity in self.all_entities)

    def entities_by_domain(self, domain: str) -> tuple[RegisterEntity, ...]:
        return tuple(entity for entity in self.all_entities if entity.domain == domain)


class SmartIonRegistryError(ValueError):
    pass


class _YamlUnavailable:
    @staticmethod
    def safe_load(_: str) -> Any:
        raise SmartIonRegistryError("PyYAML is required to load the register file")


def _load_yaml_module() -> Any:
    try:
        import yaml  # type: ignore
    except ModuleNotFoundError:
        return _YamlUnavailable()
    return yaml


def _load_item(data: dict[str, Any], domain: str) -> RegisterEntity:
    return RegisterEntity(
        name=str(data["name"]),
        address=int(data["address"]),
        unique_id=str(data["unique_id"]),
        slave=int(data["slave"]),
        domain=domain,
        input_type=data.get("input_type"),
        write_type=data.get("write_type"),
        scan_interval=data.get("scan_interval"),
        data_type=data.get("data_type"),
    )


def _require_mapping(value: Any, message: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SmartIonRegistryError(message)
    return value


def load_device_profile(path: str | Path) -> DeviceProfile:
    yaml_module = _load_yaml_module()
    payload = yaml_module.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise SmartIonRegistryError("Expected a list with one connection profile")
    root = _require_mapping(payload[0], "Expected the first YAML item to be a mapping")
    connection = ModbusConnection(
        name=str(root["name"]),
        type=str(root["type"]),
        host=str(root.get("host") or "") or None,
        port=int(root.get("port") or 0) or None,
        delay=int(root.get("delay") or 0),
        timeout=int(root.get("timeout") or 5),
    )
    switches = tuple(_load_item(item, "switch") for item in root.get("switches", []))
    sensors = tuple(_load_item(item, "sensor") for item in root.get("sensors", []))
    unique_ids = [entity.unique_id for entity in (*switches, *sensors)]
    if len(unique_ids) != len(set(unique_ids)):
        raise SmartIonRegistryError("Duplicate unique_id detected")
    return DeviceProfile(connection=connection, switches=switches, sensors=sensors)
