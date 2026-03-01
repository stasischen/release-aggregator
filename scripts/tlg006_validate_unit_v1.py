#!/usr/bin/env python3
"""TLG-006 validator for unit_blueprint_v1 draft.

Checks:
- TLG-001 top-level contract essentials
- TLG-002 mandatory node suffix coverage
- TLG-003 rubric threshold/range checks on interactive nodes
- TLG-004 repair link resolvability via registry (from payload.pattern_meta)
- Reading overlay consistency checks (question_id/evidence mapping)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any
import re

MANDATORY_SUFFIXES = ["L1", "L2", "L3", "D1", "G1", "G2", "P1", "P2", "P3", "P4", "P5", "P6", "R1"]
INTERACTIVE_OUTPUT_MODES = {"chunk_assembly", "frame_fill", "response_builder", "pattern_transform", "guided", "review_retrieval"}
CONTENT_FORM_TO_GENRE = {
    "dialogue": {"dialogue"},
    "comprehension_check": {"dialogue"},
    "notice": {"notice", "article"},
    "message_thread": {"message", "email"},
    "functional_phrase_pack": {"dialogue"},
    "pattern_card": {"dialogue"},
    "grammar_note": {"article", "notice"},
    "practice_card": {"dialogue", "message"},
    "roleplay_prompt": {"dialogue"},
    "message_prompt": {"message", "email"},
    "review_card": {"notice", "article", "dialogue", "message"},
}
HANGUL_RE = re.compile(r"[\uAC00-\uD7A3]")
CJK_IDEOGRAPH_RE = re.compile(r"[\u4E00-\u9FFF]")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def suffix_of(node_id: str) -> str:
    return node_id.split("-")[-1]


def load_repair_ids(path: Path) -> set[str]:
    data = load_json(path)
    return {str(e.get("repair_id", "")) for e in data.get("entries", []) if e.get("repair_id")}


def resolve_lang_profile_path(target_lang: str, explicit_path: str | None) -> Path:
    if explicit_path:
        return Path(explicit_path)
    return Path(f"docs/tasks/lang_profiles/{target_lang}_generation_profile_v1.json")


def build_profile_indexes(profile: dict[str, Any]) -> tuple[set[str], set[str], dict[str, dict[str, Any]]]:
    supported_genres = set(profile.get("supported_genres", []))
    register_ids = {str(rp.get("register_id", "")) for rp in profile.get("register_profiles", []) if rp.get("register_id")}
    register_map = {str(rp.get("register_id", "")): rp for rp in profile.get("register_profiles", []) if rp.get("register_id")}
    return supported_genres, register_ids, register_map


def validate(blueprint: dict[str, Any], repair_ids: set[str] | None, lang_profile: dict[str, Any] | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if blueprint.get("version") != "unit_blueprint_v1":
        errors.append("ERR_UNSUPPORTED_VERSION_V1: version must be unit_blueprint_v1")
    if blueprint.get("adapter_version") != "frontend_unit_adapter_v1":
        errors.append("ERR_UNSUPPORTED_ADAPTER_VERSION: adapter_version must be frontend_unit_adapter_v1")

    unit = blueprint.get("unit") or {}
    unit_target_lang = str(unit.get("target_lang", "")).strip()
    support_langs = unit.get("support_langs", [])
    if not isinstance(support_langs, list) or not {"zh_tw", "en"}.issubset(set(support_langs)):
        errors.append("ERR_MISSING_SUPPORT_LANGS: support_langs must include zh_tw and en")

    supported_genres: set[str] = set()
    register_ids: set[str] = set()
    register_map: dict[str, dict[str, Any]] = {}
    if lang_profile is not None:
        profile_lang = str(lang_profile.get("target_lang", "")).strip()
        if profile_lang and profile_lang != unit_target_lang:
            errors.append(f"ERR_LANG_MISMATCH: unit.target_lang={unit_target_lang}, profile.target_lang={profile_lang}")
        supported_genres, register_ids, register_map = build_profile_indexes(lang_profile)
    else:
        warnings.append("WARN_LANG_PROFILE_MISSING: skip register/genre style validation")

    sequence = blueprint.get("sequence") or []
    suffixes = {suffix_of(str(n.get("node_id", ""))) for n in sequence}
    missing_suffixes = [s for s in MANDATORY_SUFFIXES if s not in suffixes]
    if missing_suffixes:
        errors.append(f"ERR_TLG_MISSING_MANDATORY_NODE: missing {missing_suffixes}")

    l1_dialogue_lines: list[str] = []
    for node in sequence:
        node_id = str(node.get("node_id", ""))
        if node_id.endswith("-L1"):
            payload = node.get("payload") or {}
            turns = payload.get("dialogue_turns", [])
            if isinstance(turns, list):
                for t in turns:
                    if isinstance(t, dict):
                        for k in ("text", "line_ko"):
                            v = str(t.get(k, "")).strip()
                            if v:
                                l1_dialogue_lines.append(v)

    for node in sequence:
        node_id = str(node.get("node_id", ""))
        output_mode = str(node.get("output_mode", "none"))
        content_form = str(node.get("content_form", "")).strip()
        payload = node.get("payload") or {}
        node_contract = payload.get("node_contract") or {}
        node_goal = str(node_contract.get("node_goal_zh_tw", "")).strip()

        if output_mode in INTERACTIVE_OUTPUT_MODES:
            rubric = payload.get("rubric")
            if not isinstance(rubric, dict):
                errors.append(f"ERR_TLG_RUBRIC_MISSING: {node_id}")
                continue

            threshold = rubric.get("pass_threshold")
            min_attempts = rubric.get("min_attempts")
            max_hints = rubric.get("max_hints_for_pass")
            required_elements = rubric.get("required_elements", [])

            if not isinstance(threshold, (int, float)) or threshold < 0.5 or threshold > 1.0:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} pass_threshold={threshold}")
            if not isinstance(min_attempts, int) or min_attempts < 1 or min_attempts > 5:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} min_attempts={min_attempts}")
            if not isinstance(max_hints, int) or max_hints < 0 or max_hints > 5:
                errors.append(f"ERR_TLG_THRESHOLD_INVALID: {node_id} max_hints_for_pass={max_hints}")
            if not isinstance(required_elements, list) or len(required_elements) == 0:
                errors.append(f"ERR_TLG_REQUIRED_ELEMENTS_EMPTY: {node_id}")

        if node_id.endswith("-P4") and output_mode == "response_builder":
            if not payload.get("trigger_type") or not payload.get("repair_goal"):
                errors.append(f"ERR_TLG_MISSING_REPAIR_METADATA: {node_id}")

        # Pedagogical blocker: objective-task type mismatch
        if content_form == "comprehension_check":
            if any(k in node_goal for k in ["詢問", "回答", "表達", "說明"]) and "聽懂" not in node_goal and "判斷" not in node_goal:
                errors.append(f"ERR_OBJECTIVE_TASK_TYPE_MISMATCH: {node_id} goal={node_goal}")
        if content_form in {"roleplay_prompt", "message_prompt"}:
            if any(k in node_goal for k in ["聽懂", "判斷", "辨識"]) and not any(k in node_goal for k in ["表達", "說", "寫", "回覆"]):
                errors.append(f"ERR_OBJECTIVE_TASK_TYPE_MISMATCH: {node_id} goal={node_goal}")

        # Pedagogical blocker: canonical payload mismatch for comprehension
        if content_form == "comprehension_check":
            items = payload.get("items")
            if not isinstance(items, list) or not items:
                errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} missing items")
            else:
                for idx, it in enumerate(items):
                    if not isinstance(it, dict):
                        errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} items[{idx}] not object")
                        continue
                    # conflicting payload styles in one item
                    if "choices" in it and "response_choices_ko" in it:
                        errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} items[{idx}] mixed choices/response_choices_ko")
                    if not it.get("prompt_ko"):
                        errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} items[{idx}] missing prompt_ko")

            # L2 should be anchored to L1
            if node_id.endswith("-L2"):
                anchor_node_id = str(payload.get("source_anchor_node_id", "")).strip()
                anchor_line = str(payload.get("source_anchor_line", "")).strip()
                if not anchor_node_id:
                    errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} missing source_anchor_node_id")
                if anchor_node_id and not anchor_node_id.endswith("-L1"):
                    errors.append(f"ERR_PAYLOAD_SCHEMA_CANONICAL_MISMATCH: {node_id} source_anchor_node_id must point to L1")
                if anchor_line and l1_dialogue_lines and anchor_line not in l1_dialogue_lines:
                    errors.append(f"ERR_LOGIC_PRECONDITION_FAIL: {node_id} source_anchor_line not found in L1")

        pattern_meta = payload.get("pattern_meta") or {}
        repair_links = pattern_meta.get("repair_links", [])
        if repair_ids is not None and isinstance(repair_links, list):
            for rid in repair_links:
                rid_text = str(rid)
                if rid_text and rid_text not in repair_ids:
                    errors.append(f"ERR_TLG_PATTERN_REPAIR_LINK_UNRESOLVED: {node_id} -> {rid_text}")

        reading_overlay = payload.get("reading_overlay")
        if isinstance(reading_overlay, dict):
            q_ids = {q.get("question_id") for q in reading_overlay.get("question_blueprint", []) if isinstance(q, dict)}
            em_ids = {e.get("question_id") for e in reading_overlay.get("evidence_mapping", []) if isinstance(e, dict)}
            if q_ids and em_ids and not q_ids.issubset(em_ids):
                errors.append(f"ERR_TLR_EVIDENCE_QUESTION_MISMATCH: {node_id}")
            if not reading_overlay.get("evidence_mapping"):
                errors.append(f"ERR_TLR_MISSING_EVIDENCE_MAPPING: {node_id}")

        constraints = payload.get("generation_constraints")
        if isinstance(constraints, dict):
            c_lang = str(constraints.get("target_lang", "")).strip()
            c_genre = str(constraints.get("genre", "")).strip()
            c_register = str(constraints.get("register_target", "")).strip()

            if c_lang and c_lang != unit_target_lang:
                errors.append(f"ERR_LANG_MISMATCH: {node_id} generation_constraints.target_lang={c_lang} unit.target_lang={unit_target_lang}")

            if lang_profile is not None:
                if c_genre and c_genre not in supported_genres:
                    errors.append(f"ERR_GENRE_STYLE_MISMATCH: {node_id} unsupported genre={c_genre}")
                allowed_genres = CONTENT_FORM_TO_GENRE.get(content_form)
                if allowed_genres and c_genre and c_genre not in allowed_genres:
                    errors.append(f"ERR_GENRE_STYLE_MISMATCH: {node_id} content_form={content_form} incompatible genre={c_genre}")
                if c_register and c_register not in register_ids:
                    errors.append(f"ERR_REGISTER_MISMATCH: {node_id} unknown register_target={c_register}")

                # Pedagogical blocker: register/genre mismatch by role
                if content_form == "review_card":
                    if c_genre in {"notice", "article"}:
                        errors.append(f"ERR_REGISTER_GENRE_MISMATCH_BY_ROLE: {node_id} review_card genre={c_genre}")
                if content_form in {"dialogue", "roleplay_prompt"} and c_genre not in {"dialogue"}:
                    errors.append(f"ERR_REGISTER_GENRE_MISMATCH_BY_ROLE: {node_id} {content_form} genre={c_genre}")

                # Deterministic marker check: if profile requires markers, node summary should contain at least one marker.
                rp = register_map.get(c_register)
                if isinstance(rp, dict):
                    required_markers = [str(m) for m in rp.get("required_markers", []) if str(m).strip()]
                    forbidden_markers = [str(m) for m in rp.get("forbidden_markers", []) if str(m).strip()]
                    summary_target = str(node.get("summary_target_lang", ""))
                    if required_markers and summary_target and not any(marker in summary_target for marker in required_markers):
                        warnings.append(f"WARN_STYLE_WEAK_COHESION: {node_id} missing expected marker for register={c_register}")
                    if forbidden_markers and summary_target and any(marker in summary_target for marker in forbidden_markers):
                        errors.append(f"ERR_REGISTER_MISMATCH: {node_id} contains forbidden marker for register={c_register}")

        # Pedagogical blocker: script contamination for KO target text
        if unit_target_lang == "ko":
            def _scan_text(value: Any, path: str) -> None:
                if isinstance(value, dict):
                    for k, v in value.items():
                        _scan_text(v, f"{path}.{k}")
                elif isinstance(value, list):
                    for i, v in enumerate(value):
                        _scan_text(v, f"{path}[{i}]")
                elif isinstance(value, str):
                    s = value.strip()
                    if not s:
                        return
                    p = path.lower()
                    if "zh_tw" in p or "zh-tw" in p or ".en" in p or "_en" in p:
                        return
                    if HANGUL_RE.search(s) and CJK_IDEOGRAPH_RE.search(s):
                        errors.append(f"ERR_SCRIPT_CONTAMINATION: {node_id} {path}")

            _scan_text(payload, "payload")

    if not blueprint.get("scheduled_followups"):
        warnings.append("WARN_TLG_MISSING_FOLLOWUPS: scheduled_followups is empty")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate unit_blueprint_v1 against TLG-001..006 core rules")
    parser.add_argument("--blueprint", required=True, help="Path to unit_blueprint_v1 JSON")
    parser.add_argument("--repair-registry", help="Optional repair registry path for repair link resolution")
    parser.add_argument("--lang-profile", help="Optional path to lang_generation_profile_v1 JSON; defaults to unit.target_lang profile")
    args = parser.parse_args()

    blueprint = load_json(Path(args.blueprint))
    repair_ids = load_repair_ids(Path(args.repair_registry)) if args.repair_registry else None
    unit_target_lang = str((blueprint.get("unit") or {}).get("target_lang", "")).strip()
    lang_profile = None
    if unit_target_lang:
        lang_profile_path = resolve_lang_profile_path(unit_target_lang, args.lang_profile)
        if lang_profile_path.exists():
            lang_profile = load_json(lang_profile_path)
        elif args.lang_profile:
            raise FileNotFoundError(f"Language profile not found: {lang_profile_path}")

    errors, warnings = validate(blueprint, repair_ids, lang_profile)

    for err in errors:
        print(err)
    for warn in warnings:
        print(warn)

    if errors:
        print(f"TLG-006 UNIT RESULT: FAIL (errors={len(errors)}, warnings={len(warnings)})")
        return 1
    print(f"TLG-006 UNIT RESULT: PASS (warnings={len(warnings)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
