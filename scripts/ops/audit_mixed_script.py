import json
import os
import glob

from pathlib import Path

# Define repo root and content-ko path
# Based on layout: f:\Githubs\lingo\release-aggregator\scripts\ops\audit_mixed_script.py
current_dir = Path(__file__).resolve().parent
repo_root = current_dir.parents[1]
# content-ko is expected to be a sibling of the current repo (release-aggregator)
content_ko_root = repo_root.parent / "content-ko"

base_path = content_ko_root / "content" / "i18n" / "zh_tw" / "learning_library" / "knowledge"

scopes = [
    (base_path / "grammar" / "particle", "*.json"),
    (base_path / "connector", "**/*.json"),
    (base_path / "pattern" / "greetings", "*.json")
]

all_files = []
for scope, pattern in scopes:
    files = list(scope.glob(pattern)) if "**" not in pattern else list(scope.rglob(pattern.replace("**/", "")))
    all_files.extend([str(f) for f in files])

print(f"Total files to check: {len(all_files)}")

results = []

def find_corrupted_chars(text):
    bad_chars = []
    for char in text:
        # Hangul Syllables
        if '\uAC00' <= char <= '\uD7A3': continue
        # Hangul Jamo
        if '\u1100' <= char <= '\u11FF': continue
        if '\u3130' <= char <= '\u318F': continue
        # ASCII
        if '\u0020' <= char <= '\u007E': continue
        # Common Full Width CJK punctuation
        if char in '，。！？：；（）“”』『【】—「」…、': continue
        
        # If it's a Chinese character, it's a bad char for "ko" string in example bank
        if '\u4E00' <= char <= '\u9FFF':
            bad_chars.append(char)
        elif ord(char) > 0x7E: # Any non-ASCII non-Hangul non-CJK Punctuation
             bad_chars.append(char)
    return bad_chars

for path in all_files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            item_id = data.get("id", "unknown")
            examples = data.get("example_bank", [])
            for i, ex in enumerate(examples):
                ko_text = ex.get("ko", "")
                bad = find_corrupted_chars(ko_text)
                if bad:
                    results.append({
                        "item_id": item_id,
                        "example_index": i,
                        "ko_text": ko_text,
                        "corrupted_chars": list(set(bad))
                    })
    except Exception as e:
        print(f"Error reading {path}: {e}")

print(f"Audit completed. Found {len(results)} corrupted examples.")
if results:
    for res in results[:5]: # Print first 5
        print(f"Item: {res['item_id']}, Index: {res['example_index']}, Text: {res['ko_text']}, Bad: {res['corrupted_chars']}")

# Save to output_path in the current script directory
output_path = current_dir / "mixed_script_results.json"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
