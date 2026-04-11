# Dry-Run Report: KG-MIG-010 Bucket C1 Extraction (V1) - Refined

## 1. Overview
本報告為 `kg-mig-010` 任務中針對 Bucket C 第一批次 (C1) 「高信心完整例句」的二次精煉預演成果。本輪修正重點在於排除非獨立句 (Standalone Sentences) 的片段與短語，並完成對 3 個 `duplicate_existing` 項目之 merge target 唯一性驗證。

## 2. Summary Statistics

| Metric | Count | Description |
| :--- | :--- | :--- |
| **Total Candidates processed** | 31 | Candidates from 13:16 reviewed inventory |
| **Ready for Extraction** | 17 | Verified standalone, unique sentences |
| **Merged (Verified Unique)** | 2 | Confirmed single canonical target in existing bank |
| **Merged (Ambiguous Collision)** | 1 | Multiple canonical candidates found - **BLOCKER** |
| **Downgraded (Context-Bound)** | 11 | Morphology patterns, clause fragments, and minimal phrases |

## 3. Duplicate Analysis (Verified)

### 3.1 Existing Bank Collisions
以下項目與全域銀行中的現有句子重複，經驗證狀態如下：
- `빵하고 우유를 샀어요.` -> `verified_unique` (`ex.ko.grammar.particle.and_with_hago.bread_and_milk.v1`)
- `화장실이 어디예요?` -> `verified_unique` (`ex.ko.pattern.facility.toilet_query.v1`)
- `여기 앉아도 돼요?` -> **`ambiguous_existing_duplicate`**
  - Found candidates in: `grammar.permission` vs `pattern.social_basic`.
  - **Note**: This item blocks C1 implementation for `kg.grammar.permission.allow`.

## 4. Policy Alignment & Downgrades

根據 `EXAMPLE_EXTRACTION_POLICY_V1.md` 與二次審核標準，以下項目暫不提取至全域銀行，保留在 KI 本地 Markdown 中：

### 4.1 Morphology Patterns (A -> B)
- `가다 → 갑니다`, `먹다 → 먹습니다`, `학생 → 학생입니다`

### 4.2 Clause Fragments & Half-Clauses
- `비가 올까 봐`, `먹자니 배가 부르고`

### 4.3 Idiomatic Phrase Templates
- `밥 먹듯이 하다`, `물 쓰듯이 쓰다`

### 4.4 Minimal Dictionary-Style Phrases
- `집이 없다`, `친구가 없다`, `책이 있다`, `친구가 있다`

## 5. Representative Case Studies (Refined)

### Case A: Standalone Sentence (Ready)
- **Surface**: `寬敞且位置也好 (넓을뿐더러 위치도 좋아요)`
- **Verdict**: 語法典型且語意完整。

## 6. Verdict & Next Steps

### Verdict: [PASS WITH BLOCKERS]
C1 批次中 17 筆高質量獨立句與 2 筆唯一重複項已通過驗證。**剩餘 1 筆 `這裡可以坐嗎？` 因現有銀行內容冗餘 (Ambiguity) 處於阻塞狀態。**

### Recommended Next Actions:
1. **Implementation**: 執行 17 筆提取與 2 筆指向性合併。
2. **Deduplication**: 在執行 `這裡可以坐嗎？` 的 Decoupling 前，需先完成 `content-ko` 既存銀行的重複項清理。
3. **Verification**: 詳見 `KG_MIG_010_BUCKET_C1_VERIFICATION_NOTE_V1.md`.
