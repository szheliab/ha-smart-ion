import json
from pathlib import Path


def test_translation_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    for language in ("en", "uk"):
        data = json.loads((root / "translations" / f"{language}.json").read_text(encoding="utf-8"))
        assert data["config"]["step"]["user"]["title"] == "Smart iOn CS-8"

