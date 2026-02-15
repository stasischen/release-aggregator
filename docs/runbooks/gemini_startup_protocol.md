# Gemini Startup Protocol (開工協議)

## Goal
At session start, ask user what to do first, then load only the relevant active protocols before execution.

## Startup Sequence
1. Ask user for current objective.
2. Detect touched repo(s) and stage scope.
3. Load only required active docs from control tower.
4. Echo selected docs and execution boundary.
5. Start execution.

## Mandatory Startup Question
Use this exact prompt at start:

`今天要做哪個任務？請提供 task_id（若有）、目標 repo、是否只做單一 stage。`

## Optional Clarifying Questions
- `是否要先做規範檢查（contract/gate）再改內容？`
- `本次是否包含收工報告（yes/no）？`

## Routing Rules (What to Read)
Always read:
- `docs/index.md`
- `docs/workflow_map.md`
- `docs/runbooks/agent_reference_order.md`

Then load by scope:
- If stage execution: `docs/runbooks/gemini_stage_execution_protocol.md`
- If closeout requested: `docs/runbooks/gemini_closeout_protocol.md`
- If repo includes `content-ko`: `docs/runbooks/closeout_content.md` and `docs/ops/stage_contract_matrix_ko.md`
- If repo includes `content-pipeline`: `docs/runbooks/closeout_pipeline.md`
- If repo includes `lingo-frontend-web`: `docs/runbooks/closeout_frontend.md`
- If repo includes `release-aggregator`: `docs/runbooks/closeout_release.md`
- If repo includes `core-schema`: `docs/runbooks/closeout_schema.md`


## Boundary Rules
- **Language**: Always communicate in **Traditional Chinese (繁體中文)** unless explicitly requested otherwise.
- **Worklog**: You MUST update the worklog for **EVERY** commit you make.
- Do not read protocol/workflow docs from `Lingourmet_universal` for active decisions.
- Archive docs under `docs/archive/universal/**` are comparison-only.
- If user did not define stage, do not auto-jump across stages.

## Startup Output Format
Before doing work, output:
- `objective`
- `task_id`
- `touched_repos`
- `stage_scope`
- `active_docs_used`
- `execution_plan`

## Recommended Session Opener
```text
今天要做哪個任務？請給我 task_id（若有）、目標 repo（可多個）、以及這次是否只做單一 stage。
你回覆後，我會先列出我要依據的協議文件，再開始執行。
```
