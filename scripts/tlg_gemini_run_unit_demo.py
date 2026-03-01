#!/usr/bin/env python3
"""Run one-unit Gemini demo pipeline end-to-end.

Flow:
1) prepare unit input (apply theme override)
2) generate skeleton blueprint (TLG-005 script)
3) Gemini semantic writer -> unit blueprint JSON
4) structural validation gate (TLG-006)
5) Gemini reviewer -> review report JSON
6) LLM review gate
7) emit modular preview JSON (in run directory)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPT_DIR = REPO_ROOT / "docs/tasks/prompts/gemini"
PATTERN_LIBRARY = REPO_ROOT / "docs/tasks/pattern_library/ko_survival_pattern_library_v1.json"
REPAIR_REGISTRY = REPO_ROOT / "docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def save_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write(text)


def read_text(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        return f.read()


def extract_json_with_required_keys(text: str, required_keys: set[str]) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    matches: list[dict[str, Any]] = []
    for i, ch in enumerate(text):
        if ch not in "{[":
            continue
        try:
            obj, _ = decoder.raw_decode(text[i:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and required_keys.issubset(set(obj.keys())):
            matches.append(obj)
    if not matches:
        raise ValueError(f"No JSON object found with required keys: {sorted(required_keys)}")
    # Prefer the largest matching object to avoid grabbing nested sub-objects.
    matches.sort(key=lambda d: len(json.dumps(d, ensure_ascii=False)))
    return matches[-1]


def run_cmd(cmd: list[str], cwd: Path, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def run_gemini(prompt_text: str, model: str, cwd: Path) -> str:
    cmd = [
        "gemini",
        "--approval-mode",
        "yolo",
        "--output-format",
        "text",
        "--model",
        model,
        "--prompt",
        "Follow all instructions in stdin. Output JSON only.",
    ]
    res = run_cmd(cmd, cwd=cwd, input_text=prompt_text)
    output = (res.stdout or "") + ("\n" + res.stderr if res.stderr else "")
    if res.returncode != 0:
        raise RuntimeError(f"Gemini call failed (code={res.returncode}):\n{output}")
    return output


def render_template(template_name: str, payload: dict[str, Any]) -> str:
    template = read_text(PROMPT_DIR / template_name)
    pretty = json.dumps(payload, ensure_ascii=False, indent=2)
    return template.replace("{{UNIT_INPUT_CONTEXT}}", pretty).replace("{{UNIT_BLUEPRINT_CONTEXT}}", pretty)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one-unit Gemini demo pipeline")
    parser.add_argument("--seed-input", default="staging/tlg005_input.a1_u01.json")
    parser.add_argument("--theme-zh-tw", required=True, help="Override unit_intent.theme_zh_tw")
    parser.add_argument("--scenario", default="", help="Optional override for unit_intent.scenario")
    parser.add_argument("--primary-outcome", default="", help="Optional override for unit_intent.primary_outcome")
    parser.add_argument("--model", default="gemini-2.5-pro")
    parser.add_argument("--outdir", default="", help="Optional output run directory")
    args = parser.parse_args()

    seed_path = (REPO_ROOT / args.seed_input).resolve()
    seed = load_json(seed_path)
    unit_id = str(seed.get("unit_id", "UNIT"))

    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.outdir).resolve() if args.outdir else (REPO_ROOT / f"staging/gemini_runs/{unit_id}_{ts}")
    run_dir.mkdir(parents=True, exist_ok=True)

    intent = seed.setdefault("unit_intent", {})
    intent["theme_zh_tw"] = args.theme_zh_tw
    if args.scenario:
        intent["scenario"] = args.scenario
    if args.primary_outcome:
        intent["primary_outcome"] = args.primary_outcome

    unit_input_path = run_dir / "01_unit_input.json"
    save_json(unit_input_path, seed)

    skeleton_path = run_dir / "02_skeleton_blueprint.json"
    gen = run_cmd(
        [
            "python",
            "scripts/tlg005_generate_unit_v1.py",
            "--input",
            str(unit_input_path),
            "--pattern-library",
            str(PATTERN_LIBRARY),
            "--output",
            str(skeleton_path),
        ],
        cwd=REPO_ROOT,
    )
    save_text(run_dir / "02_generate.log", (gen.stdout or "") + (gen.stderr or ""))
    if gen.returncode != 0:
        print((gen.stdout or "") + (gen.stderr or ""))
        return 1

    skeleton = load_json(skeleton_path)

    semantic_prompt = render_template("semantic_writer_prompt.md", skeleton)
    save_text(run_dir / "03_semantic_writer.prompt.md", semantic_prompt)
    semantic_raw = run_gemini(semantic_prompt, args.model, REPO_ROOT)
    save_text(run_dir / "04_semantic_writer.raw.txt", semantic_raw)
    semantic_blueprint = extract_json_with_required_keys(semantic_raw, {"version", "unit", "sequence"})
    semantic_blueprint_raw_path = run_dir / "05_blueprint_llm.raw.json"
    save_json(semantic_blueprint_raw_path, semantic_blueprint)

    semantic_blueprint_path = run_dir / "05_blueprint_llm.json"
    norm = run_cmd(
        [
            "python",
            "scripts/tlg005_normalize_blueprint_v1.py",
            "--input",
            str(semantic_blueprint_raw_path),
            "--output",
            str(semantic_blueprint_path),
        ],
        cwd=REPO_ROOT,
    )
    save_text(run_dir / "05_normalize.log", (norm.stdout or "") + (norm.stderr or ""))
    if norm.returncode != 0:
        print((norm.stdout or "") + (norm.stderr or ""))
        return 1

    gate_struct = run_cmd(
        [
            "python",
            "scripts/tlg006_validate_unit_v1.py",
            "--blueprint",
            str(semantic_blueprint_path),
            "--repair-registry",
            str(REPAIR_REGISTRY),
        ],
        cwd=REPO_ROOT,
    )
    save_text(run_dir / "06_structural_gate.log", (gate_struct.stdout or "") + (gate_struct.stderr or ""))

    reviewer_prompt = render_template("reviewer_prompt.md", semantic_blueprint)
    save_text(run_dir / "07_reviewer.prompt.md", reviewer_prompt)
    reviewer_raw = run_gemini(reviewer_prompt, args.model, REPO_ROOT)
    save_text(run_dir / "08_reviewer.raw.txt", reviewer_raw)
    review_report = extract_json_with_required_keys(
        reviewer_raw,
        {"version", "unit_id", "overall_decision", "scores", "blocking_findings", "node_reviews", "summary_zh_tw"},
    )
    review_report_path = run_dir / "09_llm_review_report.json"
    save_json(review_report_path, review_report)

    gate_llm = run_cmd(
        [
            "python",
            "scripts/tlg006_llm_review_gate.py",
            "--blueprint",
            str(semantic_blueprint_path),
            "--report",
            str(review_report_path),
        ],
        cwd=REPO_ROOT,
    )
    save_text(run_dir / "10_llm_gate.log", (gate_llm.stdout or "") + (gate_llm.stderr or ""))

    preview_path = run_dir / "11_modular_preview.json"
    if gate_struct.returncode == 0 and gate_llm.returncode == 0:
        adapt = run_cmd(
            [
                "python",
                "scripts/tlg005_adapt_for_modular_viewer.py",
                "--input",
                str(semantic_blueprint_path),
                "--output",
                str(preview_path),
                "--title-zh-tw",
                f"{unit_id} Gemini Demo Preview",
                "--theme-zh-tw",
                args.theme_zh_tw,
            ],
            cwd=REPO_ROOT,
        )
        save_text(run_dir / "11_adapter.log", (adapt.stdout or "") + (adapt.stderr or ""))
    else:
        save_text(run_dir / "11_adapter.log", "Skipped adapter due to gate failure.\n")

    summary = {
        "run_dir": str(run_dir),
        "unit_id": unit_id,
        "model": args.model,
        "structural_gate_pass": gate_struct.returncode == 0,
        "llm_gate_pass": gate_llm.returncode == 0,
        "semantic_blueprint": str(semantic_blueprint_path),
        "semantic_blueprint_raw": str(semantic_blueprint_raw_path),
        "review_report": str(review_report_path),
        "preview_path": str(preview_path) if preview_path.exists() else "",
    }
    save_json(run_dir / "run_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
