# Dry-Run Report: KG-MIG-010 Bucket C1 Extraction (V1) - Refined

## 1. Overview
本報告為 `kg-mig-010` 任務中針對 Bucket C 第一批次 (C1) 「高信心完整例句」的二次精煉預演成果。本輪修正重點在於排除非獨立句 (Standalone Sentences) 的片段與短語，並將重複項對齊至既存銀行之正規 ID。

## 2. Summary Statistics

| Metric | Count | Description |
| :--- | :--- | :--- |
| **Total Candidates processed** | 31 | Candidates from 13:16 reviewed inventory |
| **Ready for Extraction** | 17 | Verified standalone, unique sentences |
| **Merged (Existing Bank)** | 3 | Duplicates mapped to internal `example_sentence` IDs |
| **Downgraded (Context-Bound)** | 11 | Morphology patterns, clause fragments, and minimal phrases |

## 3. Duplicate Analysis (ID-Based)

### 3.1 Existing Bank Collisions
以下項目與全域銀行中的現有句子重複，已對齊至正規 ID 映射。執行時應僅更新 Knowledge Item 的引用連結：
- `빵하고 우유를 샀어요.` -> `ex.ko.grammar.particle.and_with_hago.bread_and_milk.v1`
- `여기 앉아도 돼요?` -> `ex.ko.grammar.permission.sit_here.v1`
- `화장실이 어디예요?` -> `ex.ko.pattern.facility.toilet_query.v1`

## 4. Policy Alignment & Downgrades

根據 `EXAMPLE_EXTRACTION_POLICY_V1.md` 與二次審核標準，以下項目暫不提取至全域銀行，保留在 KI 本地 Markdown 中：

### 4.1 Morphology Patterns (A -> B)
- `가다 → 갑니다`
- `먹다 → 먹습니다`
- `학생 → 학생입니다`

### 4.2 Clause Fragments & Half-Clauses
- `비가 올까 봐` (原因小句片段)
- `먹자니 배가 부르고` (-고 結尾之半句)

### 4.3 Idiomatic Phrase Templates
- `밥 먹듯이 하다` (習慣用語模板)
- `물 쓰듯이 쓰다` (習慣用語模板)

### 4.4 Minimal Dictionary-Style Phrases
- `집이 없다`
- `친구가 없다`
- `책이 있다`
- `친구가 있다`

## 5. Representative Case Studies (Refined)

### Case A: Standalone Sentence (Ready)
- **Surface**: `넓을뿐더러 위치도 좋아요`
- **Verdict**: 語法典型且語意完整。

### Case B: Communicative Question (Ready)
- **Surface**: `지금 뭐 하고 있어요?`
- **Verdict**: 具備完整的語用功能與終止形結尾。

## 6. Verdict & Next Steps

### Verdict: [PASS WITH REFINEMENT]
C1 批次經精煉後，剩餘 **17 筆** 高質量獨立句可啟動正式 Decoupling。

### Recommended Next Actions:
1. **Implementation**: 依據 `KG_MIG_010_BUCKET_C1_EXTRACTION_MANIFEST_V1.json` 建立 17 筆新 JSON 並引用 3 筆既存 ID。
2. **Markdown Cleanup**: 針對降級為 `context_bound` 的 11 項目，確保其保留在 Markdown 內。
