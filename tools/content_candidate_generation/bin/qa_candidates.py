import os
import json
import argparse
import datetime
from typing import List, Dict, Any

import re
from difflib import SequenceMatcher

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def has_chinese(text: str) -> bool:
    if not text: return False
    # Basic check for Chinese characters
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def get_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

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
            
    # Explicit Chinese check for summary
    summary = candidate.get("review_summary_zh_tw", "")
    if summary and not has_chinese(summary):
        issues.append({
            "severity": "error",
            "rule_id": "ZH_SUMMARY_MISSING",
            "message_zh_tw": "中文摘要缺失或不包含中文字元",
            "field_path": "review_summary_zh_tw"
        })
        
    return issues

def lint_unit_fit(candidate: Dict[str, Any], brief: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues = []
    target_levels = brief.get("target_levels", [])
    target_units = brief.get("target_units", [])
    
    level = candidate.get("target_level")
    if level not in target_levels:
        issues.append({
            "severity": "error",
            "rule_id": "LEVEL_MISMATCH",
            "message_zh_tw": f"等級不符: 預期 {target_levels}，實際 {level}",
            "field_path": "target_level"
        })
    
    # A1 Guard
    if level == "A1":
        title = candidate.get("title_zh_tw", "")
        if len(title) > 20:
            issues.append({
                "severity": "warning",
                "rule_id": "A1_COMPLEXITY_RISK",
                "message_zh_tw": "A1 標題過長，可能超出初學者負荷",
                "field_path": "title_zh_tw"
            })
        
    if target_units and candidate.get("target_unit_id") not in target_units:
        issues.append({
            "severity": "warning",
            "rule_id": "UNIT_MISMATCH",
            "message_zh_tw": f"單元不符: 預期 {target_units}，實際 {candidate.get('target_unit_id')}",
            "field_path": "target_unit_id"
        })
        
    return issues

def lint_position(candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
    issues = []
    pos = candidate.get("target_position")
    if not isinstance(pos, dict):
        issues.append({
            "severity": "error",
            "rule_id": "TARGET_POSITION_INVALID",
            "message_zh_tw": "位置資訊格式錯誤 (應為 object)",
            "field_path": "target_position"
        })
    else:
        if not any(k in pos for k in ["slot", "after_lesson_id", "before_lesson_id"]):
             issues.append({
                "severity": "error",
                "rule_id": "TARGET_POSITION_INVALID",
                "message_zh_tw": "位置資訊不全 (缺失 slot, after_lesson_id 或 before_lesson_id)",
                "field_path": "target_position"
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
        
    # Content Similarity
    items = []
    for c in candidates:
        items.append({
            "id": c.get("candidate_id"), 
            "text": get_preview_text(c.get("foreign_preview")),
            "title": c.get("title_zh_tw", "")
        })
        
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            p1 = items[i]
            p2 = items[j]
            
            # Exact Match
            if p1["text"] == p2["text"] and p1["id"] != p2["id"]:
                batch_issues.append({
                    "severity": "warning",
                    "rule_id": "DUPLICATE_CONTENT",
                    "message_zh_tw": f"內容重複: {p1['id']} 與 {p2['id']} 的預覽內容完全相同。",
                    "involved_candidates": [p1["id"], p2["id"]]
                })
            
            # Title Similarity
            if p1["title"] and p2["title"]:
                sim = get_similarity(p1["title"], p2["title"])
                if sim > 0.8:
                    batch_issues.append({
                        "severity": "warning",
                        "rule_id": "DUP_TITLE_SIMILAR_HIGH",
                        "message_zh_tw": f"標題相似度過高 ({sim:.2f}): {p1['id']} ({p1['title']}) 與 {p2['id']} ({p2['title']})",
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
    
    # Attach batch-wide issues to involved candidates
    for issue in batch_wide_issues:
        involved = issue.get("involved_candidates", [])
        for cid in involved:
            for c in candidates:
                if c.get("candidate_id") == cid:
                    if "qa_flags" not in c: c["qa_flags"] = []
                    # Avoid duplicate attachment if re-running
                    if not any(f["rule_id"] == issue["rule_id"] and f["message_zh_tw"] == issue["message_zh_tw"] for f in c["qa_flags"]):
                        c["qa_flags"].append(issue)

    total_errors = 0
    total_warnings = 0
    
    for c in candidates:
        cid = c.get("candidate_id", "UNKNOWN")
        issues = c.get("qa_flags", [])
        issues.extend(lint_required_fields(c, required_fields))
        issues.extend(lint_unit_fit(c, brief))
        issues.extend(lint_position(c))
        
        # Deduplicate and re-attach
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
