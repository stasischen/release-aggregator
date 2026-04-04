# Korean Stage Contract Matrix (KO First)

## Rules
- Promotion is allowed only when all hard gates pass.
- Each stage must emit `handoff.stage-XX.json` validated by `handoff_stage.schema.json`.
- If hard gate fails, stop and return `status=FAIL`.

## STAGE-01 (content-ko): Source Intake
- owner_repo: content-ko
- consumer_repo: content-ko (STAGE-02)
- inputs:
  - LLLO source bundle (dialogue/article/grammar source)
- command:
  - `python3 scripts/import_lllo_raw.py`
- outputs:
  - `content/source/ko/**`
  - `artifacts/stage1/source_manifest.json`
  - `artifacts/stage1/handoff.stage-01.json`
- hard_gates:
  - source_manifest_exists == true
  - source_schema_valid == true

## STAGE-02 (content-ko): Tokenization + Mapping
- owner_repo: content-ko
- consumer_repo: content-ko (STAGE-03) and content-pipeline
- inputs:
  - `content/source/ko/**`
  - language profile: `docs/ops/language_profiles/ko_tokenization_profile.md`
- command:
  - `python3 scripts/run_mapping_pipeline.py`
- outputs:
  - `artifacts/stage2/token_candidates.jsonl`
  - `artifacts/stage2/mapping_accepted.jsonl`
  - `artifacts/stage2/mapping_conflicts.jsonl`
  - `artifacts/stage2/mapping_report.json`
  - `artifacts/stage2/handoff.stage-02.json`
- hard_gates:
  - duplicate_final_atom_id == 0
  - unresolved_ratio <= 0.10
  - reconstruction_pass_rate >= 0.98
  - contract_id_format_pass == true

## STAGE-03 (content-ko): Dictionary Core/I18n Build
- owner_repo: content-ko
- consumer_repo: content-pipeline
- inputs:
  - `artifacts/stage2/mapping_accepted.jsonl`
- command:
  - `python3 scripts/build_dictionary_from_mapping.py`
- outputs:
  - `content/ko/core/dictionary/*.json`
  - `content/ko/i18n/zh_tw/dictionary/*.json`
  - `artifacts/stage3/dictionary_report.json`
  - `artifacts/stage3/handoff.stage-03.json`
- hard_gates:
  - dictionary_core_schema_pass == true
  - dictionary_i18n_schema_pass == true
  - empty_senses_count == 0
  - missing_source_refs_count == 0

## STAGE-04 (content-pipeline): Build + QA Gates
- owner_repo: content-pipeline
- consumer_repo: release-aggregator
- inputs:
  - content-ko canonical sources + stage handoffs
- command:
  - `./scripts/build.sh`
  - `./ci/smoke_test.sh`
- outputs:
  - `dist/**`
  - `dist/qa/qa_summary.json`
  - `dist/qa/handoff.stage-04.json`
- hard_gates:
  - build_pass == true
  - smoke_pass == true
  - qa_hard_gates_pass == true
  - filename_pattern_pass == true

## STAGE-05 (release-aggregator): Aggregate + Manifest
- owner_repo: release-aggregator
- consumer_repo: lingo-frontend-web
- inputs:
  - `content-pipeline/dist/**`
  - `core-schema/schemas/manifest.schema.json`
  - `core-schema/validators/validate.py`
- command:
  - `./scripts/release.sh --version vX.Y.Z --source-commit <content-pipeline-commit>`
  - or `./scripts/release.sh --output <staging_path> --pipeline-dist <dist_path> --core-schema <core_schema_path> --source-repo <name> --source-commit <commit>`
- outputs:
  - `staging/vX.Y.Z/**`
  - `staging/vX.Y.Z/global_manifest.json`
  - `staging/vX.Y.Z/handoff.stage-05.json`
- hard_gates:
  - manifest_schema_pass == true
  - provenance_fields_complete == true

## STAGE-06 (lingo-frontend-web): Intake + Runtime Verify
- owner_repo: lingo-frontend-web
- consumer_repo: production runtime
- inputs:
  - `release-aggregator/staging/vX.Y.Z/**`
- command:
  - `./scripts/sync_content.sh --version vX.Y.Z`
  - `flutter test test/core/asset_integrity_test.dart`
  - `flutter test test/repositories/event_repository_integration_test.dart`
- outputs:
  - synced assets under frontend intake path
  - `docs/handoffs/handoff.stage-06.json`
- hard_gates:
  - asset_sync_pass == true
  - runtime_integration_pass == true
