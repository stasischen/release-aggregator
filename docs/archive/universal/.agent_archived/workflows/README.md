# Agent Workflows (工作流指南)

本目錄包含本項目中 AI Agent 與開發者共用的工作流文檔。
This directory contains workflow documentation shared by AI Agents and developers in this project.

---

## 📂 目錄結構 (Directory Structure)

```
.agent/workflows/
├── 開工.md                    # 開工協議 (Session start)
├── 收工.md                    # 收工協議 (Session wrap-up)
├── v5_content_pipeline.md      # ⭐ V5 核心管線 (Authority)
│   └── v5_content_pipeline/
│       ├── 0_writer/           # Phase 0: Writing
│       ├── 1_translation/      # Phase 1: Translation
│       ├── 2_atoms/            # Phase 2: Atoms/POS
│       ├── 3_mapping/          # Phase 3: Mapping
│       ├── 4_dictionary/       # Phase 4: Dictionary
│       ├── 8_staging/          # Phase 8: Staging
│       └── 9_deploy/           # Phase 9: Deployment
├── universal_project_rules.md  # 專案通用規則 (Mandatory Rules)
│
├── standards/                  # 核心技術標準 (Coding & QA)
│   ├── type_safety.md
│   ├── shift_left_testing.md
│   └── qa_content_integrity.md
│
├── linguistics/                # 語言專家稽核 (Expert Audit)
│   ├── audit_ko_content.md
│   ├── audit_de_content.md
│   └── audit_th_content.md
│
└── archive/                    # 已過時之文檔 (Archives)
```

---

## 🛠️ 常用指令 (Common Commands)

- **/開工**: 開始新的一個工作階段 (Session start).
- **/收工**: 完成並整理當前工作階段 (Session wrap-up).
- **/v5_content_pipeline**: ⭐ 執行 V5 模組化管線流程.
- **/universal_project_rules**: 閱讀專案通用守則 (Mandatory).
- **/audit_ko_content**: 啟動韓語內容專家稽核.
- **/generate_models**: 執行 Flutter 模型生成.

---

**Last Updated**: 2026-01-25
