from __future__ import annotations

import json
import sys
from pathlib import Path

from .registry import DEFAULT_REGISTRY_PATH, load_default_library


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    path = Path(args[0]) if args else DEFAULT_REGISTRY_PATH
    library = load_default_library(path)
    print(json.dumps(library.as_summary(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
