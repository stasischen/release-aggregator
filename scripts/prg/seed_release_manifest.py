import json
import os
from datetime import datetime

# Paths
CWD = os.path.dirname(os.path.abspath(__file__))
AGGREGATOR_ROOT = os.path.abspath(os.path.join(CWD, "..", ".."))
FRONTEND_ROOT = os.path.abspath(os.path.join(AGGREGATOR_ROOT, "..", "lingo-frontend-web"))

MANIFEST_PATH = os.path.join(FRONTEND_ROOT, "assets", "content", "production", "manifest.json")
CATALOG_PATH = os.path.join(FRONTEND_ROOT, "assets", "content", "production", "lesson_catalog.json")
OUTPUT_PATH = os.path.join(AGGREGATOR_ROOT, "staging", "prd.release_manifest.seed.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def seed():
    print(f"Loading manifest from {MANIFEST_PATH}")
    manifest_data = load_json(MANIFEST_PATH)
    
    print(f"Loading catalog from {CATALOG_PATH}")
    catalog_data = load_json(CATALOG_PATH)
    
    # Index catalog by lesson_id
    catalog_lessons = {l["lesson_id"]: l for l in catalog_data.get("lessons", [])}
    
    entries = []
    reconciliation_needed = []
    
    for m_lesson in manifest_data.get("lessons", []):
        lesson_id = m_lesson["level_id"]
        c_lesson = catalog_lessons.get(lesson_id)
        
        # Determine content_type
        content_type = m_lesson.get("type", "dialogue")
        if content_type == "yarn": # Some might be 'yarn' in internal paths but 'dialogue' in manifest
            content_type = "dialogue"
        
        # Map content_type to allowed Enums
        # dialogue, video, article, grammar-heavy
        type_mapping = {
            "video": "video",
            "dialogue": "dialogue",
            "article": "article",
            "yarn": "dialogue"
        }
        content_type = type_mapping.get(content_type, "dialogue")
        
        # Determine course_type
        # lesson, bonus, supplemental
        course_type = m_lesson.get("category", "lesson")
        if course_type not in ["lesson", "bonus", "supplemental"]:
            course_type = "lesson"
            
        # Determine unit_id
        unit_id = "unknown_unit"
        if c_lesson:
            unit_id = c_lesson.get("unit_id", "unknown_unit")
        elif content_type == "video":
            unit_id = "bonus_video" # Default for old videos
            
        if unit_id == "unknown_unit":
            reconciliation_needed.append(lesson_id)
            
        # source_refs
        # For now, use the lesson_id as the primary source ref
        source_refs = [lesson_id]
        
        entry = {
            "unit_id": unit_id,
            "lesson_id": lesson_id,
            "release_status": "production",
            "content_type": content_type,
            "course_type": course_type,
            "source_refs": source_refs,
            "contract_version": "cm-v1.0.0",
            "viewer_verified": True,
            "qa_gate_passed": True,
            "staging_only": False,
            "notes": f"Initial seed from legacy production assets. Original title: {m_lesson.get('title', {}).get('ko', 'N/A')}"
        }
        entries.append(entry)
        
    # Output reconciliation warnings
    if reconciliation_needed:
        print(f"\nWARNING: {len(reconciliation_needed)} lessons found in manifest but missing from catalog (no unit_id):")
        for rid in reconciliation_needed[:10]:
            print(f"  - {rid}")
        if len(reconciliation_needed) > 10:
            print(f"  ... and {len(reconciliation_needed)-10} more")
            
    # Check for lessons in catalog but not in manifest
    not_in_manifest = []
    manifest_ids = {l["level_id"] for l in manifest_data.get("lessons", [])}
    for l_id in catalog_lessons:
        if l_id not in manifest_ids:
            not_in_manifest.append(l_id)
            
    if not_in_manifest:
        print(f"\nINFO: {len(not_in_manifest)} lessons found in catalog but NOT in manifest (will NOT be in production):")
        for nid in not_in_manifest[:10]:
            print(f"  - {nid}")
        if len(not_in_manifest) > 10:
            print(f"  ... and {len(not_in_manifest)-10} more")

    # Construct final manifest
    result = {
        "version": "1.0.0",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "entries": entries
    }
    
    save_json(OUTPUT_PATH, result)
    print(f"\nSUCCESS: Generated release manifest with {len(entries)} entries at {OUTPUT_PATH}")

if __name__ == "__main__":
    seed()
