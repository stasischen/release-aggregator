# Dictionary Remaining Drift Inventory (2026-05-03)

本報告對 `content_v2/inventory/dictionary/2026-04-30-fix/` 下的 JSONL 檔案進行了全面掃描，識別出剩餘的高風險 dictionary drift。

## 統計摘要

- **P0_CORRUPTED_DATA**: 0 筆 (初步掃描未發現單一 entry_no 下 hanja 不一致，但有更嚴重的 gloss 污染列在 P1)
- **P1_ENTRY_STRUCTURE_DRIFT**: 57 筆 (高風險：source_refs 雜亂且 entry_no 多樣)
- **P1_ROW_LEVEL_HANJA_DRIFT**: 390 筆 (高風險：metadata.hanja 存在於多個 entry_no 之上，可能造成歧義)
- **P2_NON_CONTIGUOUS_ENTRY_NO**: 3166 筆 (中風險：entry_no 不從 1 開始或不連續)
- **NO_ACTION**: 其餘正常

---

## P1_ENTRY_STRUCTURE_DRIFT / P1_ROW_LEVEL_HANJA_DRIFT (精選高風險案例)

> [!IMPORTANT]
> 以下詞條出現明顯的內容污染或結構混亂，建議優先人工審核或使用 Codex 進行精確修正。

### 1. ko:n:명단 (名單) - **GLOSS CONTAMINATION**
- **atom_id**: `ko:n:명단`
- **file path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl`
- **Current JSONL Snippet**:
  ```json
  {"atom_id": "ko:n:명단", "definitions": {"zh_tw": [{"entry_no": 2, "gloss": "字幕", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 3, "gloss": "名單", "is_provisional": true, "sense_id": "s2"}]}, "metadata": {"hanja": "名單", ...}, ...}
  ```
- **Issue Summary**: Gloss 污染。`entry_no: 2` 的 gloss 為 "字幕"，但 "字幕" 的韓文應為 `자막`。且 `entry_no` 從 2 開始。
- **Evidence**: `metadata.hanja` 為 "名單"，與 "字幕" 語義完全不符。
- **Suggested Action**: 刪除 `entry_no: 2` (字幕)，將 `entry_no: 3` (名單) 改為 `entry_no: 1`。
- **Auto-fixable**: no
- **Needs second-pass**: yes

### 2. ko:n:문구 (文句/文具) - **GLOSS CONTAMINATION**
- **atom_id**: `ko:n:문구`
- **file path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl`
- **Current JSONL Snippet**:
  ```json
  {"atom_id": "ko:n:문구", "definitions": {"zh_tw": [{"entry_no": 2, "gloss": "自然地；天然地", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 3, "gloss": "語句", "is_provisional": true, "sense_id": "s2"}]}, "metadata": {"hanja": "文句", ...}, ...}
  ```
- **Issue Summary**: Gloss 污染。`entry_no: 2` 的 gloss 為 "自然地"，與 `문구` 完全無關。
- **Evidence**: `metadata.hanja` 為 "文句"，與 "自然地" 語義完全不符。
- **Suggested Action**: 刪除 `entry_no: 2`，將 `entry_no: 3` (語句) 改為 `entry_no: 1`，並考慮補回 `entry_no: 2` (文具)。
- **Auto-fixable**: no
- **Needs second-pass**: yes

### 3. ko:v:취하다 (採取/醉) - **ROW_LEVEL_HANJA_DRIFT**
- **atom_id**: `ko:v:취하다`
- **file path**: `content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl`
- **Issue Summary**: Row-level Hanja `取-` 覆蓋了包含 "醉" 語義的多個 entry。
- **Evidence**: `entry_no: 1` 包含 "採取" 和 "醉"，`entry_no: 2` 也包含 "採取" 和 "醉"。結構極度混亂。
- **Suggested Action**: 拆分 `entry_no`，將 "採取" 關聯至 `取-`，"醉" 關聯至 `醉-` (或 null)。
- **Auto-fixable**: no
- **Needs second-pass**: yes

### 4. ko:v:타다 (搭乘/燃燒/彈奏...) - **ENTRY_STRUCTURE_DRIFT**
- **atom_id**: `ko:v:타다`
- **file path**: `content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl`
- **Issue Summary**: 極高 source variance (跨 6 個 batch) 且 `entry_no` 分佈為 `[1, 2, 3, 4, 8]`。
- **Evidence**: `entry_no: 8` ("沾上") 與前幾個 entry 語義跨度極大，且中間缺失 5, 6, 7。
- **Suggested Action**: 重新梳理 `entry_no` 並將 metadata 下放至 definition-level。
- **Auto-fixable**: no
- **Needs second-pass**: yes

---

## P2_NON_CONTIGUOUS_ENTRY_NO (範例)

> [!NOTE]
> 此類問題通常是自動化工具可以修復的，主要是 `entry_no` 序列不完整或不從 1 開始。

- `ko:affix:-가` (Entry_nos: [3]) -> 應為 [1]
- `ko:v:주장하다` (Entry_nos: [2]) -> 應為 [1]
- `ko:v:이해하다` (Entry_nos: [2]) -> 應為 [1]
- `ko:v:먹다` (Entry_nos: [1, 3]) -> 應為 [1, 2]

---

## 繁體中文摘要

- **P0**: 0 筆 (未發現嚴重的 hanja 衝突，但 P1 中的 gloss 污染等同 P0 等級)
- **P1**: 447 筆 (含 57 筆結構漂移與 390 筆 Hanja 漂移)
- **P2**: 3166 筆 (主要為 entry_no 序列問題)

**後續處理建議：**
1. **Codex Exact Patch**: 所有的 **P2** (非連續 entry_no) 都可以交給 Codex 自動重編序號，安全性高。
2. **人工確認 (High Priority)**: 
   - `ko:n:명단`, `ko:n:문구` 等明顯出現 Gloss 混入他詞現象的詞條必須人工核對 batch source。
   - `ko:v:취하다`, `ko:v:구하다` 等多根同音詞需將 metadata.hanja 下放並區分 entry。
3. **第二輪掃描**: 建議在修復 P2 後進行第二輪掃描，聚焦於 `translation.zh_tw` 與 `definitions` 的內容一致性。
