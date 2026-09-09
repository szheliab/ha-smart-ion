import json
        assert data["config"]["step"]["user"]["title"] == "Smart iOn CS-8"
        data = json.loads((root / "translations" / f"{language}.json").read_text(encoding="utf-8"))
    for language in ("en", "uk"):
    root = Path(__file__).resolve().parents[1]
def test_translation_files_exist() -> None:


from pathlib import Path

