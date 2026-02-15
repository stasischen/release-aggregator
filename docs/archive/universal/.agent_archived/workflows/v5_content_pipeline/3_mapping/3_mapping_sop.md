---
description: Phase 3 SOP: Chunk Mapping & Plus-Syntax Multi-ID Strategy
---
# Phase 3 Mapping SOP

**Dependencies**: Phase 2 Atoms must be passed.

## 🛡️ Pre-flight Check
- **Guidance**: Read [Linguistic Guide](../linguistics/audit_ko_content.md) BEFORE mapping.
- **Homonym Check**: Verify collisions (e.g., `배` boat vs pear).
- **Batch Limit**: Call `notify_user` every **20 unique chunks**.

## 3. Field Definitions
| Column | Description | Example |
| :--- | :--- | :--- |
| `chunk_id` | **[Key]** `lang_surface` | `ko_그림보다` |
| `surface` | **[Input]** Surface text from atoms | `그림보다` |
| `atom_id` | **[Mapped ID]** Use `+` for compounds | `ko_N_그림+ko_P_보다` |
| `tags` | **[Metadata]** `auto-extracted` or `manual` | `manual` |

## 4. Mapping Rules
### A. Uniqueness & Plus-Syntax
- **Rule**: One Surface = One Atom ID (Default).
- **Compound**: Use `ID1+ID2` format (e.g., `lang_POS_lemma+lang_POS_lemma`).
- **Integrity**: `Concatenation(Components) == Surface` must be true.

### B. Priority
1. **Manual**: If `tags != auto-extracted`, NEVER overwrite.
2. **Auto**: New entries marked `auto-extracted`.

## 5. Workflow

### 1. Sync & Detect Conflicts
```bash
python -m tools.v5.3_mapping.sync {lang}
```
- **Output**: Watch for `⚠️ Conflict Detected`.

### 2. Analysis Report
```bash
python tools/v5/3_mapping/analyze_chunks.py {lang}
```
- **Action**: Check `chunk_analysis_report_{lang}.md`.
- **Verify**: Ensure `OTHER` usage is near zero.

### 3. Resolve Conflicts
- **File**: `content/3_mapping/{lang}/chunk_mapping.csv`
- **Action**: Manually resolve homonyms or ambiguous mappings.

## 6. Handover
- **Next Step**: Read [Phase 4 Dictionary SOP](../4_dictionary/4_dictionary_sop.md).
