import os
import json
import argparse
import datetime
from typing import List, Dict, Any

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def map_target_position(pos_obj: Any) -> int:
    """
    Map canonical target_position object to review-station MVP integer.
    MVP Mapping:
    - unit_intro -> 0
    - unit_mid -> 1
    - unit_tail -> 2
    - others -> 1 (default mid)
    """
    if not isinstance(pos_obj, dict):
        return 1
    
    slot = pos_obj.get("slot")
    if slot == "unit_intro":
        return 0
    if slot == "unit_mid":
        return 1
    if slot == "unit_tail":
        return 2
    
    # If using absolute anchors, default to 1 (mid) for now
    if "after_lesson_id" in pos_obj or "before_lesson_id" in pos_obj:
        return 1
        
    return 1

def ensure_preview_map(preview: Any) -> Dict[str, Any]:
    if isinstance(preview, dict):
        return preview
    return {"raw_text": str(preview)}

def convert_to_review_item(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "candidate_id": candidate.get("candidate_id"),
        "batch_id": candidate.get("batch_id"),
        "candidate_type": candidate.get("candidate_type"),
        "target_level": candidate.get("target_level"),
        "target_unit_id": candidate.get("target_unit_id"),
        "target_position": map_target_position(candidate.get("target_position")),
        "title_zh_tw": candidate.get("title_zh_tw"),
        "subtitle_zh_tw": candidate.get("subtitle_zh_tw"),
        "can_do_zh_tw": candidate.get("can_do_zh_tw", []),
        "review_summary_zh_tw": candidate.get("review_summary_zh_tw"),
        "novelty_rationale_zh_tw": candidate.get("novelty_rationale_zh_tw"),
        "risk_flags_zh_tw": candidate.get("risk_flags_zh_tw", []),
        "agent_recommendation": candidate.get("agent_recommendation", "accept"),
        "scores": candidate.get("scores", {}),
        "foreign_preview": ensure_preview_map(candidate.get("foreign_preview")),
        "human_decision": "unreviewed",
        "human_notes_zh_tw": "",
        "updated_at": datetime.datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Review Ready Bundle Exporter")
    parser.add_argument("--input", required=True, help="Path to candidate_packs.normalized.json")
    parser.add_argument("--output", help="Path to output review_ready_bundle.json")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        log(f"Error: Input file {args.input} not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = data.get("candidates", [])
    review_items = [convert_to_review_item(c) for c in candidates]

    batch_dir = os.path.dirname(os.path.abspath(args.input))
    output_path = args.output or os.path.join(batch_dir, "review_ready_bundle.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(review_items, f, ensure_ascii=False, indent=2)

    log(f"Exported {len(review_items)} candidates to review bundle.")
    log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
