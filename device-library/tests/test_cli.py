import json

from smart_ion.cli import main


def test_cli_main(capsys) -> None:
    assert main([]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["device_name"] == "Smart iOn CS-8"
    assert len(output["switches"]) == 8
    assert len(output["sensors"]) == 1
