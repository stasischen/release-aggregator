# Lingo System Control Tower

Welcome to the central documentation hub for the Lingo multi-repo system.

## ✅ Current Human Handbook (V5 Alignment)

- [Human Handbook Start Here](human-handbook/00_START_HERE.md) - Current source-of-truth entrypoint for humans.
- [End-to-End Stages (Current)](human-handbook/01_E2E_STAGES.md) - Stage definitions for V5 content lifecycle.
- [Tool Catalog (Current)](human-handbook/02_TOOL_CATALOG.md) - Tools currently used in active flow.
- [Stage Checklists](human-handbook/03_STAGE_CHECKLISTS.md) - Gate checklist before moving to next stage.

## 📋 Recent Worklogs

| Date | File |
| :--- | :--- |
| 2026-05-03 | [2026-05-03.md](worklogs/2026-05-03.md) |
| 2026-05-02 | [2026-05-02.md](worklogs/2026-05-02.md) |
| 2026-05-01 | [2026-05-01.md](worklogs/2026-05-01.md) |
| 2026-04-30 | [2026-04-30.md](worklogs/2026-04-30.md) |
| 2026-04-29 | [2026-04-29.md](worklogs/2026-04-29.md) |
| 2026-04-28 | [2026-04-28.md](worklogs/2026-04-28.md) |
| 2026-04-27 | [2026-04-27.md](worklogs/2026-04-27.md) |
| 2026-04-26 | [2026-04-26.md](worklogs/2026-04-26.md) |
| 2026-04-25 | [2026-04-25.md](worklogs/2026-04-25.md) |
| 2026-04-24 | [2026-04-24.md](worklogs/2026-04-24.md) |

> [!TIP]
> Worklog 唯一存放處：`docs/worklogs/YYYY-MM-DD.md`。
> 所有 Repo 的收工協議 (`/wrap`) 都會自動寫入此處。
> 若 recent list 過期，執行 `python scripts/update_recent_worklogs.py`。

## 🎯 Task Registry (任務總表)

👉 **[TASK_INDEX.md](tasks/TASK_INDEX.md)** — 所有任務的全景索引（Active / Completed 分開顯示）

> [!IMPORTANT]
> Agent 開工時讀取 `TASK_INDEX.md` 即可掌握全局。

## 🚀 Agent Entry Point (Agent 開工必讀)

1. **[/start](../../.agent/workflows/start.md)** - 入口指令 shim。
2. **[Agent Reference Order](runbooks/agent_reference_order.md)** - 文件的參考順序規範。
3. **[Gemini Startup Protocol](runbooks/gemini_startup_protocol.md)** - 開工協議 (Step-by-step)。
4. **[TASK_INDEX.md](tasks/TASK_INDEX.md)** - 領取任務。

## 📑 SOPs & Protocols (標準協議)

- **[GSD Multi-Repo Workflow](runbooks/gsd_multi_repo_workflow.md)** - 跨倉庫編排的工作流。
- **[Gemini Stage Execution Protocol](runbooks/gemini_stage_execution_protocol.md)** - 單階段執行協議。
- **[Gemini Closeout Protocol](runbooks/gemini_closeout_protocol.md)** - 收工協議 (/wrap) 主體與分配器。
- **[Codex <-> Antigravity Orchestration](runbooks/codex_antigravity_orchestration.md)** - 跨機協作與計畫包封協議。
- **[Multi-Model Task Orchestration](runbooks/multi_model_task_orchestration.md)** - GPT 5.5 / Codex / Gemini / DeepSeek / Qwen 的日常任務分工與封包規範。
- **[Multi-Model Project Review](review/MULTI_MODEL_PROJECT_REVIEW.md)** - Gemini / DeepSeek / GPT / Codex 分工式架構 review 流程。
- **[Project Review Packet Template](review/PROJECT_REVIEW_PACKET_TEMPLATE.md)** - 給 GPT 的濃縮 review 包格式。
- **[Model Input Specs](review/MODEL_INPUT_SPECS.md)** - 給 Gemini、DeepSeek、GPT 的固定輸入規格。
- **[Handoff Summary Template](handoffs/HANDOFF_SUMMARY_TEMPLATE.md)** - milestone / 換 thread / 換機器時使用的標準交接卡。
- **[Korean Stage Contract Matrix](ops/stage_contract_matrix_ko.md)** - 韓文階段產出規範。

## 🛠️ Operational Runbooks (技術手冊)

- **[Runbooks Overview](runbooks/README.md)** - 手冊目錄總覽。
- **[Zellij Setup](runbooks/zellij_control_tower_setup.md)** - 多倉庫終端環境佈置。
- **[LLLO Ingestion Bootstrap](runbooks/lllo_ingestion_bootstrap.md)** - 韓文內容導入引導。
- **[Universal Archive Migration](runbooks/universal_archive_migration.md)** - 舊文件遷移至 Control Tower。
- **[Worklog Governance](ops/worklog_and_directory_governance.md)** - 日誌檔案命名與存放規範。

## 📘 Guides & Reference (參考指南)

- [Reversible Decomposition](guides/REVERSIBLE_DECOMPOSITION.md) - 原子化與還原策略。
- [Content Creation SOP](guides/CONTENT_CREATION_SOP.md) - 課程編寫與品質規範。
- [Data Model Contracts](guides/DATA_MODEL_CONTRACTS.md) - 跨 Repo 資料結構定義。
- [System Asset Strategy](guides/RELEASE_ASSET_STRATEGY.md) - 資產追蹤與發佈模式。
- [Repo Responsibilities](guides/REPO_RESPONSIBILITIES.md) - 倉庫職責總覽。
- [Video Content Scalability Roadmap](guides/VIDEO_CONTENT_SCALABILITY_ROADMAP.md) - 影片內容擴展與架構演進規劃。

## Guides (Legacy / Archived)

- [LEGACY: Learning Library Schema Freeze v0](tasks/assets/LEARNING_LIBRARY_SCHEMA_FREEZE_V0.md) - **Deprecated**: Replaced by V5 normalization spec.
- [V5 Automation Architecture (Archived pointer)](guides/V5_AUTOMATION_ARCHITECTURE.md)
- [Content vs Pipeline Separation (Archived pointer)](guides/CONTENT_PIPELINE_SEPARATION.md)
- [Legacy Archive Root](archive/legacy/README.md)

## 🇰🇷 Korean Specific Standards
- [KO Data Standardization SOP](../../content-ko/docs/SOPs/KO_DATA_STANDARDIZATION_PROTOCOL.md) - V5 韓文原子化標籤協議。
- [KO Review Expert Guidance](../../content-ko/docs/prompts/KO_REVIEW_EXPERT_GUIDANCE.md) - 韓文數據審理專家指南與提示詞。

## 🛠️ Internal Tools / Viewers

- **[KO Content Dev Viewer](../../content-ko/scripts/tools/dict_viewer/index.html)** - Korean atomic data development viewer (for `content-ko` devs).
- **[Modular UI Viewer](../tools/modular-viewer/index.html)** - Core curriculum and grammar detail viewer (for content production and preview).
- **[Release Artifact Viewer](../tools/core_i18n_viewer/index.html)** - Core + I18N package validator (for `aggregator` release checks).

## Repositories

- **[core-schema](../../core-schema)**: Source of truth for data contracts.
- **[content-ko](../../content-ko)**: Korean content source and ingestion layer.
- **[content-pipeline](../../content-pipeline)**: Build logic and validation gates.
- **[release-aggregator](.)**: Release management and documentation (You are here).
- **[lingo-frontend-web](../../lingo-frontend-web)**: Web application and asset intake.
