import os
import json
import argparse
import datetime
from typing import List, Dict, Any

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

def convert_to_backlog_seed(candidate: Dict[str, Any]) -> Dict[str, Any]:
    # Mapping logic from candidate to backlog seed
    return {
        "seed_id": f"SEED-{candidate.get('candidate_id')}",
        "candidate_id": candidate.get("candidate_id"),
        "work_type": candidate.get("candidate_type"),
        "priority": "medium",
        "title_zh_tw": candidate.get("title_zh_tw"),
        "suggested_tasks": [
            "Content verification",
            "Asset procurement (audio/visual)",
            "Formatting for production"
        ],
        "dependencies": [],
        "notes_zh_tw": candidate.get("review_summary_zh_tw", ""),
        "human_notes": candidate.get("human_notes_zh_tw", ""),
        "status": "pending_production"
    }

def main():
    parser = argparse.ArgumentParser(description="Accepted Candidate to Backlog Seed Adapter")
    parser.add_argument("--input", required=True, help="Path to accepted_candidates.json")
    parser.add_argument("--output", help="Path to output backlog_seed.json")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        log(f"Error: Input file {args.input} not found.")
        return

    with open(args.input, "r", encoding="utf-8") as f:
        accepted_data = json.load(f)

    if isinstance(accepted_data, dict) and "items" in accepted_data:
        candidates = accepted_data["items"]
    elif isinstance(accepted_data, list):
        candidates = accepted_data
    else:
        log("Error: Unexpected format in accepted_candidates.json")
        return

    # Only process accepted candidates
    accepted_candidates = [c for c in candidates if c.get("human_decision") == "accept"]
    
    seeds = [convert_to_backlog_seed(c) for c in accepted_candidates]

    batch_dir = os.path.dirname(os.path.abspath(args.input))
    output_path = args.output or os.path.join(batch_dir, "backlog_seed.json")
    
    output_data = {
        "backlog_type": "production_seed",
        "exported_at": datetime.datetime.now().isoformat(),
        "total_seeds": len(seeds),
        "seeds": seeds
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    log(f"Exported {len(seeds)} accepted candidates to backlog seed.")
    log(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
