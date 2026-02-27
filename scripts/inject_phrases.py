import os
import json
from pathlib import Path

CONTENT_KO_ROOT = Path("f:/Githubs/lingo/content-ko")
MAPPING_PHRASE = CONTENT_KO_ROOT / "content" / "mappings" / "mapping_phrase.json"
CORE_ATOMS_DIR = CONTENT_KO_ROOT / "content" / "core" / "dictionary" / "atoms"
I18N_DICTS_DIR = CONTENT_KO_ROOT / "content" / "i18n" / "zh_tw" / "dictionary"

PHRASE_DATA = {
    "안녕하세요": ["你好/您好"],
    "반가워요": ["很高興見到你"],
    "반갑습니다": ["很高興見到你 (正式)"],
    "감사합니다": ["謝謝"],
    "고마워요": ["謝謝/謝了"],
    "실례합니다": ["對不起/打擾了/借過"],
    "다행이네요": ["那太好了/太幸運了"],
    "정말요": ["真的嗎？"],
    "알겠어요": ["我知道了/明白了"],
    "물론이죠": ["當然/沒錯"],
    "그렇군요": ["原來如此/這樣啊"],
    "그렇죠": ["對呀/就是說嘛"]
}

if not MAPPING_PHRASE.exists():
    print(f"Error: {MAPPING_PHRASE} not found.")
    exit(1)

with open(MAPPING_PHRASE, "r", encoding="utf-8") as f:
    mapping = json.load(f)

# Ensure Directories
(CORE_ATOMS_DIR / "PHRASE").mkdir(parents=True, exist_ok=True)
I18N_DICTS_DIR.mkdir(parents=True, exist_ok=True)

for surface, phrase_id in mapping.items():
    lemma = phrase_id.split(":")[-1]
    fs_safe_id = phrase_id.replace(":", "__")
    
    core_file = CORE_ATOMS_DIR / "PHRASE" / f"{fs_safe_id}.json"
    i18n_file = I18N_DICTS_DIR / f"{fs_safe_id}.json"
    
    # Core Atom
    core_data = {
        "atom_id": phrase_id,
        "lemma_id": lemma,
        "surface_forms": [lemma],
        "pos": "PHRASE",
        "senses": [{"definition_ref": "base", "labels": []}],
        "source_refs": ["system:phrase_injection"],
        "upos": "PHRASE"
    }
    
    with open(core_file, "w", encoding="utf-8") as f:
        json.dump(core_data, f, ensure_ascii=False, indent=2)
        
    # I18n Atom
    i18n_data = {
        "atom_id": phrase_id,
        "learner_lang": "zh_tw",
        "headword": lemma,
        "pos": "PHRASE",
        "definitions": {"zh_tw": PHRASE_DATA.get(lemma, [""])}
    }
    
    with open(i18n_file, "w", encoding="utf-8") as f:
        json.dump(i18n_data, f, ensure_ascii=False, indent=2)

print("✅ Injected phrase atoms.")

# Cleanup/Migration
for p in ["감사합니다"]:
    old_core = CORE_ATOMS_DIR / "N" / f"ko__n__{p}.json"
    old_i18n = I18N_DICTS_DIR / f"ko__n__{p}.json"
    if old_core.exists():
        old_core.unlink()
        print(f"🗑️ Removed old core: {old_core}")
    if old_i18n.exists():
        old_i18n.unlink()
        print(f"🗑️ Removed old i18n: {old_i18n}")

# Update Gold Standards
C1_21 = CONTENT_KO_ROOT / "content" / "gold_standards" / "dialogue" / "C1" / "C1-21.jsonl"
if C1_21.exists():
    with open(C1_21, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    updated = False
    for line in lines:
        if "ko:n:감사합니다" in line:
            line = line.replace("ko:n:감사합니다", "ko:phrase:감사합니다")
            updated = True
        new_lines.append(line)
    
    if updated:
        with open(C1_21, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"📝 Updated gold standard: {C1_21}")
