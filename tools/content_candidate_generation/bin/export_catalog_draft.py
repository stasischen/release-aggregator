import os
import json
import argparse
import datetime
from typing import List, Dict, Any

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def convert_to_catalog_item(candidate: Dict[str, Any]) -> Dict[str, Any]:
    # Mapping logic from candidate to catalog draft
    # Catalog draft structure is a simplified version for PM review/import
    return {
        "candidate_id": candidate.get("candidate_id"),
        "title_zh_tw": candidate.get("title_zh_tw"),
        "subtitle_zh_tw": candidate.get("subtitle_zh_tw"),
        "candidate_type": candidate.get("candidate_type"),
        "target_level": candidate.get("target_level"),
        "target_unit_id": candidate.get("target_unit_id"),
        "target_position_ref": candidate.get("target_position"),
        "can_do_zh_tw": candidate.get("can_do_zh_tw", []),
        "estimated_minutes": candidate.get("estimated_minutes", 10),
        "theme_tags": candidate.get("theme_tags", []),
        "skill_tags": candidate.get("skill_tags", []),
        "grammar_focus": candidate.get("grammar_focus", []),
        "dictionary_focus_terms": candidate.get("dictionary_focus_terms", []),
        "source_batch_id": candidate.get("batch_id"),
        "accepted_at": candidate.get("updated_at") or datetime.datetime.now().isoformat()
    }

def main():
    parser = argparse.ArgumentParser(description="Accepted Candidate to Catalog Draft Adapter")
    parser.add_argument("--input", required=True, help="Path to accepted_candidates.json")
    parser.add_argument("--output", help="Path to output catalog_draft.json")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        log(f"Error: Input file {args.input} not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        accepted_data = json.load(f)

    # In some cases, review station might export a bundle-like object. 
    # Handle both list and object with 'items' key.
    if isinstance(accepted_data, dict) and "items" in accepted_data:
        candidates = accepted_data["items"]
    elif isinstance(accepted_data, list):
        candidates = accepted_data
    else:
        log("Error: Unexpected format in accepted_candidates.json (expected list or object with 'items')")
        return

    # Only process accepted candidates
    accepted_candidates = [c for c in candidates if c.get("human_decision") == "accept"]
    
    catalog_items = [convert_to_catalog_item(c) for c in accepted_candidates]

    batch_dir = os.path.dirname(os.path.abspath(args.input))
    output_path = args.output or os.path.join(batch_dir, "catalog_draft.json")
    
    output_data = {
        "catalog_version": "v1-draft",
        "exported_at": datetime.datetime.now().isoformat(),
        "total_items": len(catalog_items),
        "items": catalog_items
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    log(f"Exported {len(catalog_items)} accepted candidates to catalog draft.")
    log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
