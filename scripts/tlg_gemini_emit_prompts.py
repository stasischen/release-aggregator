#!/usr/bin/env python3
"""Render Gemini prompt pack for one unit from local JSON artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(text)


def render(template: str, payload: dict) -> str:
    pretty = json.dumps(payload, ensure_ascii=False, indent=2)
    return template.replace("{{UNIT_INPUT_CONTEXT}}", pretty).replace("{{UNIT_BLUEPRINT_CONTEXT}}", pretty)


def main() -> int:
    parser = argparse.ArgumentParser(description="Emit Gemini planner/writer/reviewer prompts")
    parser.add_argument("--unit-input", required=True, help="Path to tlg005 unit input JSON")
    parser.add_argument("--blueprint", required=True, help="Path to unit_blueprint_v1 JSON")
    parser.add_argument("--outdir", required=True, help="Output directory for rendered prompts")
    args = parser.parse_args()

    unit_input = load_json(Path(args.unit_input))
    blueprint = load_json(Path(args.blueprint))
    outdir = Path(args.outdir)

    base = Path("docs/tasks/prompts/gemini")
    planner_t = load_text(base / "planner_prompt.md")
    writer_t = load_text(base / "semantic_writer_prompt.md")
    reviewer_t = load_text(base / "reviewer_prompt.md")

    save_text(outdir / "01_planner.prompt.md", render(planner_t, unit_input))
    save_text(outdir / "02_semantic_writer.prompt.md", render(writer_t, blueprint))
    save_text(outdir / "03_reviewer.prompt.md", render(reviewer_t, blueprint))

    print(f"Wrote prompt pack: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
