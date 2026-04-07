import re
import argparse
import sys
from pathlib import Path

def check_file(path):
    if not Path(path).exists():
        print(f"File not found: {path}")
        return False
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 1. Catch Korean code blocks/inline code with Chinese characters. Example: `사話`
    backtick_corruption = re.compile(r'`[^`]*[\u4E00-\u9FFF][^`]*`')
    
    # 2. Catch Hangul and Hanja directly adjacent (unseparated). Example: `통化`
    unseparated_mixed = re.compile(r'[\uAC00-\uD7A3][\u4E00-\u9FFF]|[\u4E00-\u9FFF][\uAC00-\uD7A3]')
    
    # 3. Catch Korean sentences not isolated in backticks (heuristic but effective for these reports)
    # This looks for Hangul blocks longer than 2 words that aren't inside backticks
    # (Matches Hangul and spaces, NOT starting with a backtick on the line before)
    # However, to be safe, we'll start with the most obvious adjacencies.
    
    found_any = False
    for i, line in enumerate(lines):
        # Existing backtick check
        matches = backtick_corruption.findall(line)
        if matches:
            found_any = True
            print(f"Line {i+1}: Mixed-script in backticks: {matches}")
        
        # New adjacency check (even if not in backticks)
        mixed_matches = unseparated_mixed.findall(line)
        if mixed_matches:
            found_any = True
            print(f"Line {i+1}: Unseparated mixed-script: {mixed_matches}")

    if not found_any:
        print(f"No corruption found in {path}")
    return found_any

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit markdown reports for mixed-script corruption.")
    parser.add_argument("files", nargs="*", help="Optional list of files to check.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    
    if args.files:
        targets = args.files
    else:
        # Default targets
        targets = [
            repo_root / "docs" / "tasks" / "KNOWLEDGE_LAB_ENRICHMENT_PILOT_EXTRACTION_NOTE.md",
            repo_root / "docs" / "tasks" / "KNOWLEDGE_LAB_ENRICHMENT_EXTRACT_READY_MANIFEST.md"
        ]

    any_fail = False
    for target in targets:
        print(f"Checking {target}...")
        if check_file(target):
            any_fail = True
        print("-" * 20)

    if any_fail:
        print("ERROR: Corruption detected. Please fix reports.")
        sys.exit(1)
    else:
        print("SUCCESS: All reports verified.")
        sys.exit(0)
