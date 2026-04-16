請依 `plan-delegate-review` workflow 工作。

你這個 thread 只負責：
- `migrate_legacy_forms.py`

這一輪的子目標是：
- 將 legacy form migration 收斂成可重跑、可驗證、可審計的 V5 normalization tool
- 保持 review pipeline 的既有 decision / anchor / metadata contract 不變

請注意，這不是 review pipeline identity 重寫。
你必須只處理 legacy form migration 的邏輯，不要改動 video review JSONL 的 identity contract。

## Core Decisions

1. `engine/rules/standard_v5_decomposition.json` 是唯一 machine authority。
2. `KO_SEGMENTATION_RULES.md` 保持 human-review canonical reference，但不作為 script runtime source。
3. `migration_v5` 只能作為 metadata 與審計訊號，不應成為永久鎖死的跳過依據。
4. 是否跳過某 row，應以「目前 row 已經是 canonical result」為準，而不是只看 `migration_v5: true`。
5. `source_ref`、`source_revision`、`decision` 等既有欄位必須在 round-trip 中保留，不得被 migration 抹除。

## Required Reading

先讀：
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/migrate_legacy_forms.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/normalize_video_atoms.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/qa_gate.py`
- `/Users/ywchen/Dev/lingo/content-ko/scripts/ops/build_lesson_gold.py`
- `/Users/ywchen/Dev/lingo/content-ko/docs/tech/KO_SEGMENTATION_RULES.md`
- `/Users/ywchen/Dev/lingo/content-ko/engine/rules/standard_v5_decomposition.json`

再看現況 JSONL 樣本：
- `/Users/ywchen/Dev/lingo/content-ko/content/gold_standards/video/79Pwq7MTUPE.jsonl`
- `/Users/ywchen/Dev/lingo/content-ko/content/gold_standards/dialogue/A2/A2-04.jsonl`

## What You Should Do In This Round

只選一個最小切片，不要一次動整條 review stack。

建議第一輪優先：
- 收斂 `migrate_legacy_forms.py` 的 idempotency 與 canonical skip logic

如果你判斷這個切片太大，也可先做：
- 補充 migration report 的審計訊息，讓人工能看出哪些 legacy form 被展開

但一次只能做一個切片。

## Hard Constraints

禁止：
- 不改 video review JSONL identity contract
- 不改 Flutter / frontend
- 不改 `normalize_video_atoms.py`
- 不改 `dict_grammar_linking` 相關文件
- 不把 `migration_v5` 當成永遠跳過的硬旗標
- 不重命名 review decision labels
- 不把 QA summary key 改成新的語義集合

## Technical Direction

### `migrate_legacy_forms.py`

你要把它做成可重跑的 canonical normalization tool。

請保持：
- 只更新 `gold_final_atom_id`
- 保留 `source_ref`、`source_revision`、`sequence_idx`、`decision`、`lesson_id`、`line_id`
- 以 `engine/rules/standard_v5_decomposition.json` 為唯一 machine authority
- `migration_v5` 只作為審計 metadata

請實作的 idempotency 規則：
- 若 row 已經是 canonical 結果，第二次跑應該報 0 changes
- 若 row 尚未 canonical，應正常轉換並標記 `migration_v5: true`
- 不要只因為看到 `migration_v5: true` 就永久跳過；要先確認目前值已經是 canonical result

請加強 reporting：
- 明確列出哪些 legacy form 被展開
- 明確列出哪些 row 沒有變更，因為已經是 canonical

## Acceptance Criteria For This Round

你這一輪完成時，必須讓我可以：

1. 對同一份 JSONL 連跑兩次 migration，第二次回報 0 changes
2. 重新跑 migration 時不破壞 `source_ref` / `source_revision` / `decision`
3. 看到明確的 migration report，能辨識哪些 legacy forms 被 canonicalize
4. 遇到已 canonical 的 row 時不再重複改寫

## Commands

完成後至少執行：
- `git diff --stat`
- `git diff -- <你實際改到的檔案>`

如果有改 code，請再跑最少一個 idempotency 驗證。

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
