# Lingo System Control Tower

Welcome to the central documentation hub for the Lingo multi-repo system.

## 📋 Recent Worklogs

| Date | File |
| --- | --- |
| 2026-02-15 | [2026-02-15.md](worklogs/2026-02-15.md) |
| 2026-02-13 | [2026-02-13.md](worklogs/2026-02-13.md) |

> [!TIP]
> Worklog 唯一存放處：`release-aggregator/docs/worklogs/YYYY-MM-DD.md`。
> 所有 Repo 的收工協議 (`/wrap`) 都會自動寫入此處。

## 🎯 Task Registry (任務總表)

👉 **[TASK_INDEX.md](tasks/TASK_INDEX.md)** — 所有任務的全景索引（Active / Completed 分開顯示）

> [!IMPORTANT]
> Agent 開工時讀取 `TASK_INDEX.md` 即可掌握全局，不需要逐一讀 JSON 檔。
> 任務完成或新增時，必須同步更新此索引。

## Navigation

- [Repository Map](repo_map.md) - Overview of all repositories and their roles.
- [Owners and Responsibilities](owners.md) - Role ownership and handoff boundaries.
- [Workflow Map](workflow_map.md) - Standard operating procedures for content and code.
- [Runbooks](runbooks/README.md) - Step-by-step guides for common tasks.
- [Zellij Control Tower Setup](runbooks/zellij_control_tower_setup.md) - Multi-repo terminal layout and launcher.
- [Agent Reference Order](runbooks/agent_reference_order.md) - Mandatory document order for agents.
- [Gemini Startup Protocol](runbooks/gemini_startup_protocol.md) - Ask objective first, then load relevant protocols.
- [Worklog and Directory Governance](ops/worklog_and_directory_governance.md) - Where daily logs and WIP records live.
- [Korean Stage Contract Matrix](ops/stage_contract_matrix_ko.md) - Gate and artifact contract for KO stages.
- [Stage Handoff JSON Schema](ops/handoff_stage.schema.json) - Required machine-readable handoff format.
- [Korean Tokenization Profile](ops/language_profiles/ko_tokenization_profile.md) - KO-specific parsing and restoration policy.
- [Gemini Stage Execution Protocol](runbooks/gemini_stage_execution_protocol.md) - One-stage execution protocol.
- [GSD Multi-Repo Workflow](runbooks/gsd_multi_repo_workflow.md) - Aggregator orchestration with per-repo execution phases.
- [Codex <-> Antigravity Orchestration](runbooks/codex_antigravity_orchestration.md) - Packetized planning/execution/report loop across machines.
- [Gemini Closeout Protocol](runbooks/gemini_closeout_protocol.md) - End-of-session protocol dispatcher.
- [Universal Archive Migration Runbook](runbooks/universal_archive_migration.md) - Move monorepo docs into control-tower archive.
- [Universal Archive Index](archive/universal/INDEX.md) - Archived monorepo document index.
- [Daily Worklog Template](worklogs/_template.md) - Template for `YYYY-MM-DD.md` daily logs.

## Guides (使用者文件 / User-Facing Docs)

- [V5 Automation Architecture](guides/V5_AUTOMATION_ARCHITECTURE.md) - V5 自動化架構。
- [Reversible Decomposition](guides/REVERSIBLE_DECOMPOSITION.md) - 原子化與還原策略。
- [Content vs Pipeline Separation](guides/CONTENT_PIPELINE_SEPARATION.md) - 職責分離計畫。
- [Content Creation SOP](guides/CONTENT_CREATION_SOP.md) - 課程編寫與品質規範。
- [Data Model Contracts](guides/DATA_MODEL_CONTRACTS.md) - 跨 Repo 資料結構定義。
- [System Asset Strategy](guides/RELEASE_ASSET_STRATEGY.md) - 資產追蹤與發佈模式。
- [Repo Responsibilities](guides/REPO_RESPONSIBILITIES.md) - 倉庫職責總覽。

## 🇰🇷 Korean Specific Standards
- [KO Data Standardization SOP](../../content-ko/docs/SOPs/KO_DATA_STANDARDIZATION_PROTOCOL.md) - V5 韓文原子化標籤協議。
- [KO Review Expert Guidance](../../content-ko/docs/prompts/KO_REVIEW_EXPERT_GUIDANCE.md) - 韓文數據審理專家指南與提示詞。

## 🛠️ Internal Tools / Viewers

- **[KO Content Dev Viewer](../../content-ko/scripts/tools/dict_viewer/index.html)** - Korean atomic data development viewer (for `content-ko` devs).
- **[Release Artifact Viewer](../tools/core_i18n_viewer/index.html)** - Core + I18N package validator (for `aggregator` release checks).

## Repositories

- **[core-schema](../../core-schema)**: Source of truth for data contracts.
- **[content-ko](../../content-ko)**: Korean content source and ingestion layer.
- **[content-pipeline](../../content-pipeline)**: Build logic and validation gates.
- **[release-aggregator](.)**: Release management and documentation (You are here).
- **[lingo-frontend-web](../../lingo-frontend-web)**: Web application and asset intake.
