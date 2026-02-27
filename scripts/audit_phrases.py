import os
import json
from pathlib import Path

CONTENT_KO_ROOT = Path("f:/Githubs/lingo/content-ko")
MAPPING_PHRASE = CONTENT_KO_ROOT / "content" / "mappings" / "mapping_phrase.json"
CORE_ATOMS_DIR = CONTENT_KO_ROOT / "content" / "core" / "dictionary" / "atoms"
I18N_DICTS_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "dictionary"

with open(MAPPING_PHRASE, "r", encoding="utf-8") as f:
    mapping = json.load(f)

phrases_to_create = []

for surface, phrase_id in mapping.items():
    lemma = phrase_id.split(":")[-1]
    fs_safe_id = phrase_id.replace(":", "__")
    
    core_file = CORE_ATOMS_DIR / "PHRASE" / f"{fs_safe_id}.json"
    i18n_file = I18N_DICTS_DIR / f"{fs_safe_id}.json"
    
    if not core_file.exists() or not i18n_file.exists():
        phrases_to_create.append({"surface": surface, "id": phrase_id, "core": core_file, "i18n": i18n_file})

print(f"Found {len(phrases_to_create)} missing or incomplete phrases.")
for p in phrases_to_create:
    print(f"- {p['surface']} ({p['id']})")
