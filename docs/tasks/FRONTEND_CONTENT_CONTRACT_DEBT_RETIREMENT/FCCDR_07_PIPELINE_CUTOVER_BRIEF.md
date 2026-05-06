# fccdr-07 Pipeline Cutover Brief

Date: 2026-05-06
Status: implemented as sidecar-first default path

## Goal

Move Learning Library runtime i18n emission from legacy bridge reads to
canonical `content_v2/i18n/<locale>/learning_library` sidecars.

This is not a frontend UI task. The frontend already has runtime coverage gates;
the remaining blocker is that `content-pipeline` still reads legacy
`content/i18n/**` paths when building Learning Library runtime artifacts.

2026-05-06 update: content-pipeline commit `c2bfba7` now loads canonical
sidecars first. Legacy bridge reads remain available only behind explicit
`--allow-legacy-i18n-bridge`; final removal is tracked by `fccdr-14`.

## Canonical Input

Sidecar entrypoint:

```text
content_v2/i18n/<locale>/learning_library/manifest.json
```

Required sidecars listed by the manifest:

- `sources.json`, keyed by `source_id`
- `sentences.json`, keyed by `source_id -> sentence_id`
- `knowledge.json`, keyed by `knowledge_id`

Turn-based rows for video/dialogue/article must preserve `turn_id`. Shared
example-bank rows use `source_id = "shared_bank"` and usually omit `turn_id`.

## Pipeline Lookup Order

The new `content-pipeline` lookup order should be:

1. Read `content_v2/i18n/<locale>/learning_library/manifest.json`.
2. Load only the sidecars listed by that manifest.
3. Emit the existing frontend runtime artifact shape from canonical sidecars.
4. Use legacy `content/i18n/**` bridge only if an explicit fallback flag is set.

The fallback flag must be named and visible in code, for example:

```text
--allow-legacy-i18n-bridge
```

Hidden fallback by filename transform or implicit path probing is not allowed
after `fccdr-07` retires.

## Required Release-Side Gates

Validate canonical sidecars:

```bash
python3 scripts/validate_content_contracts.py \
  --learning-library-i18n-sidecar-manifest /Users/ywchen/Dev/lingo/content-ko/content_v2/i18n/zh_tw/learning_library/manifest.json \
  --min-sidecar-sentence-coverage 0.95
```

During migration, permit existing bridge symbols but keep them visible:

```bash
python3 scripts/validate_content_contracts.py \
  --content-pipeline-learning-library-source /Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py \
  --legacy-learning-library-bridge-policy allow
```

After pipeline cutover, the retirement gate must pass:

```bash
python3 scripts/validate_content_contracts.py \
  --content-pipeline-learning-library-source /Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py \
  --legacy-learning-library-bridge-policy forbid
```

If the implementation keeps a temporary fallback flag for one release slice, use
`flagged` instead of `forbid` until the fallback is removed:

```bash
python3 scripts/validate_content_contracts.py \
  --content-pipeline-learning-library-source /Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py \
  --legacy-learning-library-bridge-policy flagged
```

## No-Legacy Fixture Gate

The content-pipeline implementation must include a fixture or test mode where
legacy `content/i18n` is unavailable. That run must still emit non-empty,
aligned runtime artifacts from canonical sidecars.

Minimum expected artifacts:

- `artifacts/core/sentences.json`
- `artifacts/i18n/zh_tw/sentences.json`
- `artifacts/i18n/zh_tw/sources.json`
- `artifacts/i18n/zh_tw/knowledge.json`

Minimum expected coverage:

- sentence translation coverage at or above `0.95`
- no `status = "active"` sidecar row with empty `translation`
- all video/dialogue/article sentence rows preserve `turn_id`

## Current Known Gap

`src.ko.dialogue.a1_01` still has one `needs_review` sentence:

```text
sent.src.ko.dialogue.a1_01.L01-D1-01
```

This does not block pipeline cutover, but it must be resolved before release
content freeze.

## Gemini / Content-Pipeline Prompt

Use this when handing off implementation:

```text
Repo: /Users/ywchen/Dev/lingo/content-pipeline
Read-only source repo: /Users/ywchen/Dev/lingo/content-ko
Control task: /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/FRONTEND_CONTENT_CONTRACT_DEBT_RETIREMENT/FCCDR_07_PIPELINE_CUTOVER_BRIEF.md

Task:
Update pipelines/learning_library.py so v2 Learning Library i18n reads canonical sidecars from content_v2/i18n/<locale>/learning_library/manifest.json first.

Required behavior:
1. Load manifest.json, then files.sources/files.sentences/files.knowledge.
2. Build existing runtime artifacts from sidecars without changing frontend runtime artifact shape.
3. Keep legacy content/i18n reads only behind an explicit fallback flag named like --allow-legacy-i18n-bridge.
4. Add a no-legacy fixture/test where content/i18n is unavailable and runtime i18n still emits from sidecars.
5. Do not edit content-ko source content except for fixture references required by tests.

Validation:
Run release-side gates:
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/validate_content_contracts.py --learning-library-i18n-sidecar-manifest /Users/ywchen/Dev/lingo/content-ko/content_v2/i18n/zh_tw/learning_library/manifest.json --min-sidecar-sentence-coverage 0.95
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/validate_content_contracts.py --content-pipeline-learning-library-source /Users/ywchen/Dev/lingo/content-pipeline/pipelines/learning_library.py --legacy-learning-library-bridge-policy flagged

After fallback removal, the second command must use --legacy-learning-library-bridge-policy forbid.

Output:
- Changed files
- Test commands and results
- Whether fccdr-07 can move from blocked to completed, or what blocker remains
```
