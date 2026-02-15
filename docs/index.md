# Lingo System Control Tower

Welcome to the central documentation hub for the Lingo multi-repo system.

## Navigation
- [Repository Map](repo_map.md) - Overview of all repositories and their roles.
- [Owners and Responsibilities](owners.md) - Role ownership and handoff boundaries.
- [Workflow Map](workflow_map.md) - Standard operating procedures for content and code.
- [Runbooks](runbooks/README.md) - Step-by-step guides for common tasks.
- [Worklog and Directory Governance](ops/worklog_and_directory_governance.md) - Where daily logs and WIP records live.
- [Korean Stage Contract Matrix](ops/stage_contract_matrix_ko.md) - Gate and artifact contract for KO stages.
- [Stage Handoff JSON Schema](ops/handoff_stage.schema.json) - Required machine-readable handoff format.
- [Korean Tokenization Profile](ops/language_profiles/ko_tokenization_profile.md) - KO-specific parsing and restoration policy.
- [Gemini Stage Execution Protocol](runbooks/gemini_stage_execution_protocol.md) - One-stage execution protocol.
- [Gemini Closeout Protocol](runbooks/gemini_closeout_protocol.md) - End-of-session protocol dispatcher.
- [Daily Worklog Template](worklogs/_template.md) - Template for `YYYY-MM-DD.md` daily logs.

## Repositories
- **[core-schema](../../core-schema)**: Source of truth for data contracts.
- **[content-ko](../../content-ko)**: Korean content source and ingestion layer.
- **[content-pipeline](../../content-pipeline)**: Build logic and validation gates.
- **[release-aggregator](.)**: Release management and documentation (You are here).
- **[lingo-frontend-web](../../lingo-frontend-web)**: Web application and asset intake.
