# V2 Atomized Runtime Frontend Bridge Fix

## Goal
Ensure frontend runtime surfaces receive and preserve atomized v2 content for video and sentence-bank experiences.

## Background
- Video and sentence-bank content are atomized in source artifacts, but frontend runtime currently does not consistently consume those atoms.
- Video production package files under `lingo-frontend-web/assets/content/production/packages/ko/video/core/` currently contain empty `content` payloads, so video subtitle interaction falls back to generated `gen_*` atoms.
- Sentence-bank artifacts contain atoms in `assets/artifacts/learning_library/ko/core/sentences.json`, but frontend DTO/domain mapping drops them before UI rendering.

## Scope
- `release-aggregator`: task artifact and handoff documentation.
- `content-pipeline`: video frontend sync bridge, if needed.
- `lingo-frontend-web`: asset integrity gates, sentence-bank atom parsing/model/UI, and focused tests.

## Non-Goals
- Do not change lesson data format.
- Do not modify `content-ko` source content unless a narrow validation proves a source artifact is missing.
- Do not remove `mapping_v2` origin cache.
- Do not redesign lesson runtime contract.

## Slices
1. Slice A: Fix video sync bridge so runtime package receives atomized subtitle atoms from v2 inventory/staging or canonical atomized sidecars; add an asset integrity gate preventing 0% atom coverage.
2. Slice B: Fix Sentence Bank DTO/domain/model/UI to preserve atoms and expose atom drilldown through existing dictionary interaction patterns.
3. Slice C: Add regression tests proving video and sentence-bank atom coverage cannot silently return to zero.

## Acceptance Criteria
- Video production package assets have non-empty `content.atoms` for shipped subtitle turns where atomized source data exists.
- Video subtitle parsing no longer depends on generated `gen_*` atoms for atomized shipped videos.
- Sentence Bank model retains atoms from artifact JSON.
- Sentence Bank UI exposes atom-aware interaction, not only plain sentence text.
- Tests cover video atom coverage and sentence-bank atom preservation.

## Validation
- `python3 -m unittest discover -s /Users/ywchen/Dev/lingo/content-pipeline/tests -p "test_sync_video_to_frontend*.py" -v`
- `cd /Users/ywchen/Dev/lingo/release-aggregator && make sync-frontend-assets`
- `cd /Users/ywchen/Dev/lingo/lingo-frontend-web && flutter test test/core/asset_integrity_test.dart`
- Focused frontend tests for sentence-bank atom model/UI.

