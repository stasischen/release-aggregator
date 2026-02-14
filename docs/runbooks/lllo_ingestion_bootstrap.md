# Runbook: LLLO Ingestion Bootstrap (Korean)

Standard procedure for ingesting Korean content from the LLLO source.

## Prerequisites
- Repository: `content-ko`
- Path to LLLO source: `/Users/ywchen/Dev/lllo` (Local)

## Steps

### 1. Dry Run & Analysis
- **Command**: `python3 scripts/import_lllo_raw.py --dry-run`
- **Review**: Open `content/staging/reports/missing_mapping_candidates.json`.
- **Action**: Add missing lemmas to `content/staging/manual_mapping_additions.json`.

### 2. Write Mode
- **Command**: `python3 scripts/import_lllo_raw.py`
- **Outcome**: `content/source/ko/core/dictionary/atoms/` is populated by POS categories.

### 3. Token Audit
- **Command**: `python3 scripts/audit_tokens.py`
- **Review**: Check `content/staging/reports/token_audit_gaps.json` for broken references.

## Rollback
- **Command**: `git checkout content/source/ko`
- **Action**: Delete any uncommitted categorized atom files.
