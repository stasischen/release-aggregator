# KO-DICT-01 Implementation Plan: TOPIK 3000 Base + Course Plugin

> **建立日期**: 2026-02-16
> **目的**: 以 TOPIK 3000 高頻詞為字典基底，跑一次 pipeline，把課程缺口當外掛補上。

## Goal

Replace ad-hoc mapping dictionaries with a **two-layer architecture**:

1. **Base layer** — TOPIK 3000 vocabulary, split into categorized `mapping_*.json`
2. **Plugin layer** — course-specific vocabulary discovered by pipeline gap analysis

> 把字典分兩層：第一層是 TOPIK 3000 高頻詞（人人都需要），第二層是課程專屬詞彙（只有我們的對話內容才會用到的字）。

---

## Architecture

Tokenizer auto-discovers `mapping_*.json` via glob (`engine/tokenizer.py:38-40`).

### Target File Structure

```text
content/source/ko/i18n/
├── 📚 [BASE] (TOPIK 3000)
│   ├── mapping_nouns.json
│   ├── mapping_verbs.json
│   ├── mapping_adjectives.json
│   ├── mapping_adverbs.json
│   └── mapping_misc.json
│
└── 🔌 [PLUGIN] (Course Specific)
    ├── mapping_course_names.json   ← 特殊人名、寵物名
    ├── mapping_course_proper.json  ← 特殊地名、品牌等
    ├── mapping_course_numbers.json ← 韓語字典未收錄的特殊格式數字 (如 WiFi 密碼)
    └── mapping_course_misc.json    ← 其他無法歸類的課程單詞
```

> [!IMPORTANT]
> Monolithic `mapping.json` will be **deleted**. All `ko:phrase:*` band-aids removed.

---

## Phases

### Phase 1a — Rewrite `import_vocabulary.py`

> **為什麼分檔？** Tokenizer 已經支援 glob `mapping_*.json`。分檔讓人類和 Agent 都能快速定位某個詞屬於哪個 POS 類別，也方便個別更新。

- Parse TOPIK 1000 + 2000 + 3000 markdown files
- POS heuristic: verb/adjective/noun/adverb classification
- Output 4 categorized files directly (not intermediate `mapping_topik.json`)

### Phase 1b — Delete legacy & redundant entries

> **為什麼刪？**
> - `mapping.json` (monolithic) 和分檔重複，造成隱性優先級問題
> - `ko:phrase:*` 是舊腳本的急救貼，應由 grammar rules 處理
> - 已變化形（`더워요 → 덥다`）應由動詞變化規則處理
> - `N+助詞` combo（`경찰관으로`）由 rules engine 處理

### Phase 2 — Pipeline baseline gap analysis

> [!IMPORTANT]
> **Baseline Comparison**: Phase 2 的 Gap Report 必須被視為「原始基線 (Baseline)」。我們在 Phase 3 補強詞彙與 Phase B 補強文法後，將會再次執行 Gap Analysis 與此基線對照，驗證 Unresolved Ratio 的下降。

1. Run `stage2_executor.py` with TOPIK 3000 base only
2. Collect unresolved tokens → gap report (The Baseline)
3. Gap = vocabulary in course dialogue not covered by TOPIK 3000

- Auto-generate from gap report
- Categorize into `names`, `proper`, `numbers`, `misc` based on automatic or manual tagging
- Manual review before commit
- Expected gap categories: food/drink, loanwords, colloquial, counters, technical one-offs (e.g., passwords)

---

## Verification

1. `python scripts/ops/import_vocabulary.py` → outputs 4 categorized files
2. `python scripts/ops/stage2_executor.py` → pipeline completes, gap report generated
3. Verify `mapping.json` deleted, no longer loaded by tokenizer
