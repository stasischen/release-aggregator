# Gemini Stage Execution Protocol (KO First)

## Trigger
Use this when user asks to execute a specific stage task.

## Mandatory Steps
1. Read `docs/ops/stage_contract_matrix_ko.md` and identify target stage.
2. Print planned `inputs`, `commands`, `outputs`, and `hard_gates` before execution.
3. Execute only one stage (no auto-jump to next stage).
4. Validate output and generate `handoff.stage-XX.json` matching `docs/ops/handoff_stage.schema.json`.
5. Return report with evidence.

## Stop Conditions
- Any hard gate fail => `status=FAIL`, stop immediately.
- Missing required output => `status=FAIL`, stop immediately.

## Required Report
- `stage_id`
- `repo`
- `branch`
- `commit_hash`
- `commands_run`
- `output_files`
- `gate_results`
- `status`
- `blockers`
- `handoff_file_path`

## Prompt Template
請讀取 `docs/ops/stage_contract_matrix_ko.md` 與 `docs/ops/handoff_stage.schema.json`。
本次只執行 `{STAGE_ID}`，禁止進入下一階段。
先列出 inputs/commands/outputs/hard_gates，再執行。
最後輸出符合 schema 的 `handoff.stage-XX.json` 與 report。
