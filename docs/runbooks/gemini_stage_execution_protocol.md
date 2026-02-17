# Gemini Stage Execution Protocol (KO First)

## Trigger
Use this when user asks to execute a specific stage task.

> [!IMPORTANT]
> This protocol is for `classic_stage` mode (single-repo, single-stage).
> If execution requires multi-repo orchestration or phase waves, switch to
> `docs/runbooks/gsd_multi_repo_workflow.md` (`gsd_phase` mode).

## Mandatory Steps
1. Read `docs/ops/stage_contract_matrix_ko.md` and identify target stage.
2. Print planned `inputs`, `commands`, `outputs`, and `hard_gates` before execution.
3. Execute only one stage (no auto-jump to next stage).
4. Validate output and generate `handoff.stage-XX.json` matching `docs/ops/handoff_stage.schema.json`.
5. Return report with evidence.

## GSD Compatibility Rules
- A stage task may be one task inside a larger GSD phase, but this protocol still executes one stage only.
- If blockers require changes in another repo, stop and hand back to aggregator planning.
- Do not continue to the next stage in the same session unless explicitly requested.

## Stop Conditions
- Any hard gate fail => `status=FAIL`, stop immediately.
- Missing required output => `status=FAIL`, stop immediately.

## Required Report
- `stage_id`
- `repo`
- `branch`
- `commit_hash`
- `execution_mode` (`classic_stage` or `gsd_phase`)
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
