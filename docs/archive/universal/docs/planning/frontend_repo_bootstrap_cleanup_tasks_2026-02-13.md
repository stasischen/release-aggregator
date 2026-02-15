# Frontend Repo Bootstrap & Cleanup Tasks (for Gemini)

Date: 2026-02-13  
Target repo: `git@github.com:stasischen/lingo-frontend-web.git`

## Goal

Stabilize the new frontend-only repo after split, clean root noise, and import only the frontend-relevant docs/agent protocols.

## Principles

1. Do not copy the whole monorepo docs or whole `.agent`.
2. Frontend repo is app-focused; content production pipeline docs stay in monorepo/content repos.
3. Keep only workflows needed for frontend coding, testing, and release handoff.

## Execution Order

### Phase 1: Root Cleanup (must do first)

1. Remove accidental root artifacts if not used by code:
   - `test_json_2.json`
   - `test_json_3.json`
   - `test_json_4.json`
   - `test_out.json`
2. Add ignore rules to prevent recurrence:
   - `test_json_*.json`
   - `test_out.json`
3. Verify no runtime/test references before deletion:
   - `rg -n "test_json_|test_out\\.json" .`

### Phase 2: Repo Hygiene

1. Decide and document retention/removal for legacy folders:
   - `windows_bak/`
   - `temp_dicebear/`
   - `work_log/`
   - `~/` (folder name `~`)
2. Fix hard-coded local absolute paths in scripts:
   - `extract_dicebear_assets.py`
3. Ensure `.gitignore` covers generated files and local debug outputs.

### Phase 3: Frontend Docs Import (selective)

Create a minimal `docs/` in frontend repo and copy only frontend-operational docs:

1. Keep in frontend repo:
   - top-level app docs already present:
     - `ARCHITECTURE.md`
     - `COMPONENTS.md`
     - `HANDOVER.md`
   - migration/runbook docs:
     - `docs/migration/frontend_split_preflight_2026-02-13.md`
     - `docs/migration/frontend_repo_split_migration_2026-02-13.md`
2. Keep out of frontend repo:
   - content pipeline phase docs (`v5_content_pipeline/*`)
   - translation/content writing guides
   - cross-language content orchestration internals

### Phase 4: `.agent` Protocol Import (selective)

Create minimal frontend `.agent` structure:

1. Recommended to copy:
   - `.agent/workflows/universal_project_rules.md`
   - `.agent/workflows/開工_app.md`
   - `.agent/workflows/收工_app.md`
   - `.agent/workflows/task_ownership.md`
   - `.agent/workflows/agent_sync_sop.md`
   - `.agent/workflows/standards/golden_test_guide.md`
   - `.agent/workflows/standards/shift_left_testing.md`
   - `.agent/workflows/standards/type_safety.md`
2. Do not copy:
   - `.agent/workflows/v5_content_pipeline/**`
   - content-specific SOPs (`開工_content.md`, `收工_content.md`)
   - old archive workflows

### Phase 5: Baseline Validation

1. `flutter pub get`
2. smoke bundle:
   - `flutter test test/dictionary_overlay_logic_test.dart`
   - `flutter test test/core/asset_integrity_test.dart`
   - `flutter test test/services/config_loader_test.dart`
   - `flutter test test/content/content_validation_test.dart`
3. targeted checks:
   - `flutter test test/repositories/event_repository_integration_test.dart`
   - `flutter test test/widgets/immersive_dictionary_overlay_test.dart`

## Parallel Split (Two Agents)

1. Agent A (Repo Hygiene):
   - Phase 1 + Phase 2 + baseline test rerun.
2. Agent B (Docs/Protocol Bootstrap):
   - Phase 3 + Phase 4 + docs index update.
3. Merge rule:
   - A merges first if `.gitignore` changes conflict.
   - B rebases and finalizes docs.

## Done Criteria

1. Root no longer contains accidental test artifact JSONs.
2. Frontend repo has a minimal, app-focused `docs/` and `.agent/`.
3. No content-pipeline-only docs/protocols are copied into frontend repo.
4. Smoke + targeted tests pass on frontend `main`.
