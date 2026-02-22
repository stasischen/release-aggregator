import os
import json
import re
import sys
import subprocess
from pathlib import Path

# Path Configuration
AGGREGATOR_ROOT = Path(__file__).resolve().parents[1]
DEV_ROOT = AGGREGATOR_ROOT.parent

LLLO_ROOT = DEV_ROOT / "lllo"
CONTENT_KO_ROOT = DEV_ROOT / "content-ko"

def check_dict_completeness():
    """Scans content-ko dictionary files for empty translations."""
    print("--- 1. Dictionary Completeness Check ---")
    dict_dir = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "dictionary"
    if not dict_dir.exists():
        print(f"Skipping: Dictionary directory not found at {dict_dir}")
        return True

    missing_count = 0
    total_count = 0
    for f in dict_dir.glob("*.json"):
        total_count += 1
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                zh_tw = data.get("definitions", {}).get("zh_tw", [])
                if not zh_tw or zh_tw == [""] or any(isinstance(x, str) and ("[zh-TW]" in x or "TODO" in x) for x in zh_tw):
                    print(f"  [MISSING] Missing translation: {f.name}")
                    missing_count += 1
        except Exception as e:
            print(f"  [ERROR] Error reading {f.name}: {e}")
            missing_count += 1

    print(f"  Summary: {total_count} files checked, {missing_count} issues found.")
    return missing_count == 0

def check_placeholders_in_lllo():
    """Scans LLLO source files for placeholder strings."""
    print("--- 2. LLLO Placeholder Audit ---")
    if not LLLO_ROOT.exists():
        print(f"Skipping: LLLO directory not found at {LLLO_ROOT}")
        return True

    patterns = [r"\[zh-TW\]", r"TODO:", r"MISSING"]
    issue_count = 0
    
    # We'll check .csv and .md files in locales
    locales_dir = LLLO_ROOT / "data" / "courses" / "ko" / "locales" / "zh-TW"
    if not locales_dir.exists():
        print(f"Skipping: Locales directory not found at {locales_dir}")
        return True

    for f in locales_dir.rglob("*.*"):
        if f.suffix not in (".csv", ".md"):
            continue
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                for p in patterns:
                    if re.search(p, content, re.IGNORECASE):
                        print(f"  [PLACEHOLDER] Placeholder '{p}' found in: {f.relative_to(LLLO_ROOT)}")
                        issue_count += 1
                        break # Only report once per file
        except Exception as e:
            print(f"  [ERROR] Error reading {f.name}: {e}")

    print(f"  Summary: {issue_count} files with placeholders found.")
    return issue_count == 0

def check_atom_integrity():
    """Runs content-ko's atom integrity check on gold standards."""
    print("--- 3. Atom ID Integrity Check ---")
    integrity_script = CONTENT_KO_ROOT / "scripts" / "qa" / "check_atom_extraction_integrity.py"
    gold_dir = CONTENT_KO_ROOT / "content" / "gold_standards" / "dialogue" / "A1"
    
    if not integrity_script.exists():
        print(f"Skipping: Integrity script not found at {integrity_script}")
        return True
    
    if not gold_dir.exists():
        print(f"Skipping: Gold standard directory not found at {gold_dir}")
        return True

    overall_success = True
    for f in gold_dir.glob("*.jsonl"):
        try:
            result = subprocess.run([sys.executable, str(integrity_script), str(f)], 
                                    capture_output=True, text=True, check=False)
            if result.returncode != 0:
                print(f"  [FAIL] Integrity failure in {f.name}:")
                # Parse JSON output from the script if possible, or just print stderr
                try:
                    report = json.loads(result.stdout)
                    print(json.dumps(report, indent=4, ensure_ascii=False))
                except:
                    print(result.stdout)
                overall_success = False
            else:
                print(f"  [PASS] {f.name} passed.")
        except Exception as e:
            print(f"  [ERROR] Error running integrity check on {f.name}: {e}")
            overall_success = False

    return overall_success

def main():
    print("=== Lingo Quality Gate Watchdog ===")
    
    success = True
    
    if not check_dict_completeness():
        success = False
        
    print()
    if not check_placeholders_in_lllo():
        success = False
        
    print()
    if not check_atom_integrity():
        success = False

    print("\n--- Final Result ---")
    if success:
        print("[PASS] All quality gates cleared.")
        sys.exit(0)
    else:
        print("[FAIL] Quality gates found issues. Please fix them before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()
