import json
import os
import glob
import argparse
import sys

from pathlib import Path

# Define repo root and content-ko path
# Based on layout: f:\Githubs\lingo\release-aggregator\scripts\ops\audit_mixed_script.py
current_dir = Path(__file__).resolve().parent
repo_root = current_dir.parents[1]

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

def run_audit(content_ko_root):
    # Old knowledge paths
    base_knowledge_path = content_ko_root / "content" / "i18n" / "zh_tw" / "learning_library" / "knowledge"
    # New example_sentence bank path
    ex_bank_path = content_ko_root / "content" / "core" / "learning_library" / "example_sentence"
    
    scopes = []
    if base_knowledge_path.exists():
        scopes.extend([
            (base_knowledge_path / "grammar" / "particle", "*.json"),
            (base_knowledge_path / "connector", "**/*.json"),
            (base_knowledge_path / "pattern" / "greetings", "*.json")
        ])
    
    if ex_bank_path.exists():
        scopes.append((ex_bank_path, "*.json"))
    
    all_files = []
    for scope, pattern in scopes:
        if not scope.exists():
            print(f"Warning: Scope path not found: {scope}")
            continue
        files = list(scope.glob(pattern)) if "**" not in pattern else list(scope.rglob(pattern.replace("**/", "")))
        all_files.extend([str(f) for f in files])
    
    print(f"Total files to check: {len(all_files)}")
    if not all_files:
        print("Nothing to audit. Check your content-ko path.")
        return []
    
    audit_results = []
    for path in all_files:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                item_id = data.get("id", "unknown")
                
                # Check old Knowledge item format (example_bank)
                examples = data.get("example_bank", [])
                for i, ex in enumerate(examples):
                    ko_text = ex.get("ko", "")
                    bad = find_corrupted_chars(ko_text)
                    if bad:
                        audit_results.append({
                            "item_id": item_id,
                            "type": "knowledge_ex_bank",
                            "example_index": i,
                            "ko_text": ko_text,
                            "corrupted_chars": list(set(bad))
                        })
                
                # Check new Example Sentence Bank format (surface_ko)
                surface_ko = data.get("surface_ko")
                if surface_ko:
                    bad = find_corrupted_chars(surface_ko)
                    if bad:
                        audit_results.append({
                            "item_id": item_id,
                            "type": "example_sentence_bank",
                            "ko_text": surface_ko,
                            "corrupted_chars": list(set(bad))
                        })
                        
        except Exception as e:
            print(f"Error reading {path}: {e}")
    return audit_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit mixed-script examples in learning_library.")
    parser.add_argument("--content-ko", help="Path to content-ko repo root. Default is sibling path.")
    args = parser.parse_args()

    if args.content_ko:
        ko_root = Path(args.content_ko).resolve()
    else:
        # Default sibling logic
        ko_root = repo_root.parent / "content-ko"
    
    print(f"Auditing using content-ko at: {ko_root}")
    results = run_audit(ko_root)
    
    if results is None:
        sys.exit(1)

    print(f"Audit completed. Found {len(results)} corrupted examples.")
    if results:
        for res in results[:5]: # Print first 5
            print(f"Item: {res['item_id']}, Index: {res['example_index']}, Text: {res['ko_text']}, Bad: {res['corrupted_chars']}")

    # Save to output_path in the current script directory
    output_path = current_dir / "mixed_script_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    if len(results) > 0:
        print("ERROR: Corrupted examples found.")
        sys.exit(1)
    else:
        print("SUCCESS: Audit passed cleanly.")
        sys.exit(0)
