# Dictionary Drift Forensic Samples (2026-05-03)

本報告針對 8 個指定樣本進行逐筆 forensic trace，追溯污染來源與傳播路徑。讀取基準為 `content_v2/inventory/dictionary/2026-04-30-fix/`。

---

## 1. ko:n:밤

### atom_id
`ko:n:밤`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:n:밤",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "夜晚；晚上", "sense_id": "s1"},
    {"entry_no": 2, "gloss": "例子；例句", "sense_id": "s2"},
    {"entry_no": 2, "gloss": "禮貌；禮節", "sense_id": "s3"},
    {"entry_no": 2, "gloss": "是 (答話)", "sense_id": "s4"}
  ]},
  "translation": {"zh_tw": "夜晚；晚上"},
  "source_refs": [
    "content_v2_staging:batch_251_300.jsonl:26",
    "content_v2_staging:batch_6051_6100.jsonl:19"
  ]
}
```

### Source Refs Records

**source_ref 1: `batch_251_300.jsonl:26`** — Clean source
```json
{"id": "ko:n:밤", "lemma": "밤", "pos": "N",
 "metadata": {"nikl_level": "초급", "rank": 276, "explanation": "어두운 때; 이 깊다"},
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": "夜晚；晚上"}]}}
```

**source_ref 2: `batch_6051_6100.jsonl:19`** — Contaminated source (actually `ko:n:예`)
```json
{"id": "ko:n:예", "lemma": "예", "pos": "N",
 "metadata": {
   "rank_collision": true,
   "rank_collision_rank": 6062,
   "rank_collision_source_lemma": "밤",
   "rank_collision_source_word": "밤02",
   "rank_collision_reason": "staged lemma differs from canonical NIKL rank source"
 },
 "definitions": {"zh_tw": [
   {"sense_id": "s1", "gloss": "例子；例句"},
   {"sense_id": "s2", "gloss": "禮貌；禮節"},
   {"sense_id": "s3", "gloss": "是 (答話)"}
 ]}}
```

### Observed Drift
ko:n:밤 吸收了 ko:n:예 的全部三個 gloss（「例子；例句」「禮貌；禮節」「是 (答話)」），作為 entry_no 2 合併到自己的定義中。這三個 gloss 語義與 밤（夜晚）完全無關。

### Earliest Contaminated Artifact
`content_v2/staging/dictionary/main/batch_6051_6100.jsonl:19` — 該行本身的 atom_id 是 `ko:n:예`，但帶有指向 `밤02` 的 rank_collision metadata。此記錄在 2026-04-29 inventory 中已存在，污染早於 2026-04-30-fix。

### Trace Path
1. NIKL 詞庫 rank 6062 的規範 lemma 為 `밤02`
2. Staging batch_6051_6100 將 `ko:n:예` 分配給了 rank 6062（原因：NIKL 來源版本或重新排序）
3. Rank collision metadata 記錄此衝突：`ko:n:예` 佔用了 `밤02` 的 rank
4. Merge 步驟使用 rank 作為 merging key，將 `ko:n:예` 的 gloss 合併進 `ko:n:밤`（因為 rank collision 指向 밤）
5. 2026-04-30-fix 未修正此問題，直接繼承了污染

### Duplicate / Merge Review Record
- `semantic_review_queue.csv`: 未直接標記 `ko:n:밤`，但 `ko:n:예` 被標記為 `p0_duplicate_and_multi_sense`（4 sources）
- `rank_cleanup_queue.csv`: `ko:n:밤` → ranked, nikl_topik_agree, band B（clean entry）

### Likely Cause
**Rank collision propagation bug**。Merge 演算法在處理 rank_collision 時，將 collision source（밤）錯誤地當作 merge target，而非保留實際 atom_id（예）作為獨立條目。這導致 예 的 gloss 被注入到 밤 中。

### Confidence
**High** (95%)。污染鏈完整可追溯：batch_6051_6100 的 rank_collision metadata → 最終 inventory 的 source_refs 直接指向 `ko:n:예` 記錄。

### Recommended Fix Type
`manual_lexical_review` — 需人工確認 rank 6062 的正確 lemma 歸屬（밤02 vs 예），然後：
- 刪除 ko:n:밤 的 entry_no 2 全部三個 gloss
- 若 rank 6062 確實屬於 밤02，則 batch_6051_6100.jsonl:19 應改 atom_id 為 ko:n:밤 的另一個 sense

---

## 2. ko:n:명단

### atom_id
`ko:n:명단`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:n:명단",
  "definitions": {"zh_tw": [
    {"entry_no": 2, "gloss": "字幕", "sense_id": "s1"},
    {"entry_no": 3, "gloss": "名單", "sense_id": "s2"}
  ]},
  "metadata": {"hanja": "名單", "explanation": "합격자 명단"},
  "translation": {"zh_tw": "字幕"},
  "source_refs": [
    "content_v2_staging:batch_6201_6250.jsonl:29",
    "content_v2_staging:batch_6201_6250.jsonl:30",
    "content_v2_staging:gloss_fill_workflow_batch_30_output.staging.jsonl:4"
  ]
}
```

### Source Refs Records

**source_ref 1: `batch_6201_6250.jsonl:29`** — Clean, empty gloss
```json
{"id": "ko:n:명단", "lemma": "명단", "pos": "N",
 "metadata": {"nikl_level": "중급", "rank": 6222, "origin": "漢字: 名單"},
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": ""}]}}
```

**source_ref 2: `batch_6201_6250.jsonl:30`** — Contamination vector (actually `ko:n:자막`)
```json
{"id": "ko:n:자막", "lemma": "자막", "pos": "N",
 "metadata": {
   "rank_collision": true,
   "rank_collision_rank": 6222,
   "rank_collision_source_lemma": "명단",
   "rank_collision_source_word": "명단01",
   "rank_collision_reason": "staged lemma differs from canonical NIKL rank source"
 },
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": "字幕"}]}}
```

**source_ref 3: `gloss_fill_workflow_batch_30_output.staging.jsonl:4`** — Clean filled
```json
{"id": "ko:n:명단", "lemma": "명단",
 "metadata": {"gloss_status": "filled", "source_basis": "naver", "source_type": "hanja",
   "primary_gloss": "名單", "rank": 6222},
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": "名單"}]}}
```

### Observed Drift
ko:n:명단 的 entry_no 2 gloss 為「字幕」，這屬於 ko:n:자막（subtitle）。entry_no 從 2 開始，且 translation 欄位也被污染為「字幕」。

### Earliest Contaminated Artifact
`content_v2/staging/dictionary/main/batch_6201_6250.jsonl:30`（ko:n:자막 帶 rank_collision 指向 명단）。此紀錄在 batch 生成階段即存在。

### Trace Path
1. batch_6201_6250.jsonl:29 = ko:n:명단（empty gloss）— clean
2. batch_6201_6250.jsonl:30 = ko:n:자막（gloss: 字幕），帶 rank_collision → 명단01
3. rank 6222 的 NIKL canonical lemma 為 명단01，但 staging 將 자막 分配到此 rank
4. Merge 將 자막 的 gloss 合併進 명단（因 rank collision 指向 명단）
5. gloss_fill workflow 正確填入「名單」→ 產生 entry_no 3
6. 最終結果：entry_no 2 = 字幕（污染），entry_no 3 = 名單（正確）

### Likely Cause
**Rank collision propagation bug**（與 ko:n:밤 相同模式）。rank_collision 導致 자막 的 gloss 被注入到 명단。

### Confidence
**High** (95%)。

### Recommended Fix Type
`one_time_jsonl_repair` — Codex 可精確執行：
- 刪除 entry_no 2（字幕）
- 將 entry_no 3 改為 entry_no 1
- 修正 translation 為「名單」

---

## 3. ko:n:문구

### atom_id
`ko:n:문구`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:n:문구",
  "definitions": {"zh_tw": [
    {"entry_no": 2, "gloss": "自然地；天然地", "sense_id": "s1"},
    {"entry_no": 3, "gloss": "語句", "sense_id": "s2"}
  ]},
  "metadata": {"hanja": "文句"},
  "translation": {"zh_tw": "自然地；天然地"},
  "source_refs": [
    "content_v2_staging:batch_6201_6250.jsonl:34",
    "content_v2_staging:batch_6201_6250.jsonl:35",
    "content_v2_staging:gloss_fill_workflow_batch_30_output.staging.jsonl:5"
  ]
}
```

### Source Refs Records

**source_ref 1: `batch_6201_6250.jsonl:34`** — Clean, empty gloss
```json
{"id": "ko:n:문구", "lemma": "문구", "pos": "N",
 "metadata": {"rank": 6225, "origin": "漢字: 文句"},
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": ""}]}}
```

**source_ref 2: `batch_6201_6250.jsonl:35`** — Contamination vector (actually `ko:det:자연적`)
```json
{"id": "ko:det:자연적", "lemma": "자연적", "pos": "DET",
 "metadata": {
   "rank_collision": true,
   "rank_collision_rank": 6225,
   "rank_collision_source_lemma": "문구",
   "rank_collision_source_word": "문구01",
   "rank_collision_reason": "staged lemma differs from canonical NIKL rank source"
 },
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": "自然地；天然地"}]}}
```

**source_ref 3: `gloss_fill_workflow_batch_30_output.staging.jsonl:5`** — Clean filled
```json
{"id": "ko:n:문구", "lemma": "문구",
 "metadata": {"gloss_status": "filled", "source_basis": "naver_cluster",
   "primary_gloss": "語句", "secondary_gloss": "詞句", "rank": 6225,
   "normalized_source_gloss": "1 文具"},
 "definitions": {"zh_tw": [{"sense_id": "s1", "gloss": "語句"}]}}
```

### Observed Drift
ko:n:문구 的 entry_no 2 gloss 為「自然地；天然地」，這是 ko:det:자연적 的語義。此外，문구 應有兩個漢字義項：文句（語句、詞句）和文具（stationery），但 gloss_fill 只產生了「語句」（正確），而「文具」義項遺失。translation 欄位也被污染為「自然地；天然地」。

### Earliest Contaminated Artifact
`content_v2/staging/dictionary/main/batch_6201_6250.jsonl:35`（ko:det:자연적 帶 rank_collision 指向 문구）。

### Trace Path
與 ko:n:명단 完全相同的模式：
1. batch_6201_6250.jsonl:34 = ko:n:문구（empty）— clean
2. batch_6201_6250.jsonl:35 = ko:det:자연적，帶 rank_collision → 문구01
3. Merge 將 자연적 的 gloss 注入 문구
4. gloss_fill 正確填入「語句」
5. 最終：entry_no 2 = 自然地（污染），entry_no 3 = 語句（正確）

### Likely Cause
**Rank collision propagation bug**。

### Confidence
**High** (95%)。

### Recommended Fix Type
`one_time_jsonl_repair` — Codex 可精確執行：
- 刪除 entry_no 2（自然地；天然地）
- 將 entry_no 3 改為 entry_no 1
- 修正 translation 為「語句」
- 考慮人工補回 entry_no 2（文具），因 gloss_fill 輸入的 naver_gloss 包含「1 文具」但未被選取

---

## 4. ko:v:취하다

### atom_id
`ko:v:취하다`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:v:취하다",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "採取；選取", "sense_id": "s1"},
    {"entry_no": 1, "gloss": "醉；陶醉", "sense_id": "s2"},
    {"entry_no": 2, "gloss": "採取；採用", "sense_id": "s3"},
    {"entry_no": 2, "gloss": "喝醉；陶醉", "sense_id": "s4"}
  ]},
  "metadata": {"hanja": "取-"},
  "translation": {"zh_tw": "採取；選取"},
  "source_refs": [
    "content_v2_staging:batch_1101_1150.jsonl:14",
    "content_v2_staging:batch_2201_2250.jsonl:24"
  ]
}
```

### Source Refs Records

**source_ref 1: `batch_1101_1150.jsonl:14`** — 取/醉 mixed
```json
{"id": "ko:v:취하다", "lemma": "취하다", "pos": "V",
 "metadata": {"rank": 1113, "origin": "漢字: 取-"},
 "definitions": {"zh_tw": [
   {"sense_id": "s1", "gloss": "採取；選取"},
   {"sense_id": "s2", "gloss": "醉；陶醉"}
 ]}}
```

**source_ref 2: `batch_2201_2250.jsonl:24`** — 醉 batch，gloss 錯誤混入「採取」
```json
{"id": "ko:v:취하다:2225", "lemma": "취하다", "pos": "V",
 "metadata": {"rank": 2225, "origin": "漢字: 醉", "explanation": "술에"},
 "definitions": {"zh_tw": [
   {"sense_id": "s1", "gloss": "採取；採用"},
   {"sense_id": "s2", "gloss": "喝醉；陶醉"}
 ]}}
```

### Observed Drift
취하다 有兩個漢字：取-（採取）和 醉（喝醉）。兩個 source batch 各自都產生了兩個 sense：
- batch_1101_1150（hanja: 取-）：s1=採取；選取 ✓, s2=醉；陶醉（應屬 醉）
- batch_2201_2250（hanja: 醉）：s1=採取；採用（應屬 取-）, s2=喝醉；陶醉 ✓

Merge 後產生 4 個 sense，其中明顯重複：entry_no 1 和 entry_no 2 各自都包含「取」和「醉」義項。metadata.hanja 僅設為「取-」，忽略了「醉」。

### Earliest Contaminated Artifact
`content_v2/staging/dictionary/main/batch_2201_2250.jsonl:24` — 此 batch 的 generator 在處理 `ko:v:취하다:2225`（hanja: 醉）時，將「採取；採用」納入 sense 1。這是 **source generator 層級的 gloss 污染**。

### Duplicate / Merge Review Record
- `semantic_review_queue.csv`: `ko:v:취하다` → `p2_multi_sense_only`（1 source, 1 entry_no found, 2 senses）
- `semantic_review_queue.csv`: `ko:v:취하다:2225` → `p2_multi_sense_only`（1 source, 1 entry_no found, 2 senses）
- `rank_cleanup_queue.csv`: `ko:v:취하다` rank 1113 → topik_only, band I

### Likely Cause
**Generator gloss 污染 + Merge 未做跨 batch sense 去重**。Generator 在產生 `:2225` 變體時，未能區分「取-」和「醉」的 gloss，將兩個漢字的語義都輸出。Merge 步驟未識別 entry_no 1 和 2 之間的 sense 重複。

### Confidence
**High** (90%)。

### Recommended Fix Type
`generator_fix` + `manual_lexical_review`
- Generator 層級：需要在 prompt 中強化「同音異字動詞必須只輸出匹配該 hanja 的 gloss」
- 人工審核：確認 entry_no 1（取-）僅保留「採取」相關 gloss；entry_no 2（醉）僅保留「喝醉」相關 gloss
- 修正 metadata.hanja 為 null（或拆分成兩筆獨立 atom）

---

## 5. ko:v:타다

### atom_id
`ko:v:타다`

### Final Inventory Current Record
15 個 definitions，entry_no 分佈 [1, 2, 3, 4, 8]，跨 8 個語義域（搭乘、燃燒、曬黑、加入/沖調、彈奏、領取、怕冷熱、沾上、白色）。

```json
{
  "atom_id": "ko:v:타다",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "搭乘（交通工具）", "sense_id": "s1"},
    {"entry_no": 1, "gloss": "燃燒", "sense_id": "s2"},
    {"entry_no": 1, "gloss": "曬黑", "sense_id": "s3"},
    {"entry_no": 2, "gloss": "燃燒；燒毀", "sense_id": "s4"},
    {"entry_no": 2, "gloss": "搭乘", "sense_id": "s5"},
    {"entry_no": 2, "gloss": "加入；沖調", "sense_id": "s6"},
    {"entry_no": 2, "gloss": "彈奏", "sense_id": "s7"},
    {"entry_no": 2, "gloss": "領取", "sense_id": "s8"},
    {"entry_no": 3, "gloss": "搭乘；坐", "sense_id": "s9"},
    {"entry_no": 3, "gloss": "領取（工資、獎項等）", "sense_id": "s10"},
    {"entry_no": 3, "gloss": "沖泡；兌（水）", "sense_id": "s11"},
    {"entry_no": 3, "gloss": "怕；容易受（冷、熱等）影響", "sense_id": "s12"},
    {"entry_no": 3, "gloss": "彈奏（弦樂器）", "sense_id": "s13"},
    {"entry_no": 4, "gloss": "白色", "sense_id": "s14"},
    {"entry_no": 8, "gloss": "沾上", "sense_id": "s15"}
  ]},
  "metadata": {"hanja": null, "explanation": "버스에 ~; 차에"},
  "source_refs": [
    "content_v2_staging:batch_2101_2150.jsonl:18",
    "content_v2_staging:batch_251_300.jsonl:10",
    "content_v2_staging:batch_5551_5600.jsonl:10",
    "content_v2_staging:batch_6451_6500.jsonl:58",
    "content_v2_staging:batch_unranked_29.jsonl:39",
    "content_v2_staging:gloss_fill_workflow_batch_25_output.staging.jsonl:12"
  ]
}
```

### Source Refs Records

**source 1: `batch_2101_2150.jsonl:18`** — rank 2121, origin ""
```json
{"id": "ko:v:타다",
 "metadata": {"rank": 2121, "explanation": "기차를 타다; 커피를 타다"},
 "definitions": {"zh_tw": [
   "燃燒；燒毀", "搭乘", "加入；沖調", "彈奏", "領取"
 ]}}
```

**source 2: `batch_251_300.jsonl:10`** — rank 260, origin null
```json
{"id": "ko:v:타다",
 "metadata": {"rank": 260, "explanation": "버스에 ~; 차에"},
 "definitions": {"zh_tw": [
   "乘坐；騎", "燃燒；燒", "焦急", "順著；趁著"
 ]}}
```

**source 3: `batch_5551_5600.jsonl:10`** — rank 260, origin null
```json
{"id": "ko:v:타다",
 "metadata": {"rank": 260, "explanation": "버스를 ~; 차에"},
 "definitions": {"zh_tw": [
   "搭乘（交通工具）", "燃燒", "曬黑"
 ]}}
```

**source 4: `batch_6451_6500.jsonl:58`** — rank 5568, origin ""
```json
{"id": "ko:v:타다",
 "metadata": {"rank": 5568, "explanation": "월급을 ~"},
 "definitions": {"zh_tw": [
   "燃燒", "搭乘；坐", "領取（工資、獎項等）", "沖泡；兌（水）",
   "怕；容易受（冷、熱等）影響", "彈奏（弦樂器）"
 ]}}
```

**source 5: `batch_unranked_29.jsonl:39`** — unranked overlay (ko:v:타다:1)，gloss_fill 前
```json
{"id": "ko:v:타다:1",
 "metadata": {"overlay_kind": "unranked", "explanation": "때가"},
 "definitions": {"zh_tw": [{"gloss": ""}]}}
```

**source 6: `gloss_fill_workflow_batch_25_output.staging.jsonl:12`** — unranked overlay, gloss_fill 後
```json
{"id": "ko:v:타다:1",
 "metadata": {"gloss_status": "filled", "source_basis": "naver_cluster",
   "source_type": "native", "selected_cluster": "be_stained",
   "normalized_source_gloss": "染上. 沾上"},
 "definitions": {"zh_tw": [{"gloss": "沾上"}]}}
```

**Rank collision: `batch_6451_6500.jsonl` 周邊** — `ko:n:하양` rank 6500，rank_collision_source_lemma: `타다`
```json
{"id": "ko:n:하양",
 "metadata": {
   "rank_collision": true, "rank_collision_rank": 6500,
   "rank_collision_source_lemma": "타다",
   "rank_collision_source_word": "타다03"
 },
 "definitions": {"zh_tw": [{"gloss": "白色"}]}}
```

### Observed Drift

1. **Rank collision 污染**：entry_no 4「白色」來自 ko:n:하양（white），因 rank_collision_source_lemma: `타다`。
2. **Source batch variance**：同一個 lemma 在 5 個 staging batch 中分別出現，各 batch 產生不同的 gloss set（如「搭乘」出現 4 個不同措辭版本）。
3. **Merge dedup 失敗**：Merge 將所有 batch 的 gloss 串接，未去除近義重複。結果有 15 個 sense，但核心語義僅約 8 個。
4. **entry_no 不連續**：entry_no 分佈 [1, 2, 3, 4, 8]，中間缺少 5, 6, 7（可能因 collision 條目被移除但未重新編號）。
5. **gloss_fill overlay**：unranked overlay 的「沾上」被分配為 entry_no 8，造成結構不連續。

### Earliest Contaminated Artifact
- 「白色」污染：`content_v2/staging/dictionary/extensions/ranked/batch_6451_6500.jsonl` — ko:n:하양 在 rank 6500 的 collision
- 其他 drift：source batch 生成階段即存在的 variance

### Duplicate / Merge Review Record
- `duplicate_candidates.csv`: `ko:v:타다` → 4 sources（batch_2101_2150, batch_251_300, batch_5551_5600, batch_6401_6450）
- `semantic_review_queue.csv`: `ko:v:타다` → `p0_duplicate_and_multi_sense`（4 sources, 3 entry_nos found, 6 unique senses）
- `rank_cleanup_queue.csv`: `ko:v:타다` rank 260 → band B, nikl_topik_agree

### Likely Cause
**多重原因疊加**：
1. Source batch variance（5 個獨立 batch 各自產出不同的 gloss set）
2. Rank collision（하양 → 타다，注入「白色」）
3. Merge dedup 失敗（近義 gloss 未被合併）
4. Unranked overlay 的 entry_no 分配不一致

### Confidence
**High** (95%)。

### Recommended Fix Type
`manual_lexical_review` — 這是 8 個樣本中最複雜的案例：
- 需人工釐清 8 個語義域，去重合併近義 gloss
- 刪除「白色」（屬 ko:n:하양）
- 重新編排 entry_no 為連續序列
- 將 metadata 下放至 definition-level（每個 entry 標記其來源 batch 與語義域）

---

## 6. ko:n:지방

### atom_id
`ko:n:지방`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:n:지방",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "地方；地區", "sense_id": "s1", "hanja": "地方"},
    {"entry_no": 1, "gloss": "鄉下；郊外", "sense_id": "s2", "hanja": "地方"},
    {"entry_no": 2, "gloss": "脂肪", "sense_id": "s3", "hanja": "脂肪"}
  ]},
  "metadata": {"hanja": null, "explanation": "남쪽 지방"},
  "translation": {"zh_tw": "地方；地區"},
  "source_refs": [
    "content_v2_staging:batch_251_300.jsonl:25",
    "content_v2_staging:batch_7901_7950.jsonl:7",
    "content_v2_staging:gloss_fill_workflow_batch_37_output.staging.jsonl:10"
  ]
}
```

### Source Refs Records

**source 1: `batch_251_300.jsonl:25`** — 地方
```json
{"id": "ko:n:지방",
 "metadata": {"rank": 275, "origin": "漢字: 地方", "explanation": "남쪽 지방"},
 "definitions": {"zh_tw": [{"gloss": "地方；區域"}]}}
```

**source 2: `batch_7901_7950.jsonl:7`** — 脂肪 (extension)
```json
{"id": "ko:n:지방:7920",
 "metadata": {"rank": 7920, "origin": "漢字: 脂肪", "explanation": "식물성 지방",
   "overlay_kind": "ranked", "overlay_priority": 1},
 "definitions": {"zh_tw": [{"gloss": ""}]}}
```

**source 3: `gloss_fill_workflow_batch_37_output.staging.jsonl:10`** — 脂肪 filled
```json
{"id": "ko:n:지방:7920",
 "metadata": {"gloss_status": "filled", "source_basis": "naver_cluster",
   "source_type": "hanja", "selected_cluster": "fat", "primary_gloss": "脂肪"},
 "definitions": {"zh_tw": [{"gloss": "脂肪"}]}}
```

### Observed Drift
Minor gloss refinement：source 的「地方；區域」→ final 的「地方；地區」+「鄉下；郊外」。這是合理的 gloss 細化，非污染。「脂肪」義項正確地由 gloss_fill workflow 從漢字推導並作為 entry_no 2 疊加。

### Earliest Contaminated Artifact
N/A — 無明顯污染。

### Gloss Fill Workflow Input/Output
- **Input**: `gloss_fill_workflow_batch_37_input.jsonl:10` — id: `ko:n:지방:7920`, naver_gloss: `"地方；纸位牌；脂肪；油脂；脂膏；膏脂"`, fill_policy: `use_naver_then_preserve`
- **Output**: selected_cluster: `fat`, primary_gloss: `脂肪` ✓

### Likely Cause
N/A — 此條目為範例中 **最乾淨** 的案例。

### Confidence
**High** (95%) — no drift, correctly handled.

### Recommended Fix Type
`no_action` — 結構正確、gloss 正確、entry_no 連續、hanja 正確下放至 definition-level。

---

## 7. ko:n:기능

### atom_id
`ko:n:기능`

### Final Inventory Current Record
```json
{
  "atom_id": "ko:n:기능",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "功能；機能", "sense_id": "s1", "hanja": "機能"},
    {"entry_no": 2, "gloss": "功能；職能", "sense_id": "s2", "hanja": "技能"},
    {"entry_no": 2, "gloss": "技能", "sense_id": "s3", "hanja": "技能"}
  ]},
  "metadata": {"hanja": null, "explanation": "이 다양하다"},
  "translation": {"zh_tw": "功能；機能"},
  "source_refs": [
    "content_v2_staging:batch_501_550.jsonl:29",
    "content_v2_staging:batch_5301_5350.jsonl:14"
  ]
}
```

### Source Refs Records

**source 1: `batch_501_550.jsonl:29`** — 機能
```json
{"id": "ko:n:기능",
 "metadata": {"rank": 531, "origin": "漢字: 機能", "explanation": "이 다양하다"},
 "definitions": {"zh_tw": [{"gloss": "功能；機能"}]}}
```

**source 2: `batch_5301_5350.jsonl:14`** — 技能/機能 mixed + 生成器 typo
```json
{"id": "ko:n:기능",
 "metadata": {"rank": 5325, "origin": "漢字: 技能, 機能"},
 "definitions": {"zh_tw": [
   {"gloss": "功能；職能"},
   {"gloss": "技能；機難"}
 ]}}
```

### Observed Drift
1. **Generator typo**: source batch_5301_5350 的 s2 gloss 為「技能；**機難**」，應為「技能；**機能**」。「機難」是明顯的 generator 輸出錯誤。
2. **2026-04-30-fix partial correction**: final inventory 將「技能；機難」修正為「技能」（刪除了錯誤的「機難」部分），這是一個手動或自動修正。
3. **Hanja misalignment**: entry_no 2 的 gloss「功能；職能」被標記為 hanja「技能」，但「功能；職能」語義上應屬 hanja「機能」。source batch 的 origin 為「漢字: 技能, 機能」，表示該 batch 試圖同時覆蓋兩個漢字，最終 merge 未能正確分離。

### Earliest Contaminated Artifact
`content_v2/staging/dictionary/main/batch_5301_5350.jsonl:14` — generator typo「機難」。

### Duplicate / Merge Review Record
- `duplicate_candidates.csv`: `ko:n:기능` → 2 sources
- `semantic_review_queue.csv`: `ko:n:기능` → `p0_duplicate_and_multi_sense`（2 sources, 1 entry_no found, 2 senses）
- `rank_cleanup_queue.csv`: `ko:n:기능` rank 531 → conflict_rank, band I

### Likely Cause
**Generator typo + merge hanja confusion**。Generator 在處理「技能, 機能」雙漢字時產出 typo「機難」。Merge 將兩個不同 rank（531 = 機能, 5325 = 技能）的條目合併為一個 atom，但 entry_no 2 下的 gloss「功能；職能」語義歸屬錯誤。

### Confidence
**Medium-High** (80%) — 語義歸屬需要人工判斷：기능 是否適合在一個 atom 下同時覆蓋「機能」和「技能」。

### Recommended Fix Type
`manual_lexical_review`
- 確認「功能；職能」應歸屬 hanja「技能」還是「機能」
- 若應分離，考慮拆成兩個獨立 atom（ko:n:기능 機能 和 ko:n:기능 技能）
- Generator typo「機難」已在 2026-04-30-fix 修正

---

## 8. ko:n:예

### atom_id
`ko:n:예`

### Final Inventory Current Record
9 個 definitions，僅 3 個真實語義，entry_no 重度重複。

```json
{
  "atom_id": "ko:n:예",
  "definitions": {"zh_tw": [
    {"entry_no": 1, "gloss": "例子", "sense_id": "s1", "hanja": "例"},
    {"entry_no": 2, "gloss": "禮儀", "sense_id": "s2", "hanja": "禮"},
    {"entry_no": 3, "gloss": "是", "sense_id": "s3", "hanja": null},
    {"entry_no": 1, "gloss": "例子；範例", "sense_id": "s4", "hanja": "例"},
    {"entry_no": 2, "gloss": "禮節；禮貌", "sense_id": "s5", "hanja": "禮"},
    {"entry_no": 1, "gloss": "例子、實例、先例", "sense_id": "s6", "hanja": "例"},
    {"entry_no": 2, "gloss": "禮節、禮貌", "sense_id": "s7", "hanja": "禮"},
    {"entry_no": 3, "gloss": "是、好的 (肯定回答)", "sense_id": "s8", "hanja": null},
    {"entry_no": 2, "gloss": "禮", "sense_id": "s9", "hanja": "禮"}
  ]},
  "metadata": {"hanja": null, "explanation": "를 들다"},
  "translation": {"zh_tw": "例子"},
  "source_refs": [
    "content_v2_staging:batch_3251_3300.jsonl:32",
    "content_v2_staging:batch_401_450.jsonl:48",
    "content_v2_staging:batch_451_500.jsonl:2",
    "content_v2_staging:batch_unranked_20.jsonl:37",
    "content_v2_staging:gloss_fill_workflow_batch_17_output.staging.jsonl:29"
  ]
}
```

### Source Refs Records

**source 1: `batch_3251_3300.jsonl:32`** — rank 3289, origin null
```json
{"definitions": {"zh_tw": [
  "例子、實例、先例", "禮節、禮貌", "是、好的 (肯定回答)"
]}}
```

**source 2: `batch_401_450.jsonl:48`** — rank 452, origin "漢字: 例"
```json
{"definitions": {"zh_tw": [
  "例子", "禮儀", "是"
]}}
```

**source 3: `batch_451_500.jsonl:2`** — rank 452, origin "漢字: 例 / 禮"
```json
{"definitions": {"zh_tw": [
  "例子；範例", "禮節；禮貌"
]}}
```

**source 4: `batch_unranked_20.jsonl:37`** — unranked overlay (ko:n:예:1)
```json
{"id": "ko:n:예:1",
 "metadata": {"overlay_kind": "unranked", "explanation": "가 바르다"},
 "definitions": {"zh_tw": [{"gloss": ""}]}}
```

**source 5: `gloss_fill_workflow_batch_17_output.staging.jsonl:29`** — 禮 (filled)
```json
{"id": "ko:n:예:1",
 "metadata": {"gloss_status": "filled", "source_basis": "naver_cluster",
   "source_type": "hanja", "selected_cluster": "manners_etiquette"},
 "definitions": {"zh_tw": [{"gloss": "禮"}]}}
```

### Observed Drift

1. **Merge dedup 完全失敗**：3 個真實語義（例子、禮、是）但產生了 9 個 definitions。相同的 gloss 概念以不同措辭重複出現：
   - 「例子」(s1) + 「例子；範例」(s4) + 「例子、實例、先例」(s6) → 都應合併為一個「例子」sense
   - 「禮儀」(s2) + 「禮節；禮貌」(s5) + 「禮節、禮貌」(s7) + 「禮」(s9) → 都應合併為一個「禮」sense
   - 「是」(s3) + 「是、好的 (肯定回答)」(s8) → 都應合併為一個「是」sense

2. **2026-04-29 regression**: 上一個 inventory 版本（2026-04-29）的 ko:n:예 完全是錯誤條目——atom_id 為 `ko:n:예술`（藝術），gloss 為「藝術」，source_refs 指向 batch_201_250.jsonl:5。2026-04-30-fix 修正了這個 atom_id 張冠李戴的問題，但引入了 merge dedup 失敗的新問題。

3. **Unranked overlay 多餘**：ko:n:예:1 的 gloss_fill 產出「禮」，但 main batch 的 예 已包含「禮儀/禮節」sense。此 overlay 是重複的。

4. **Cross-rank merging**：예 出現在兩個不同 rank（3289 和 452），merge 將兩者合併。

### Earliest Contaminated Artifact
- 2026-04-29 inventory 的 `ko:n:예` → `ko:n:예술` identity swap（已在 2026-04-30-fix 修正）
- 當前 merge dedup 問題為 merge 步驟造成

### Duplicate / Merge Review Record
- `duplicate_candidates.csv`: `ko:n:예` → 4 sources（batch_3251_3300, batch_401_450, batch_451_500, batch_6051_6100）
- `semantic_review_queue.csv`: `ko:n:예` → `p0_duplicate_and_multi_sense`（4 sources, 4 entry_nos found, 3 unique senses）
- `rank_cleanup_queue.csv`: `ko:n:예` rank 452 → band I, nikl_topik_agree

### Likely Cause
**Merge dedup 失敗**。 예 在 NIKL 詞庫中作為不同 homonym 以多個 rank 存在（rank 452 = 例, rank 3289 = 禮/例/是）。Merge 將所有 source batch 的 gloss 直接串接，未進行跨 source 的 sense similarity dedup。Unranked overlay 又疊加了另一個「禮」 sense。

### Confidence
**High** (95%)。

### Recommended Fix Type
`one_time_jsonl_repair` — Codex 可精確執行：
- 合併近義 gloss：保留每個概念的最佳措辭
- 3 個 sense → 3 個 entry_no（1, 2, 3）
- 刪除多餘的 unranked overlay gloss（「禮」已由 main batch 覆蓋）

---

## 繁體中文摘要

### 哪些是 generator 造成

- **ko:v:취하다** — Generator 在 batch_2201_2250 中處理 `ko:v:취하다:2225`（hanja: 醉）時，錯誤地將「採取；採用」納入 gloss（應只輸出「喝醉」相關）。此為 prompt/hanja-disambiguation 不足造成的 gloss 污染。
- **ko:n:기능** — Generator 在 batch_5301_5350 中產出 typo「技能；機難」，應為「技能；機能」。且該 batch 的 origin 為「技能, 機能」（雙漢字），generator 未正確分離兩個漢字的 gloss。

### 哪些是 source already dirty

- **ko:n:밤** — Rank collision 污染早於 2026-04-30-fix。batch_6051_6100 中 `ko:n:예` 帶 rank_collision 指向 `밤02`，merge 時將 예 的 gloss 注入了 밤。此污染在 2026-04-29 inventory 中已存在。
- **ko:n:명단** — 相同模式。batch_6201_6250 中 `ko:n:자막` 帶 rank_collision 指向 `명단01`，merge 將 자막 的 gloss 注入 명단。
- **ko:n:문구** — 相同模式。batch_6201_6250 中 `ko:det:자연적` 帶 rank_collision 指向 `문구01`，merge 將 자연적 的 gloss 注入 문구。
- **ko:v:타다** — 多重污染來源：5 個 source batch 的 gloss variance + rank collision（하양 → 타다）+ unranked overlay 的「沾上」。所有問題在 staging batch 生成階段即存在。

### 哪些可以 Codex 修

以下可直接交付 Codex 做 `one_time_jsonl_repair`，安全性高，不需人工語義判斷：

| atom_id | 操作 | 風險 |
|---------|------|------|
| **ko:n:명단** | 刪除 entry_no 2（字幕），entry_no 3→1，修正 translation | Low |
| **ko:n:문구** | 刪除 entry_no 2（自然地），entry_no 3→1，修正 translation | Low（但「文具」義項需人工確認是否補回） |
| **ko:n:예** | 合併近義 gloss 至 3 個 entry_no，刪除重複 | Low-Medium（需確認最佳措辭選擇） |
| **ko:n:밤** | 刪除 entry_no 2 全部三個 gloss（來自 예 的污染） | Low |
| **ko:v:타다** | entry_no 重新編序、刪除「白色」（entry_no 4）、去重合併 | Medium（去重需 sense-level 判斷） |

### 哪些必須人工審

| atom_id | 原因 |
|---------|------|
| **ko:v:취하다** | 需要判斷「取-」和「醉」兩個漢字是否應拆分為獨立 atom，以及每個 entry 應保留哪些正確 gloss。Generator 修正後仍需人工驗證。 |
| **ko:n:기능** | 「功能；職能」在 hanja「技能」下的語義歸屬需要韓語語言學判斷。需決定是否拆分「機能」和「技能」為兩個 atom。 |
| **ko:v:타다** | 8 個語義域的去重合併需要韓語語義層級的人工審核（哪些 gloss 可合併、哪些是不同的 sense）。entry_no 8「沾上」的語義歸屬也需確認。 |
| **ko:n:문구** | 「文具」義項在 gloss_fill 的 naver_gloss 中存在但未被選取，需人工決定是否補回。 |

---

*Report generated: 2026-05-03*
*Data source: content_v2/inventory/dictionary/2026-04-30-fix/*.jsonl + content_v2/staging/dictionary/**
