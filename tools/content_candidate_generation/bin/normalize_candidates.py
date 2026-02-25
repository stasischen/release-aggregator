import os
import json
import argparse
import datetime

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def normalize_candidate(raw):
    # In a real scenario, this would handle different LLM output structures.
    # For now, we ensure it matches the canonical schema or adds defaults.
    
    normalized = raw.copy()
    
    # Ensure mandatory fields or mark for QA
    mandatory_fields = [
        "candidate_id", "batch_id", "candidate_type", "target_level",
        "target_unit_id", "target_position", "title_zh_tw", "subtitle_zh_tw",
        "can_do_zh_tw", "review_summary_zh_tw", "novelty_rationale_zh_tw",
        "risk_flags_zh_tw", "agent_recommendation", "scores", "foreign_preview"
    ]
    
    for field in mandatory_fields:
        if field not in normalized:
            normalized[field] = None # Leave for QA to catch
            
    # Optional fields with defaults
    if "theme_tags" not in normalized:
        normalized["theme_tags"] = []
    if "skill_tags" not in normalized:
        normalized["skill_tags"] = []
    if "qa_flags" not in normalized:
        normalized["qa_flags"] = []
        
    return normalized

def main():
    parser = argparse.ArgumentParser(description="API Raw Normalize Adapter")
    parser.add_argument("--input", required=True, help="Path to raw candidates JSON")
    parser.add_argument("--output", help="Path to normalized output JSON")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        log(f"Error: Input file {args.input} not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_candidates = data.get("candidates", [])
    normalized_candidates = [normalize_candidate(c) for c in raw_candidates]

    batch_dir = os.path.dirname(os.path.abspath(args.input))
    output_path = args.output or os.path.join(batch_dir, "candidate_packs.normalized.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": normalized_candidates}, f, ensure_ascii=False, indent=2)

    log(f"Normalized {len(normalized_candidates)} candidates.")
    log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
