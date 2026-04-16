# Knowledge Lab Content Normalization Plan (V1)

## 1. Overview

本計畫旨在將目前 `content-ko` 中尚處於遷移過渡期 (Migration-era) 的 Knowledge Lab 內容，標準化為 V1 Frozen Spec 所定義的規範。

核心目標是從 **item-local** 型態轉向 **canonical reusable** 型態，並提升 Markdown 的互動性。

---

## 2. Normalization Buckets

所有現有 Knowledge Lab 內容需歸類至以下四個 Bucket，並依序處理：

### Bucket A: Already Canonical
*   **特徵**：Core JSON 已使用 `example_sentence_refs`；I18n Markdown 已符合 [Markdown Profile](../guides/KNOWLEDGE_LAB_MARKDOWN_PROFILE_V1.md)。
*   **範例**：`kg.grammar.particle.*` (大多數助詞)。
*   **處理**：維持原樣，僅需定期做 integrity check。

### Bucket B: Pending Decoupling (High Priority)
*   **特徵**：I18n JSON 仍含有 `example_bank` 陣列。
*   **範圍**：共 14 個項目，分布於 `connector/` 下的各子目錄 (cause, condition, contrast, conversion, sequence)。
*   **處理**：
    1.  將 `example_bank` 內容提取至全域 `example_sentence` 銀行。
    2.  在 Core JSON 中移除 `example_bank`（若有）並改用 `example_sentence_refs`。
    3.  刪除 I18n JSON 中的 `example_bank` 欄位。

### Bucket C: Markdown Enrichment (Medium Priority)
*   **特徵**：`explanation_md_zh_tw` 中含有與教學直接相關的純文字例句、變體示範、或對話片段。
*   **典型模式**：
    -   `(例: 비가 왔어요. 그래서 우산을 썼어요.)` -> 完整且具備重用價值的句子。
    -   `가다 → 가요` -> 形態變化對照。
    -   `A: ... B: ...` -> 語境對話片段。
*   **處理與導向**：
    1.  **Reusable Full Sentences**: 應優先提取至全域 `example_sentence` 銀行，並由 Core JSON 的 `example_sentence_refs` 承接。不可將完整句子長期僅保留在 Markdown 的 inline chips 中。
    2.  **Fragments / Morphology**: 短片段或純變形對照，轉換為 **Inline Sentence Chips**：`[ko:韓文原文|zh:中文翻譯]`。
    3.  **Ambiguous / Mixed Dialogues**: 涉及對話、語境極強的短句，標記為 `Manual Review`，視情況保留為純 Markdown 或手動處理。

### Bucket D: Legacy I18n Cleanup (Low Priority)
*   **特徵**：全域 `example_sentence` 銀行中的 I18n 檔案仍使用舊版欄位。
*   **範圍**：共 11 個項目，皆位於 `ex.ko.ending.*` 分類。
*   **處理**：
    1.  **Core Parity Check**: 在進行 I18n 欄位重新命名 (Rename) 前，必須先確認對應的 Core 檔案存在。
    2.  **Orphan Handling**: 若為孤兒資料 (I18n 存在但 Core 缺失)，應轉由 `Manual Review` 處理，不執行自動化 Normalization。
    3.  **Rename**: 將欄位名稱 `zh_tw` 重新命名為 `translation_zh_tw`。

---

## 3. Detailed Inventory (Snapshot)

### 3.1 Bucket B (Pending Decoupling) - 14 Items
- `connector/cause`: `geuraeseo`, `geureomeuro`, `geureonikka`, `ttaraseo`
- `connector/condition`: `geureomyeon`
- `connector/contrast`: `geuraedo`, `geureochiman`, `geureona`, `geureonde`, `hajiman`
- `connector/conversion`: `geurende` (shared with contrast)
- `connector/sequence`: `geurigo`, `geurigo_naseo`, `geuriseo`

### 3.2 Bucket D (Legacy Schema) - 11 Files
- `ex.ko.ending.additive.smart_kind.v1.json`
- `ex.ko.ending.cause.rain_umbrella.v1.json`
- `ex.ko.ending.clarification.as_you_know.v1.json`
- `ex.ko.ending.comparison.water_money.v1.json`
- `ex.ko.ending.condition.parent_heart.v1.json`
- `ex.ko.ending.contrast.trash_regret.v1.json`
- `ex.ko.ending.contrast.weather_gloom.v1.json`
- `ex.ko.ending.emotion.dog_snack.v1.json`
- `ex.ko.ending.restriction.alcohol_drunk.v1.json`
- `ex.ko.ending.state_change.cold_weather.v1.json`
- `ex.ko.ending.state_retention.shoe_in.v1.json`

---

## 4. Normalization Rules & Constraints

### 4.1 Extraction (Bucket B -> Global Bank)
- **ID Pattern**: 使用 `ex.ko.[category].[subcategory].[desc].v1`。
- **Provenance**: `source_type` 設為 `knowledge_item_extraction`，並填寫 `original_ki_ref`。
- **Clean String**: 移除所有 Markdown 標記，僅保留純韓文 `surface_ko`。

### 4.2 Markdown Normalization (Bucket C)
- **Inline Chips**: 優先處理長度大於 2 個單詞的片段。
- **No HTML**: 絕對禁止使用 `<b>` 或 `<span>`。
- **Headings**: 確保使用 `###` 配合 Bento UI Emoji (📐, ⚠️, 💬)。

---

## 5. Implementation Roadmap

1.  **Phase 1: Dry-run `kg-mig-010`**
    - 針對 Bucket B 進行模擬提取。
    - 產出 Extraction Manifest 並人工核對 ID 命名。
2.  **Phase 2: Execution `kg-mig-010`**
    - 正式將例句寫入全域銀行。
    - 同步更新 Knowledge Item 為 `example_sentence_refs`。
3.  **Phase 3: Markdown Enrichment (Two-pass Process)**
    - **Pass 1 (Scan & Propose)**: 使用腳本掃描 `explanation_md_zh_tw` 中的例句模式，產出待審核清單 (Candidate Manifest)。不可直接以 Regex 判斷結果寫回正式檔案。
    - **Pass 2 (Review & Apply)**: 人工/Agent 審核清單後，再執行核准項目的批次替換。
4.  **Phase 4: Manual Polish & Contextual Fragments**
    - 處理 Ambiguous 項目（如對話片段 `A: ... B: ...`）或需精細標註的形態變化。

---

## 6. Acceptance Criteria

### 6.1 Planning Phase Acceptance (Current)
- [ ] **Inventory complete**: 清楚列出待處理的 Bucket B 項目與 Bucket D 檔案。
- [ ] **Buckets defined**: 內容特徵與處理邏輯符合 V1 Frozen Spec（區分 Global Refs 與 Inline Chips）。
- [ ] **Batch order defined**: 優先序符合工程依賴關係（B -> D -> C）。
- [ ] **Dry-run scope fixed**: 明確定義 `kg-mig-010` 的測試範圍。
- [ ] **Manual review boundaries defined**: 標出哪些 Ambiguous 項目需人工介入。

### 6.2 Later Execution Acceptance (Post-Production)
- [ ] 所有 Knowledge Items 均不含 `example_bank` 欄位。
- [ ] 所有 Knowledge Items 的 `example_sentence_refs` 均能對應到有效的全域 ID。
- [ ] **Render Sampling**: 在既有 Knowledge Lab / modular viewer runtime 抽樣驗證 Bucket B 與 Bucket C 各 1-2 個 Item。
- [ ] **Visual Integrity**: 確認 inline chips 與 example refs 不會引發 Render Crash、Fail-soft 異常或明顯樣式跑版。
- [ ] `content-pipeline` 下的 audit 腳本執行結果為 `[SUCCESS]`。
- [ ] `explanation_md_zh_tw` 中無遺留之純文字 Full Sentences（皆已提取或轉換）。

---

## 7. Execution Guardrails

為確保實作過程不損害內容完整性，執行 Agent 必須遵守以下防線：

1.  **Git State**: 執行批次寫入 (Batch Write) 前，必須確保 Working Tree 為 `Clean` 狀態，以便隨時 Rollback。
2.  **Schema Sanity**: 任何 JSON 寫入動作後，必須通過 `JSON parse` 驗證，並符合 `core-schema` 對應項目的驗證規則。
3.  **Integrity Gate**: 批次處理後，必須跑過 `integrity_gate.py` 或現有的 `audit_ko_content_v5.py`。
4.  **No Blind Replace**: 嚴禁在未完成 Dry-run Review 前，直接將 Regex/AI 產出的 Markdown 替換結果批次寫回正式內容檔案。
