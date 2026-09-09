from pathlib import Path

from device_library.src.smart_ion.models import load_device_profile


def test_load_device_profile() -> None:
    root = Path(__file__).resolve().parents[2]
    profile = load_device_profile(root / "docs" / "smart-ion-registers.yaml")
    assert profile.device_name == "Smart iOn CS-8"
    assert profile.connection.host == "192.168.0.96"
    assert profile.connection.is_tcp is True
    assert len(profile.switches) == 8
    assert len(profile.sensors) == 1
    assert profile.switches[0].address_hex == "0x000"
    assert profile.sensors[0].entity_key == "smart_ion_1_address"
    assert profile.entities_by_domain("switch") == profile.switches
