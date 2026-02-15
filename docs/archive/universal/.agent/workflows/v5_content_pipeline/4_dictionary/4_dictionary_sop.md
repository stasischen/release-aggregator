---
description: Phase 4 SOP: Dictionary Build, Sync & Enrichment
---
# Phase 4 Dictionary SOP

**Dependencies**: Phase 3 Mapping must be complete.

## 🎯 Objectives
1. **Alignment**: Every atom has `lemma`, `pos`, `definition`.
2. **Enrichment**: Add `note` and `examples`.
3. **Scale**: Populate ALL 6 target languages.

## 🛠️ Execution

### Step 0: Legacy Isolation
**Goal**: Isolate orphaned IDs before sync.
```bash
python tools/v5/4_dictionary/isolate_legacy.py {lang}
```
- **Action**: Check `_legacy_migration.csv`. Use it to patch renames, then keep as backup.

### Step 1: Sync & Audit
**Goal**: Create new entries without overwriting.
```bash
python -m tools.v5.core.sync {lang}
```
- **Files**:
  - `lingoblocks_core.csv`: Verbs, ADJs (Lexical).
  - `lingoblocks_noun.csv`: Nouns.
  - `lingoblocks_func.csv`: Structural particles.
  - `lingoblocks_others.csv`: **BUFFER ONLY**. Exclude from translation.
- **Fail Condition**: If sync blocked by `UNK/WORD`, go back to Phase 2.

### Step 2: Linguistic Audit
**Goal**: Verify Lemma/POS accuracy.
- **Korean Rule**: Verbs/ADJs must end in `-다`.
- **System**: Align POS tags with `chunk_system_spec.md`.

### Step 3: Enrichment Loop
**Goal**: Creative translation and context.
- **Loop**: `zh_TW` -> `en` -> `ja` -> etc.
- **Idioms**: Edit `1_translation/{lang}/idioms_source.csv` only. Sync will propagate.
- **Assets**: Use `lingoblocks_assets.csv` for pure grammar notes (No examples).

## 🛡️ Data Contract

| Column | Standard | Note |
| :--- | :--- | :--- |
| `id` | **IMMUTABLE** | From Phase 3. |
| `lemma` | **Dict Form** | Root form (e.g. `가다`). |
| `trans_{lang}` | **Precision** | Natural translation. |
| `note` | **Nuance** | Grammar/Culture notes. |

## 5. Final Audit (Gate 4) 🛑
```bash
python -m tools.v5.4_dictionary.audit_p4 {lang}
```
- **Pass Condition**: 0 `[TODO]` entries.
- **Fail Condition**: Any `[TODO]` or `UNK` tags.

## 🏁 Checklist
- [ ] Automated Audit passed (`✅ PASS`).
- [ ] No `UNK` tags.
- [ ] All Korean predicates in dictionary form.
- [ ] `verified_p4.txt` created.

**Next Step**: [Phase 5 Staging SOP](../8_staging/8_staging_sop.md)
