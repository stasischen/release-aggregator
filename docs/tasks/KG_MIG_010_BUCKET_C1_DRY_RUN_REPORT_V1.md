# Dry-Run Report: KG-MIG-010 Bucket C1 Extraction (V1)

## 1. Overview
本報告為 `kg-mig-010` 任務中針對 Bucket C 第一批次 (C1) 「高信心完整例句」的提取預演成果。本次預演對 31 個原定 `extractable` 的候選項進行了規範化、去重以及策略一致性檢查。

## 2. Summary Statistics

| Metric | Count | Description |
| :--- | :--- | :--- |
| **Total Candidates processed** | 31 | Candidates from 13:16 reviewed inventory |
| **Ready for Extraction** | 25 | High-confidence, unique standalone sentences |
| **Merged (Existing Bank)** | 3 | Duplicates found in current `example_sentence` bank |
| **Merged (Batch Internal)** | 0 | No internal duplicates found in this 31-item slice |
| **Downgraded (Context-Bound)** | 3 | Morphology patterns (A -> B) caught by policy |

## 3. Duplicate Analysis

### 3.1 Existing Bank Collisions
以下項目與全域銀行中的現有句子重複，建議執行時採「合併（Merge）」處理，僅更新 Knowledge Item 的引用連結：
- `빵하고 우유를 샀어요.` (Already in `ex.ko.connector.conjunction.hago_3.v1`)
- `여기 앉아도 돼요?` (Existing in bank)
- `화장실이 어디예요?` (Existing in bank)

### 3.2 Batch Internal Collisions
- 本批次 31 項中無內部重複項目。

## 4. Policy Alignment & Downgrades

根據 `EXAMPLE_EXTRACTION_POLICY_V1.md`，以下項目雖具備例句形式，但本質屬於「形態變化示範 (Morphology Pattern)」，應保留在 KI 本地 Markdown 中：
- `가다 → 갑니다` (Source: `kg.grammar.ending.sumndia`)
- `먹다 → 먹습니다` (Source: `kg.grammar.ending.sumndia`)
- `학생 → 학생입니다` (Source: `kg.grammar.ending.sumndia`)

## 5. Representative Case Studies

### Case A: Ready (High Confidence)
- **Source**: `kg.grammar.ending.additive_eulppunderseo`
- **Surface**: `넓을뿐더러 위치도 좋아요`
- **Proposed ID**: `ex.ko.grammar.ending.additive_eulppunderseo.v1`
- **Verdict**: 語法典型且語意完整。

### Case B: Multi-Sentence KI Handling
- **Source**: `kg.grammar.copula.itda`
- **Candidate 1**: `책이 있다` -> `ex.ko.grammar.copula.itda.v1`
- **Candidate 2**: `친구가 있다` -> `ex.ko.grammar.copula.itda_2.v1`
- **Candidate 3**: `집에 있어요` -> `ex.ko.grammar.copula.itda_3.v1`
- **Verdict**: 針對同一 KI 提煉多句時，自動附加索引後綴以確保 ID 唯一性。

## 6. Verdict & Next Steps

### Verdict: [PASS WITH MINOR ADJUSTMENTS]
C1 批次數據質量極高，經去重與形態過濾後，剩餘 25 筆可安全執行正式 Decoupling。

### Recommended Next Actions:
1. **Approval**: 審閱 `KG_MIG_010_BUCKET_C1_EXTRACTION_MANIFEST_V1.json` 確認 ID 映射。
2. **Implementation**: 啟動 C1 正式寫入，建立 `content-ko` 銀行實體 JSON 並替換 KI 引用。
3. **Markdown Sync**: 針對降級為 `context_bound` 的 3 筆，確保其 Markdown 維持現狀或轉換為 Inline Chip。
