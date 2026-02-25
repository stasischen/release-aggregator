import os
import json
import re
import sys
import subprocess
import argparse
from pathlib import Path

# Path Configuration
AGGREGATOR_ROOT = Path(__file__).resolve().parents[1]
DEV_ROOT = AGGREGATOR_ROOT.parent

LLLO_ROOT = DEV_ROOT / "lllo"
CONTENT_KO_ROOT = DEV_ROOT / "content-ko"

def get_active_atoms(scope):
    """Retrieves all atoms used in the specified scope from content-ko gold standards."""
    gold_dir = CONTENT_KO_ROOT / "content" / "gold_standards" / "dialogue" / scope
    active_atoms = set()
    if not gold_dir.exists():
        print(f"Warning: Gold directory for scope {scope} not found.")
        return active_atoms
        
    for file_path in gold_dir.glob("*.jsonl"):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    atom_id = data.get("gold_final_atom_id")
                    if atom_id:
                        for part in atom_id.split('+'):
                            active_atoms.add(part)
                except:
                    continue
    return active_atoms

def check_dict_completeness(scope=None):
    """Scans dictionary files for placeholders, optionally limited to a scope."""
    print(f"--- 1. Dictionary Completeness Check ({scope if scope else 'All'}) ---")
    dict_dir = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "dictionary"
    if not dict_dir.exists():
        print(f"Skipping: Dictionary directory not found at {dict_dir}")
        return True

    active_atoms = None
    if scope:
        active_atoms = get_active_atoms(scope)
        print(f"  Scoping check to {len(active_atoms)} atoms used in {scope}")

    missing_count = 0
    total_count = 0
    
    # If scoped, only check relevant files
    files_to_check = []
    if active_atoms is not None:
        for atom_id in active_atoms:
            safe_name = atom_id.replace(':', '__')
            files_to_check.append(dict_dir / f"{safe_name}.json")
    else:
        files_to_check = list(dict_dir.glob("*.json"))

    for f in files_to_check:
        total_count += 1
        if not f.exists():
            print(f"  [MISSING] File not found: {f.name}")
            missing_count += 1
            continue
            
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                zh_tw = data.get("definitions", {}).get("zh_tw", [])
                if not zh_tw or zh_tw == [""] or any(isinstance(x, str) and ("[zh-TW]" in x or "TODO" in x) for x in zh_tw):
                    print(f"  [PLACEHOLDER] Issue in: {f.name}")
                    missing_count += 1
        except Exception as e:
            print(f"  [ERROR] Error reading {f.name}: {e}")
            missing_count += 1

    print(f"  Summary: {total_count} files checked, {missing_count} issues found.")
    return missing_count == 0

def check_placeholders_in_lllo(scope=None):
    """Scans LLLO source files for placeholder strings, optionally scoped."""
    print(f"--- 2. LLLO Placeholder Audit ({scope if scope else 'All'}) ---")
    if not LLLO_ROOT.exists():
        print(f"Skipping: LLLO directory not found at {LLLO_ROOT}")
        return True

    patterns = [r"\[zh-TW\]", r"TODO:", r"MISSING"]
    issue_count = 0
    
    # Locales directory
    locales_dir = LLLO_ROOT / "data" / "courses" / "ko" / "locales" / "zh-TW"
    if not locales_dir.exists():
        print(f"Skipping: Locales directory not found at {locales_dir}")
        return True

    for f in locales_dir.rglob("*.*"):
        if f.suffix not in (".csv", ".md"):
            continue
        
        # If scope is set, only check files starting with that scope (e.g., A1-*.csv)
        if scope and not f.name.startswith(scope):
            continue
            
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read()
                for p in patterns:
                    if re.search(p, content, re.IGNORECASE):
                        print(f"  [PLACEHOLDER] Placeholder '{p}' found in: {f.relative_to(LLLO_ROOT)}")
                        issue_count += 1
                        break 
        except Exception as e:
            print(f"  [ERROR] Error reading {f.name}: {e}")

    print(f"  Summary: {issue_count} files with placeholders found.")
    return issue_count == 0

def check_atom_integrity(scope=None):
    """Runs content-ko's atom integrity check on gold standards."""
    print(f"--- 3. Atom ID Integrity Check ({scope if scope else 'All'}) ---")
    integrity_script = CONTENT_KO_ROOT / "scripts" / "qa" / "check_atom_extraction_integrity.py"
    
    # Default to A1 if no scope
    search_scope = scope if scope else "A1"
    gold_dir = CONTENT_KO_ROOT / "content" / "gold_standards" / "dialogue" / search_scope
    
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
    parser = argparse.ArgumentParser(description="Lingo Quality Gate Watchdog")
    parser.add_argument("--scope", help="Specific scope to check (e.g., A1, B1)")
    parser.add_argument("--run-id", help="Run ID for traceability")
    args = parser.parse_args()
    
    print(f"=== Lingo Quality Gate Watchdog (ID: {args.run_id or 'manual'}) ===")
    
    success = True
    
    if not check_dict_completeness(args.scope):
        success = False
        
    print()
    if not check_placeholders_in_lllo(args.scope):
        success = False
        
    print()
    if not check_atom_integrity(args.scope):
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
