#!/usr/bin/env python3
from pathlib import Path


def main():
    repo_root = Path(__file__).resolve().parents[1]
    workflow_path = repo_root / ".agent" / "workflows" / "gsd.md"

    if not workflow_path.exists():
        raise SystemExit(f"GSD workflow not found: {workflow_path}")

    print(workflow_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
