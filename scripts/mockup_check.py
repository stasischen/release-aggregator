#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, List, Dict, Optional

# Constants for validation
MIN_NODE_COUNT = 10
INPUT_ROLES = {"immersion_input", "structure_pattern", "structure_grammar"}
OUTPUT_ROLES = {"controlled_output", "immersion_output", "review_retrieval"}

MIXED_PATTERNS = [
    (re.compile(r"7時"), "Found Chinese 時 in Korean string; likely should be '7시'."),
    (re.compile(r"二\s*잔"), "Found Chinese 二 in Korean quantity; likely should be '두 잔'."),
    (re.compile(r"하端"), "Found Chinese 端 in Korean word; likely should be '하단'."),
    (re.compile(r"外部\s*음식"), "Found Chinese 外部 mixed into Korean phrase; likely should be '외부 음식'."),
]

# Supported values based on unit_blueprint_v0 schema and UNITFAC upgrades
SUPPORTED_LEARNING_ROLES = {
    "immersion_input", "structure_pattern", "structure_grammar",
    "controlled_output", "immersion_output", "review_retrieval",
    "cross_unit_transfer"
}

SUPPORTED_OUTPUT_MODES = {
    "none", "chunk_assembly", "frame_fill", "response_builder",
    "pattern_transform", "guided", "open_task", "retell",
    "transform", "review_retrieval"
}

SUPPORTED_CONTENT_FORMS = {
    "dialogue", "notice", "message_thread", "comparison_card",
    "pattern_card", "grammar_note", "functional_phrase_pack",
    "practice_card", "roleplay_prompt", "message_prompt",
    "review_card", "comprehension_check"
}

class MockupChecker:
    def __init__(self, schema_path: Optional[Path] = None):
        self.errors = []
        self.warnings = []
        self.schema = None
        if schema_path and schema_path.exists():
            try:
                with open(schema_path, "r", encoding="utf-8") as f:
                    self.schema = json.load(f)
            except Exception as e:
                self.errors.append(f"Failed to load schema: {e}")

    def log_error(self, msg: str, node_id: str = None, path: str = None):
        prefix = f"[{node_id}]" if node_id else ""
        suffix = f" (at {path})" if path else ""
        self.errors.append(f"{prefix} ERROR: {msg}{suffix}")

    def log_warning(self, msg: str, node_id: str = None, path: str = None):
        prefix = f"[{node_id}]" if node_id else ""
        suffix = f" (at {path})" if path else ""
        self.warnings.append(f"{prefix} WARN: {msg}{suffix}")

    def iter_strings(self, obj: Any, path: str = "$"):
        if isinstance(obj, dict):
            for k, v in obj.items():
                yield from self.iter_strings(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                yield from self.iter_strings(v, f"{path}[{i}]")
        elif isinstance(obj, str):
            yield path, obj

    def check_fixture(self, fixture_path: Path):
        self.errors = []
        self.warnings = []
        
        try:
            with open(fixture_path, "r", encoding="utf-8") as f:
                fixture = json.load(f)
        except Exception as e:
            self.log_error(f"Failed to parse JSON: {e}")
            return False

        # A. Basic Shape
        if fixture.get("version") != "unit_blueprint_v0":
            self.log_error("fixture.version must be 'unit_blueprint_v0'")
        
        sequence = fixture.get("sequence", [])
        if not isinstance(sequence, list):
            self.log_error("fixture.sequence must be an array")
            return False

        # B. Data Hygiene & Mixed Script
        for s_path, value in self.iter_strings(fixture):
            for pattern, msg in MIXED_PATTERNS:
                if pattern.search(value):
                    self.log_error(f"{msg} Value={value!r}", path=s_path)
            
            # ERR_MISSING_ZH_TW (Basic check for empty strings in TW fields)
            if "_zh_tw" in s_path.lower() or s_path.endswith(".zh_tw"):
                if not value or value.strip() == "" or "TODO" in value:
                     self.log_warning(f"Field seems empty or contains TODO: {value!r}", path=s_path)

        # C. Sequence Rules (UNITFAC-002)
        if len(sequence) < MIN_NODE_COUNT:
            self.log_error(f"ERR_MIN_NODE_COUNT: Unit has {len(sequence)} nodes, minimum {MIN_NODE_COUNT} required for PR.")

        found_input = False
        found_output = False
        first_input_idx = -1
        found_comp_check = False

        for i, node in enumerate(sequence):
            node_id = node.get("id", f"node_{i}")
            role = node.get("learning_role")
            form = node.get("content_form")
            mode = node.get("output_mode")

            # Contract checks
            if role not in SUPPORTED_LEARNING_ROLES:
                self.log_error(f"Unsupported learning_role: {role}", node_id=node_id)
            if form not in SUPPORTED_CONTENT_FORMS:
                self.log_error(f"Unsupported content_form: {form}", node_id=node_id)
            if mode not in SUPPORTED_OUTPUT_MODES:
                self.log_error(f"Unsupported output_mode: {mode}", node_id=node_id)

            # Order Violation
            if role in INPUT_ROLES:
                found_input = True
                if first_input_idx == -1:
                    first_input_idx = i
            if role in OUTPUT_ROLES:
                found_output = True
                if not found_input:
                    self.log_error("ERR_ORDER_VIOLATION: Output node appeared before any input/structure node.", node_id=node_id)

            # Comprehension Check
            if form == "comprehension_check":
                found_comp_check = True

            # Payload Checks
            payload = node.get("payload") or {}
            if "answers_ko" in payload:
                self.log_warning("Uses legacy payload.answers_ko; prefer reference_answers_ko", node_id=node_id)
            
            # Bilingual mismatch
            if "notice_items" in payload and "notice_items_zh_tw" in payload:
                if len(payload["notice_items"]) != len(payload["notice_items_zh_tw"]):
                    self.log_warning(f"notice_items length mismatch: {len(payload['notice_items'])} vs {len(payload['notice_items_zh_tw'])}", node_id=node_id)

        if found_input and not found_comp_check:
            self.log_error("ERR_MISSING_COMPREHENSION: No comprehension_check found in the sequence.")

        return len(self.errors) == 0

def main():
    parser = argparse.ArgumentParser(description="Unified mockup check for unit fixtures.")
    parser.add_argument("files", nargs="*", help="Fixture JSON files to validate.")
    parser.add_argument("--index", help="Path to fixtures index JSON (e.g. modular/data/fixtures.json)")
    parser.add_argument("--schema", help="Path to unit_blueprint_v0.schema.json")
    
    args = parser.parse_args()
    
    checker = MockupChecker(schema_path=Path(args.schema) if args.schema else None)
    
    files_to_check = [Path(f) for f in args.files]
    
    if args.index:
        idx_path = Path(args.index)
        if idx_path.exists():
            try:
                with open(idx_path, "r", encoding="utf-8") as f:
                    idx_data = json.load(f)
                    for unit in idx_data.get("units", []):
                        rel_path = unit.get("path")
                        if rel_path:
                            # Try relative to index file first
                            candidate = (idx_path.parent / rel_path).resolve()
                            if not candidate.exists():
                                # Heuristic: if index is in a 'data' folder, try one level up (viewer relative)
                                candidate = (idx_path.parent.parent / rel_path).resolve()
                            files_to_check.append(candidate)
            except Exception as e:
                print(f"ERROR: Failed to read index {args.index}: {e}")
                sys.exit(2)

    if not files_to_check:
        print("No files to check. Provide files as arguments or use --index.")
        sys.exit(0)

    total_errors = 0
    total_warnings = 0
    failed_files = 0

    print(f"Running mockup-check on {len(files_to_check)} files...\n")

    for f_path in files_to_check:
        if not f_path.exists():
            print(f"FAILED: File not found: {f_path}")
            failed_files += 1
            continue
        
        print(f"Checking {f_path.name}...")
        is_ok = checker.check_fixture(f_path)
        
        if checker.errors:
            for err in checker.errors:
                print(f"  {err}")
        if checker.warnings:
            for warn in checker.warnings:
                print(f"  {warn}")
        
        total_errors += len(checker.errors)
        total_warnings += len(checker.warnings)
        
        if not is_ok:
            failed_files += 1
            print(f"RESULT: {f_path.name} FAILED ({len(checker.errors)} errors, {len(checker.warnings)} warnings)\n")
        else:
            print(f"RESULT: {f_path.name} PASSED ({len(checker.warnings)} warnings)\n")

    print(f"Summary: {len(files_to_check)} files checked, {failed_files} failed.")
    print(f"Total Blocker Errors: {total_errors}")
    print(f"Total Warnings: {total_warnings}")

    if failed_files > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
