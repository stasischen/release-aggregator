# Cross-Repo Execution Checklist (Translation 2-Phase)

Target stage order:
1. `content`
2. `content-translate`
3. `tokenize`
4. `dict-translate`
5. `speech`

## A. `content-ko`

Files to add/update:
- `scripts/ops/export_content_handoff.py`
- `scripts/ops/export_tokenize_handoff.py`
- `scripts/ops/README.md`

Expected output (shared handoff root):
- `<handoff_root>/<run_id>/01-content/content.items.json`
- `<handoff_root>/<run_id>/03-tokenize/tokenize.items.json`
- `<handoff_root>/<run_id>/03-tokenize/dictionary.json`

Run commands:
```bash
cd /Users/ywchen/Dev/lingo/content-ko
python3 scripts/ops/export_content_handoff.py \
  --run-id 20260220_demo \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs

python3 scripts/ops/export_tokenize_handoff.py \
  --run-id 20260220_demo \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs
```

## B. `content-pipeline`

Files to add/update:
- `scripts/handoff/run_handoff_stage.py`
- `README.md`

Expected output (shared handoff root):
- `<handoff_root>/<run_id>/02-content-translate/content.translations.json`
- `<handoff_root>/<run_id>/04-dict-translate/dictionary.translations.json`
- `<handoff_root>/<run_id>/05-speech/timeline.json`
- `<handoff_root>/<run_id>/05-speech/audio/**/*`
- `<frontend_intake_root>/<run_id>/packages/<lang>/course/*` (course, frontend target)
- `<frontend_intake_root>/<run_id>/packages/<lang>/i18n/*` (i18n, frontend target)
- `<frontend_intake_root>/<run_id>/packages/<lang>/core/*` (compat fallback)

Run commands:
```bash
cd /Users/ywchen/Dev/lingo/content-pipeline
python3 scripts/handoff/run_handoff_stage.py \
  --stage content-translate \
  --run-id 20260220_demo \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs

python3 scripts/handoff/run_handoff_stage.py \
  --stage dict-translate \
  --run-id 20260220_demo \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs

python3 scripts/handoff/run_handoff_stage.py \
  --stage speech \
  --run-id 20260220_demo \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs

python3 scripts/handoff/export_frontend_intake.py \
  --run-id 20260220_demo \
  --lang ko \
  --ui-lang zh-TW \
  --handoff-root /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs \
  --output-root /Users/ywchen/Dev/lingo/release-aggregator/staging/frontend_intake
```

## C. `core-schema`

Files to add/update:
- `schemas/handoff_manifest.schema.json`
- `examples/handoff_manifest.json`
- `README.md`

Validation command:
```bash
cd /Users/ywchen/Dev/lingo/core-schema
python3 validators/validate.py \
  --schema schemas/handoff_manifest.schema.json \
  --target examples/handoff_manifest.json
```

## D. `release-aggregator`

Files to add/update:
- `docs/guides/PROJECT_STRUCTURE_REPLAN_2026-02-20.md`
- `docs/tasks/CROSS_REPO_EXECUTION_CHECKLIST_TRANSLATION_2PHASE.md`

Optional quick verification:
```bash
find /Users/ywchen/Dev/lingo/release-aggregator/staging/handoffs/20260220_demo -maxdepth 3 -type f | sort
```
