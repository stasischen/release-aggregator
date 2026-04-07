import re
import argparse
from pathlib import Path

def check_file(path):
    if not Path(path).exists():
        print(f"File not found: {path}")
        return
    
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern to find Korean code blocks/inline code with Chinese characters
    # Example: `사話`
    corrupted_pattern = re.compile(r'`[^`]*[\u4E00-\u9FFF][^`]*`')
    found_any = False
    for i, line in enumerate(lines):
        matches = corrupted_pattern.findall(line)
        if matches:
            found_any = True
            # We want to allow Chinese in translations (which are in parentheses)
            # but NOT inside the backticks which typically represent Korean strings.
            print(f"Line {i+1}: {line.strip()}")
            print(f"  Possible corruption: {matches}")
    if not found_any:
        print(f"No corruption found in {path}")

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

    for target in targets:
        print(f"Checking {target}...")
        check_file(target)
        print("-" * 20)
