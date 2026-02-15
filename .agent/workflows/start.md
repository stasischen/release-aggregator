---
description: control-tower startup shim
---
# Startup Shim (Control Tower)

Active protocol source:
- `/Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/gemini_startup_protocol.md`

Rules:
1. Do not use local repo workflows as source-of-truth.
2. Use only `release-aggregator/docs/**` as active protocol.
3. If legacy comparison is needed, read only `release-aggregator/docs/archive/universal/**`.

Startup prompt:
`今天要做哪個任務？請提供 task_id（若有）、目標 repo、是否只做單一 stage。`

Before execution, agent must output:
- `active_docs_used`
- `archive_docs_used` (if any)
- `decision_source`
