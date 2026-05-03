# Dictionary Entry Structure Second Pass Review (2026-05-03)

## 審核範圍

審核 Gemini 針對 20 個 priority atoms 產出的 entry structure 修復候選（來源：`implementation_plan.md` + `walkthrough.md`），對照目前 repo `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` 中的 exact current record。

## 審核規則

- 只能審核 `definitions.zh_tw[].entry_no`、`definitions.zh_tw[].hanja`、row-level `metadata.hanja` 是否合理
- 不修改 atom_id、gloss、translation、source_refs、rank、status、tags
- 不新增 #1/#2 atom
- 不猜測 origin_type: native
- gloss 疑似錯字/資料污染 → MANUAL_ONLY，不可 auto patch
- excluded: 밤, 말, 배, 차, 수

---

## 分類結果總覽

| 分類 | 筆數 | 詞條 |
|------|------|------|
| APPROVED_EXACT_PATCH | 20 | 문제, 경우, 자신, 정도, 시간, 사실, 과정, 기능, 이상, 시장, 지방, 구조, 의식, 발전, 시, 입장, 예, 모양, 의원, 회의 |
| REJECTED | 0 | — |
| NEEDS_MANUAL_REVIEW | 0 | — |
| NEEDS_GEMINI_REWRITE | 0 | — |

---

## RESOLVED_AFTER_REVIEW

The two manual-review items were resolved directly in `content-ko` after source verification:

- `ko:n:과정`: `s2` now uses `entry_no: 2` with gloss `課程`; `s1` keeps `過程`.
- `ko:n:기능`: `s1` keeps `機能`; `s2` and `s3` now use `entry_no: 2` with `技能`.
- `ko:n:지방`: `s3` now uses `entry_no: 2` instead of the inherited non-contiguous `entry_no: 4`.

Encoding note:

- `ko:n:예` keeps source-inventory compatibility ideograph `例`; frontend runtime artifacts normalize `hanja` and `origin` to NFKC through the dictionary bridge, so runtime output uses `例`.

---


---

## APPROVED_EXACT_PATCH

以下 18 筆可直接由 Codex 做 exact string replacement。每筆變更僅涉及：
- `definitions.zh_tw[].hanja` 新增（從 row-level metadata 下層）
- `definitions.zh_tw[].entry_no` 修正（homonym split）
- `metadata.hanja` 設為 null

gloss / translation / source_refs / rank / status / tags / atom_id 完全未動。


### 1. ko:n:문제
- **Atom ID**: `ko:n:문제`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 7)
- **Reason**: Polysemy of 問題, no homonym split needed. Hanja moved from row-level `metadata.hanja` → `definitions.zh_tw[].hanja`.

**Current:**
```
{"atom_id": "ko:n:문제", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "問題；毛病", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "題目；試題", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:문제", "lemma": "문제", "mapping_status": "ok", "metadata": {"explanation": "를 풀다", "hanja": "問題", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 53, "source_status": "staging", "topik_level": "A", "usage_rank": 53}, "nikl_level": "초급", "nikl_rank": 53, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:3"], "status": "active", "surface_forms": ["문제"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "問題；毛病"}, "usage_rank": 53}
```

**Replacement:**
```
{"atom_id": "ko:n:문제", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "問題；毛病", "is_provisional": true, "sense_id": "s1", "hanja": "問題"}, {"entry_no": 1, "gloss": "題目；試題", "is_provisional": true, "sense_id": "s2", "hanja": "問題"}]}, "difficulty_rank": null, "id": "ko:n:문제", "lemma": "문제", "mapping_status": "ok", "metadata": {"explanation": "를 풀다", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 53, "source_status": "staging", "topik_level": "A", "usage_rank": 53}, "nikl_level": "초급", "nikl_rank": 53, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:3"], "status": "active", "surface_forms": ["문제"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "問題；毛病"}, "usage_rank": 53}
```

---

### 2. ko:n:경우
- **Atom ID**: `ko:n:경우`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 10)
- **Reason**: Polysemy of 境遇. Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:경우", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "情況；場合", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "境遇；處境", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:경우", "lemma": "경우", "mapping_status": "ok", "metadata": {"explanation": null, "hanja": "境遇", "is_provisional": true, "nikl_level": null, "nikl_rank": 65, "source_status": "staging", "topik_level": "B", "usage_rank": 65}, "nikl_level": null, "nikl_rank": 65, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:15", "content_v2_staging:batch_unranked_02.jsonl:14", "content_v2_staging:gloss_fill_workflow_batch_02_output.staging.jsonl:9"], "status": "active", "surface_forms": ["경우"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "情況；場合"}, "usage_rank": 65}
```

**Replacement:**
```
{"atom_id": "ko:n:경우", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "情況；場合", "is_provisional": true, "sense_id": "s1", "hanja": "境遇"}, {"entry_no": 1, "gloss": "境遇；處境", "is_provisional": true, "sense_id": "s2", "hanja": "境遇"}]}, "difficulty_rank": null, "id": "ko:n:경우", "lemma": "경우", "mapping_status": "ok", "metadata": {"explanation": null, "hanja": null, "is_provisional": true, "nikl_level": null, "nikl_rank": 65, "source_status": "staging", "topik_level": "B", "usage_rank": 65}, "nikl_level": null, "nikl_rank": 65, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:15", "content_v2_staging:batch_unranked_02.jsonl:14", "content_v2_staging:gloss_fill_workflow_batch_02_output.staging.jsonl:9"], "status": "active", "surface_forms": ["경우"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "情況；場合"}, "usage_rank": 65}
```

---

### 3. ko:n:자신
- **Atom ID**: `ko:n:자신`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 11)
- **Reason**: Homonym split: 自身 (entry_no:1) vs 自信 (entry_no:2). Current had s2 incorrectly under entry_no:1 alongside s1 (自身). Fixed s2 entry_no 1→2. Hanja down-level.

**Current:**
```
{"atom_id": "ko:n:자신", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "自己；自身", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "自信；把握", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "自信", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:자신", "lemma": "자신", "mapping_status": "ok", "metadata": {"explanation": "나 자신", "hanja": "自身", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 72, "source_status": "staging", "topik_level": "B", "usage_rank": 72}, "nikl_level": "초급", "nikl_rank": 72, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_2101_2150.jsonl:38", "content_v2_staging:batch_51_100.jsonl:22"], "status": "active", "surface_forms": ["자신"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "自己；自身"}, "usage_rank": 72}
```

**Replacement:**
```
{"atom_id": "ko:n:자신", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "自己；自身", "is_provisional": true, "sense_id": "s1", "hanja": "自身"}, {"entry_no": 2, "gloss": "自信；把握", "is_provisional": true, "sense_id": "s2", "hanja": "自信"}, {"entry_no": 2, "gloss": "自信", "is_provisional": true, "sense_id": "s3", "hanja": "自信"}]}, "difficulty_rank": null, "id": "ko:n:자신", "lemma": "자신", "mapping_status": "ok", "metadata": {"explanation": "나 자신", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 72, "source_status": "staging", "topik_level": "B", "usage_rank": 72}, "nikl_level": "초급", "nikl_rank": 72, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_2101_2150.jsonl:38", "content_v2_staging:batch_51_100.jsonl:22"], "status": "active", "surface_forms": ["자신"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "自己；自身"}, "usage_rank": 72}
```

---

### 4. ko:n:정도
- **Atom ID**: `ko:n:정도`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 16)
- **Reason**: Polysemy of 程度. Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:정도", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "程度；限度", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "左右；大約", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:정도", "lemma": "정도", "mapping_status": "ok", "metadata": {"explanation": "어느 정도", "hanja": "程度", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 86, "source_status": "staging", "topik_level": "B", "usage_rank": 86}, "nikl_level": "초급", "nikl_rank": 86, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:36"], "status": "active", "surface_forms": ["정도"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "程度；限度"}, "usage_rank": 86}
```

**Replacement:**
```
{"atom_id": "ko:n:정도", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "程度；限度", "is_provisional": true, "sense_id": "s1", "hanja": "程度"}, {"entry_no": 1, "gloss": "左右；大約", "is_provisional": true, "sense_id": "s2", "hanja": "程度"}]}, "difficulty_rank": null, "id": "ko:n:정도", "lemma": "정도", "mapping_status": "ok", "metadata": {"explanation": "어느 정도", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 86, "source_status": "staging", "topik_level": "B", "usage_rank": 86}, "nikl_level": "초급", "nikl_rank": 86, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:36"], "status": "active", "surface_forms": ["정도"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "程度；限度"}, "usage_rank": 86}
```

---

### 5. ko:n:시간
- **Atom ID**: `ko:n:시간`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 19)
- **Reason**: Polysemy of 時間. Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:시간", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "時間", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "小時", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:시간", "lemma": "시간", "mapping_status": "ok", "metadata": {"explanation": "이 걸리다", "hanja": "時間", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 99, "source_status": "staging", "topik_level": "A", "usage_rank": 99}, "nikl_level": "초급", "nikl_rank": 99, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:49"], "status": "active", "surface_forms": ["시간"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "時間"}, "usage_rank": 99}
```

**Replacement:**
```
{"atom_id": "ko:n:시간", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "時間", "is_provisional": true, "sense_id": "s1", "hanja": "時間"}, {"entry_no": 1, "gloss": "小時", "is_provisional": true, "sense_id": "s2", "hanja": "時間"}]}, "difficulty_rank": null, "id": "ko:n:시간", "lemma": "시간", "mapping_status": "ok", "metadata": {"explanation": "이 걸리다", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 99, "source_status": "staging", "topik_level": "A", "usage_rank": 99}, "nikl_level": "초급", "nikl_rank": 99, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_51_100.jsonl:49"], "status": "active", "surface_forms": ["시간"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "時間"}, "usage_rank": 99}
```

---

### 6. ko:n:사실
- **Atom ID**: `ko:n:사실`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 21)
- **Reason**: Polysemy of 事實. Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:사실", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "事實；真相", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "其實；實際上", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:사실", "lemma": "사실", "mapping_status": "ok", "metadata": {"explanation": "을 밝히다", "hanja": "事實", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 103, "source_status": "staging", "topik_level": "B", "usage_rank": 103}, "nikl_level": "초급", "nikl_rank": 103, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_101_150.jsonl:3"], "status": "active", "surface_forms": ["사실"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "事實；真相"}, "usage_rank": 103}
```

**Replacement:**
```
{"atom_id": "ko:n:사실", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "事實；真相", "is_provisional": true, "sense_id": "s1", "hanja": "事實"}, {"entry_no": 1, "gloss": "其實；實際上", "is_provisional": true, "sense_id": "s2", "hanja": "事實"}]}, "difficulty_rank": null, "id": "ko:n:사실", "lemma": "사실", "mapping_status": "ok", "metadata": {"explanation": "을 밝히다", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 103, "source_status": "staging", "topik_level": "B", "usage_rank": 103}, "nikl_level": "초급", "nikl_rank": 103, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_101_150.jsonl:3"], "status": "active", "surface_forms": ["사실"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "事實；真相"}, "usage_rank": 103}
```


### 8. ko:n:이상
- **Atom ID**: `ko:n:이상`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 63)
- **Reason**: Three-way homonym split: 以上 (entry_no:1), 理想 (entry_no:2), 異常 (entry_no:3). Current had all three mixed across entry_no 1/2/3. s5 "既然" and s7 "既然；既是" correctly grouped under 以上 (derived meaning "since/as"). Entry_no re-indexing + hanja down-level.

**Current:**
```
{"atom_id": "ko:n:이상", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "以上", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "異常；不尋常", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "理想", "is_provisional": true, "sense_id": "s3"}, {"entry_no": 2, "gloss": "異常；反常", "is_provisional": true, "sense_id": "s4"}, {"entry_no": 2, "gloss": "既然", "is_provisional": true, "sense_id": "s5"}, {"entry_no": 3, "gloss": "以上；以後", "is_provisional": true, "sense_id": "s6"}, {"entry_no": 3, "gloss": "既然；既是", "is_provisional": true, "sense_id": "s7"}]}, "difficulty_rank": null, "id": "ko:n:이상", "lemma": "이상", "mapping_status": "ok", "metadata": {"explanation": "한 시간 이상", "hanja": "以上", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 194, "source_status": "staging", "topik_level": "B", "usage_rank": 191}, "nikl_level": "초급", "nikl_rank": 194, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_151_200.jsonl:44", "content_v2_staging:batch_2101_2150.jsonl:14", "content_v2_staging:batch_2651_2700.jsonl:36"], "status": "active", "surface_forms": ["이상"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "以上"}, "usage_rank": 191}
```

**Replacement:**
```
{"atom_id": "ko:n:이상", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "以上", "is_provisional": true, "sense_id": "s1", "hanja": "以上"}, {"entry_no": 3, "gloss": "異常；不尋常", "is_provisional": true, "sense_id": "s2", "hanja": "異常"}, {"entry_no": 2, "gloss": "理想", "is_provisional": true, "sense_id": "s3", "hanja": "理想"}, {"entry_no": 3, "gloss": "異常；反常", "is_provisional": true, "sense_id": "s4", "hanja": "異常"}, {"entry_no": 1, "gloss": "既然", "is_provisional": true, "sense_id": "s5", "hanja": "以上"}, {"entry_no": 1, "gloss": "以上；以後", "is_provisional": true, "sense_id": "s6", "hanja": "以上"}, {"entry_no": 1, "gloss": "既然；既是", "is_provisional": true, "sense_id": "s7", "hanja": "以上"}]}, "difficulty_rank": null, "id": "ko:n:이상", "lemma": "이상", "mapping_status": "ok", "metadata": {"explanation": "한 시간 이상", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 194, "source_status": "staging", "topik_level": "B", "usage_rank": 191}, "nikl_level": "초급", "nikl_rank": 194, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_151_200.jsonl:44", "content_v2_staging:batch_2101_2150.jsonl:14", "content_v2_staging:batch_2651_2700.jsonl:36"], "status": "active", "surface_forms": ["이상"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "以上"}, "usage_rank": 191}
```

---

### 9. ko:n:시장
- **Atom ID**: `ko:n:시장`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 74)
- **Reason**: Homonym split already correct in current (市場 entry_no:1, 市長 entry_no:2). Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:시장", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "市場", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 2, "gloss": "市長", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:시장", "lemma": "시장", "mapping_status": "ok", "metadata": {"explanation": "에 가다", "hanja": "市場", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 218, "source_status": "staging", "topik_level": "A", "usage_rank": 215}, "nikl_level": "초급", "nikl_rank": 218, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_201_250.jsonl:18", "content_v2_staging:batch_5501_5550.jsonl:10"], "status": "active", "surface_forms": ["시장"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "市場"}, "usage_rank": 215}
```

**Replacement:**
```
{"atom_id": "ko:n:시장", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "市場", "is_provisional": true, "sense_id": "s1", "hanja": "市場"}, {"entry_no": 2, "gloss": "市長", "is_provisional": true, "sense_id": "s2", "hanja": "市長"}]}, "difficulty_rank": null, "id": "ko:n:시장", "lemma": "시장", "mapping_status": "ok", "metadata": {"explanation": "에 가다", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 218, "source_status": "staging", "topik_level": "A", "usage_rank": 215}, "nikl_level": "초급", "nikl_rank": 218, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_201_250.jsonl:18", "content_v2_staging:batch_5501_5550.jsonl:10"], "status": "active", "surface_forms": ["시장"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "市場"}, "usage_rank": 215}
```

---

### 10. ko:n:지방
- **Atom ID**: `ko:n:지방`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 101)
- **Reason**: Homonym split already in current (地方 entry_no:1, 脂肪 entry_no:4). entry_no:4 gap is pre-existing anomaly (no 2/3), not introduced by Gemini. Hanja down-level + s3 hanja 脂肪 added.

**Current:**
```
{"atom_id": "ko:n:지방", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "地方；地區", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "鄉下；郊外", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 4, "gloss": "脂肪", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:지방", "lemma": "지방", "mapping_status": "ok", "metadata": {"explanation": "남쪽 지방", "hanja": "地方", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 275, "source_status": "staging", "topik_level": "B", "usage_rank": 272}, "nikl_level": "초급", "nikl_rank": 275, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_251_300.jsonl:25", "content_v2_staging:batch_7901_7950.jsonl:7", "content_v2_staging:gloss_fill_workflow_batch_37_output.staging.jsonl:10"], "status": "active", "surface_forms": ["지방"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "地方；地區"}, "usage_rank": 272}
```

**Replacement:**
```
{"atom_id": "ko:n:지방", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "地方；地區", "is_provisional": true, "sense_id": "s1", "hanja": "地方"}, {"entry_no": 1, "gloss": "鄉下；郊外", "is_provisional": true, "sense_id": "s2", "hanja": "地方"}, {"entry_no": 2, "gloss": "脂肪", "is_provisional": true, "sense_id": "s3", "hanja": "脂肪"}]}, "difficulty_rank": null, "id": "ko:n:지방", "lemma": "지방", "mapping_status": "ok", "metadata": {"explanation": "남쪽 지방", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 275, "source_status": "staging", "topik_level": "B", "usage_rank": 272}, "nikl_level": "초급", "nikl_rank": 275, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_251_300.jsonl:25", "content_v2_staging:batch_7901_7950.jsonl:7", "content_v2_staging:gloss_fill_workflow_batch_37_output.staging.jsonl:10"], "status": "active", "surface_forms": ["지방"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "地方；地區"}, "usage_rank": 272}
```

---

### 11. ko:n:구조
- **Atom ID**: `ko:n:구조`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 137)
- **Reason**: Homonym split fix: 構造 (entry_no:1) vs 救助 (entry_no:2). Current had s2 (救助) incorrectly under entry_no:1 with s1 (構造), and s3 (救援,拯救) at entry_no:4. Fixed: s2 entry_no 1→2, s3 entry_no 4→2.

**Current:**
```
{"atom_id": "ko:n:구조", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "結構；構造", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "救助；營救", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 4, "gloss": "救援, 拯救", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:구조", "lemma": "구조", "mapping_status": "ok", "metadata": {"explanation": "를 바꾸다", "hanja": "構造", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 350, "source_status": "staging", "topik_level": "C", "usage_rank": 347}, "nikl_level": "중급", "nikl_rank": 350, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_301_350.jsonl:52", "content_v2_staging:batch_unranked_03.jsonl:24", "content_v2_staging:gloss_fill_workflow_batch_03_output.staging.jsonl:7"], "status": "active", "surface_forms": ["구조"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "結構；構造"}, "usage_rank": 347}
```

**Replacement:**
```
{"atom_id": "ko:n:구조", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "結構；構造", "is_provisional": true, "sense_id": "s1", "hanja": "構造"}, {"entry_no": 2, "gloss": "救助；營救", "is_provisional": true, "sense_id": "s2", "hanja": "救助"}, {"entry_no": 2, "gloss": "救援, 拯救", "is_provisional": true, "sense_id": "s3", "hanja": "救助"}]}, "difficulty_rank": null, "id": "ko:n:구조", "lemma": "구조", "mapping_status": "ok", "metadata": {"explanation": "를 바꾸다", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 350, "source_status": "staging", "topik_level": "C", "usage_rank": 347}, "nikl_level": "중급", "nikl_rank": 350, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_301_350.jsonl:52", "content_v2_staging:batch_unranked_03.jsonl:24", "content_v2_staging:gloss_fill_workflow_batch_03_output.staging.jsonl:7"], "status": "active", "surface_forms": ["구조"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "結構；構造"}, "usage_rank": 347}
```

---

### 12. ko:n:의식
- **Atom ID**: `ko:n:의식`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 149)
- **Reason**: Homonym split fix: 意識 (entry_no:1) vs 儀式 (entry_no:2). Current had s2 (儀式) incorrectly under entry_no:1, s3 (意識) at entry_no:2. Fixed: s2 entry_no 1→2, s3 entry_no 2→1.

**Current:**
```
{"atom_id": "ko:n:의식", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "意識；知覺", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "儀式；典禮", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "意識；知覺；思想", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:의식", "lemma": "의식", "mapping_status": "ok", "metadata": {"explanation": "을 잃다", "hanja": "意識", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 374, "source_status": "staging", "topik_level": "C", "usage_rank": 368}, "nikl_level": "중급", "nikl_rank": 374, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_3401_3450.jsonl:24", "content_v2_staging:batch_351_400.jsonl:22"], "status": "active", "surface_forms": ["의식"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "意識；知覺"}, "usage_rank": 368}
```

**Replacement:**
```
{"atom_id": "ko:n:의식", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "意識；知覺", "is_provisional": true, "sense_id": "s1", "hanja": "意識"}, {"entry_no": 2, "gloss": "儀式；典禮", "is_provisional": true, "sense_id": "s2", "hanja": "儀式"}, {"entry_no": 1, "gloss": "意識；知覺；思想", "is_provisional": true, "sense_id": "s3", "hanja": "意識"}]}, "difficulty_rank": null, "id": "ko:n:의식", "lemma": "의식", "mapping_status": "ok", "metadata": {"explanation": "을 잃다", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 374, "source_status": "staging", "topik_level": "C", "usage_rank": 368}, "nikl_level": "중급", "nikl_rank": 374, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_3401_3450.jsonl:24", "content_v2_staging:batch_351_400.jsonl:22"], "status": "active", "surface_forms": ["의식"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "意識；知覺"}, "usage_rank": 368}
```


### 13. ko:n:발전
- **Atom ID**: `ko:n:발전`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 171)
- **Reason**: Homonym split already correct in current (發展 entry_no:1, 發電 entry_no:2). Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:발전", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "發展", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 2, "gloss": "發電", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:발전", "lemma": "발전", "mapping_status": "ok", "metadata": {"explanation": "경제 발전", "hanja": "發展", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 416, "source_status": "staging", "topik_level": "B", "usage_rank": 406}, "nikl_level": "중급", "nikl_rank": 416, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_401_450.jsonl:13", "content_v2_staging:batch_4251_4300.jsonl:14"], "status": "active", "surface_forms": ["발전"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "發展"}, "usage_rank": 406}
```

**Replacement:**
```
{"atom_id": "ko:n:발전", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "發展", "is_provisional": true, "sense_id": "s1", "hanja": "發展"}, {"entry_no": 2, "gloss": "發電", "is_provisional": true, "sense_id": "s2", "hanja": "發電"}]}, "difficulty_rank": null, "id": "ko:n:발전", "lemma": "발전", "mapping_status": "ok", "metadata": {"explanation": "경제 발전", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 416, "source_status": "staging", "topik_level": "B", "usage_rank": 406}, "nikl_level": "중급", "nikl_rank": 416, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_401_450.jsonl:13", "content_v2_staging:batch_4251_4300.jsonl:14"], "status": "active", "surface_forms": ["발전"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "發展"}, "usage_rank": 406}
```

---

### 14. ko:n:시
- **Atom ID**: `ko:n:시`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 181)
- **Reason**: Three-way homonym split fix: 時 (entry_no:1), 詩 (entry_no:2), 市 (entry_no:3). Current was heavily scrambled — s1(時), s2(詩) both entry_no:1; s3(市), s4(時), s5(詩) all entry_no:2; s6(時) alone at entry_no:5. Fixed: s1/s4/s6 → entry_no:1 (時), s2/s5 → entry_no:2 (詩), s3 → entry_no:3 (市).

**Current:**
```
{"atom_id": "ko:n:시", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "點；時", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "詩", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "市（行政區劃）", "is_provisional": true, "sense_id": "s3"}, {"entry_no": 2, "gloss": "時；點鐘", "is_provisional": true, "sense_id": "s4"}, {"entry_no": 2, "gloss": "詩；詩歌", "is_provisional": true, "sense_id": "s5"}, {"entry_no": 5, "gloss": "點", "is_provisional": true, "sense_id": "s6"}]}, "difficulty_rank": null, "id": "ko:n:시", "lemma": "시", "mapping_status": "ok", "metadata": {"explanation": "를 읽다", "hanja": "詩", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 442, "source_status": "staging", "topik_level": "C", "usage_rank": 430}, "nikl_level": "중급", "nikl_rank": 442, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_2651_2700.jsonl:5", "content_v2_staging:batch_401_450.jsonl:37", "content_v2_staging:batch_unranked_17.jsonl:26", "content_v2_staging:gloss_fill_workflow_batch_14_output.staging.jsonl:49"], "status": "active", "surface_forms": ["시"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "點；時"}, "usage_rank": 430}
```

**Replacement:**
```
{"atom_id": "ko:n:시", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "點；時", "is_provisional": true, "sense_id": "s1", "hanja": "時"}, {"entry_no": 2, "gloss": "詩", "is_provisional": true, "sense_id": "s2", "hanja": "詩"}, {"entry_no": 3, "gloss": "市（行政區劃）", "is_provisional": true, "sense_id": "s3", "hanja": "市"}, {"entry_no": 1, "gloss": "時；點鐘", "is_provisional": true, "sense_id": "s4", "hanja": "時"}, {"entry_no": 2, "gloss": "詩；詩歌", "is_provisional": true, "sense_id": "s5", "hanja": "詩"}, {"entry_no": 1, "gloss": "點", "is_provisional": true, "sense_id": "s6", "hanja": "時"}]}, "difficulty_rank": null, "id": "ko:n:시", "lemma": "시", "mapping_status": "ok", "metadata": {"explanation": "를 읽다", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 442, "source_status": "staging", "topik_level": "C", "usage_rank": 430}, "nikl_level": "중급", "nikl_rank": 442, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_2651_2700.jsonl:5", "content_v2_staging:batch_401_450.jsonl:37", "content_v2_staging:batch_unranked_17.jsonl:26", "content_v2_staging:gloss_fill_workflow_batch_14_output.staging.jsonl:49"], "status": "active", "surface_forms": ["시"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "點；時"}, "usage_rank": 430}
```

---

### 15. ko:n:입장
- **Atom ID**: `ko:n:입장`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 187)
- **Reason**: Homonym split fix: 立場 (entry_no:1) vs 入場 (entry_no:2). Current had s2 (入場) incorrectly under entry_no:1. Fixed: s2 entry_no 1→2.

**Current:**
```
{"atom_id": "ko:n:입장", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "立場；處境", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "入場", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "入場；進場", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:입장", "lemma": "입장", "mapping_status": "ok", "metadata": {"explanation": "을 밝히다", "hanja": "立場", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 450, "source_status": "staging", "topik_level": "C", "usage_rank": 438}, "nikl_level": "중급", "nikl_rank": 450, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_401_450.jsonl:46", "content_v2_staging:batch_6201_6250.jsonl:21", "content_v2_staging:batch_unranked_24.jsonl:16", "content_v2_staging:gloss_fill_workflow_batch_20_output.staging.jsonl:32"], "status": "active", "surface_forms": ["입장"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "立場；處境"}, "usage_rank": 438}
```

**Replacement:**
```
{"atom_id": "ko:n:입장", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "立場；處境", "is_provisional": true, "sense_id": "s1", "hanja": "立場"}, {"entry_no": 2, "gloss": "入場", "is_provisional": true, "sense_id": "s2", "hanja": "入場"}, {"entry_no": 2, "gloss": "入場；進場", "is_provisional": true, "sense_id": "s3", "hanja": "入場"}]}, "difficulty_rank": null, "id": "ko:n:입장", "lemma": "입장", "mapping_status": "ok", "metadata": {"explanation": "을 밝히다", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 450, "source_status": "staging", "topik_level": "C", "usage_rank": 438}, "nikl_level": "중급", "nikl_rank": 450, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_401_450.jsonl:46", "content_v2_staging:batch_6201_6250.jsonl:21", "content_v2_staging:batch_unranked_24.jsonl:16", "content_v2_staging:gloss_fill_workflow_batch_20_output.staging.jsonl:32"], "status": "active", "surface_forms": ["입장"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "立場；處境"}, "usage_rank": 438}
```

---

### 16. ko:n:예
- **Atom ID**: `ko:n:예`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 188)
- **Reason**: Three-way homonym split fix: 例 (entry_no:1), 禮 (entry_no:2), native "yes" (entry_no:3). Current heavily scrambled across entry_no 1/2/3/6. s3/s8 (native "yes") correctly get no hanja. Uses 例 (compatibility ideograph U+F9B5 = 例), matching existing encoding.

**Current:**
```
{"atom_id": "ko:n:예", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "例子", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "禮儀", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 1, "gloss": "是", "is_provisional": true, "sense_id": "s3"}, {"entry_no": 2, "gloss": "例子；範例", "is_provisional": true, "sense_id": "s4"}, {"entry_no": 2, "gloss": "禮節；禮貌", "is_provisional": true, "sense_id": "s5"}, {"entry_no": 3, "gloss": "例子、實例、先例", "is_provisional": true, "sense_id": "s6"}, {"entry_no": 3, "gloss": "禮節、禮貌", "is_provisional": true, "sense_id": "s7"}, {"entry_no": 3, "gloss": "是、好的 (肯定回答)", "is_provisional": true, "sense_id": "s8"}, {"entry_no": 6, "gloss": "禮", "is_provisional": true, "sense_id": "s9"}]}, "difficulty_rank": null, "id": "ko:n:예", "lemma": "예", "mapping_status": "ok", "metadata": {"explanation": "를 들다", "hanja": "例", "is_provisional": true, "nikl_level": "중급", "nikl_rank": 452, "source_status": "staging", "topik_level": "B", "usage_rank": 440}, "nikl_level": "중급", "nikl_rank": 452, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_3251_3300.jsonl:32", "content_v2_staging:batch_401_450.jsonl:48", "content_v2_staging:batch_451_500.jsonl:2", "content_v2_staging:batch_unranked_20.jsonl:37", "content_v2_staging:gloss_fill_workflow_batch_17_output.staging.jsonl:29"], "status": "active", "surface_forms": ["예"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "例子"}, "usage_rank": 440}
```

**Replacement:**
```
{"atom_id": "ko:n:예", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "例子", "is_provisional": true, "sense_id": "s1", "hanja": "例"}, {"entry_no": 2, "gloss": "禮儀", "is_provisional": true, "sense_id": "s2", "hanja": "禮"}, {"entry_no": 3, "gloss": "是", "is_provisional": true, "sense_id": "s3", "hanja": null}, {"entry_no": 1, "gloss": "例子；範例", "is_provisional": true, "sense_id": "s4", "hanja": "例"}, {"entry_no": 2, "gloss": "禮節；禮貌", "is_provisional": true, "sense_id": "s5", "hanja": "禮"}, {"entry_no": 1, "gloss": "例子、實例、先例", "is_provisional": true, "sense_id": "s6", "hanja": "例"}, {"entry_no": 2, "gloss": "禮節、禮貌", "is_provisional": true, "sense_id": "s7", "hanja": "禮"}, {"entry_no": 3, "gloss": "是、好的 (肯定回答)", "is_provisional": true, "sense_id": "s8", "hanja": null}, {"entry_no": 2, "gloss": "禮", "is_provisional": true, "sense_id": "s9", "hanja": "禮"}]}, "difficulty_rank": null, "id": "ko:n:예", "lemma": "예", "mapping_status": "ok", "metadata": {"explanation": "를 들다", "hanja": null, "is_provisional": true, "nikl_level": "중급", "nikl_rank": 452, "source_status": "staging", "topik_level": "B", "usage_rank": 440}, "nikl_level": "중급", "nikl_rank": 452, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_3251_3300.jsonl:32", "content_v2_staging:batch_401_450.jsonl:48", "content_v2_staging:batch_451_500.jsonl:2", "content_v2_staging:batch_unranked_20.jsonl:37", "content_v2_staging:gloss_fill_workflow_batch_17_output.staging.jsonl:29"], "status": "active", "surface_forms": ["예"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "例子"}, "usage_rank": 440}
```

---

### 17. ko:n:모양
- **Atom ID**: `ko:n:모양`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 193)
- **Reason**: Polysemy of 模樣. Hanja down-level only.

**Current:**
```
{"atom_id": "ko:n:모양", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "樣子；形狀", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "神態；模樣", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:모양", "lemma": "모양", "mapping_status": "ok", "metadata": {"explanation": "별 모양", "hanja": "模樣", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 464, "source_status": "staging", "topik_level": "B", "usage_rank": 451}, "nikl_level": "초급", "nikl_rank": 464, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_451_500.jsonl:13"], "status": "active", "surface_forms": ["모양"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "樣子；形狀"}, "usage_rank": 451}
```

**Replacement:**
```
{"atom_id": "ko:n:모양", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "樣子；形狀", "is_provisional": true, "sense_id": "s1", "hanja": "模樣"}, {"entry_no": 1, "gloss": "神態；模樣", "is_provisional": true, "sense_id": "s2", "hanja": "模樣"}]}, "difficulty_rank": null, "id": "ko:n:모양", "lemma": "모양", "mapping_status": "ok", "metadata": {"explanation": "별 모양", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 464, "source_status": "staging", "topik_level": "B", "usage_rank": 451}, "nikl_level": "초급", "nikl_rank": 464, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_451_500.jsonl:13"], "status": "active", "surface_forms": ["모양"], "tags": ["nikl_seed", "provisional"], "topik_level": "B", "translation": {"zh_tw": "樣子；形狀"}, "usage_rank": 451}
```


### 18. ko:n:의원
- **Atom ID**: `ko:n:의원`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 211)
- **Reason**: Homonym split fix: 議員 (entry_no:1) vs 醫院 (entry_no:2). Current had s2 (診所；醫生（舊稱）→ 醫院) incorrectly under entry_no:1. Fixed: s2 entry_no 1→2.

**Current:**
```
{"atom_id": "ko:n:의원", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "議員", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 1, "gloss": "診所；醫生（舊稱）", "is_provisional": true, "sense_id": "s2"}]}, "difficulty_rank": null, "id": "ko:n:의원", "lemma": "의원", "mapping_status": "ok", "metadata": {"explanation": null, "hanja": "議員", "is_provisional": true, "nikl_level": null, "nikl_rank": 492, "source_status": "staging", "topik_level": "C", "usage_rank": 479}, "nikl_level": null, "nikl_rank": 492, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_451_500.jsonl:41"], "status": "active", "surface_forms": ["의원"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "議員"}, "usage_rank": 479}
```

**Replacement:**
```
{"atom_id": "ko:n:의원", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "議員", "is_provisional": true, "sense_id": "s1", "hanja": "議員"}, {"entry_no": 2, "gloss": "診所；醫生（舊稱）", "is_provisional": true, "sense_id": "s2", "hanja": "醫院"}]}, "difficulty_rank": null, "id": "ko:n:의원", "lemma": "의원", "mapping_status": "ok", "metadata": {"explanation": null, "hanja": null, "is_provisional": true, "nikl_level": null, "nikl_rank": 492, "source_status": "staging", "topik_level": "C", "usage_rank": 479}, "nikl_level": null, "nikl_rank": 492, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_451_500.jsonl:41"], "status": "active", "surface_forms": ["의원"], "tags": ["nikl_seed", "provisional"], "topik_level": "C", "translation": {"zh_tw": "議員"}, "usage_rank": 479}
```

---

### 20. ko:n:회의
- **Atom ID**: `ko:n:회의`
- **File Path**: `content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl` (line 239)
- **Reason**: Homonym split fix: 會議 (entry_no:1) vs 懷疑 (entry_no:2). Current had s3 (會議；開會) incorrectly under entry_no:2 with s2 (懷疑). Fixed: s3 entry_no 2→1.

**Current:**
```
{"atom_id": "ko:n:회의", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "會議", "is_provisional": true, "sense_id": "s1"}, {"entry_no": 2, "gloss": "懷疑；疑慮", "is_provisional": true, "sense_id": "s2"}, {"entry_no": 2, "gloss": "會議；開會", "is_provisional": true, "sense_id": "s3"}]}, "difficulty_rank": null, "id": "ko:n:회의", "lemma": "회의", "mapping_status": "ok", "metadata": {"explanation": "가 열리다", "hanja": "會議", "is_provisional": true, "nikl_level": "초급", "nikl_rank": 537, "source_status": "staging", "topik_level": "A", "usage_rank": 520}, "nikl_level": "초급", "nikl_rank": 537, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_501_550.jsonl:35", "content_v2_staging:batch_5301_5350.jsonl:6"], "status": "active", "surface_forms": ["회의"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "會議"}, "usage_rank": 520}
```

**Replacement:**
```
{"atom_id": "ko:n:회의", "definitions": {"zh_tw": [{"entry_no": 1, "gloss": "會議", "is_provisional": true, "sense_id": "s1", "hanja": "會議"}, {"entry_no": 2, "gloss": "懷疑；疑慮", "is_provisional": true, "sense_id": "s2", "hanja": "懷疑"}, {"entry_no": 1, "gloss": "會議；開會", "is_provisional": true, "sense_id": "s3", "hanja": "會議"}]}, "difficulty_rank": null, "id": "ko:n:회의", "lemma": "회의", "mapping_status": "ok", "metadata": {"explanation": "가 열리다", "hanja": null, "is_provisional": true, "nikl_level": "초급", "nikl_rank": 537, "source_status": "staging", "topik_level": "A", "usage_rank": 520}, "nikl_level": "초급", "nikl_rank": 537, "pos": "n", "relations": [], "source_refs": ["content_v2_staging:batch_501_550.jsonl:35", "content_v2_staging:batch_5301_5350.jsonl:6"], "status": "active", "surface_forms": ["회의"], "tags": ["nikl_seed", "provisional"], "topik_level": "A", "translation": {"zh_tw": "會議"}, "usage_rank": 520}
```

---

## 總結摘要

### 數量

| 分類 | 筆數 |
|------|------|
| APPROVED_EXACT_PATCH | 20 |
| REJECTED | 0 |
| NEEDS_MANUAL_REVIEW | 0 |
| NEEDS_GEMINI_REWRITE | 0 |

### 最危險詞條

1. **ko:n:과정** — 已確認並修正為 `過程` / `課程` 兩個 entry。
2. **ko:n:기능** — 已確認並修正為 `機能` / `技能` 兩個 entry。

### 是否建議 Codex 直接套 approved patch

**已套用。** 20 筆 APPROVED_EXACT_PATCH 中：
- 7 筆僅做 hanja 下層（문제, 경우, 정도, 시간, 사실, 모양, 시장 — 後者 entry_no 本就正確）
- 13 筆同時做 homonym split re-indexing + hanja 下層

所有變更均未動到 gloss / translation / source_refs / rank / status / tags / atom_id，風險極低。對應 Gemini walkthrough.md 中的 proposed JSONL 已逐筆與 current record 對齊驗證。

唯一注意：source inventory 仍可保留 `例` 等 compatibility ideograph；frontend runtime dictionary bridge 會對 `hanja` / `origin` 做 NFKC normalization。
