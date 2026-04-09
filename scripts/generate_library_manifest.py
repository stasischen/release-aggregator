import os
import json
import shutil
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path(__file__).resolve().parent
AGGREGATOR_ROOT = SCRIPTS_DIR.parent
CONTENT_KO_ROOT = AGGREGATOR_ROOT.parent / "content-ko"

MOCKUP_DATA_ROOT = AGGREGATOR_ROOT / "docs" / "tasks" / "mockups" / "modular" / "data"

I18N_KNOWLEDGE_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "knowledge"
CORE_KNOWLEDGE_DIR = CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "knowledge"
I18N_SENTENCE_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "example_sentence"
CORE_SENTENCE_DIR = CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "example_sentence"

OUTPUT_LIBRARY_DIR = MOCKUP_DATA_ROOT / "library"
OUTPUT_MANIFEST = MOCKUP_DATA_ROOT / "library_manifest.json"
OUTPUT_SENTENCES = MOCKUP_DATA_ROOT / "global_sentences.json"

def generate_global_sentences():
    print(f"Aggregating sentences from: {CORE_SENTENCE_DIR}")
    sentences = {}
    
    if not CORE_SENTENCE_DIR.exists():
        print("Sentence core directory not found.")
        return sentences

    # Load core sentences
    for file in CORE_SENTENCE_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                sid = data.get("id")
                if sid:
                    sentences[sid] = {
                        "id": sid,
                        "ko": data.get("surface_ko") or data.get("ko", ""),
                        "knowledge_refs": data.get("knowledge_refs", [])
                    }
        except Exception as e:
            print(f"Error reading sentence core {file}: {e}")

    # Load i18n translations
    if I18N_SENTENCE_DIR.exists():
        for file in I18N_SENTENCE_DIR.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sid = data.get("id")
                    if sid in sentences:
                        sentences[sid]["zh_tw"] = data.get("translation_zh_tw") or data.get("zh_tw", "")
            except Exception as e:
                print(f"Error reading sentence i18n {file}: {e}")

    with open(OUTPUT_SENTENCES, "w", encoding="utf-8") as f:
        json.dump(sentences, f, ensure_ascii=False, indent=2)
    
    print(f"Generated global_sentences.json with {len(sentences)} items.")
    return sentences

def generate_manifest():
    print(f"Scanning knowledge from: {I18N_KNOWLEDGE_DIR}")
    
    # Ensure output directory exists
    OUTPUT_LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    
    categories_tree = {}
    all_items = []
    
    # Walk through i18n directory
    for root, dirs, files in os.walk(I18N_KNOWLEDGE_DIR):
        for file in files:
            if not file.endswith(".json"):
                continue
                
            i18n_path = Path(root) / file
            rel_path = i18n_path.relative_to(I18N_KNOWLEDGE_DIR)
            
            # rel_path format: category/subcategory/filename.json or category/filename.json
            parts = rel_path.parts
            if len(parts) < 2:
                continue # Skip top-level files if any
                
            category_id = parts[0]
            subcategory_id = parts[1] if len(parts) > 2 else "general"
            
            # Load I18N content
            try:
                with open(i18n_path, "r", encoding="utf-8") as f:
                    i18n_data = json.load(f)
            except Exception as e:
                print(f"Error reading {i18n_path}: {e}")
                continue
                
            # Load Core content for metadata
            core_path = CORE_KNOWLEDGE_DIR / rel_path
            metadata = {
                "level": "A1",
                "surface": "",
                "example_sentence_refs": []
            }
            if core_path.exists():
                try:
                    with open(core_path, "r", encoding="utf-8") as f:
                        core_data = json.load(f)
                        metadata['level'] = core_data.get('level', 'A1')
                        metadata['surface'] = core_data.get('surface', '')
                        metadata['example_sentence_refs'] = core_data.get('example_sentence_refs', [])
                except Exception as e:
                    print(f"Error reading core {core_path}: {e}")
            
            item_id = i18n_data.get("id", file.replace(".json", ""))
            item_title = i18n_data.get("title_zh_tw", item_id)
            
            # Sync file to mockup
            target_path = OUTPUT_LIBRARY_DIR / file
            shutil.copy2(i18n_path, target_path)
            
            item_entry = {
                "id": item_id,
                "category": category_id,
                "sub": subcategory_id,
                "title": item_title,
                "level": metadata['level'],
                "path": f"data/library/{file}",
                "surface": metadata['surface'],
                "example_sentence_refs": metadata['example_sentence_refs']
            }
            
            all_items.append(item_entry)
            
            # Build category structure
            if category_id not in categories_tree:
                categories_tree[category_id] = {
                    "id": category_id,
                    "title": category_id.capitalize(),
                    "sub_map": {}
                }
            
            if subcategory_id not in categories_tree[category_id]["sub_map"]:
                categories_tree[category_id]["sub_map"][subcategory_id] = {
                    "id": subcategory_id,
                    "title": subcategory_id.capitalize(),
                    "items": []
                }
            
            categories_tree[category_id]["sub_map"][subcategory_id]["items"].append(item_entry)

    # Convert tree to final format
    final_categories = []
    # Sort categories to keep grammar first if possible
    sorted_cat_keys = sorted(categories_tree.keys(), key=lambda x: (x != 'grammar', x != 'pattern', x))
    
    for c_id in sorted_cat_keys:
        cat = categories_tree[c_id]
        sub_list = []
        for s_id in sorted(cat["sub_map"].keys()):
            sub_list.append({
                "id": s_id,
                "title": cat["sub_map"][s_id]["title"]
            })
        
        final_categories.append({
            "id": c_id,
            "title": self_map_cat_title(c_id),
            "sub": sub_list
        })

    manifest = {
        "categories": final_categories,
        "featured": all_items[:5],
        "items": all_items
    }

    with open(OUTPUT_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
        
    print(f"Generated manifest with {len(all_items)} items.")

def self_map_cat_title(cid):
    mapping = {
        "grammar": "韓文法 (Grammar)",
        "pattern": "必修句型 (Patterns)",
        "connector": "連接詞 (Connectors)",
        "expression": "慣用語 (Expressions)"
    }
    return mapping.get(cid, cid.capitalize())

if __name__ == "__main__":
    generate_global_sentences()
    generate_manifest()
