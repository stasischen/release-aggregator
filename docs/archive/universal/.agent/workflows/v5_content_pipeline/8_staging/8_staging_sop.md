---
description: Phase 8 SOP: Build Staging (JSON Compilation)
---
# Phase 8 SOP: Build Staging

**Objective**: Transform CSVs (`5_full_view`) into optimized JSONs (`8_output`) with externalized translations.

## Validations (Pre-flight)
- **Phase 5 Passed**: `audit_view` checks must be green.
- **Dictionary Ready**: Phase 4 Dictionary must be synced.

## Workflow

### 1. Run Builder
```bash
python -m tools.v5.8_staging.builder {lang}
```
**Logic**:
- Injects `dict` definitions into Atoms.
- **Strings Separation**: Extracts lesson translations to `Strings_{locale}.json`.
- **Dict Export**: Exports dictionary to `dict_{src}_{tgt}.json`.
- **Clean Structure**: Lesson JSONs contain SOURCE/TARGET text only.

### 2. Output Verification
**Target**: `lingourmet_universal/content/8_output/{lang}/`

| File Type | Pattern | Description |
|:---|:---|:---|
| Lesson JSON | `{id}.json` | Atomic structure + Target content. |
| Lesson Strings | `Strings_{locale}.json` | Translations keyed by `line_id`. |
| Dict Translations | `dict_{src}_{tgt}.json` | Dictionary meanings per locale. |

**Checklist**:
- [ ] NO embedded translations in Lesson JSON (e.g., no `"en": "..."`).
- [ ] All `line_id`s present in `Strings_{locale}.json`.
- [ ] `dict_{src}_{tgt}.json` exists for all locales.

## Handover
- **Next Step**: Read [Phase 9 Deploy SOP](../9_deploy/9_deploy_sop.md).
