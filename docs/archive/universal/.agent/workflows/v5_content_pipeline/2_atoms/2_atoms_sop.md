---
description: Phase 2 SOP: Atoms Rectification & Fidelity Verification (V5 Standard)
---
# Phase 2 Atoms SOP

**Dependencies**: Phase 1 Translation MUTS be marked `PASSED` in `audit_report_p1.md`.

## 🛡️ Pre-flight Check (開工門禁)
- **Batch Limit**: Audit in chunks of **10-15 lines**. Pause for review.
- **Quote Evidence**: Always quote (Before -> After) in report.
- **Git Clean**: Ensure clean `git status` before patching.

## 📚 Linguistic & Architectural Standards

### 1. Perfect Reconstruction Rule (完美還原)
- **Rule**: `Concatenated Atoms == Source Text` (including spaces/punct).
- **Goal**: 100% UI rendering accuracy.

### 2. Space Management (空格管理)
- **Langs**: DE, EN, KO, TH.
- **Format**: ID=`{lang}_SPACE`, Text=`" "`, POS=`SPACE`.

### 3. Dual-Layer POS (雙層詞性)

| Category | V5 Tag (Teaching) | UD Tag (Universal) | Note |
| :--- | :--- | :--- | :--- |
| **Core** | `V`, `ADJ`, `AUX` | `VERB`, `ADJ` | Content words. |
| **Lexical** | `N`, `PROP`, `NUM` | `NOUN`, `PROPN` | Dictionary entries. |
| **Literal** | `XNUM`, `TAG` | `NUM`, `X` | Numbers/Variables. |
| **Structural** | `P`, `E`, `M` | `ADP`, `PART` | Particles/Affixes. |
| **Layout** | `PUNCT`, `SPACE` | `PUNCT` | Rendering only. |

### Atom JSON Data Contract
| Field | Description | Example |
| :--- | :--- | :--- |
| `id` | `lang_POS_lemma` (Use `+` for compound) | `ko_N_그림+ko_P_보다` |
| `text` | Exact source substring | `그림보다` |
| `pos` | Teaching POS | `ADJ` |
| `upos` | Universal POS | `VERB` |

## 🛡️ Language Specific Rules
### Thai (TH)
- **No Style**: No `+` merging (except technical tags).
- **Preserve Spaces**: Respect author's spacing strictly.

## 🚀 Workflow (執行流程)

### 1. Validation & Integrity (自動驗證)

```bash
# 1. Check Perfect Reconstruction
python -m tools.v5.2_atoms.validation {lang}

# 2. Check P1/P2 Sync & Columns
python tools/v5/qa/integrity_guard_universal.py {lang}
```

### 2. Content Audit (內容審查)
- **Action**: Verify `atoms_json` logic (German separable verbs, Korean particles).
- **Repair**: Use `tools/v5/repair/patch_{lang}.py`. **No manual CSV edits.**

## 3. Handover
- **Sign-off**: Mark `DATA INTEGRITY: 🟢 PASSED` in `1_translation/{lang}/audit_report_{lang}_p2.md`.
- **Next Step**: Read [Phase 3 Mapping SOP](../3_mapping/3_mapping_sop.md).
