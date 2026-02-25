# Task Index (任務索引)

本檔案是所有 Task 的人類可讀索引。Agent 開工時**必須先讀此檔案**。

> [!IMPORTANT]
> 新增或完成任務時，必須同步更新此索引。

---

## 🗺️ Execution Roadmap (執行路線圖)

```text
Phase A: Viewer + 辭典（content-ko 內部閉環）
│  ├── ✅ A1: Viewer 增強 — 辭典彈出、多義詞顯示     [VIEWER-01]
│  ├── 🔧 A2: 辭典品質驗證 — Viewer 逐課檢查 688 字   [MAPPING_DICTIONARY]
│  └── ✅ A3: 多義詞標記 — senseIndex 機制 + Yarn 標記 [KO_RESOLUTION_100PCT]
│
Phase B: Pipeline Build（content-ko → content-pipeline）
│  ├── 📅 B1: 確認 build output 格式（JSON schema）    [CONTENT_PIPELINE_SEPARATION]
│  └── 📅 B2: 跑完整 build，輸出 production assets
│
Phase C: 前端整合（lingo-frontend-web）
│  ├── 🔧 C1: Viewer 功能整合 — 預錄音檔 + 句子高亮 + Grammar Notes [FRONTEND_VIEWER_INTEGRATION]
│  ├── 📅 C2: 對照 build output，確認前端 parser
│  ├── 📅 C3: 導入新資產，flutter test
│  └── 📅 C4: 驗證多義詞在 App 內顯示效果
```

**原則：上游先定義格式 → 驗證完畢 → 才往下游推送。**
**例外：C1 的資料格式已由 Aggregator Viewer 驗證通過，可以立即啟動。**

---

## Active Tasks (進行中)

### Phase A — 當前優先

| Task ID | 描述 | Phase | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- |
| MAPPING_DICTIONARY | 字典映射標準化 + 品質驗證（含雙層詞性落地） | A2 | 8/15 tasks | [JSON](MAPPING_DICTIONARY_TASKS.json) · [PLAN](KO_DICT_01_PLAN.md) |
| CROSS_LANG_REVIEW_LOCK | 跨語系 review/lock 流程（多機協作 + 規則分離） | A2/B1 | 0/7 tasks | [JSON](CROSS_LANG_REVIEW_LOCK_TASKS.json) · [PLAN](CROSS_LANG_REVIEW_LOCK_PIPELINE_PLAN.md) |
| TTS_GENERATION | 高品質 Edge-TTS 語音生成 | Phase B | 5/5 tasks | [JSON](TTS_GENERATION_TASKS.json) |
| CONTENT_V5_MIGRATION_L0 | Legacy L0 Content V5 Standardization | A2 | 0/X tasks | [PLAN](CONTENT_V5_MIGRATION_L0.md) |
| STABLE_TEST_RCA | Root Cause Analysis for Skipped Stable Tests | QA | 0/3 tasks | [PLAN](STABLE_TEST_ROOT_CAUSE_ANALYSIS.md) |
| KO_ATOM_TRANSLATION_EXTRACTION | A1 atom 翻譯補齊 + 從課文抽取 atom 品質稽核 | A2/B1 | 4/6 tasks | [JSON](KO_ATOM_TRANSLATION_AND_EXTRACTION_TASKS.json) |

### Phase C — 前端整合（可立即啟動）

| Task ID | 描述 | Phase | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- |

### Future / Automation (未來優化)

| Task ID | 描述 | Phase | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- |
| CONTENT_CANDIDATE_GENERATION_FRAMEWORK | 候選內容生成雙流程框架（API + Agent + QA + 審核台對接） | B/C | 11/27 tasks | [JSON](CONTENT_CANDIDATE_GENERATION_FRAMEWORK_TASKS.json) · [PLAN](CONTENT_CANDIDATE_GENERATION_FRAMEWORK_PLAN.md) |

### Phase B/C — 待 Phase A 完成後啟動

| Task ID | 描述 | Phase | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- |
| CONTENT_PIPELINE_SEPARATION | 職責分離 + Build 格式 | B1 | 0/6 phases | [JSON](CONTENT_PIPELINE_SEPARATION_TASKS.json) |

---

## Completed Tasks (已完成)

| Task ID | 描述 | 完成時間 | 檔案 |
| :--- | :--- | :--- | :--- |
| VIEWER_ENHANCEMENT | Viewer 辭典彈出 + 舊課程顯示 | 2026-02-15 | [ARCHIVE](archive/20260215_VIEWER_ENHANCEMENT_TASKS.json) |
| KO_RESOLUTION_100PCT | 韓語 Token 解析 100% | 2026-02-15 | [ARCHIVE](archive/20260215_KO_RESOLUTION_100PCT_TASKS.json) |
| FRONTEND_VIEWER_INTEGRATION | Viewer 整合 (音檔/高亮/文法) | 2026-02-22 | [ARCHIVE](archive/20260222_FRONTEND_VIEWER_INTEGRATION_TASKS.json) |
| WORKFLOW_OPTIMIZATION | 工作流優化 (Ingest/Quality Gate/Index) | 2026-02-22 | [ARCHIVE](archive/20260222_WORKFLOW_OPTIMIZATION_TASKS.json) |
| FUTURE_BACKLOG | 自動化與優化提案 | 2026-02-22 | [ARCHIVE](archive/20260222_FUTURE_BACKLOG_TASKS.json) |
| CONTENT_CANDIDATE_REVIEW | Content Candidate Review Station 審核台 | 2026-02-25 | [ARCHIVE](archive/20260225_CONTENT_CANDIDATE_REVIEW_TASKS.json) |
| DIALOGUE_UI_REDESIGN | Zen Study 介面改版：居中對焦、翻譯開關、垂直字典 | 2026-02-25 | [ARCHIVE](archive/20260225_DIALOGUE_UI_REDESIGN_TASKS.json) |
| KO_GEMINI_REVIEW | KO 全量 Gemini 人工審核（mapping + TOPIK POS，含 i18n/base 詞性人工複核） | 2026-02-25 | [ARCHIVE](archive/20260225_KO_GEMINI_REVIEW_TASKS.json) |
| KO_B2_C1_OPTIMIZATION | B2/C1 課程優化：角色大修、商務/評論語氣、翻譯與文法補全 | 2026-02-25 | [ARCHIVE](archive/20260225_KO_B2_C1_OPTIMIZATION_TASKS.json) |

---

## 📌 Conventions (慣例)

### 共享 Plan 檔案

所有 implementation plan **必須存放在 `release-aggregator/docs/tasks/`**，命名慣例：

```text
{TASK_ID}_PLAN.md    — 例如 KO_DICT_01_PLAN.md
{TASK_ID}_TASKS.json  — 例如 MAPPING_DICTIONARY_TASKS.json
```

> [!IMPORTANT]
> **不要只把 plan 放在個別 Agent 的 brain 資料夾。** 放在 release-aggregator 確保：
>
> - 任何電腦上的 Agent 都能讀到
> - 版本控制 (git) 追蹤變更歷史
> - 人類和 Agent 共享同一份文件

### 封存 (Archive)

完成的 Task JSON 和 Plan **應移至 `docs/tasks/archive/`**，且檔名開頭應加上日期：

- 命名格式：`YYYYMMDD_{ORIGINAL_NAME}`
- 例如：`20260215_VIEWER_ENHANCEMENT_TASKS.json`

`TASK_INDEX.md` 中的「已完成」區塊應指向這些封存檔案，以保持主目錄整潔，同時保留歷史記錄。
