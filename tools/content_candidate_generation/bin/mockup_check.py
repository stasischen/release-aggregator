
import os
import json
import argparse
import re
from typing import List, Dict, Any

def has_korean(text: str) -> bool:
    if not text: return False
    return bool(re.search(r'[\uac00-\ud7af]', text))

def has_chinese(text: str) -> bool:
    if not text: return False
    return bool(re.search(r'[\u4e00-\u9fff]', text))

class MockupChecker:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.issues = []
        self.data = None

    def log_issue(self, severity: str, rule_id: str, message: str, path: str = ""):
        self.issues.append({
            "severity": severity,
            "rule_id": rule_id,
            "message": message,
            "path": path
        })

    def check(self):
        if not os.path.exists(self.file_path):
            self.log_issue("error", "FILE_NOT_FOUND", f"File not found: {self.file_path}")
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception as e:
            self.log_issue("error", "JSON_INVALID", f"Invalid JSON: {str(e)}")
            return False

        self._check_top_level()
        if self.data:
            self._check_unit()
            self._check_sequence()
        
        return len([i for i in self.issues if i["severity"] == "error"]) == 0

    def _check_top_level(self):
        required = ["version", "unit", "sequence"]
        for field in required:
            if field not in self.data:
                self.log_issue("error", "MISSING_FIELD", f"Missing top-level field: {field}")

    def _check_unit(self):
        unit = self.data.get("unit", {})
        if not isinstance(unit, dict): return
        
        required = ["unit_id", "level", "target_language", "title_zh_tw"]
        for field in required:
            if field not in unit:
                self.log_issue("error", "MISSING_UNIT_FIELD", f"Missing unit field: {field}")

    def _check_sequence(self):
        sequence = self.data.get("sequence", [])
        if not isinstance(sequence, list):
            self.log_issue("error", "INVALID_SEQUENCE", "Sequence must be a list")
            return

        node_ids = set()
        for i, node in enumerate(sequence):
            path = f"sequence[{i}]"
            node_id = node.get("id")
            if not node_id:
                self.log_issue("error", "MISSING_NODE_ID", "Node missing ID", path)
            else:
                if node_id in node_ids:
                    self.log_issue("error", "DUPLICATE_NODE_ID", f"Duplicate node ID: {node_id}", path)
                node_ids.add(node_id)

            # Check required node fields
            required = ["candidate_type", "content_form", "learning_role", "title_zh_tw"]
            for field in required:
                if field not in node:
                    self.log_issue("error", "MISSING_NODE_FIELD", f"Node {node_id} missing field: {field}", path)

            # Check payload based on content_form
            payload = node.get("payload", {})
            content_form = node.get("content_form")
            if content_form == "dialogue":
                if "dialogue_turns" not in payload:
                    self.log_issue("warning", "MISSING_PAYLOAD_FIELD", f"Dialogue node {node_id} missing dialogue_turns", path)
            elif content_form == "pattern_card":
                if "frames" not in payload:
                    self.log_issue("warning", "MISSING_PAYLOAD_FIELD", f"Pattern card {node_id} missing frames", path)

            # Language guards
            self._check_language_consistency(node, path)

    def _check_language_consistency(self, node, path):
        # Basic check: target language fields should contain target language characters
        # and not Chinese (if it's a 'pure' target field)
        node_id = node.get("id", "??")
        
        # Check sample_lines
        samples = node.get("sample_lines", [])
        for s in samples:
            if not has_korean(s):
                self.log_issue("warning", "LANG_EXPECTATION_MISS", f"Node {node_id} sample line might missing Korean: {s}", path)

        # Check payload recursively for 'text' vs 'zh_tw'
        payload = node.get("payload", {})
        self._check_dict_langs(payload, path + ".payload", node_id)

    def _check_dict_langs(self, d, path, node_id):
        if not isinstance(d, dict): return
        
        for k, v in d.items():
            current_path = f"{path}.{k}"
            if isinstance(v, str):
                if k == "text" or k.endswith("_ko"):
                    if has_chinese(v) and not has_korean(v):
                        self.log_issue("warning", "MIXED_SCRIPT_GUARD", f"Node {node_id} field {k} contains Chinese but no Korean: {v}", current_path)
                if k.endswith("_zh_tw") or k == "zh_tw":
                    if not has_chinese(v) and has_korean(v):
                        self.log_issue("warning", "LANG_EXPECTATION_MISS", f"Node {node_id} field {k} seems to be Korean instead of Chinese: {v}", current_path)
            elif isinstance(v, dict):
                self._check_dict_langs(v, current_path, node_id)
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        self._check_dict_langs(item, f"{current_path}[{i}]", node_id)
                    elif isinstance(item, str) and (k == "text" or k.endswith("_ko")):
                         if has_chinese(item) and not has_korean(item):
                            self.log_issue("warning", "MIXED_SCRIPT_GUARD", f"Node {node_id} list {k}[{i}] contains Chinese: {item}", f"{current_path}[{i}]")

def main():
    parser = argparse.ArgumentParser(description="Multi-fixture QA/Lint tool for Mockup Blueprints")
    parser.add_argument("files", nargs="+", help="Fixture JSON files to check")
    parser.add_argument("--verbose", action="store_true", help="Print all issues including warnings")
    
    args = parser.parse_args()
    
    all_pass = True
    for file_path in args.files:
        checker = MockupChecker(file_path)
        success = checker.check()
        
        print(f"\nChecking {file_path}...")
        if not checker.issues:
            print("  ✅ No issues found.")
        else:
            errors = [i for i in checker.issues if i["severity"] == "error"]
            warnings = [i for i in checker.issues if i["severity"] == "warning"]
            
            for issue in checker.issues:
                if issue["severity"] == "error" or args.verbose:
                    icon = "❌" if issue["severity"] == "error" else "⚠️"
                    print(f"  {icon} [{issue['rule_id']}] {issue['message']} (Path: {issue['path']})")
            
            print(f"  Summary: {len(errors)} errors, {len(warnings)} warnings")
            if errors:
                all_pass = False
        
    if not all_pass:
        exit(1)

if __name__ == "__main__":
    main()
