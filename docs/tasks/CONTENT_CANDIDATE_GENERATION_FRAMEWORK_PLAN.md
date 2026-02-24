# Content Candidate Generation Framework Plan

## Goal

在 `release-aggregator` 建立一套可持續運作的「候選內容生成框架」，同時支援兩條生成路徑：

- `API flow`：批次量產候選（速度/成本優先）
- `Agent flow`：Gap analysis + 高品質策展（品質/上下文優先）

兩條路徑最後都必須輸出相同的 review-ready 格式，供 `Content Candidate Review Station` 匯入審核。

## Scope (v1)

- 定義共用 schema（candidate / generation brief / QA report）
- 定義 API 生成流程規格與批次輸出格式
- 定義 Agent 生成流程規格與自審格式（中文摘要強制）
- 定義 normalize + QA 規則，統一成審核台可用 bundle
- 定義 accepted candidates 對接 catalog/backlog 的 adapter 輸出格式

## Out of Scope (v1)

- 實際串接特定雲端 API provider
- 真正內容寫回 `lingo-frontend-web` 或 `content-ko`
- 自動 commit / 自動 PR

## Key Principles

1. `One review format`: API/Agent 輸出必須能合流為同一份 `review_ready_bundle.json`
2. `Chinese-first review`: 每筆候選必須附中文摘要與中文風險說明
3. `QA before review`: 缺欄位/重複/難度風險先在 QA report 標記
4. `Batch reproducibility`: 每一批次都要有 `generation_brief` 與 `generation_report`

## Target Outputs Per Batch

建議批次目錄結構（示意）：

```text
batches/{batch_id}/
  generation_brief.json
  gap_report.json                  # agent flow optional
  candidate_packs.api.raw.json     # api flow optional
  candidate_packs.agent.raw.json   # agent flow optional
  candidate_packs.normalized.json
  qa_report.json
  review_ready_bundle.json
  review_results.json              # from review station
  accepted_candidates.json         # from review station
  catalog_draft.json               # adapter output
  backlog_seed.json                # adapter output
```

## Workstreams

### A. Shared Contracts

- `candidate schema v1`（審核台欄位為主）
- `generation_brief schema v1`
- `qa_report schema v1`
- status / risk / score enum 規範

### B. API Generation Flow

- prompt templates（lesson / grammar_note / dictionary_pack / path_node）
- batch runner（輸入 brief，輸出 raw candidates）
- raw -> normalized adapter

### C. Agent Generation Flow

- gap analysis spec（中文輸出）
- candidate generation spec（中文摘要強制）
- self-review spec（風險、重複、建議決策）
- raw -> normalized adapter

### D. Normalize + QA + Review Integration

- normalize pipeline（API/Agent 共用 canonical schema）
- QA rules（required fields / duplicate similarity / A1 guard / unit fit）
- review-ready bundle exporter（審核台匯入格式）

### E. Accepted Output Adapters

- `accepted_candidates.json -> catalog_draft.json`
- `accepted_candidates.json -> backlog_seed.json`

## Milestones

1. `M1` 共用 schema 與 batch convention 定稿
2. `M2` API flow raw -> normalized -> review bundle 跑通（mock provider 可）
3. `M3` Agent flow gap + candidate + self-review spec 定稿並可產出 mock batch
4. `M4` accepted adapters（catalog/backlog）可輸出草稿
5. `M5` E2E dry run（生成 -> QA -> 審核台 -> 匯出）

## Acceptance Criteria (Framework Level)

- API 與 Agent 兩條流程都能輸出合法 `review_ready_bundle.json`
- 每筆候選都有中文摘要欄位（審核台可直接使用）
- `qa_report.json` 能列出 blocking errors 與 warnings（含 candidate_id）
- `accepted_candidates.json` 能成功轉出 `catalog_draft.json` 與 `backlog_seed.json`
- 至少完成一個示範批次 dry run（可用 mock generator）

## Gemini Handoff (Detailed Execution Plan)

本節用來直接分派給 Gemini。建議依賴順序執行，避免先做流程再回頭改 schema。

### Suggested Repo Layout (v1)

建議在 `release-aggregator` 新增以下結構（可依既有工具風格微調）：

```text
tools/content_candidate_generation/
  README.md
  bin/
    run_api_batch.dart                # AGG-GEN-005 (MVP 可先 script)
    normalize_candidates.dart         # AGG-GEN-006 / 012
    run_qa.dart                       # AGG-GEN-007
    export_review_bundle.dart         # AGG-GEN-008
    export_catalog_draft.dart         # AGG-GEN-013
    export_backlog_seed.dart          # AGG-GEN-014
  lib/
    schemas/
      candidate_schema_v1.json        # AGG-GEN-001 (JSON Schema or typed spec doc)
      generation_brief_schema_v1.json # AGG-GEN-002
      qa_report_schema_v1.json        # AGG-GEN-007
    specs/
      api_prompt_templates.md         # AGG-GEN-004
      agent_gap_analysis_spec.md      # AGG-GEN-009
      agent_generation_spec.md        # AGG-GEN-010
      agent_self_review_spec.md       # AGG-GEN-011
    src/
      models/                         # typed models if using Dart
      normalize/
      qa/
      adapters/
      utils/
  docs/
    batches/
      README.md                       # AGG-GEN-003 convention
      examples/
        sample_batch/                 # AGG-GEN-015 dry run fixture
```

如果 Gemini 不想先建 Flutter/Dart 工具，也可以先用 `Python scripts + JSON docs` 落地 v1；重點是輸出契約與 batch 結構先穩定。

## Shared Canonical Data Contract (v1)

### 1) `candidate` (canonical, review-ready compatible)

最低需求（blocker if missing）：

- `candidate_id` (string)
- `batch_id` (string)
- `candidate_type` (`lesson` | `grammar_note` | `dictionary_pack` | `path_node`)
- `target_level` (e.g. `A1`)
- `target_unit_id` (string)
- `target_position` (object; `after_lesson_id` or `before_lesson_id` or `slot`)
- `title_zh_tw` (string)
- `subtitle_zh_tw` (string)
- `can_do_zh_tw` (string[])
- `review_summary_zh_tw` (string)
- `novelty_rationale_zh_tw` (string)
- `risk_flags_zh_tw` (string[])
- `agent_recommendation` (`accept` | `revise` | `reject`)
- `scores` (object: `fit`, `novelty`, `learnability`, `reuse`, `engagement`, `cost`)
- `foreign_preview` (object or string, default collapsed in review UI)

推薦欄位（warning if missing）：

- `theme_tags`
- `skill_tags`
- `estimated_minutes`
- `grammar_focus`
- `dictionary_focus_terms`
- `production_cost` (`low` | `med` | `high`)
- `confidence`
- `source_notes`
- `qa_flags` (normalize/qa stage writes here)

### 2) `generation_brief.json`

用途：描述「這一批」要生什麼。必填建議：

- `batch_id`
- `goal`（中文）
- `target_levels`（e.g. `["A1"]`）
- `target_units`（e.g. `["A1-U2", "A1-U3"]`）
- `candidate_types`
- `count_targets`（每類目標數量）
- `variant_policy`（`none` / `3-variants`）
- `cost_preference`（`low-first` / `balanced` / `quality-first`）
- `language_policy`（中文摘要必填、外語預覽語種）
- `exclusion_rules`（避免重複主題）
- `input_snapshots`（catalog / grammar index / dictionary snapshots paths）

### 3) `qa_report.json`

結構建議：

- `batch_id`
- `generated_at`
- `summary`
  - `total_candidates`
  - `blocking_error_count`
  - `warning_count`
  - `passed_count`
- `items` (array)
  - `candidate_id`
  - `severity` (`error` | `warning`)
  - `rule_id`
  - `message_zh_tw`
  - `field_path` (optional)
  - `suggested_fix_zh_tw` (optional)

## Batch Convention (AGG-GEN-003 Detailed)

### Batch ID Naming

建議格式：

`YYYYMMDD_{level}_{units}_{types}_{run_tag}`

例：
- `20260224_A1_U2-U3_lessons_v1`
- `20260224_A1_U3_grammar-pathnodes_explore`

### Required Metadata Files Per Batch

- `generation_brief.json` (required)
- `generation_report.json` (required if generator executed)
- `candidate_packs.normalized.json` (required before QA)
- `qa_report.json` (required before review)
- `review_ready_bundle.json` (required for review station import)

## Task-by-Task Spec (for Gemini)

以下對應 `CONTENT_CANDIDATE_GENERATION_FRAMEWORK_TASKS.json`。

### AGG-GEN-001 — Shared schema v1 (canonical candidate)

**Goal**
- 定義 API/Agent 共用的 canonical candidate schema，並與審核台欄位相容。

**Deliverables**
- `tools/content_candidate_generation/lib/schemas/candidate_schema_v1.json`
- `tools/content_candidate_generation/docs/candidate_schema_v1.md`（欄位解釋 + 例子）

**Implementation Notes**
- 優先採 JSON Schema（Draft 7+）或等價 machine-readable schema。
- 明確標示 required vs optional。
- `scores.*` 請統一 0-5 integer（便於 UI 比較）。

**Acceptance**
- 能驗證至少 3 筆 sample candidate（pass）
- 缺 `title_zh_tw` 或 `can_do_zh_tw` 時驗證 fail
- 與審核台現有欄位名一致（避免 rename）

### AGG-GEN-002 — Generation brief schema v1

**Goal**
- 定義批次生成任務的輸入契約（給 API/Agent runner 用）。

**Deliverables**
- `.../schemas/generation_brief_schema_v1.json`
- `.../docs/generation_brief_examples.md`
- 至少 2 份 sample brief（lesson batch / grammar batch）

**Acceptance**
- sample brief 可通過 schema validation
- 能覆蓋 `count/variants/exclusions/cost_preference`

### AGG-GEN-003 — Batch directory convention + manifests

**Goal**
- 統一批次資料夾與輸出檔名，降低追蹤與重跑成本。

**Deliverables**
- `tools/content_candidate_generation/docs/batches/README.md`
- `docs/batches/examples/sample_batch/README.md`（示意）
- batch manifest spec（可放 `batch_manifest.json`）

**Acceptance**
- README 清楚描述 required/optional files
- sample batch 結構與命名可供照抄

### AGG-GEN-004 — API flow prompt templates

**Goal**
- 建立 API 生成用 prompt/template 規格（四種類型）。

**Deliverables**
- `.../specs/api_prompt_templates.md`
- 4 種模板：
  - `lesson`
  - `grammar_note`
  - `dictionary_pack`
  - `path_node`
- JSON output contract section（要求模型輸出欄位）

**Critical Requirements**
- 中文摘要欄位強制輸出
- 明確要求 `novelty_rationale_zh_tw`
- 明確要求 `target_position`
- 要求模型自評 `scores`

**Acceptance**
- 每種模板都附 1 組 sample input/output（可縮短）
- 模板可對應 `generation_brief` 欄位

### AGG-GEN-005 — API batch runner MVP (provider-agnostic)

**Goal**
- 讀取 `generation_brief.json`，產出 `candidate_packs.api.raw.json`（先可用 mock provider）。

**Deliverables**
- runner script / CLI (`bin/run_api_batch.dart` or python equivalent)
- `generation_report.json` output spec
- mock provider mode（無 API key 也能演示）

**Implementation Notes**
- provider-agnostic：先用 interface / adapter，不綁死單一廠商。
- 建議支援 `--dry-run`。

**Acceptance**
- 用 mock brief 可產出 raw file 與 generation report
- report 內含 batch_id、count、duration、provider、errors summary

### AGG-GEN-006 — API raw normalize adapter

**Goal**
- 將 API raw output 轉為 canonical schema（補齊欄位、統一 enum/tag）。

**Deliverables**
- normalize CLI
- `candidate_packs.normalized.json`
- normalization mapping docs（欄位對映 / default 值）

**Acceptance**
- 對缺 optional 欄位可補 default 並標 warning
- 對缺 required 欄位保留項目但標記為 QA error（不要直接吞掉）

### AGG-GEN-007 — QA rules + qa_report.json

**Goal**
- 自動檢查欄位完整性、重複度、A1 難度風險、中文摘要存在性等。

**Deliverables**
- `qa_report_schema_v1.json`
- QA rules spec doc（rule IDs + severity）
- QA runner CLI
- `qa_report.json`

**Required Rules (v1)**
- `REQ_FIELD_MISSING`
- `ZH_SUMMARY_MISSING`
- `CAN_DO_EMPTY`
- `TARGET_POSITION_INVALID`
- `DUP_TITLE_SIMILARITY_HIGH`
- `DUP_THEME_OVERLAP_HIGH`
- `LEVEL_A1_COMPLEXITY_RISK`
- `UNIT_FIT_LOW_CONFIDENCE`

**Acceptance**
- `qa_report.json` 可列出 candidate_id + 中文訊息
- 規則可區分 `error` / `warning`

### AGG-GEN-008 — Review-ready bundle exporter

**Goal**
- 產出可直接匯入審核台的 `review_ready_bundle.json`。

**Deliverables**
- exporter CLI
- bundle spec doc

**Bundle Shape (suggested)**
- `bundle_version`
- `batch_id`
- `generated_at`
- `items` (canonical candidates + qa summary snippets)

**Acceptance**
- 審核台可成功匯入（至少用 mock review station payload 驗證）
- items 內欄位符合審核台現行需求

### AGG-GEN-009 — Agent gap analysis spec + schema

**Goal**
- 定義 Agent 找缺口的輸出格式與方法，輸出中文報告。

**Deliverables**
- `.../specs/agent_gap_analysis_spec.md`
- `gap_report.schema.json`（可選，但建議）
- sample `gap_report.json`

**Gap Dimensions (v1)**
- 單元節點密度
- 情境覆蓋缺口
- 技能覆蓋缺口
- 文法站內容缺口
- 回聲站/複習內容缺口

**Acceptance**
- sample gap report 能對應至少 3 個具體缺口
- 每個缺口都有 priority 與建議候選類型

### AGG-GEN-010 — Agent generation spec (Chinese-first)

**Goal**
- 定義 Agent 如何根據 gap report + brief 產生高品質候選。

**Deliverables**
- `.../specs/agent_generation_spec.md`
- prompt/checklist（若用 markdown spec 即可）
- sample agent raw output（含中文摘要欄位）

**Required Fields in Agent Raw**
- canonical required fields 或可映射欄位
- `review_summary_zh_tw`
- `novelty_rationale_zh_tw`
- `risk_flags_zh_tw`
- `agent_recommendation`

**Acceptance**
- 可從 spec 產出 1 批 mock candidates
- 中文摘要足以讓不懂外語的人做初審

### AGG-GEN-011 — Agent self-review spec

**Goal**
- 定義 Agent 第二輪自審格式（不是生成完直接丟審核台）。

**Deliverables**
- `.../specs/agent_self_review_spec.md`
- self-review checklist + scoring policy
- sample reviewed output

**Review Dimensions**
- 語言自然度
- 難度符合度（A1 guard）
- 教學可操作性（can-do 是否具體）
- 與現有內容重複度
- 製作成本 / 依賴素材風險

**Acceptance**
- 每筆候選都能產出中文建議決策與修稿說明

### AGG-GEN-012 — Agent raw normalize adapter

**Goal**
- 將 agent raw / self-reviewed outputs 正規化為 canonical schema。

**Deliverables**
- normalize adapter（可共用 AGG-GEN-006 核心）
- mapping docs（agent-specific fields -> canonical）

**Acceptance**
- 能處理 agent 額外欄位（保留到 `source_notes` 或 `meta`）
- 產出結果可直接進 QA

### AGG-GEN-013 — Accepted adapter (catalog draft)

**Goal**
- 把審核台匯出的 `accepted_candidates.json` 轉成 `catalog_draft.json` 草稿。

**Deliverables**
- exporter CLI
- `catalog_draft.schema.json`（或 doc）
- mapping spec（candidate -> catalog metadata）

**Minimum Mapping**
- title/subtitle
- unit/position
- can-do
- estimated time
- tags
- grammar focus / dictionary focus (if present)

**Acceptance**
- 對 1 份 sample accepted file 可產生合法 draft
- 缺欄位項目會在 output 或 report 中標示，不 silent fail

### AGG-GEN-014 — Accepted adapter (backlog seed)

**Goal**
- 把 `accepted_candidates.json` 轉成 backlog seed（供 task/agent 後續實作）。

**Deliverables**
- exporter CLI
- `backlog_seed` format doc + sample

**Suggested Output Fields**
- `seed_id`
- `candidate_id`
- `work_type`（lesson/grammar/dict/path-node）
- `priority`
- `suggested_tasks`（list）
- `dependencies`
- `notes_zh_tw`

**Acceptance**
- 可由 accepted candidates 自動產出可讀 backlog seed

### AGG-GEN-015 — End-to-end dry run

**Goal**
- 完成一次示範批次，驗證雙流程框架至少一條可跑通，並測試審核台銜接。

**Deliverables**
- `docs/batches/examples/sample_batch/` 完整樣本
- dry-run report（markdown）
- 問題清單與下一步

**Recommended Scope**
- `A1` `1 unit`
- `lesson + grammar_note` 兩類即可
- 先用 mock API provider + mock/templated agent output

**Acceptance**
- 生成 -> normalize -> QA -> review bundle -> review station import -> accepted adapter 至少走通一次
- 列出阻塞點與技術債（中文）

### AGG-GEN-016 — Multilingual curriculum architecture blueprint (lllo)

**Goal**
- 規劃 `lllo` 的多語系課程內容目錄與資料分層，支援「中文學各種語言」先行，後續再擴充其他 learner locale。

**Deliverables**
- `docs/architecture/multilingual_curriculum_blueprint.md`（可先放在 `release-aggregator/docs/` 草案）
- `core` vs `pedagogy overlay` 欄位切分表（lesson / grammar / dictionary / path node）
- `lllo` 目錄草案（`target_language` × `learner_locale`）

**Required Decisions**
- `target_language` 與 `learner_locale` 分離（不可把每個組合複製成獨立課程）
- `zh-TW` 作為第一個 pedagogy overlay source-of-truth
- accepted candidate 如何映射到 `core` 與 `pedagogy/zh-TW`

**Acceptance**
- 至少涵蓋 `ko` + `zh-TW` 的完整樣例路徑
- 能解釋未來新增 `en` learner locale 時哪些檔案可重用、哪些要翻譯

### AGG-GEN-017 — Curriculum learning-loop design (Immersion + Spaced Review + Structured)

**Goal**
- 定義課程骨架與內容節奏，讓候選生成不只補素材，而是補到正確的學習環節。

**Deliverables**
- `docs/tasks/AGG_GEN_017_CURRICULUM_LEARNING_LOOP_SPEC.md`（正式規格草案，含 survival blueprint 與 A1 sample）
- 課程設計規格（單元內學習循環、跨單元複習節奏）
- candidate taxonomy 對應表（`lesson / grammar_note / dictionary_pack / path_node` 各自扮演角色）
- review/QA 需要檢查的教學結構欄位清單（例如 pattern focus, review timing hints）

**Design Requirements**
- 同時覆蓋三種學習模式：
  - 沉浸式學習（情境輸入/輸出）
  - 間歇複習（spaced repetition / retrieval）
  - 結構化學習（常用句型 / 文法規則）
- 明確定義單元內每一階段的目的、輸入與輸出
- 定義哪些 candidate type 可作為複習內容、哪些只適合首次引入

**Acceptance**
- 提供至少 1 個 `A1` 單元的樣例流程（含 lesson/grammar/review 節點）
- 可直接反推 generation brief 的欄位需求與 count targets

### AGG-GEN-018 — Schema/brief extensions for multilingual pedagogy + review cadence metadata

**Goal**
- 擴充 canonical candidate 與 generation brief，使其可表達多語系教學 overlay 與複習節奏資訊。

**Deliverables**
- schema patch spec（或直接更新 v1.1 schema）：
  - `target_language`
  - `learner_locale_source`
  - `localization_targets`（optional）
  - review cadence hints（e.g. `review_window_days`, `revisit_after_units`）
  - structure tags（常用句型/文法/情境角色）
- generation brief example（含 `zh-TW -> en` 後續 localize 規劃）

**Acceptance**
- API/Agent specs 可引用新欄位而不破壞 v1 審核流程
- review bundle exporter 能明確說明哪些欄位保留給審核台、哪些欄位為 metadata

## Dependency Order (Gemini Assignment Suggestion)

建議分配順序（可平行的已標示）：

1. `AGG-GEN-001` + `AGG-GEN-002`（可平行）
2. `AGG-GEN-003`
3. `AGG-GEN-004`
4. `AGG-GEN-005` → `AGG-GEN-006`
5. `AGG-GEN-007` → `AGG-GEN-008`
6. `AGG-GEN-016` + `AGG-GEN-017`（課程架構/內容策略先定）
7. `AGG-GEN-018`（回寫 schema/brief 擴充）
8. `AGG-GEN-009` + `AGG-GEN-010` + `AGG-GEN-011`（規格類可平行）
9. `AGG-GEN-012`
10. `AGG-GEN-013` + `AGG-GEN-014`（可平行）
11. `AGG-GEN-015`

## What You (PM/Product, Chinese-only) Should Review

你不需要逐句看外語，請只看以下輸出（中文）：

- `generation_brief.json`（這批目標是否正確）
- `gap_report.json`（缺口優先順序是否合理）
- `qa_report.json` summary（有沒有太多 blocker）
- `review_ready_bundle.json` 中每筆的中文摘要與風險
- `backlog_seed.json`（是否符合你想派工的粒度）

## Definition of Done (Practical)

達到以下條件就可以開始常態使用：

- 審核台可以穩定匯入 `review_ready_bundle.json`
- 你能完成一批中文審核並匯出 `accepted_candidates.json`
- adapter 可產生 `catalog_draft.json` 與 `backlog_seed.json`
- 下一位 agent / Gemini 能不靠口頭說明，直接照 plan + tasks 開工
