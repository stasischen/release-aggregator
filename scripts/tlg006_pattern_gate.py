#!/usr/bin/env python3
"""TLG-006 gate for target language pattern library.

Current scope:
- Reuse TLG-004 contract validation from pattern_library_codec
- Enforce repair link resolvability via repair strategy registry (blocker)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from pattern_library_codec import load_json, load_repair_registry_ids, validate_library


def main() -> int:
    parser = argparse.ArgumentParser(description="TLG-006 gate: validate pattern library against repair registry")
    parser.add_argument("--library", required=True, help="Pattern library JSON path")
    parser.add_argument("--repair-registry", required=True, help="Repair strategy registry JSON path")
    args = parser.parse_args()

    library_path = Path(args.library)
    repair_registry_path = Path(args.repair_registry)

    data = load_json(library_path)
    repair_registry_ids = load_repair_registry_ids(repair_registry_path)
    errors, warnings = validate_library(data, repair_registry_ids=repair_registry_ids)

    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)

    if errors:
        print(f"TLG-006 RESULT: FAIL (errors={len(errors)}, warnings={len(warnings)})")
        return 1

    print(f"TLG-006 RESULT: PASS (warnings={len(warnings)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
