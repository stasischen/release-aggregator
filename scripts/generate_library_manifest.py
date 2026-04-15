import os
import json
from pathlib import Path

# Configuration
SCRIPTS_DIR = Path(__file__).resolve().parent
AGGREGATOR_ROOT = SCRIPTS_DIR.parent
CONTENT_KO_ROOT = AGGREGATOR_ROOT.parent / "content-ko"

MOCKUP_DATA_ROOT = AGGREGATOR_ROOT / "docs" / "tasks" / "mockups" / "modular" / "data"
RUNTIME_OUTPUT_DIR = MOCKUP_DATA_ROOT / "runtime" / "zh_tw"

I18N_KNOWLEDGE_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "knowledge"
CORE_KNOWLEDGE_DIR = CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "knowledge"
I18N_SENTENCE_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "learning_library" / "example_sentence"
CORE_SENTENCE_DIR = CONTENT_KO_ROOT / "content" / "core" / "learning_library" / "example_sentence"

OUTPUT_MANIFEST = MOCKUP_DATA_ROOT / "library_manifest.json"
OUTPUT_SENTENCES = MOCKUP_DATA_ROOT / "global_sentences.json"
OUTPUT_RUNTIME_KNOWLEDGE = RUNTIME_OUTPUT_DIR / "knowledge.json"
OUTPUT_RUNTIME_SENTENCES = RUNTIME_OUTPUT_DIR / "example_sentence.json"


def ensure_output_dirs():
    RUNTIME_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_runtime_knowledge():
    runtime_source = CONTENT_KO_ROOT / "runs" / "learning_library_runtime" / "zh_tw" / "knowledge.json"
    if runtime_source.exists():
        try:
            return load_json(runtime_source)
        except Exception as e:
            print(f"Error reading runtime knowledge {runtime_source}: {e}")
    return []

def generate_global_sentences():
    print(f"Aggregating sentences from: {CORE_SENTENCE_DIR}")
    sentences = []

    if not CORE_SENTENCE_DIR.exists():
        print("Sentence core directory not found.")
        write_json(OUTPUT_SENTENCES, sentences)
        write_json(OUTPUT_RUNTIME_SENTENCES, sentences)
        return sentences

    core_map = {}

    for file in CORE_SENTENCE_DIR.glob("*.json"):
        try:
            data = load_json(file)
            sid = data.get("id")
            if sid:
                core_map[sid] = {
                    "id": sid,
                    "ko": data.get("surface_ko") or data.get("ko", ""),
                    "knowledge_refs": data.get("knowledge_refs", []),
                    "level": data.get("level", ""),
                    "tags": data.get("tags", []),
                    "provenance": data.get("provenance", {})
                }
        except Exception as e:
            print(f"Error reading sentence core {file}: {e}")

    if I18N_SENTENCE_DIR.exists():
        for file in I18N_SENTENCE_DIR.glob("*.json"):
            try:
                data = load_json(file)
                sid = data.get("id")
                if sid and sid in core_map:
                    sentences.append({
                        "id": sid,
                        "source": core_map[sid],
                        "i18n": {
                            "id": sid,
                            "locale": "zh_tw",
                            "translation": data.get("translation") or data.get("translation_zh_tw") or data.get("zh_tw", "")
                        }
                    })
            except Exception as e:
                print(f"Error reading sentence i18n {file}: {e}")

    sentences.sort(key=lambda item: item.get("id", ""))
    write_json(OUTPUT_SENTENCES, sentences)
    write_json(OUTPUT_RUNTIME_SENTENCES, sentences)

    print(f"Generated example_sentence runtime with {len(sentences)} items.")
    return sentences

def generate_manifest():
    print(f"Scanning knowledge from: {I18N_KNOWLEDGE_DIR}")
    
    # Ensure output directory exists
    ensure_output_dirs()

    runtime_knowledge = load_runtime_knowledge()
    runtime_index = {item.get("id"): item for item in runtime_knowledge if item.get("id")}
    
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
            
            runtime_item = runtime_index.get(file.replace(".json", "")) or runtime_index.get(Path(file).stem)
            if not runtime_item:
                print(f"Skipping {i18n_path}: no matching runtime knowledge item found.")
                continue

            item_id = runtime_item.get("id")
            core_data = runtime_item.get("source", {})
            i18n_data = runtime_item.get("i18n", {})
            item_title = i18n_data.get("title") or item_id
            metadata = {
                "level": core_data.get("level", "A1"),
                "surface": core_data.get("surface", ""),
                "example_sentence_refs": core_data.get("example_sentence_refs", [])
            }
            
            item_entry = {
                "id": item_id,
                "category": category_id,
                "sub": subcategory_id,
                "title": item_title,
                "level": metadata['level'],
                "path": "data/runtime/zh_tw/knowledge.json",
                "runtime_id": item_id,
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

    all_items.sort(key=lambda item: (
        item.get("category", ""),
        item.get("sub", ""),
        item.get("title", ""),
        item.get("id", "")
    ))

    manifest = {
        "categories": final_categories,
        "featured": all_items[:5],
        "items": all_items
    }

    write_json(OUTPUT_RUNTIME_KNOWLEDGE, runtime_knowledge)
    write_json(OUTPUT_MANIFEST, manifest)
        
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
