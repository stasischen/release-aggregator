#!/usr/bin/env python3
"""Watch content-ko knowledge files and regenerate the modular library manifest.

This is a lightweight polling watcher with no extra dependencies.
Run it alongside the modular viewer during content editing so newly added
knowledge items are automatically reflected in docs/tasks/mockups/modular/data.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
CONTENT_KO_ROOT = REPO_ROOT.parent / "content-ko"
GENERATOR = SCRIPT_DIR / "generate_library_manifest.py"

WATCH_DIRS = [
    CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "knowledge",
    CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "knowledge",
    CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "example_sentence",
    CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "example_sentence",
]


def snapshot() -> str:
    h = hashlib.sha256()
    for base in WATCH_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.json")):
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            h.update(str(path.relative_to(CONTENT_KO_ROOT)).encode("utf-8"))
            h.update(str(stat.st_mtime_ns).encode("utf-8"))
            h.update(str(stat.st_size).encode("utf-8"))
    return h.hexdigest()


def run_generator() -> None:
    print("[watch] regenerating modular library manifest...")
    subprocess.run([sys.executable, str(GENERATOR)], check=True)


def main(interval: float = 2.0) -> int:
    last = None
    print("[watch] starting library manifest watcher")
    print("[watch] content root:", CONTENT_KO_ROOT)
    try:
        run_generator()
        last = snapshot()
        while True:
            time.sleep(interval)
            current = snapshot()
            if current != last:
                last = current
                run_generator()
    except KeyboardInterrupt:
        print("\n[watch] stopped")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
