import os
import json
import argparse
import datetime
import re

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def parse_target_position(placement_str):
    """
    Parses strings like:
    - "after A1-U04-L2" -> {"after_lesson_id": "A1-U04-L2"}
    - "before A1-U04-L3" -> {"before_lesson_id": "A1-U04-L3"}
    - "slot unit_mid" -> {"slot": "unit_mid"}
    """
    if not placement_str:
        return {"slot": "unit_tail"}
    
    match_after = re.match(r"after\s+(.+)", placement_str, re.IGNORECASE)
    if match_after:
        return {"after_lesson_id": match_after.group(1).strip()}
    
    match_before = re.match(r"before\s+(.+)", placement_str, re.IGNORECASE)
    if match_before:
        return {"before_lesson_id": match_before.group(1).strip()}
    
    match_slot = re.match(r"slot\s+(.+)", placement_str, re.IGNORECASE)
    if match_slot:
        return {"slot": match_slot.group(1).strip()}
    
    # Fallback
    return {"slot": placement_str}

def normalize_agent_candidate(raw_item, batch_id):
    planning = raw_item.get("planning", {})
    pedia = raw_item.get("pedia", {})
    validation = raw_item.get("validation", {})
    payload = raw_item.get("payload", {})
    
    # Mapping
    normalized = {
        "candidate_id": raw_item.get("internal_id") or f"{batch_id}-{raw_item.get('type')}-{id(raw_item)}",
        "batch_id": batch_id,
        "candidate_type": raw_item.get("type"),
        "target_level": planning.get("target_level"),
        "target_unit_id": planning.get("target_unit_id"),
        "target_position": parse_target_position(planning.get("placement")),
        "title_zh_tw": planning.get("title"),
        "subtitle_zh_tw": pedia.get("subtitle"),
        "can_do_zh_tw": pedia.get("can_do", []),
        "review_summary_zh_tw": pedia.get("summary"),
        "novelty_rationale_zh_tw": pedia.get("novelty"),
        "placement_rationale_zh_tw": planning.get("rationale"),
        "risk_flags_zh_tw": validation.get("risk", []),
        "agent_recommendation": validation.get("recommendation", "accept"),
        "scores": validation.get("scores", {
            "fit": 0.5,
            "novelty": 0.5,
            "learnability": 0.5,
            "reuse": 0.5,
            "engagement": 0.5,
            "cost": 0.5
        }),
        "foreign_preview": payload.get("foreign_preview"),
        "metadata": {
            "source": "agent_flow",
            "raw_internal_id": raw_item.get("internal_id")
        }
    }
    
    # Default values for optional fields in schema
    normalized["theme_tags"] = raw_item.get("theme_tags", [])
    normalized["skill_tags"] = raw_item.get("skill_tags", [])
    normalized["qa_flags"] = []
    
    return normalized

def main():
    parser = argparse.ArgumentParser(description="Agent Raw Normalize Adapter")
    parser.add_argument("--input", required=True, help="Path to raw agent candidates JSON")
    parser.add_argument("--output", help="Path to normalized output JSON")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        log(f"Error: Input file {args.input} not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    batch_id = data.get("batch_id", "unknown_batch")
    raw_candidates = data.get("candidates", [])
    
    normalized_candidates = [normalize_agent_candidate(c, batch_id) for c in raw_candidates]

    batch_dir = os.path.dirname(os.path.abspath(args.input))
    output_path = args.output or os.path.join(batch_dir, "candidate_packs.normalized.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": normalized_candidates}, f, ensure_ascii=False, indent=2)

    log(f"Normalized {len(normalized_candidates)} agent candidates.")
    log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
