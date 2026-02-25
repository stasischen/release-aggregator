import os
import json
import argparse
import datetime
import uuid

def log(msg):
    print(f"[{datetime.datetime.now().isoformat()}] {msg}")

class MockProvider:
    def generate(self, brief, candidate_type, count):
        candidates = []
        for i in range(count):
            cid = f"{brief['batch_id']}-{candidate_type}-{i+1:03d}"
            candidate = {
                "candidate_id": cid,
                "batch_id": brief['batch_id'],
                "candidate_type": candidate_type,
                "target_level": brief['target_levels'][0],
                "target_unit_id": brief.get('target_units', ["UNKNOWN"])[0],
                "target_position": {"slot": "unit_mid"},
                "title_zh_tw": f"實用對話 {i+1} (Mock)",
                "subtitle_zh_tw": f"學習基礎對話場景 {i+1}",
                "can_do_zh_tw": ["能用韓文進行基本對談"],
                "review_summary_zh_tw": "由 MockProvider 生成的範例內容，用於測試流程。",
                "novelty_rationale_zh_tw": "增加現有單元的練習密度。",
                "risk_flags_zh_tw": [],
                "agent_recommendation": "accept",
                "scores": {
                    "fit": 0.8,
                    "novelty": 0.5,
                    "learnability": 0.9,
                    "reuse": 0.7,
                    "engagement": 0.8,
                    "cost": 1.0
                },
                "foreign_preview": {
                    "dialogue": [
                        {"speaker": "A", "text": "안녕하세요", "translation_zh_tw": "你好"},
                        {"speaker": "B", "text": "반갑습니다", "translation_zh_tw": "見到你很高興"}
                    ]
                }
            }
            candidates.append(candidate)
        return candidates

def main():
    parser = argparse.ArgumentParser(description="API Batch Runner MVP")
    parser.add_argument("--brief", required=True, help="Path to generation_brief.json")
    parser.add_argument("--output", help="Path to output raw file")
    parser.add_argument("--dry-run", action="store_true", help="Do not call real APIs")
    args = parser.parse_args()

    if not os.path.exists(args.brief):
        log(f"Error: Brief file {args.brief} not found.")
        return

    with open(args.brief, "r", encoding="utf-8") as f:
        brief = json.load(f)

    batch_dir = os.path.dirname(os.path.abspath(args.brief))
    output_path = args.output or os.path.join(batch_dir, "candidate_packs.api.raw.json")
    report_path = os.path.join(batch_dir, "generation_report.json")

    log(f"Starting batch: {brief['batch_id']}")
    log(f"Target units: {brief.get('target_units', 'All')}")
    
    provider = MockProvider()
    all_candidates = []
    
    start_time = datetime.datetime.now()
    
    for ctype, count in brief.get('count_targets', {}).items():
        log(f"Generating {count} candidates of type: {ctype}")
        candidates = provider.generate(brief, ctype, count)
        all_candidates.extend(candidates)
        
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    log(f"Generation completed. Total candidates: {len(all_candidates)}")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"candidates": all_candidates}, f, ensure_ascii=False, indent=2)
    
    report = {
        "batch_id": brief['batch_id'],
        "generated_at": end_time.isoformat(),
        "duration_seconds": duration,
        "provider": "MockProvider",
        "total_count": len(all_candidates),
        "status": "success"
    }
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    log(f"Raw candidates saved to: {output_path}")
    log(f"Generation report saved to: {report_path}")

if __name__ == "__main__":
    main()
