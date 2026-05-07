# Task Index (任務索引)

本檔案是所有 Task 的人類可讀索引。Agent 開工時**必須先讀此檔案**。

> [!IMPORTANT]
> 新增或完成任務時，必須同步更新此索引。

---

## 🗺️ Execution Roadmap (執行路線圖)

```text
Layer 1: 內容回收 / Staging Recovery
│  ├── 先把既有 dialogue / video 拉回 staging
│  ├── 補 readiness_flag / segmentation_status
│  └── 不直接推 production
│
Layer 2: 前端承接 / Frontend Contract Integration
│  ├── 先讓 viewer / frontend 吃新版 source-build artifact
│  ├── 驗證 Architecture 與 Modular/KLab Viewer Refactor
│  ├── 通過 ULV Runtime Mock Verification (真 content 驗收)
│  └── 最後才轉入 Flutter Transfer
│
Layer 3: 單元重構 / Unit-by-Unit Refactor
│  ├── 先做 dialogue / travel / daily-life
│  ├── 再做 video
│  ├── 再做 grammar-heavy
│  └── 再做 article / reading
│
Layer 4: 技能深化 / Skill-Layer Expansion
│  ├── audio
│  ├── reading
│  ├── writing
│  ├── vocab / collocation
│  ├── grammar progression
│  ├── assessment
│  └── personalization
│
Layer 5: Legacy Backfill
│  └── 最後才回頭做 L0 V4 -> V5 遷移
```

**正式架構文件：** [COURSE_REFACTOR_EXECUTION_ARCHITECTURE.md](assets/COURSE_REFACTOR_EXECUTION_ARCHITECTURE.md)
**原則：先恢復可見與可驗證，再做前端承接，再做課程重構；不要把 segmentation 修復和單元重構綁在一起。**

---

## Active Tasks (進行中)

### Layer 1 — 內容回收 / Staging Recovery

| TASK_ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| STABLE_TEST_RCA | Root Cause Analysis for Skipped Stable Tests | QA | pro | 0/3 tasks | [PLAN](STABLE_TEST_ROOT_CAUSE_ANALYSIS.md) |

### Layer 2 — 前端承接 / Frontend Contract Integration

**順序原則：** `MODULAR_VIEWER_REFACTOR` 與 `ULV_RUNTIME_MOCK_VERIFICATION` 已完成封存；後續 Flutter 轉接請直接沿用它們的驗證結果與既有 contract，再把通過驗證的 overlay / link 行為正式 migrate 到前端實作（例如 `kg-ui-019`）。

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FRONTEND_V2_INTAKE_COMPLETION | 前端 study / dictionary / UI 顯示資料收斂到 `content_v2` 衍生 stable contract | C+/Frontend Contract | flash -> pro | 6/6 tasks | [JSON](FRONTEND_V2_INTAKE_COMPLETION/TASKS.json) · [BRIEF](FRONTEND_V2_INTAKE_COMPLETION/TASK_BRIEF.md) |
| FRONTEND_UI_COMPLETENESS_QA | Frontend v2 product UI completeness gaps（artifact default、video routes、dictionary disambiguation、pilot placeholders） | C+/Frontend QA | flash -> pro | 4/5 tasks | [JSON](FRONTEND_UI_COMPLETENESS_QA/TASKS.json) · [BRIEF](FRONTEND_UI_COMPLETENESS_QA/TASK_BRIEF.md) |
| LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF | Learning Library `LLCM-008` handoff：將 artifact-backed prototype 轉為 Knowledge-First Lab index-first product path | C+/Frontend Contract | flash -> pro | 5/5 tasks | [JSON](LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/TASKS.json) · [BRIEF](LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF/TASK_BRIEF.md) |
| LEARNING_LIBRARY_REFERENCE_UI_RESTRUCTURE | Knowledge Bank / Sentence Evidence / Dictionary examples 教育 app reference flow 重構（focused catalog、例句證據層、字典反查例句、dark-mode gates） | C+/Frontend Product UI | flash -> pro | 6/8 tasks | [JSON](LEARNING_LIBRARY_REFERENCE_UI_RESTRUCTURE/TASKS.json) · [BRIEF](LEARNING_LIBRARY_REFERENCE_UI_RESTRUCTURE/TASK_BRIEF.md) |
| LIBRARY_REFERENCE_STITCH_UI_TRANSFER | Google Stitch Library reference UI transfer（Knowledge-First Lab reference browser / Sentence evidence / Dictionary / Video overlay；遵守 source-first 多層架構與 light/dark 安全） | C+/Frontend Product UI | flash -> pro | 5/10 tasks | [JSON](LIBRARY_REFERENCE_STITCH_UI_TRANSFER/TASKS.json) · [BRIEF](LIBRARY_REFERENCE_STITCH_UI_TRANSFER/TASK_BRIEF.md) |
| FRONTEND_CONTENT_CONTRACT_DEBT_RETIREMENT | v2 frontend/content temporary bridge retirement（locale fallback、legacy i18n merge、shared_bank semantics、dictionary core/i18n split、POS composition split） | C+/Frontend Contract | flash -> pro | 17/17 tasks | [JSON](FRONTEND_CONTENT_CONTRACT_DEBT_RETIREMENT/TASKS.json) · [BRIEF](FRONTEND_CONTENT_CONTRACT_DEBT_RETIREMENT/TASK_BRIEF.md) |
| MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF | Modular lesson runtime UI cleanup and product-contract boundary brief | C+/Frontend Contract | flash -> pro | 4/4 tasks | [JSON](MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF/TASKS.json) · [BRIEF](MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF/TASK_BRIEF.md) |
| MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF | Modular lesson runtime article/support/video contract options inventory | C+/Frontend Contract | flash -> pro | 4/4 tasks | [JSON](MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF/TASKS.json) · [BRIEF](MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF/TASK_BRIEF.md) |
| MODULAR_LESSON_RUNTIME_IMPLEMENTATION | Modular lesson runtime article/support/video smoke-gate implementation | C+/Frontend Contract | flash -> pro | 5/5 tasks | [JSON](MODULAR_LESSON_RUNTIME_IMPLEMENTATION/TASKS.json) · [BRIEF](MODULAR_LESSON_RUNTIME_IMPLEMENTATION/TASK_BRIEF.md) |
| V2_ATOMIZED_RUNTIME_FRONTEND_BRIDGE_FIX | Video / Sentence Bank atomized v2 runtime bridge repair | C+/Frontend Contract | flash -> pro | 3/3 tasks | [JSON](V2_ATOMIZED_RUNTIME_FRONTEND_BRIDGE_FIX/TASKS.json) · [BRIEF](V2_ATOMIZED_RUNTIME_FRONTEND_BRIDGE_FIX/TASK_BRIEF.md) |
| STITCH_UI_PROTOTYPING | 快速前端 UI 原型設計與 Design Token 確立 (Home, Grammar Lab, Shadowing) | C+/UI | flash -> pro | 3/5 tasks | [JSON](STITCH_UI_PROTOTYPING_TASKS.json) · [PLAN](STITCH_UI_PROTOTYPING_PLAN.md) |

### Layer 3 — 單元重構 / Unit-by-Unit Refactor

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TARGET_LANG_COURSE_FACTORY | 目標語系課程工廠（目標語內容優先 + 中英文教學層 + 前端轉換） | C+/Ops | flash -> pro | 10/20 tasks | [JSON](TARGET_LANG_COURSE_FACTORY_TASKS.json) |

### Layer 4 — 技能深化 / Skill-Layer Expansion

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TARGET_LANG_AUDIO_SKILLS | 目標語系聽力/發音層（手機 App、無真人依賴） | C+/Ops | flash -> pro | 0/10 tasks | [JSON](TARGET_LANG_AUDIO_SKILLS_TASKS.json) · [PLAN](TARGET_LANG_AUDIO_SKILLS_PLAN.md) |
| TARGET_LANG_READING_SKILLS | 目標語系閱讀層（文本理解/證據定位/推論） | C+/Ops | flash -> pro | 0/10 tasks | [JSON](TARGET_LANG_READING_SKILLS_TASKS.json) · [PLAN](TARGET_LANG_READING_SKILLS_PLAN.md) |
| TARGET_LANG_WRITING_SKILLS | 目標語系寫作層（句級到段落級產出） | C+/Ops | flash -> pro | 0/6 tasks | [JSON](TARGET_LANG_WRITING_SKILLS_TASKS.json) · [PLAN](TARGET_LANG_WRITING_SKILLS_PLAN.md) |
| TARGET_LANG_VOCAB_COLLOCATION | 目標語系詞彙/搭配層（功能詞塊與語域） | C+/Ops | flash -> pro | 0/6 tasks | [JSON](TARGET_LANG_VOCAB_COLLOCATION_TASKS.json) · [PLAN](TARGET_LANG_VOCAB_COLLOCATION_PLAN.md) |
| TARGET_LANG_GRAMMAR_PROGRESSION | 目標語系文法進階層（功能導向 unlock + DAG） | C+/Ops | flash -> pro | 0/6 tasks | [JSON](TARGET_LANG_GRAMMAR_PROGRESSION_TASKS.json) · [PLAN](TARGET_LANG_GRAMMAR_PROGRESSION_PLAN.md) |
| TARGET_LANG_ASSESSMENT_LAYER | 目標語系測評層（placement/progress/mastery） | C+/Ops | flash -> pro | 0/6 tasks | [JSON](TARGET_LANG_ASSESSMENT_LAYER_TASKS.json) · [PLAN](TARGET_LANG_ASSESSMENT_LAYER_PLAN.md) |
| TARGET_LANG_PERSONALIZATION_LAYER | 目標語系個人化層（動態派題與補救） | C+/Ops | flash -> pro | 0/6 tasks | [JSON](TARGET_LANG_PERSONALIZATION_LAYER_TASKS.json) · [PLAN](TARGET_LANG_PERSONALIZATION_LAYER_PLAN.md) |

### Layer 5 — Legacy Backfill

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CONTENT_V5_MIGRATION_L0 | Legacy L0 Content V5 Standardization | A2 | flash -> pro | 0/8 tasks | [JSON](CONTENT_V5_MIGRATION_L0_TASKS.json) · [PLAN](CONTENT_V5_MIGRATION_L0.md) |
| BATCH_V5_VIDEO_GATE | Batch process remaining 4 pilot videos (V5 Gate) | Ops | flash -> pro | 0/4 tasks | [PLAN](BATCH_V5_VIDEO_GATE_PLAN.md) |

### Future / Automation (未來優化)

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| VIDEO_INGESTION_PIPELINE | 影片自動化導入管線 (YouTube Subtitles -> Source/I18N -> Product) | CI/Ops | flash -> pro | 0/10 tasks | [PLAN](VIDEO_INGESTION_PIPELINE_PLAN.md) |

### Parallel Content Enrichment (可平行但不得阻塞主線)

| Task ID | 描述 | Phase | DeepSeek | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| GRAMMAR_INDEX_BRIDGE_SYNC | Published grammar ID bridge sync（`dict_grammar_mapping.json` ↔ `assets/content/grammar/grammar_index.json`；維持 G-KO-* 與實體資產映射一致） | C+/Ops | flash -> pro | 0/3 tasks | [JSON](GRAMMAR_INDEX_BRIDGE_SYNC_TASKS.json) · [PLAN](GRAMMAR_INDEX_BRIDGE_SYNC_PLAN.md) |
| DICTIONARY_ENTRY_DRIFT_REVIEW | Korean dictionary entry drift audit（homonym/polysemy、Hanja/source metadata、`mapping_v2.entry_refs` readiness） | C+/Lexicon | pro | 0/4 tasks | [PLAN](DICTIONARY_ENTRY_DRIFT_REVIEW_PLAN.md) |


### Completed Pending Archive (已完成待封存)

| Task Id | 描述 | 進度 | 檔案 |
| :--- | :--- | :--- | :--- |
| KG-UI-019 | Dictionary-to-Grammar Deep Linking UI | done | [JSON](archive/20260428/20260428_KG-UI-019_TASKS.json) · [PLAN](archive/20260428/20260428_KG-UI-019_PLAN.md) |
| PRODUCTION_RELEASE_GATING | Staging candidate / production release gate | done | [JSON](archive/20260428/20260428_PRODUCTION_RELEASE_GATING_TASKS.json) |
| UNIFIED_LESSON_VIEW_FLUTTER_TRANSFER | Modular Viewer 下游：將凍結的 unified lesson view contract 轉入 Flutter（shell / state / adapters / QA） | 8/8 tasks | [JSON](archive/20260428/20260428_UNIFIED_LESSON_VIEW_FLUTTER_TRANSFER_TASKS.json) |
| MODULAR_VIEWER_REFACTOR | Modular Viewer 重構 | done | [JSON](archive/20260428/20260428_MODULAR_VIEWER_REFACTOR_TASKS.json) |
| KNOWLEDGE_LAB_VIEWER_REFACTOR | Knowledge Lab Viewer 重構 | done | [JSON](archive/20260428/20260428_KNOWLEDGE_LAB_VIEWER_REFACTOR_TASKS.json) |
| UNIFIED_LESSON_VIEW_ARCHITECTURE | Unified Lesson View 架構定義 | done | [JSON](archive/20260428/20260428_UNIFIED_LESSON_VIEW_ARCHITECTURE_TASKS.json) |
| ULV_RUNTIME_MOCK_VERIFICATION | ULV Runtime Mock 驗證 | done | [JSON](archive/20260428/20260428_ULV_RUNTIME_MOCK_VERIFICATION_TASKS.json) |
| COURSE_MODULE_COMPOSITION | 課程模組組裝 | done | [JSON](archive/20260428/20260428_COURSE_MODULE_COMPOSITION_TASKS.json) |
| LEARNING_LIBRARY_CONTENTKO_MIGRATION | Learning Library artifact 正式化（Knowledge-First Lab handoff 已拆到 active `LEARNING_LIBRARY_KNOWLEDGE_FIRST_LAB_HANDOFF`） | done-with-followup | [JSON](archive/20260428/20260428_LEARNING_LIBRARY_CONTENTKO_MIGRATION_TASKS.json) |
| KNOWLEDGE_LAB_ENRICHMENT | Knowledge Lab 內容充實 | 8/8 tasks | [JSON](archive/20260428/20260428_KNOWLEDGE_LAB_ENRICHMENT_TASKS.json) |
| CONTENT_V2_FRONTEND_EXPORT_SYNC | Frontend Sync Realignment (Batch E) | done | [JSON](archive/20260428/20260428_CONTENT_V2_FRONTEND_EXPORT_SYNC_TASKS.json) |
| SDA-007 | Dictionary Structure Upgrade | done | [PLAN](archive/20260428/20260428_SDA-007_PLAN.md) |
| ULV_MODULAR_RUNTIME_INSIGHTS | Modular Lesson Runtime 學習洞察 (In-App Insights) | done | [JSON](archive/20260428/20260428_ULV_MODULAR_RUNTIME_INSIGHTS_TASKS.json) |
| CLOZE_CONTENT_PIPELINE_SCHEMA | Cloze Content Pipeline Schema Implementation | done | [JSON](archive/20260428/20260428_CLOZE_CONTENT_PIPELINE_SCHEMA_TASKS.json) |
| ULV_MODULAR_RUNTIME_ERROR_LOGGING | Modular Lesson Runtime 錯誤細節追蹤 (Error Logging) | done | [JSON](archive/20260428/20260428_ULV_MODULAR_RUNTIME_ERROR_LOGGING_TASKS.json) |


### Archived Legacy Review Tasks

| Task ID | 描述 | 狀態 | 檔案 |
| :--- | :--- | :--- | :--- |
| GOLDEN_STANDARD_RECONCILIATION | Legacy golden/surgery reconciliation plan, superseded by `GOLDEN_REVIEW_INTEGRATION_PLAN_V1` | archived | [PLAN](archive/20260419/20260419_GOLDEN_STANDARD_RECONCILIATION_PLAN_V0.md) · [INV](archive/20260419/20260419_REVIEW_ARTIFACT_INVENTORY_V0.md) |
| GOLDEN_REVIEW_MATERIALIZATION | Legacy materialization tracker for committed overrides, now archived | archived | [JSON](archive/20260419/20260419_GOLDEN_REVIEW_MATERIALIZATION_TASKS.json) · [PLAN](archive/20260419/20260419_GOLDEN_REVIEW_MATERIALIZATION_PLAN_V1.md) |


### Deferred / Later

| Task ID | 描述 | Phase | 進度 | 檔案 |
| :--- | :--- | :--- | :--- | :--- |


---

## Completed Tasks (已完成)

| Task ID | 描述 | 完成時間 | 檔案 |
| :--- | :--- | :--- | :--- |
| YT_VIDEO_ATOMIZATION_EF65DUUDCEQ | YouTube 影片原子化：Talking About Daily Routines (eF65dUUDcEQ) 全量完成並促銷 | 2026-04-19 | [PLAN](YT_VIDEO_ATOMIZATION_EF65DUUDCEQ_PLAN.md) |
| KO_7500_DICT_MAPPING | NIKL 7500 詞頻表與核心詞典 Token 基礎映射完成 | 2026-04-19 | [INDEX](TASK_INDEX.md) |
| COURSE_PEDAGOGY_OPTIMIZATION | 語言學習效果優化（理解檢查/變體遷移/修復策略/檢索複習/guided rubric/followup 設計） | 2026-04-17 | [JSON](archive/20260417/20260417_COURSE_PEDAGOGY_OPTIMIZATION_TASKS.json) · [PLAN](archive/20260417/20260417_COURSE_PEDAGOGY_OPTIMIZATION_PLAN.md) |
| VIDEO_SUBTITLE_ENRICHMENT | 影片字幕校對與補全 (zh_tw) | 2026-04-07 | [PLAN](archive/20260407/20260407_VIDEO_SUBTITLE_ENRICHMENT_PLAN.md) · [JSON](archive/20260407/20260407_VIDEO_SUBTITLE_ENRICHMENT_TASKS.json) |
| VIEWER_ENHANCEMENT | Viewer 辭典彈出 + 舊課程顯示 | 2026-02-15 | [ARCHIVE](archive/20260215/20260215_VIEWER_ENHANCEMENT_TASKS.json) |
| KO_RESOLUTION_100PCT | 韓語 Token 解析 100% | 2026-02-15 | [ARCHIVE](archive/20260215/20260215_KO_RESOLUTION_100PCT_TASKS.json) |
| FRONTEND_VIEWER_INTEGRATION | Viewer 整合 (音檔/高亮/文法) | 2026-02-22 | [ARCHIVE](archive/20260222/20260222_FRONTEND_VIEWER_INTEGRATION_TASKS.json) |
| WORKFLOW_OPTIMIZATION | 工作流優化 (Ingest/Quality Gate/Index) | 2026-02-22 | [ARCHIVE](archive/20260222/20260222_WORKFLOW_OPTIMIZATION_TASKS.json) |
| FUTURE_BACKLOG | 自動化與優化提案 | 2026-02-22 | [ARCHIVE](archive/20260222/20260222_FUTURE_BACKLOG_TASKS.json) |
| CONTENT_CANDIDATE_REVIEW | Content Candidate Review Station 審核台 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_CONTENT_CANDIDATE_REVIEW_TASKS.json) |
| KO_GEMINI_REVIEW | KO 全量 Gemini 人工審核（mapping + TOPIK POS，含 i18n/base 詞性人工複核） | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_KO_GEMINI_REVIEW_TASKS.json) |
| DIALOGUE_UI_REDESIGN | Zen Study 介面改版：居中對焦、翻譯開關、垂直字典 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_DIALOGUE_UI_REDESIGN_TASKS.json) |
| KO_DICT_LAYERING | Dictionary 常用度分層重建（1-1000 基礎 / 1001-2000 擴充 / quarantine 隔離） | 2026-04-17 | [JSON](archive/20260417/20260417_KO_DICT_LAYERING_TASKS.json) |
| KO_B2_C1_OPTIMIZATION | B2/C1 課程優化：角色大修、商務/評論語氣、翻譯與文法補全 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_KO_B2_C1_OPTIMIZATION_TASKS.json) |
| TTS_GENERATION | 高品質 Edge-TTS 語音生成 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_TTS_GENERATION_TASKS.json) |
| CONTENT_CANDIDATE_GENERATION_FRAMEWORK | 候選內容生成雙流程框架（API + Agent + QA + 審核台對接） | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_CONTENT_CANDIDATE_GENERATION_FRAMEWORK_TASKS.json) |
| KO_ATOM_TRANSLATION_EXTRACTION | A1 atom 翻譯補齊 + 從課文抽取 atom 品質稽核 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_KO_ATOM_TRANSLATION_AND_EXTRACTION_TASKS.json) |
| CROSS_LANG_REVIEW_LOCK | 跨語系 review/lock 流程（多機協作 + 規則分離） | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_CROSS_LANG_REVIEW_LOCK_TASKS.json) |
| CONTENT_PIPELINE_SEPARATION | 職責分離 + Build 格式 | 2026-02-25 | [ARCHIVE](archive/20260225/20260225_CONTENT_PIPELINE_SEPARATION_TASKS.json) |
| MAPPING_DICTIONARY | 字典映射標準化 + 品質驗證（含雙層詞性落地） | 2026-02-27 | [ARCHIVE](archive/20260227/20260227_MAPPING_DICTIONARY_TASKS.json) |
| COURSE_UNIT_FACTORY | 課程單元量產工廠（unit blueprint 模板化 + lint + multi-unit mockup 驗證） | 2026-02-27 | [ARCHIVE](archive/20260227/20260227_COURSE_UNIT_FACTORY_TASKS.json) |
| CONTENT_PIPELINE_POST_SEPARATION_GAPS | Universal Pipeline 後續缺口收斂 | 2026-02-27 | [ARCHIVE](archive/20260227/20260227_CONTENT_PIPELINE_POST_SEPARATION_GAPS_TASKS.json) |

---

## 📌 Conventions (慣例)

### 共享 Plan 檔案

所有 implementation plan **必須存放在 `docs/tasks/`** 的 active working set，命名慣例：

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

### Active / Assets / Archive

- `docs/tasks/` 根層：active working set，放正在執行的 plan、tasks、verification、walkthrough
- `docs/tasks/assets/`：可重用的 reference、spec、schema、contract、guide、mockup
- `docs/tasks/` active task 表中的 `DeepSeek` 欄位用來標示預設 routing：`flash` = 起草/掃描/整理，`flash -> pro` = 先整理再決策，`pro` = 直接決策/review/root-cause
- 開工前可用 `python scripts/check_task_readiness.py <TASK_ID>` 檢查 ready / blocked subtasks
- `docs/tasks/archive/`：已完成或封存的歷史文件
- `docs/tasks/machines/*.json`：每台電腦本機的 gitignored claim 記錄，用來標示目前身份與正在處理的 task
- `docs/tasks/MACHINE_STATUS.md`：共享的 machine claim 摘要，用來讓其他電腦快速看見誰正在做什麼
- machine claim 的最小流程：先更新本機 JSON，再更新並 push `MACHINE_STATUS.md`，之後才開始實作

### 封存 (Archive)

完成的 Task JSON 和 Plan **應移至 `docs/tasks/archive/YYYYMMDD/`**，且檔名開頭應加上日期：

- 命名格式：`YYYYMMDD_{ORIGINAL_NAME}`
- 例如：`20260215_VIEWER_ENHANCEMENT_TASKS.json`

`TASK_INDEX.md` 中的「已完成」區塊應指向這些封存檔案，以保持主目錄整潔，同時保留歷史記錄。
