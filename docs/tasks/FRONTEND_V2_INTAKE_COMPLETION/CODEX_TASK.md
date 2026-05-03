# Codex Implementation Packet

請只做這個任務。

## 目標

依 `FRONTEND_V2_INTAKE_COMPLETION` task brief，把 frontend study/dictionary/UI 顯示資料來源收斂到 `content_v2` 衍生的 stable contract。每次只做一個 implementation slice，避免跨 repo 大改。

## 限制

- 不要重構無關檔案。
- 不要改 public API，除非 `TASK_BRIEF.md` 或 GPT 5.5 decision 明確核准。
- 不要把 `content-ko/content_v2` raw inventory path 直接變成 Flutter runtime path。
- 不要混入 Stitch UI、visual redesign、或課程內容重寫。
- 每改一段先跑 targeted tests，或說明無法測試原因。
- 不要 revert 使用者或其他 agent 的 unrelated changes。

## Target Repo

- Primary: `lingo-frontend-web`
- Coordination: `release-aggregator`
- Source truth reference: `content-ko/content_v2`

## Scope In

- `lingo-frontend-web/lib/features/study/data/repositories/`
- `lingo-frontend-web/lib/core/repositories/dictionary_repository.dart`
- `lingo-frontend-web/lib/core/services/config_loader.dart`
- `lingo-frontend-web/lib/core/services/i18n_overlay_service.dart`
- `lingo-frontend-web/test/content/`
- `release-aggregator/scripts/prg/`
- `release-aggregator/tests/test_prg_frontend_contract.py`
- `release-aggregator/docs/tasks/FRONTEND_V2_INTAKE_COMPLETION/`

## Scope Out

- `lingo-frontend-web/docs/stitch_designs/`
- General UI theme/token work
- Course authoring or content rewrite under `content-ko/content_v2`
- Dictionary quality cleanup unrelated to frontend contract

## 相關檔案

- `docs/tasks/FRONTEND_V2_INTAKE_COMPLETION/TASK_BRIEF.md`
- `lingo-frontend-web/docs/frontend_content_v2_realignment_plan_2026-04-19.md`
- `lingo-frontend-web/docs/operations/content_artifact_intake.md`
- `release-aggregator/docs/review/2026-05-02_PRG_DRIFT_INVENTORY.md`

## Required Reads

- `docs/tasks/FRONTEND_V2_INTAKE_COMPLETION/TASK_BRIEF.md`
- Latest `docs/tasks/FRONTEND_V2_INTAKE_COMPLETION/HANDOFF_SUMMARY.md` when present
- Any GPT decision note in this task directory when present

## Implementation Steps

1. Inspect current frontend loaders and production assets.
2. Write or update inventory/decision notes in this task directory before code changes.
3. Make the narrowest code change for the current slice.
4. Run targeted validation commands.
5. Report changed files, tests, skipped validation, and residual risks.

## 驗收標準

- [ ] Implementation stays within the approved slice.
- [ ] Direct production path construction is reduced or isolated behind a resolver/adapter.
- [ ] Real Korean v2-derived fixture coverage is added or strengthened.
- [ ] PRG/frontend contract validation is updated when release artifact shape changes.
- [ ] `TASK_INDEX.md` and handoff are updated at milestone boundaries.

## Required Output

- Changed files
- Commands run and pass/fail
- Any skipped validation with reason
- Remaining risks
- Whether GPT 5.5 review is required before next slice
