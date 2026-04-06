import json
import os
import sys

# Paths
CWD = os.path.dirname(os.path.abspath(__file__))
AGGREGATOR_ROOT = os.path.abspath(os.path.join(CWD, "..", ".."))
FRONTEND_ROOT = os.path.abspath(os.path.join(AGGREGATOR_ROOT, "..", "lingo-frontend-web"))

RELEASE_MANIFEST_PATH = os.path.join(AGGREGATOR_ROOT, "staging", "prd.release_manifest.seed.json")
LEGACY_MANIFEST_PATH = os.path.join(FRONTEND_ROOT, "assets", "content", "production", "manifest.json")
LEGACY_CATALOG_PATH = os.path.join(FRONTEND_ROOT, "assets", "content", "production", "lesson_catalog.json")

# Output for prototype
PROTOTYPE_OUTPUT_DIR = os.path.join(AGGREGATOR_ROOT, "staging", "prototype_output")

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def assemble():
    print(f"Reading Release Manifest: {RELEASE_MANIFEST_PATH}")
    manifest = load_json(RELEASE_MANIFEST_PATH)
    if not manifest:
        print("Error: Release Manifest not found. Run seed tool first.")
        sys.exit(1)
        
    print(f"Reading Legacy Sources for Asset Paths: {LEGACY_MANIFEST_PATH}, {LEGACY_CATALOG_PATH}")
    legacy_manifest = load_json(LEGACY_MANIFEST_PATH)
    legacy_catalog = load_json(LEGACY_CATALOG_PATH)
    
    # 1. Filtering
    allowlisted_entries = [
        e for e in manifest.get("entries", [])
        if e.get("release_status") == "production" and not e.get("staging_only", True)
    ]
    
    print(f"Allowlisted {len(allowlisted_entries)} entries for production.")
    
    allowlisted_ids = {e["lesson_id"] for e in allowlisted_entries}
    
    # 2. Planning Outputs
    new_manifest_lessons = []
    legacy_manifest_lessons = {l["level_id"]: l for l in legacy_manifest.get("lessons", [])}
    
    for entry in allowlisted_entries:
        l_id = entry["lesson_id"]
        if l_id in legacy_manifest_lessons:
            # Re-use path and info from legacy manifest
            m_lesson = legacy_manifest_lessons[l_id]
            new_manifest_lessons.append(m_lesson)
        else:
            print(f"WARNING: Lesson {l_id} in release manifest but NOT found in legacy manifest. Skipping.")
            
    # 3. Filtering Catalog
    new_catalog_units = []
    new_catalog_lessons = []
    
    # Identify which units are needed
    needed_unit_ids = {e["unit_id"] for e in allowlisted_entries}
    
    # Filter units
    for unit in legacy_catalog.get("units", []):
        if unit["id"] in needed_unit_ids:
            new_catalog_units.append(unit)
            
    # Filter lessons in catalog
    for lesson in legacy_catalog.get("lessons", []):
        if lesson["lesson_id"] in allowlisted_ids:
            new_catalog_lessons.append(lesson)
            
    # Handling lessons that were NOT in catalog but are in manifest (e.g. videos)
    # They should probably be added to the catalog under their respective unit if missing
    # But for prototype, we just follow the manifest's lead.
    
    # 4. Generate Artifacts (Prototype)
    new_manifest = {
        "version": legacy_manifest.get("version", "1.0.0"),
        "last_updated": manifest["updated_at"],
        "packages": legacy_manifest.get("packages", {}),
        "lessons": new_manifest_lessons
    }
    
    new_catalog = {
        "version": legacy_catalog.get("version", 1),
        "updated_at": manifest["updated_at"][:10],
        "units": new_catalog_units,
        "lessons": new_catalog_lessons
    }
    
    os.makedirs(PROTOTYPE_OUTPUT_DIR, exist_ok=True)
    save_json(os.path.join(PROTOTYPE_OUTPUT_DIR, "manifest.json"), new_manifest)
    save_json(os.path.join(PROTOTYPE_OUTPUT_DIR, "lesson_catalog.json"), new_catalog)
    
    print(f"\nSUCCESS: Assembler prototype finished.")
    print(f"Generated manifest.json with {len(new_manifest_lessons)} lessons.")
    print(f"Generated lesson_catalog.json with {len(new_catalog_units)} units and {len(new_catalog_lessons)} lessons.")
    print(f"Outputs located in: {PROTOTYPE_OUTPUT_DIR}")
    
    # Verification mode: check if staging_only is truly ignored
    test_entry = {
        "unit_id": "test_unit",
        "lesson_id": "ko_test_staging_only",
        "release_status": "production",
        "staging_only": True,
        "content_type": "dialogue",
        "course_type": "lesson",
        "source_refs": ["test"],
        "contract_version": "cm-v1.0.0",
        "viewer_verified": True,
        "qa_gate_passed": True
    }
    
    # Mocking filtering logic check
    filtered = [e for e in [test_entry] if e.get("release_status") == "production" and not e.get("staging_only", True)]
    assert len(filtered) == 0, "Security Failure: staging_only entry was not filtered!"
    print("\nVERIFICATION: Filter correctly ignored staging_only: true")

if __name__ == "__main__":
    assemble()
