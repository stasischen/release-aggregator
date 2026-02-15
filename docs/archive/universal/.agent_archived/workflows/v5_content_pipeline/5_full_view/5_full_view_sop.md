---
description: Phase 5 SOP: Full View Merge & Content QA
---
# Phase 5: Build & Deployment (SOP)

This phase compiles the verified content into the final **V5 Game Asset Format**.
Unlike V4, this format is **Self-Contained** (Language Packs), meaning all dictionary definitions are embedded directly into the lesson files to reduce runtime dependency.

## 1. 📚 Linguistic Standards (語言標準)

各語言的具體審查標準（敬語、語法、常見錯誤）請參閱以下專家工作流：
Refer to the expert workflows below for specific language standards (honorifics, grammar, common errors):

- **Korean (KO)**: `[[../../linguistics/audit_ko_content.md]]`
- **Thai (TH)**: `[[../../linguistics/audit_th_content.md]]`
- **German (DE)**: `[[../../linguistics/audit_de_content.md]]`

## 2. V5 Game Data Schema (New Structure)

Each output file (`.json`) represents a **Course Unit** (Lesson).

```json
{
  "meta": {
    "id": "lesson_01",
    "version": "5.0",
    "source_lang": "ko",
    "target_lang": "en" // If building for specific locale, or "universal" if contains all
  },
  "content": [
    {
      "line_id": "l0_sample_001",
      "speaker": "Lisa",
      "text": {
        "source": "안녕하세요!",
        "en": "Hello!",
        "zh_TW": "你好！"
      },
      "chunks": [
        {
          "id": "de_PHRASE_tomaten_auf_den_augen",
          "surface": "Tomaten auf den Augen",
          "trans": "視而不見 (Blind to obvious things)",
          "note": "Originally refers to having tomatoes solely... (Long text)",
          "atom_indices": [3, 4, 5, 6],
          "ui_type": "idiom"
        }
      ],
      "atoms": [
        {
          "surface": "안녕하세요",
          "id": "ko_INTJ_hello",
          "pos": "INTJ",
          "dict": {
            "lemma": "안녕하세요",
            "trans_en": "Hello",
            "trans_zh_TW": "你好",
            "note": "Greeting used at any time of day",
            "examples": "안녕하세요! 잘 지내시나요?"
          }
        }
      ]
    }
  ]
}
```

## 3. Workflow (工作流程)

### Step 1: Merger (Prepare Source)

Input: `1_translation/*.csv` + `2_atoms/*.csv`
Output: `5_full_view/*.csv`
Command: `python -m tools.v5.core.merger {lang}`

### Step 2: Linguist QA (Strict Multi-Lang Audit)

**Target**: `5_full_view/*.csv` (Source of Truth)
**Tool**: `audit_view` (Supports dynamic dictionary join and bulk scanning)

**⚠️ MANDATORY POLICY**:

- **No Skip Policy**: Every language (EN, ZH_TW, JA, KO, RU) MUST be reviewed.
- **Report Policy**: A progress table `audit_reports/{lang}_audit_report.md` MUST be maintained.
- **Green Status**: A file is only 🟢 (Verified) after a HUMAN reads it in ALL target languages.

#### A. Automated Validation (Foundation)

Before manual reading, run automated scans to catch syntax and dictionary gaps.

```bash
# 1. Dictionary & Translation Presence Scan (Run for EVERY target lang)
# Syntax: python -m tools.v5.5_build.audit_view <dir> <target_lang> --scan
python -m tools.v5.5_build.audit_view lingostory_universal/content/5_full_view/th zh_TW --scan
```

- **If Red flags (❌/⚠️):** Stop. Go to Feedback Loop to fix Dictionary or Translation source.
- **Check for Column Corruption**: Open the CSV. If you see text leaking across columns (e.g., Russian in the English column), it's likely a CSV quoting error. **Fix source quoting immediately.**

#### B. Manual Semantic Audit (The Cross-Check)

You MUST cross-reference the **Source Text**, **Sentence Translation**, and **Atom Definition** for every language.

```bash
# Verify specific language
python -m tools.v5.5_build.audit_view lingostory_universal/content/5_full_view/th/{file}.csv {lang}
```

**Verification Checklist**:

1. **Semantic Match**: Does the sentence translation align with the _Atoms_ displayed?
    - If Source is `[V] Eat` but Translation is `Go`, it's a hallucination.
2. **Tag Consistency**: Are tags like `{$player_name}` or `{$th_me}` preserved?
    - _Note_: Dropping `{$th_end}` is often acceptable for subtitle clarity if the meaning is preserved.
3. **Speaker Accuracy**: Does the tone (polite/casual) match the Speaker ID?
4. **Cultural/Slang Checks**: Are culture-specific terms (e.g., `Wai`, `7-Eleven services`) translated correctly, not just literally?
5. **Segmentation Hygiene**: Are atoms cut at logical linguistic boundaries?
    - _Bad_: `[ADJ] ThaiOne`. _Good_: `[ADJ] Thai` + `[DET] One`.

#### C. Reporting & Accountability

Create or update `audit_reports/{lang}_audit_report.md` with the following structure:

| File Name       | EN  | ZH_TW | JA  | KO  | RU  | Verification Notes                        |
| :-------------- | :-: | :---: | :-: | :-: | :-: | :---------------------------------------- |
| `demo_file.csv` | 🟢  |  🟢   | 🟡  | 🟢  | 🟡  | 🟢 = Human Reviewed, 🟡 = Only Scan Pass. |

**Feedback Loop (How to Fix)**:

- **Translation Error**: Edit `1_translation/{lang}/{file}.csv`.
- **Segmentation/Atom Error**: Edit `2_atoms/{lang}/{file}.csv` -> Fix `atoms_json`.
- **Dictionary Error**: Edit `4_dictionary/{lang}/*.csv`.
- **After Edit**: Re-run `merger` to regenerate Full View before re-auditing.

### Step 3: Proceed to Build (Phase 8)

Once QA is complete, proceed to the Build Phase.
See: `[[../8_staging/SOP.md]]`

## 4. Final Audit Checklist (Pre-Build)

Before moving to **Phase 8 (Build Staging)**, the Agent must confirm:

### 🗺️ Coverage & Accountability

- [ ] **Multi-Language Verification**: Every target language (EN, ZH_TW, JA, KO, RU) has a corresponding 🟢 status in the audit report.
- [ ] **Audit Report Sync**: `audit_reports/{lang}_audit_report.md` is created and accurately reflects the current state.
- [ ] **Bulk Scan Pass**: `python -m tools.v5.5_build.audit_view <dir> <lang> --scan` returns **ZERO** MISSING or TODO items for ALL languages.

### 🗣️ Linguistic & Semantic Quality

- [ ] **Atomic Alignment**: The sentence translation semantically matches the definitions of its component Atoms.
- [ ] **Contextual Accuracy**: Cultural nuances (e.g., Thai `Wai`, 7-11 services, honorifics) are localized, not just literally translated.
- [ ] **Tag Integrity**: Critical tags (e.g., `{$player_name}`, `{$npc_name}`) are preserved across all languages.
- [ ] **Speaker Tone**: Politeness levels and gender-specific particles match the Speaker ID.

### 🛠️ Technical Data Integrity

- [ ] **CSV Hygiene**: No "Column Leaking" caused by unquoted commas in translations.
- [ ] **Dictionary Mapping**: All Atom IDs in `2_atoms` have a corresponding entry in `4_dictionary`.
- [ ] **No Placeholders**: Zero `[TODO]` or `MISSING` strings in any translation column.
