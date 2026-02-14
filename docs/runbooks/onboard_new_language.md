# Runbook: Onboarding a New Language

This guide outlines the process for adding a new language pack to the Lingo system.

## Prerequisites
1. Access to `core-schema` and `content-pipeline`.
2. Raw content source (e.g., LLLO CSV/MD).
3. Assigned language code (e.g., `th` for Thai).

## Steps

### 1. Bootstrap Content Repo
- Create a new repository `content-<lang>`.
- Initialize directory structure according to [CONTRACT_DICTIONARY_GRAMMAR.md](../../../core-schema/docs/CONTRACT_DICTIONARY_GRAMMAR.md).

### 2. Implementation Ingestion Layer
- Port `content-ko/scripts/import_lllo_raw.py` to the new repo.
- Customize decomposition and lemma resolution for the target language.

### 3. Setup Build Pipeline
- Add a new pipeline script in `content-pipeline/pipelines/build_<lang>_zh_tw.py`.
- Configure CI/CD to trigger on PRs in `content-<lang>`.

### 4. Verification
- **Command**: `python3 pipelines/build_<lang>_zh_tw.py`
- Validate that atoms are generated in the correct POS subdirectories.

## Validation Gates
> [!IMPORTANT]
> **Manual Review Required**: A linguist must review the `missing_mapping_candidates.json` report before the first production build.
