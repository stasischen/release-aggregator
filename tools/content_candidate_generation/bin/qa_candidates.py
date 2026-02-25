import os
import json
import argparse
import datetime
from typing import List, Dict, Any

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def lint_required_fields(candidate: Dict[str, Any], required: List[str]) -> List[Dict[str, Any]]:
    issues = []
    # Fields that are allowed to be empty arrays (but must exist)
    allow_empty_list = ["risk_flags_zh_tw", "theme_tags", "skill_tags", "grammar_focus", "dictionary_focus_terms"]
    
    for field in required:
        if field not in candidate:
            issues.append({
                "severity": "error",
                "rule_id": "REQ_FIELD_MISSING",
                "message_zh_tw": f"缺失必要欄位: {field}",
                "field_path": field
            })
            continue
            
        val = candidate.get(field)
        if val is None or val == "":
             issues.append({
                "severity": "error",
                "rule_id": "FIELD_EMPTY",
                "message_zh_tw": f"欄位內容為空: {field}",
                "field_path": field
            })
        elif isinstance(val, list) and len(val) == 0 and field not in allow_empty_list:
            issues.append({
                "severity": "error",
                "rule_id": "ARRAY_EMPTY",
                "message_zh_tw": f"列表內容為空: {field}",
                "field_path": field
            })
    return issues

def lint_unit_fit(candidate: Dict[str, Any], brief: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues = []
    target_levels = brief.get("target_levels", [])
    target_units = brief.get("target_units", [])
    
    if candidate.get("target_level") not in target_levels:
        issues.append({
            "severity": "error",
            "rule_id": "LEVEL_MISMATCH",
            "message_zh_tw": f"等級不符: 預期 {target_levels}，實際 {candidate.get('target_level')}",
            "field_path": "target_level"
        })
        
    if target_units and candidate.get("target_unit_id") not in target_units:
        issues.append({
            "severity": "warning",
            "rule_id": "UNIT_MISMATCH",
            "message_zh_tw": f"單元不符: 預期 {target_units}，實際 {candidate.get('target_unit_id')}",
            "field_path": "target_unit_id"
        })
        
    return issues

def get_preview_text(foreign_preview: Any) -> str:
    if isinstance(foreign_preview, dict):
        return json.dumps(foreign_preview, sort_keys=True)
    return str(foreign_preview)

def check_duplicates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    batch_issues = []
    
    # ID Uniqueness
    ids = [c.get("candidate_id") for c in candidates if c.get("candidate_id")]
    if len(ids) != len(set(ids)):
        duplicates = set([x for x in ids if ids.count(x) > 1])
        batch_issues.append({
            "severity": "error",
            "rule_id": "DUPLICATE_ID",
            "message_zh_tw": f"候選 ID 重複: {list(duplicates)}"
        })
        
    # Content Similarity (Simple Exact Match)
    previews = []
    for c in candidates:
        previews.append({
            "id": c.get("candidate_id"), 
            "text": get_preview_text(c.get("foreign_preview"))
        })
        
    for i in range(len(previews)):
        for j in range(i + 1, len(previews)):
            p1 = previews[i]
            p2 = previews[j]
            if p1["text"] == p2["text"] and p1["id"] != p2["id"]:
                batch_issues.append({
                    "severity": "warning",
                    "rule_id": "DUPLICATE_CONTENT",
                    "message_zh_tw": f"內容重複: {p1['id']} 與 {p2['id']} 的預覽內容完全相同。",
                    "involved_candidates": [p1["id"], p2["id"]]
                })
    
    return batch_issues

def main():
    parser = argparse.ArgumentParser(description="Content Candidate QA Tool (MVP)")
    parser.add_argument("--normalized", required=True, help="Path to candidate_packs.normalized.json")
    parser.add_argument("--brief", required=True, help="Path to generation_brief.json")
    parser.add_argument("--output", help="Path to output qa_report.json")
    args = parser.parse_args()

    if not os.path.exists(args.normalized):
        log(f"Error: Normalized file {args.normalized} not found.")
        return
    if not os.path.exists(args.brief):
        log(f"Error: Brief file {args.brief} not found.")
        return

    with open(args.normalized, "r", encoding="utf-8") as f:
        norm_data = json.load(f)
    with open(args.brief, "r", encoding="utf-8") as f:
        brief = json.load(f)

    candidates = norm_data.get("candidates", [])
    
    # Required fields from schema (hardcoded for MVP based on candidate_schema_v1.json)
    required_fields = [
        "candidate_id", "batch_id", "candidate_type", "target_level",
        "target_unit_id", "target_position", "title_zh_tw", "subtitle_zh_tw",
        "can_do_zh_tw", "review_summary_zh_tw", "novelty_rationale_zh_tw",
        "risk_flags_zh_tw", "agent_recommendation", "scores", "foreign_preview"
    ]

    report_items = []
    batch_wide_issues = check_duplicates(candidates)
    
    total_errors = 0
    total_warnings = 0
    
    for c in candidates:
        cid = c.get("candidate_id", "UNKNOWN")
        issues = []
        issues.extend(lint_required_fields(c, required_fields))
        issues.extend(lint_unit_fit(c, brief))
        
        # Attach issues to candidate
        c["qa_flags"] = issues
        
        errors = len([i for i in issues if i["severity"] == "error"])
        warnings = len([i for i in issues if i["severity"] == "warning"])
        
        total_errors += errors
        total_warnings += warnings
        
        report_items.append({
            "candidate_id": cid,
            "pass": errors == 0,
            "error_count": errors,
            "warning_count": warnings,
            "issues": issues
        })

    # Add batch-wide issues to totals
    total_errors += len([i for i in batch_wide_issues if i["severity"] == "error"])
    total_warnings += len([i for i in batch_wide_issues if i["severity"] == "warning"])

    report = {
        "batch_id": brief.get("batch_id"),
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": {
            "total_candidates": len(candidates),
            "pass": total_errors == 0,
            "total_errors": total_errors,
            "total_warnings": total_warnings
        },
        "batch_wide_issues": batch_wide_issues,
        "per_candidate_reports": report_items
    }

    batch_dir = os.path.dirname(os.path.abspath(args.normalized))
    output_path = args.output or os.path.join(batch_dir, "qa_report.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Save updated normalized file with qa_flags
    with open(args.normalized, "w", encoding="utf-8") as f:
        json.dump(norm_data, f, ensure_ascii=False, indent=2)

    log(f"QA completed for {len(candidates)} candidates.")
    log(f"Total Errors: {total_errors}, Total Warnings: {total_warnings}")
    log(f"QA Report saved to: {output_path}")

if __name__ == "__main__":
    main()
