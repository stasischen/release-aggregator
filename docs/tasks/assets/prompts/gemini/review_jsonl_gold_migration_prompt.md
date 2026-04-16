請依 `plan-delegate-review` workflow 工作。

你這個 thread 只負責：
- `Review JSONL / Gold Migration`

這一輪的子目標是：
- 讓 video review JSONL 的 identity 與 import/export 更穩定
- 讓 legacy form migration 只依賴單一 machine authority
- 保持現有 review pipeline 的 decision / QA contract 不被打碎

請注意，這不是 release-level 的 content item 改造。
你必須只處理 review pipeline 與 gold migration 層，不要碰 `content_item.v1` 的 release identity。

## Core Decisions

1. `source_ref` 是 review row / import matching 的 canonical key。
2. `source_revision` 必須是 semantic hash，不可依賴空白或標點位置。
3. `standard_v5_decomposition.json` 是 V5 morph normalization 的 machine authority。
4. `KO_SEGMENTATION_RULES.md` 保持 human-readable canonical reference，但 machine execution 以 JSON registry 為準。
5. review decision labels 保持現有語義：
   - row decisions: `OK`, `WRONG`, `SUSPECT`
   - QA summary / gate labels: 保持現有 `PASS`, `FAIL` 與既有 summary keys
6. 不要把 row decision labels、QA summary labels、以及 migration metadata 混成同一套命名。

## Required Reading

先讀：
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/normalize_video_atoms.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/migrate_legacy_forms.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/qa_gate.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/review_diff_validator.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/build_lesson_gold.py`
- `/Users/ywchen/Dev/lingo/content-ko/docs/tech/UNIFIED_ATOMIZATION_PIPELINE.md`
- `/Users/ywchen/Dev/lingo/content-ko/docs/tech/UNIFIED_CONTENT_ITEM_SCHEMA.md`
- `/Users/ywchen/Dev/lingo/content-ko/docs/tech/KO_SEGMENTATION_RULES.md`

再看現況資料：
- `/Users/ywchen/Dev/lingo/content-ko/content/core/video_atoms/79Pwq7MTUPE_atoms.json`
- `/Users/ywchen/Dev/lingo/content-ko/content/gold_standards/video/79Pwq7MTUPE.jsonl`
- `/Users/ywchen/Dev/lingo/content-ko/engine/rules/standard_v5_decomposition.json`

## What You Should Do In This Round

只選一個最小切片，不要一次把整條 review stack 全改掉。

建議第一輪優先：
- 在 `normalize_video_atoms.py` 補上 semantic revision hash 與 import gate

如果你判斷這個切片太大，也可以先做：
- 在 `migrate_legacy_forms.py` 改成單一 registry source

但一次只能做一個切片。

## Hard Constraints

禁止：
- 不改 `content_item.v1` 的 release identity contract
- 不改 Flutter / frontend
- 不改 `dict_grammar_linking` 相關文件
- 不重命名整個 review pipeline 的 row decision labels
- 不把 `OK/WRONG/SUSPECT` 改成新的語義集合
- 不把 QA summary key 與 row decision 混成同一個層級

## Technical Direction

### `normalize_video_atoms.py`

你要處理的是 review JSONL 的穩定性，不是 release item。

請把 identity contract 明確寫成：
- `source_ref`: `video_id:turn_id:atom_index`，只作為 review/import matching key
- `sequence_idx`: row ordering only
- `lesson_id` / `line_id`: legacy compatibility metadata
- `source_revision`: semantic hash of canonical non-structural atom content

Semantic hash should:
- ignore formatting-only changes
- ignore spaces / punctuation atoms
- fail when token structure changes, atoms are added, removed, or reordered

Import gate should:
- accept unchanged semantic content even if `_atoms.json` is reserialized
- fail when the canonical atom content drifts

### `migrate_legacy_forms.py`

你要把它收斂成單一 machine authority 的 migration tool。

請保持：
- 只更新 `gold_final_atom_id`
- 保留 `migration_v5: true` 以支持 idempotency
- 以 `engine/rules/standard_v5_decomposition.json` 為唯一 machine registry

不要：
- 重新發明新的 label 系統
- 改動 human review decision policy

## Acceptance Criteria For This Round

你這一輪完成時，必須讓我可以：

1. 對一個 video atoms 檔做 export / import
2. 在只改 reserialization / whitespace 的情況下通過 semantic gate
3. 在 token 結構真的漂移時讓 import 失敗
4. 對同一份 JSONL 重跑 migration 時得到 0 changes
5. 保持現有 `OK / WRONG / SUSPECT` 與 `PASS / FAIL` 的既有契約不壞

## Commands

完成後至少執行：
- `git diff --stat`
- `git diff -- <你實際改到的檔案>`

如果你有改 code，請再跑最少一個能證明 semantic gate 的本地驗證。

## Required Output Format

回報請用：
- Current State
- Changes Made
- How To Test
- What I Should Look For
- Remaining Gaps
- Files Updated

最後附上：
- branch 名稱
- commit SHA
- 這一輪只做了哪一個切片
- 下一輪建議做什麼，但不要先做
