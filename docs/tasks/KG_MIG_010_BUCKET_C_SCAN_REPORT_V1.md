# Bucket C Scan Report: Markdown Enrichment (V1)

## 1. Overview
本報告彙整了 `kg-mig-010` 任務中對於 Knowledge Lab 既存 Markdown 內容 (Bucket C) 的盤點與分類結果。本階段僅進行「掃描、分類與規劃」，不涉及 `content-ko` 內容本體的修改。

## 2. Scope & Boundaries

### 2.1 Scan Scope
- **Target Repo**: `content-ko`
- **Path**: `content/i18n/zh_tw/learning_library/knowledge/`
- **Fields Scanned**: `explanation_md_zh_tw`, `usage_notes_zh_tw`, `summary_zh_tw`
- **Families Covered**: `grammar`, `pattern`, `tense`, `ending`, `particle`

### 2.2 Exclusion Scope
- **Connector Batch 1**: 已於前一階段完成 Decoupling，本次掃描予以排除以避免重複。
- **Source Ingestion**: 不包含 Dialogues/Articles 的直接提取。

---

## 3. Classification Logic

所有盤點項目皆歸類至以下四個標準類別：

1. **Extractable / Global Example Sentence**
   - **定義**：完整、可獨立理解的韓文句子。
   - **標記目的**：未來預計提取至全域 `example_sentence` 銀行，供跨組件引用。

2. **Inline Chip Candidate**
   - **定義**：短片段、形態變化對照 (A -> B)、或局部句型片語。
   - **標記目的**：保留在 Markdown 呈現層，轉換為互動式藥丸積木 (`[ko:|zh:]`)。
   - **Special Marker**: 若項目已被標記為 `Already Chipped`，其在分類上仍屬於 `inline_chip_candidate`。這僅代表該項目已符合呈現層規範，無須進一步處理，**不代表**它是新的 Canonical 儲存路徑。

3. **Context-Bound / Local Commentary**
   - **定義**：必須依附當前教學解說才成立的片段、錯誤示範、或純說明文字。
   - **標記目的**：維持純文字 Markdown，不轉換為互動組件。

4. **Manual Review**
   - **定義**：對話式片段 (A: / B:) 或語境極強、邊界不清晰的項目。
   - **標記目的**：需由人工判定是否值得提取或如何拆解。

---

## 4. Summary Statistics

| Classification | Count | Suggested Next Action |
| :--- | :--- | :--- |
| **Extractable** | 31 | Extract to Global Example Bank |
| **Inline Chip Candidate** | 163 | Convert to Inline Chips (includes 5 already normalized) |
| **Context-Bound** | 64 | Keep as local commentary |
| **Manual Review** | 0 | Human review required |
| **Total** | **258** | |

---

## 5. Representative Cases

### Case A: Extractable Sentence
- **Source**: `kg.grammar.copula.eopda`
- **Excerpt**: `(例: 집이 없다)`
- **Normalized**: `집이 없다`
- **Verdict**: 語意完整，適合全域化。

### Case B: Morphology Fragment (Inline Candidate)
- **Source**: `kg.grammar.ending.ayoeoyo`
- **Excerpt**: `- 가다 → 가요`
- **Verdict**: 純變形示範，應轉換為 Inline Chip。

### Case C: Context-Bound Fragment
- **Source**: `kg.grammar.particle.subject`
- **Excerpt**: `子音(例如: 집, 책) + 이`
- **Verdict**: 教學提示，不具備獨立例句價值。

---

## 6. Execution Recommendation

1. **Phase 1: High-Confidence Extraction**
   - 優先處理 `extractable` 類別中，長度大於 5 個單詞且具備對應翻譯的項目。
   
2. **Phase 2: Markdown Normalization**
   - 針對 `inline_chip_candidate` 進行批次替換，將原始文字包覆為標記語法。

3. **Risk Management**
   - 在正式寫入銀行前，必須檢查 `inventory.json` 中的 `normalized_ko_candidate` 是否與現有銀行內容碰撞。
