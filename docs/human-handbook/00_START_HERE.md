# Human Handbook: Start Here

Purpose: provide a human-readable map of the **currently used** flow from content generation to deployment.

Last reviewed: 2026-02-22

## What Is Canonical Now

Use these in order:
1. `docs/human-handbook/01_E2E_STAGES.md`
2. `docs/human-handbook/02_TOOL_CATALOG.md`
3. `docs/human-handbook/03_STAGE_CHECKLISTS.md`
4. `docs/runbooks/release_cut_and_rollback.md`

## What Is Not Canonical

Historical planning docs are archived under:
- `docs/archive/legacy/`

Legacy pointers remain in `docs/guides/` only to preserve old links.

## Current End-to-End Snapshot

1. Source content originates upstream (`lllo`) and is ingested in `content-ko`.
2. `content-ko` performs segmentation and mapping.
3. `content-pipeline` builds release artifacts under `dist`.
4. `release-aggregator` runs `scripts/release.sh` / `scripts/release.py` to stage artifacts and generate `global_manifest.json`.
5. `release-aggregator` validates manifest against `core-schema`.
6. `lingo-frontend-web` performs asset intake and production verification.
