
import json
import os

# --- ULV Contract Config ---
MANDATORY_FIELDS = {
    'dialogue': ['content', 'dialogue_turns', 'dialogue_scenes'], # At least one
    'video': ['turns', 'nodes'],
    'grammar_summary': ['sections', 'points_i18n'], # At least one
    'pattern_lab': ['pattern_builder_demos', 'pattern_builder_demo'] # At least one
}

TOOLS_BASE = "tools/modular-viewer"

def check_i18n(obj, locale='zh_tw'):
    if not obj: return False
    if isinstance(obj, str): return True
    if isinstance(obj, dict):
        if locale in obj: return True
        if 'i18n' in obj and locale in obj['i18n']: return True
    return False

def verify_fixture(fixture):
    fid = fixture['id']
    fpath = os.path.join(TOOLS_BASE, fixture['path'])
    report = {"id": fid, "status": "PASS", "errors": [], "warnings": []}

    if not os.path.exists(fpath):
        report["status"] = "FAIL"
        report["errors"].append(f"File not found: {fixture['path']}")
        return report

    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 1. Primary Surface Data Check
        content_form = data.get('content_form', 'dialogue') # default or inferred
        if fid == '79Pwq7MTUPE' or 'video' in fpath:
            content_form = 'video'
        
        if content_form == 'dialogue':
            has_turns = any(k in data for k in ['content', 'dialogue_turns', 'dialogue_scenes'])
            if not has_turns:
                report["errors"].append("Missing mandatory dialogue fields (content/turns/scenes)")
        elif content_form == 'video':
            has_video_data = 'turns' in data or ('nodes' in data and 'Start' in data['nodes'])
            if not has_video_data:
                report["errors"].append("Missing mandatory video fields (turns/nodes)")

        # 2. i18n Check (Fallback to zh_tw check)
        if not check_i18n(data.get('title_i18n', data.get('title'))):
            report["warnings"].append("Title might result in empty display in zh_tw")

        # 3. Support Details (if applicable)
        # Check for linked grammar or patterns
        if 'content' in data:
            for item in data['content']:
                if 'grammar_refs' in item or 'pattern_refs' in item:
                     report["warnings"].append(f"Knowledge-link found in {item.get('id')}, ensure runtime enrichment is active.")

    except Exception as e:
        report["status"] = "FAIL"
        report["errors"].append(f"Runtime Error: {str(e)}")

    if report["errors"]:
        report["status"] = "FAIL"
    
    return report

def main():
    fixtures_path = os.path.join(TOOLS_BASE, "data/fixtures.json")
    with open(fixtures_path, 'r', encoding='utf-8') as f:
        fixtures = json.load(f)

    results = []
    print("=== ULV Runtime Contract Verification (Python Simulator) ===")
    for u in fixtures['units']:
        res = verify_fixture(u)
        results.append(res)
        color = "\033[92m" if res['status'] == 'PASS' else "\033[91m"
        reset = "\033[0m"
        print(f"[{color}{res['status']}{reset}] {res['id']}")
        for e in res['errors']: print(f"   - ERROR: {e}")
        for w in res['warnings']: print(f"   - WARN:  {w}")

    with open("scratch/ulv_verification_results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("===========================================================")
    passed = len([r for r in results if r.status == 'PASS']) if hasattr(results[0], 'status') else len([r for r in results if r['status'] == 'PASS'])
    print(f"Summary: {passed}/{len(results)} Passed")

if __name__ == "__main__":
    main()
