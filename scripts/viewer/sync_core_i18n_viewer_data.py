#!/usr/bin/env python3
"""Sync frontend intake package files into core_i18n_viewer/data.

Example:
  python3 scripts/viewer/sync_core_i18n_viewer_data.py --run-id 20260220_demo
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

REQUIRED = {
    "course.package.json": "course/course.package.json",
    "dictionary_core.json": "core/dictionary_core.json",
    "dict_ko_zh_tw.json": "i18n/dict_ko_zh_tw.json",
    "mapping.json": "i18n/mapping.json",
}


def latest_run_id(frontend_root: Path) -> str:
    runs = sorted((p for p in frontend_root.iterdir() if p.is_dir()), key=lambda p: p.name)
    if not runs:
        raise SystemExit(f"No run directories under: {frontend_root}")
    return runs[-1].name


def validate_json(path: Path) -> None:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"Invalid JSON: {path}\n{exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frontend-root", default="staging/frontend_intake")
    parser.add_argument("--run-id", default="latest")
    parser.add_argument("--lang", default="ko")
    parser.add_argument("--viewer-data-dir", default="tools/core_i18n_viewer/data")
    args = parser.parse_args()

    frontend_root = Path(args.frontend_root)
    run_id = latest_run_id(frontend_root) if args.run_id == "latest" else args.run_id
    package_root = frontend_root / run_id / "packages" / args.lang
    viewer_data_dir = Path(args.viewer_data_dir)

    if not package_root.exists():
        raise SystemExit(f"Package root not found: {package_root}")

    viewer_data_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for out_name, rel_src in REQUIRED.items():
        src = package_root / rel_src
        if not src.exists():
            raise SystemExit(f"Missing required source file: {src}")
        validate_json(src)
        dst = viewer_data_dir / out_name
        shutil.copy2(src, dst)
        copied.append((src, dst))

    print(f"Synced run_id={run_id} lang={args.lang}")
    for src, dst in copied:
        print(f"- {src} -> {dst}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
