# COURSE_PEDAGOGY_OPTIMIZATION — Language Learning Quality Optimization Plan

## Goal

在既有 `COURSE_UNIT_FACTORY`（單元量產工廠）基礎上，針對語言學習成效做第二層優化，重點不是增加更多內容型態，而是提升：

- 理解檢查品質（不只資訊提取）
- 變體/遷移練習品質（不只換字）
- 修復策略練習（repair as interaction strategy）
- 檢索複習精度（form vs function retrieval）
- Guided output 完成標準一致性
- Followup / transfer 的教學明確性

本計畫的產出將回寫到：

- `UNITFAC-001`（contract freeze）
- `UNITFAC-004`（mockup-check）
- `UNITFAC-005`（authoring templates）
- `UNITFAC-007`（PM trial checklist）

## Why Now

目前流程已具備量產能力雛形：

- scaffold (`UNITFAC-003`)
- lint/check (`UNITFAC-004`)
- authoring templates (`UNITFAC-005`)
- pilot unit (`UNITFAC-006`)
- PM multi-unit trial guide (`UNITFAC-007`)
- batch playbook (`UNITFAC-008`)

現在最值得投入的是「教育品質標準化」，否則量產後容易出現：

- 看起來結構完整，但理解檢查弱
- output 練習多但遷移價值低
- review 有做但只在練翻譯
- PM 無法一致判斷教學品質

## Scope

### In Scope

- pedagogical metadata / rubric / taxonomy 規格
- authoring templates 與 QA checklist 的教育向補強
- mockup-check 的教育向 warning/blocker 候選
- PM review checklist 的教育向補強
- 在 `A1-U04/A1-U05`（或下一批 PR-ready units）做小規模驗證

### Out of Scope

- learner app production UI redesign
- AI 自動評分模型設計
- 聲學/ASR 系統（錄音評分）
- 大幅重構 viewer architecture

## Success Criteria

達到以下條件即可視為本 task 成功：

1. 教育優化點已從口頭建議轉成可執行規格（field/rule/template）
2. authoring template 明確要求：comprehension type / transform type / repair category / retrieval target / guided rubric / followup goal type
3. mockup-check 能至少以 warning 形式提示缺失（不一定全部 blocker）
4. PM 可在 trial 中區分「結構完成」與「教學品質偏弱」兩種問題
5. `UNITFAC-001` freeze 時能明確決定哪些欄位納入 v0.1、哪些延後

## Design Principles (Pedagogy)

1. **Input 不等於看過**
- comprehension check 應驗證理解類型，而非只有資訊提取。

2. **Transform 不等於換名詞**
- 變體練習必須包含語用或情境轉換，才能提升遷移能力。

3. **Repair 是策略，不是句庫**
- 練習要同時訓練「何時 repair」與「怎麼 repair」。

4. **Review 要分 form 與 function**
- survival 場景需要反應回收，不只是句子翻譯。

5. **Guided output 要有完成標準**
- 不做自動評分也要有人工/自評 rubric，避免「寫了就算完成」。

6. **Followup 要有遷移任務，而非提醒**
- `+1` / `+3` 應有清楚的 review/transfer 角色與 pattern refs。

## Task Breakdown

### PEDOPT-001 — Comprehension check taxonomy + payload spec

**Goal**
- 將 comprehension_check 從「泛用理解題」細分為可設計、可審、可檢查的題型 taxonomy。

**Deliverables**
- `docs/tasks/PEDOPT_001_COMPREHENSION_CHECK_SPEC.md`
- 題型定義（建議至少）：
  - `info_extract`
  - `intent`
  - `next_response`
  - `sequence`
- payload 範例（A1/A2）
- 作者常見錯誤與 PM 評估要點

**Acceptance**
- 作者能用 spec 設計至少兩種不同 comprehension 題型
- PM 可看出 comprehension 是否只靠中文對照即可作答

### PEDOPT-002 — Transform practice spec

**Goal**
- 明確定義 `pattern_transform` 的教育目標與題型，避免退化成單純換詞。

**Deliverables**
- `docs/tasks/PEDOPT_002_TRANSFORM_PRACTICE_SPEC.md`
- transform types（建議）：
  - `slot`
  - `scenario`
  - `function`
  - `politeness`
  - `correction`
- A1/A2 範例（咖啡廳 / 藥局 / 旅館）

**Acceptance**
- `UNITFAC-005` 模板可引用 transform type
- PM 可分辨「換字題」與「真遷移題」

### PEDOPT-003 — Repair strategy practice spec

**Goal**
- 將 repair practice 由句子背誦升級為互動策略訓練。

**Deliverables**
- `docs/tasks/PEDOPT_003_REPAIR_STRATEGY_SPEC.md`
- trigger recognition + repair response 設計框架
- repair categories：
  - `repeat`
  - `slow_down`
  - `rephrase`
  - `confirm`
  - `reject_replace`

**Acceptance**
- 模板可要求每單元至少一個 repair micro-node
- PM checklist 能判斷 repair 是否有策略性

### PEDOPT-004 — Review retrieval target spec

**Goal**
- 定義 `retrieval_target`（form/function/mixed），提升 review 設計品質與可檢查性。

**Deliverables**
- `docs/tasks/PEDOPT_004_RETRIEVAL_TARGET_SPEC.md`
- retrieval target 定義與 examples
- unit placement 指引（same-day / +1 / +3）

**Acceptance**
- review node 可標示回收的是表達形式還是情境反應
- 後續可回寫 `UNITFAC-001` contract freeze

### PEDOPT-005 — Guided output completion rubric spec

**Goal**
- 為 guided speaking/writing 建立完成標準與自評/人工審查 rubric（非 AI 自動評分）。

**Deliverables**
- `docs/tasks/PEDOPT_005_GUIDED_OUTPUT_RUBRIC_SPEC.md`
- rubric 結構：
  - task completion condition
  - required elements
  - acceptable variants note
  - common mistakes (zh-TW)
- A1/A2 範例

**Acceptance**
- PM 與作者對「完成」有一致標準
- 可被 `UNITFAC-005` 模板引用

### PEDOPT-006 — Dictionary pack production-readiness tags

**Goal**
- 強化 dictionary_pack 的「可產出性」，避免只變成名詞清單。

**Deliverables**
- `docs/tasks/PEDOPT_006_DICTIONARY_PRODUCTION_TAGS_SPEC.md`
- 建議欄位：
  - `production_status` (`production_ready` / `input_only`)
  - `frame_refs`
  - `register_hint`
- 作者與 PM 使用說明

**Acceptance**
- 至少可幫助區分「可直接拿來說」與「先看懂即可」詞塊

### PEDOPT-007 — Followup semantics spec (review vs transfer)

**Goal**
- 將 `scheduled_followups` 的語義從時間提醒提升為教學任務（review vs transfer）。

**Deliverables**
- `docs/tasks/PEDOPT_007_FOLLOWUP_SEMANTICS_SPEC.md`
- followup goal types：
  - `review`
  - `transfer`
- `transfer_pattern_refs` 與 `transfer_task_hint_zh_tw` 用法

**Acceptance**
- PM 可判斷 followup 是否有實際遷移目標
- 後續可納入 `UNITFAC-001` freeze 提案

### PEDOPT-008 — Listening discrimination micro-node proposal (optional)

**Goal**
- 提出 survival 導向的最小聽辨節點設計（配合現有 TTS），不進入完整語音評分。

**Deliverables**
- `docs/tasks/PEDOPT_008_LISTENING_MICRO_NODE_PROPOSAL.md`
- 節點用途與 payload 概念（可選）
- 適合 A1/A2 的 bottleneck 類型（數字/時間/高頻尾句等）

**Acceptance**
- 明確標示為 optional（不阻塞量產）
- 不要求 ASR/自動評分依賴

### PEDOPT-009 — Integrate pedagogy metadata into contracts/templates/checkers

**Goal**
- 將教育優化點落到現有工廠流程：contract / authoring template / mockup-check。

**Deliverables**
- 整合提案文件：
  - `docs/tasks/PEDOPT_009_INTEGRATION_PATCH_PLAN.md`
- 明確 mapping：
  - `UNITFAC-001`（哪些欄位納入 v0.1）
  - `UNITFAC-005`（哪些模板欄位新增）
  - `UNITFAC-004`（哪些 warning/blocker 規則新增）

**Acceptance**
- 不再只有 pedagogy spec 文件，能直接影響量產流程

### PEDOPT-010 — Pilot application + review

**Goal**
- 在實際單元上驗證部分 pedagogical upgrades（建議 `A1-U04/A1-U05` 或下一批 PR-ready 單元）。

**Deliverables**
- `docs/tasks/PEDOPT_010_PILOT_APPLICATION_REVIEW.md`
- 實作/套用紀錄（哪些欄位/節點更新）
- before/after 教學品質觀察（PM/作者角度）

**Acceptance**
- 至少證明 2-3 個規格不是紙上談兵
- 有可回寫到 freeze 的經驗結論

### PEDOPT-011 — PM educational QA checklist v2

**Goal**
- 將教育品質判準正式整合到 PM trial checklist，讓 PM 不只看「能不能播/能不能點」。

**Deliverables**
- `docs/tasks/PEDOPT_011_PM_EDU_QA_CHECKLIST_V2.md`
- 與 `UNITFAC-007` 的對接說明（可整合或引用）
- issue triage labels（教學設計 vs 資料 vs renderer）

**Acceptance**
- PM 可一致回報教育品質問題，不只 UI/資料錯誤

### PEDOPT-012 — Freeze readiness recommendation for UNITFAC-001

**Goal**
- 基於前面規格與 pilot，判定哪些 pedagogy fields/rules 可納入 `UNITFAC-001` freeze，哪些延後。

**Deliverables**
- `docs/tasks/PEDOPT_012_FREEZE_READINESS_RECOMMENDATION.md`
- freeze-ready vs defer matrix
- 風險與後續迭代建議

**Acceptance**
- `UNITFAC-001` 可直接用此文件做決策，不需再靠口頭討論

## Recommended Execution Order

先規格化高影響項，再做整合與 pilot：

1. `PEDOPT-001` + `PEDOPT-002` + `PEDOPT-003`（可平行）
2. `PEDOPT-004` + `PEDOPT-005` + `PEDOPT-007`（可平行）
3. `PEDOPT-006`（可平行於上）
4. `PEDOPT-009`（整合到 UNITFAC contracts/templates/checkers）
5. `PEDOPT-011`（PM 教學 QA checklist v2）
6. `PEDOPT-010`（pilot application）
7. `PEDOPT-012`（freeze readiness recommendation）
8. `PEDOPT-008`（optional, 可插隊或延後）

## Integration Targets (Where These Changes Land)

### UNITFAC-001 (contract freeze)

候選欄位（視 `PEDOPT-012` 結論納入）：

- `comprehension_check.question_type`
- `transform_type`
- `repair_category`
- `retrieval_target`
- `guided_output_rubric`
- `followup_goal_type`
- `transfer_pattern_refs`

### UNITFAC-004 (mockup-check)

先從 warning 開始的候選規則：

- missing comprehension type diversity
- transform node missing `transform_type`
- repair node missing trigger/repair categorization
- review node missing `retrieval_target`
- guided node missing completion rubric metadata
- followup missing review/transfer semantics

### UNITFAC-005 (authoring templates)

新增模板欄位與作者提示：

- 題型/類型標籤
- 常見錯誤提示欄
- 可接受變體說明欄
- followup 目標清晰化欄

### UNITFAC-007 (PM trial guide)

擴充 PM checklist，加入：

- comprehension quality
- transform transfer value
- repair strategy realism
- review retrieval target alignment
- guided output completion clarity

## Definition of Done

`COURSE_PEDAGOGY_OPTIMIZATION` 可封存條件：

1. 高優先度 pedagogy specs（至少 `001/002/003/004/005/007`）完成
2. 已有整合計畫（`PEDOPT-009`）指向 UNITFAC contracts/templates/checkers
3. PM educational QA checklist v2 完成（`PEDOPT-011`）
4. 至少一輪 pilot 套用與 review 完成（`PEDOPT-010`）
5. `PEDOPT-012` 可支援 `UNITFAC-001` freeze 決策

## Notes

- 本 task 以「教育品質標準化」為主，不要求立即全部轉成 blocker 規則。
- 建議採 warning-first：先建立作者與 PM 習慣，再視穩定度升級為 blocker。
