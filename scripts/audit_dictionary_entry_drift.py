#!/usr/bin/env python3
"""Audit Korean dictionary rows for homonym/polysemy and origin drift.

This script is read-only. It inspects the content-ko dictionary inventory and
emits a markdown inventory for human review.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RELEASE_AGGREGATOR_ROOT = Path(__file__).resolve().parent.parent
LINGO_ROOT = RELEASE_AGGREGATOR_ROOT.parent
DEFAULT_CONTENT_KO = LINGO_ROOT / "content-ko"
DEFAULT_REPORT = RELEASE_AGGREGATOR_ROOT / "reports" / "dictionary_entry_drift_inventory_2026-05-03.md"


@dataclass(frozen=True)
class AuditResult:
    rows: list[dict[str, Any]]
    duplicate_atom_ids: dict[str, int]
    same_surface_pos_multi_rows: list[tuple[tuple[str, str], list[dict[str, Any]]]]
    same_surface_cross_pos: list[tuple[str, list[dict[str, Any]]]]
    same_row_multi_entry: list[dict[str, Any]]
    same_row_multi_sense: list[dict[str, Any]]
    missing_origin_candidates: list[dict[str, Any]]
    row_level_origin_multi_entry: list[dict[str, Any]]
    suspicious_rows: list[dict[str, Any]]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rows(content_ko: Path) -> list[dict[str, Any]]:
    manifest_path = content_ko / "content_v2" / "inventory" / "dictionary" / "manifest.json"
    manifest = read_json(manifest_path)
    rows: list[dict[str, Any]] = []
    for shard in manifest.get("shards", {}).values():
        shard_path = content_ko / shard["path"]
        for line_no, line in enumerate(shard_path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["_source_file"] = str(shard_path.relative_to(content_ko))
            row["_source_line"] = line_no
            rows.append(row)
    return rows


def atom_id(row: dict[str, Any]) -> str:
    return str(row.get("atom_id") or row.get("id") or "").strip()


def row_pos(row: dict[str, Any]) -> str:
    return str(row.get("pos") or "").strip()


def row_lemma(row: dict[str, Any]) -> str:
    return str(row.get("lemma") or "").strip()


def zh_tw_defs(row: dict[str, Any]) -> list[dict[str, Any]]:
    definitions = row.get("definitions")
    if not isinstance(definitions, dict):
        return []
    defs = definitions.get("zh_tw")
    if not isinstance(defs, list):
        return []
    return [definition for definition in defs if isinstance(definition, dict)]


def entry_nos(row: dict[str, Any]) -> set[int]:
    out: set[int] = set()
    for definition in zh_tw_defs(row):
        raw = definition.get("entry_no", 1)
        try:
            out.add(int(raw))
        except (TypeError, ValueError):
            out.add(1)
    return out


def sense_count(row: dict[str, Any]) -> int:
    return len([definition for definition in zh_tw_defs(row) if definition.get("sense_id")])


def surfaces(row: dict[str, Any]) -> set[str]:
    out = {str(surface).strip() for surface in row.get("surface_forms") or [] if str(surface).strip()}
    lemma = row_lemma(row)
    if lemma:
        out.add(lemma)
    aid = atom_id(row)
    if ":" in aid:
        suffix = aid.split(":")[-1].strip()
        if suffix:
            out.add(suffix)
    return out


def origin_payload(row: dict[str, Any]) -> dict[str, Any]:
    metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
    out: dict[str, Any] = {}
    for key in ("hanja", "origin", "origin_type", "source_language", "source_word"):
        value = row.get(key, metadata.get(key))
        if value not in (None, ""):
            out[key] = value
    return out


def row_summary(row: dict[str, Any]) -> dict[str, Any]:
    defs = zh_tw_defs(row)
    return {
        "atom_id": atom_id(row),
        "lemma": row_lemma(row),
        "pos": row_pos(row),
        "entries": sorted(entry_nos(row)),
        "sense_count": sense_count(row),
        "origin": origin_payload(row),
        "source": f"{row.get('_source_file')}:{row.get('_source_line')}",
        "glosses": [str(definition.get("gloss", "")) for definition in defs[:6] if definition.get("gloss")],
    }


def score_suspicion(row: dict[str, Any]) -> int:
    score = 0
    entries = entry_nos(row)
    defs = zh_tw_defs(row)
    origin = origin_payload(row)
    if len(entries) > 1:
        score += 5
    if len(entries) > 1 and not origin:
        score += 3
    if len(entries) > 1 and origin:
        score += 2
    if len(defs) >= 4:
        score += 2
    if any("；" in str(definition.get("gloss", "")) for definition in defs):
        score += 1
    if any(token in str(definition.get("gloss", "")) for definition in defs for token in ("外來", "源自", "漢字", "英語", "日語")):
        score += 3
    return score


def audit(rows: list[dict[str, Any]]) -> AuditResult:
    id_counts = Counter(atom_id(row) for row in rows if atom_id(row))
    duplicate_atom_ids = {aid: count for aid, count in id_counts.items() if count > 1}

    by_surface_pos: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    by_surface: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        for surface in surfaces(row):
            by_surface_pos[(surface, row_pos(row))].append(row)
            by_surface[surface].append(row)

    same_surface_pos_multi_rows = [
        (key, values)
        for key, values in by_surface_pos.items()
        if len({atom_id(row) for row in values}) > 1
    ]
    same_surface_cross_pos = [
        (surface, values)
        for surface, values in by_surface.items()
        if len({row_pos(row) for row in values}) > 1
    ]
    same_row_multi_entry = [row for row in rows if len(entry_nos(row)) > 1]
    same_row_multi_sense = [row for row in rows if sense_count(row) > 1]
    missing_origin_candidates = [
        row
        for row in same_row_multi_entry
        if not origin_payload(row)
    ]
    row_level_origin_multi_entry = [
        row
        for row in same_row_multi_entry
        if origin_payload(row)
    ]
    suspicious_rows = sorted(rows, key=lambda row: (-score_suspicion(row), atom_id(row)))[:30]

    return AuditResult(
        rows=rows,
        duplicate_atom_ids=duplicate_atom_ids,
        same_surface_pos_multi_rows=sorted(same_surface_pos_multi_rows, key=lambda item: item[0]),
        same_surface_cross_pos=sorted(same_surface_cross_pos, key=lambda item: item[0]),
        same_row_multi_entry=sorted(same_row_multi_entry, key=atom_id),
        same_row_multi_sense=sorted(same_row_multi_sense, key=atom_id),
        missing_origin_candidates=sorted(missing_origin_candidates, key=atom_id),
        row_level_origin_multi_entry=sorted(row_level_origin_multi_entry, key=atom_id),
        suspicious_rows=suspicious_rows,
    )


def render_row_table(rows: list[dict[str, Any]], limit: int = 30) -> str:
    lines = ["| atom_id | pos | lemma | entries | senses | origin | sample glosses | source |", "|---|---:|---|---:|---:|---|---|---|"]
    for row in rows[:limit]:
        summary = row_summary(row)
        origin = ", ".join(f"{key}={value}" for key, value in summary["origin"].items()) or "-"
        glosses = "<br>".join(summary["glosses"]) or "-"
        lines.append(
            "| {atom_id} | {pos} | {lemma} | {entries} | {sense_count} | {origin} | {glosses} | {source} |".format(
                atom_id=summary["atom_id"],
                pos=summary["pos"],
                lemma=summary["lemma"],
                entries=",".join(str(entry) for entry in summary["entries"]) or "-",
                sense_count=summary["sense_count"],
                origin=origin,
                glosses=glosses,
                source=summary["source"],
            )
        )
    return "\n".join(lines)


def render_report(result: AuditResult, content_ko: Path) -> str:
    return "\n\n".join(
        [
            "# Dictionary Entry Drift Inventory",
            f"Source: `{content_ko}`",
            "## Count Summary\n\n"
            f"- total rows: {len(result.rows)}\n"
            f"- duplicate atom_id count: {len(result.duplicate_atom_ids)}\n"
            f"- same surface + same POS multi-row count: {len(result.same_surface_pos_multi_rows)}\n"
            f"- same surface cross-POS candidate count: {len(result.same_surface_cross_pos)}\n"
            f"- same row multi-entry_no count: {len(result.same_row_multi_entry)}\n"
            f"- same row multi-sense count: {len(result.same_row_multi_sense)}\n"
            f"- multi-entry rows missing row-level origin/hanja/source: {len(result.missing_origin_candidates)}\n"
            f"- multi-entry rows with row-level origin/hanja/source: {len(result.row_level_origin_multi_entry)}",
            "## Interpretation\n\n"
            "Current key model is `ko:{pos}:{lemma}`. Cross-POS same-surface rows should remain separate candidates. "
            "Same-POS homonyms are currently represented inside one atom row via `entry_no`, not as separate atom IDs.",
            "## Top Suspicious Rows\n\n" + render_row_table(result.suspicious_rows, 30),
            "## Multi-Entry Rows Missing Row-Level Origin\n\n" + render_row_table(result.missing_origin_candidates, 30),
            "## Multi-Entry Rows With Row-Level Origin\n\n"
            "These may need entry-level origin review if different `entry_no` values have different Hanja/source.\n\n"
            + render_row_table(result.row_level_origin_multi_entry, 30),
            "## Same Surface + Same POS Multi-Row Check\n\n"
            + (
                "No same-surface same-POS multi-row collisions found."
                if not result.same_surface_pos_multi_rows
                else "\n".join(
                    f"- `{surface}` / `{pos}`: {', '.join(atom_id(row) for row in rows[:8])}"
                    for (surface, pos), rows in result.same_surface_pos_multi_rows[:30]
                )
            ),
            "## Next Actions\n\n"
            "1. Review the top suspicious rows manually before editing inventory.\n"
            "2. Decide whether rows with row-level origin and multiple `entry_no` need entry-level origin metadata.\n"
            "3. Keep resolver `entry_refs` aligned with the current key model until an explicit homonym-ID migration is approved.\n"
            "4. Use tokenizer/handoff context for lesson-level disambiguation instead of changing global atom IDs prematurely.",
        ]
    ) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit dictionary entry drift.")
    parser.add_argument("--content-ko-repo", type=Path, default=DEFAULT_CONTENT_KO)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    content_ko = args.content_ko_repo.resolve()
    rows = load_rows(content_ko)
    result = audit(rows)
    report = render_report(result, content_ko)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"wrote {args.output}")
    print(f"rows={len(result.rows)} multi_entry={len(result.same_row_multi_entry)} suspicious={len(result.suspicious_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
