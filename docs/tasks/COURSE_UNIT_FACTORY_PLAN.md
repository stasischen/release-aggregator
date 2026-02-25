# COURSE_UNIT_FACTORY — Course Unit Production Pipeline Plan

## Goal

將目前已完成的課程 mockup framework（`AGG-GEN`）從「單元示範能力」升級為「可量產單元能力」：

- 有固定的 unit blueprint 契約與骨架
- 有 scaffold 工具可快速生成新單元 skeleton
- 有 fixture lint / mockup-check 在 PM 試玩前攔錯
- 有 modular viewer 可切換多單元進行批次審看
- 有 agent 可執行的量產作業流程（author -> lint -> PM review -> fix -> freeze）

## Context (Current State)

來自已完成並封存的 `CONTENT_CANDIDATE_GENERATION_FRAMEWORK`：

- `A1-U04` 完整 playable unit fixture + HTML mockup 已完成
- modular viewer 已存在（`docs/tasks/mockups/modular/`）
- multi-unit fixture index 已存在（`docs/tasks/mockups/modular/data/fixtures.json`）
- 第二單元 `A1-U05` fixture 已存在但仍為 scaffold/demo 級（節點數不足、非量產-ready）
- `validate_mockup_fixture.py` 仍偏單 fixture / A1-U04 導向

因此下一階段重點不是再做策略 demo，而是建立「量產工廠」。

## Scope

### In Scope

- `unit_blueprint` 契約與模板化
- fixture scaffold 與 QA/lint
- modular viewer 的多單元驗證流程
- PM 試玩與 acceptance checklist（多單元）
- agent 派工與交付流程文件化

### Out of Scope

- learner app（`lingo-frontend-web`）實作整合
- candidate generation API/Agent 流程再設計（已在 AGG-GEN 完成）
- production-grade auto scoring / AI feedback

## Success Criteria (Production Readiness for Units)

達到以下條件視為「開始能量產課程」：

1. 新單元 skeleton 可由一條命令生成（非手工複製 `A1-U04`）
2. 新 fixture 可跑統一 `mockup-check`
3. PM 可在 modular viewer 切換至少 3 個單元 fixture 試玩
4. 每個單元都有一致的最低骨架（不是有人做 3 節點、有人做 12 節點）
5. agent 可照 playbook 執行，不需口頭補規則

## Task Breakdown

### UNITFAC-001 — Freeze unit_blueprint v0.1 contract proposal

**Goal**
- 將教育優化欄位提案（來自 `AGG-GEN-027`）整理成 `unit_blueprint v0.1` 契約草案，並定義與 `v0` 的向下相容策略。

**Deliverables**
- `docs/tasks/UNITFAC_001_UNIT_BLUEPRINT_V0_1_CONTRACT.md`
- 欄位增補提案（例如 `learning_objective_type`, `retrieval_target`, `difficulty_scaffold_level`, `transfer_pattern_refs`）
- migration notes（`v0` fixture 可如何漸進補欄位）

**Acceptance**
- `v0` fixture 不需立即改動仍可運作
- 能明確標示 canonical key 與 optional metadata
- 後續 `UNITFAC-003/005` 可直接引用

### UNITFAC-002 — Complete A1/A2 unit skeleton spec

**Goal**
- 定義「量產-ready」的 A1/A2 單元最低節點骨架與 sequencing 規則。

**Deliverables**
- `docs/tasks/UNITFAC_002_A1_A2_UNIT_SKELETON_SPEC.md`
- 最低節點集合（input/structure/output/review/followups）
- 必要分布規則（至少一個 non-dialogue input、至少一個 review retrieval、至少一個 guided output 等）

**Acceptance**
- 可以用來判定某 fixture 是否只是 demo / 還是量產-ready
- `A1-U04` 能映射到該 spec
- `A1-U05` 可據此補齊成完整單元

### UNITFAC-003 — Scaffold generator for full unit fixtures

**Goal**
- 做出真正可用的 unit scaffold 工具，生成完整 skeleton（非 3-node demo）。

**Deliverables**
- `scripts/scaffold_unit_blueprint.py`（或等效）
- 支援輸入：`unit_id`, `theme`, `level`, `target_language`, `learner_locale_source`
- 輸出：完整 unit skeleton fixture（符合 `UNITFAC-002`）

**Acceptance**
- 一條命令生成新單元 fixture
- 生成結果可通過 JSON parse
- 可接 `UNITFAC-004` 的 lint/check

### UNITFAC-004 — Unified mockup-check (multi-fixture lint)

**Goal**
- 將 fixture 驗證從單 fixture 腳本升級為多 fixture、可批次跑的統一檢查命令。

**Deliverables**
- `scripts/mockup_check.py` 或 `scripts/validate_mockup_fixture.py` 擴充版
- 支援輸入單檔 / 目錄 / fixtures index
- 檢查項目：
  - schema syntax / JSON syntax
  - mixed-script typo
  - legacy alias drift
  - unsupported `content_form` / `output_mode`
  - mode-specific payload key presence（lightweight）
  - bilingual list length mismatch
  - `UNITFAC-002` skeleton completeness（warning 或 error）

**Acceptance**
- 可對 `A1-U04` + `A1-U05` 同時跑
- 錯誤輸出包含 `node_id` / path
- PM 或 agent 在提交前可快速執行

### UNITFAC-005 — Authoring template pack (fixture production)

**Goal**
- 為人類與 agent 提供一致的 fixture 填寫模板與 QA checklist，避免 payload 欄位與教學結構漂移。

**Deliverables**
- `docs/tasks/UNITFAC_005_AUTHORING_TEMPLATES.md`
- payload templates（按 `content_form` / `output_mode`）
- bilingual requirements checklist
- educational QA checklist（來自 `AGG-GEN-027`）

**Acceptance**
- 新作者可在不讀完整 AGG-GEN archive 的情況下填 fixture
- 模板清楚區分「必填 / 可後補 / 常見錯誤」

### UNITFAC-006 — Pilot production: A1-U05 full unit fixture

**Goal**
- 使用新 skeleton、模板與 lint，將 `A1-U05` 從 scaffold/demo 級補齊為完整 playable unit fixture。

**Deliverables**
- 更新 `docs/tasks/mockups/a1_u05_unit_blueprint_v0.json`（或 v0.1）
- PM 可在 modular viewer 試玩 `A1-U05`
- pilot 生產紀錄（簡短）

**Acceptance**
- `A1-U05` 達到 `UNITFAC-002` 最低骨架
- 通過 `UNITFAC-004` mockup-check
- 與 `A1-U04` 在 viewer 中可切換試玩

### UNITFAC-007 — Multi-unit PM trial flow + acceptance checklist

**Goal**
- 定義 PM 以 modular viewer 驗證多單元品質的一致流程。

**Deliverables**
- `docs/tasks/UNITFAC_007_MULTI_UNIT_PM_TRIAL_GUIDE.md`
- 測試路徑（至少 `A1-U04`, `A1-U05`, +1 unit）
- acceptance checklist（內容結構/互動可用性/TTS/狀態保存/切換隔離）

**Acceptance**
- PM 可在 15-20 分鐘內完成多單元抽查
- 能快速指出是資料問題、renderer 問題、還是 interaction 問題

### UNITFAC-008 — Batch production playbook (agent assembly line)

**Goal**
- 將單元量產流程標準化成 agent assembly line。

**Deliverables**
- `docs/tasks/UNITFAC_008_BATCH_PRODUCTION_PLAYBOOK.md`
- 角色分工（Author / Lint-QA / PM Review / Fixer / Freeze）
- 交付節點與 commit 規範
- 回報模板引用（可沿用 `AGG-GEN-021`）

**Acceptance**
- 兩位以上 agent 可平行生產不同單元而不互踩規則
- PM 只看 checklist 與 viewer 就能做初審

## Recommended Execution Order

最快看到量產效果的順序（工具先、pilot 再）：

1. `UNITFAC-003` + `UNITFAC-004`（可平行）
2. `UNITFAC-002`
3. `UNITFAC-005`
4. `UNITFAC-006`（A1-U05 pilot）
5. `UNITFAC-007`
6. `UNITFAC-001`（contract freeze，吸收 pilot learnings）
7. `UNITFAC-008`

> 註：若你想先穩定欄位再做工具，也可把 `UNITFAC-001` 提前；但以回饋速度來看，先做 pilot 較划算。

## Agent Assignment Suggestion

- `Stream P1`：`UNITFAC-003` scaffold generator
- `Stream P2`：`UNITFAC-004` mockup-check hardening
- `Stream P3`：`UNITFAC-002` skeleton spec + `UNITFAC-005` authoring template
- `Stream P4`：`UNITFAC-006` A1-U05 pilot production
- `Stream P5`：`UNITFAC-007` PM trial guide + `UNITFAC-008` playbook

## Dependencies on Archived AGG-GEN Outputs

Primary references:

- `docs/tasks/archive/20260225_CONTENT_CANDIDATE_GENERATION_FRAMEWORK_PLAN.md`
- `docs/tasks/archive/20260225_CONTENT_CANDIDATE_GENERATION_FRAMEWORK_TASKS.json`
- `docs/tasks/mockups/a1_u04_unit_blueprint_v0.json`
- `docs/tasks/mockups/modular/`
- `docs/tasks/AGG_GEN_021_AGENT_WORK_ORDER_TEMPLATES.md`（若已歸檔/搬移，需在本 task 內再引用或複製必要模板）
- `docs/tasks/content_candidate_generation/AGG_GEN_027_EDUCATIONAL_FLOW_OPTIMIZATION_REVIEW.md`

## Definition of Done (This Task)

`COURSE_UNIT_FACTORY` 可封存的條件：

- 至少 1 個新單元（`A1-U05`）由 scaffold + template + lint 流程完整生產完成
- modular viewer 可切換至少 3 個單元 fixture
- `mockup-check` 成為固定交付前檢查
- PM 可用 multi-unit checklist 快速抽查
- batch production playbook 可供後續 agent 持續量產單元
