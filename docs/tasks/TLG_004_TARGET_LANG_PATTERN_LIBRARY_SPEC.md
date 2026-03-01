# TLG-004 — Target Language Pattern Library Spec (Survival, v1)

| Field | Value |
| :--- | :--- |
| **Spec Name** | Target Language Pattern Library Contract |
| **Version** | `target_lang_pattern_library_v1` |
| **Status** | **FROZEN (for TLG-005/TLG-006 integration)** |
| **Effective Date** | 2026-03-01 |
| **Initial Target Lang** | `ko` |

---

## 1. Goal

建立可機器讀取、可跨語系擴展、且以目標語為主體的句型庫契約，支援：

1. `TLG-005` 依 `can_do + pattern` 產生 A1/A2 survival 單元。
2. `TLG-006` 對句型欄位做語言 gate（語法/語用/語體）驗證。
3. `TLG-003` rubric 直接引用 `required_elements / acceptable_variants / transform_types / repair_links`。

---

## 2. Design Principles

1. **Target-Lang Canonical**：句型 frame 與約束以目標語為唯一 canonical source。
2. **Cross-Lang Core + Lang Extension**：核心欄位跨語系固定，語系特例放在 extension 欄位。
3. **Can-Do Addressable**：每筆 pattern 必須可回溯到單一 `can_do`。
4. **Transform + Repair Ready**：每筆 pattern 必須可用於轉換練習與修復練習。
5. **Transfer First**：每筆 pattern 必須至少支援 2 種情境遷移。

---

## 3. Data Model (Top-Level)

Library 檔案（例如 `ko_survival_pattern_library_v1.json`）必填：

| Field | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| `library_id` | string | Yes | `{lang}_{domain}_pattern_library_v1` |
| `version` | string | Yes | Must be `target_lang_pattern_library_v1` |
| `target_lang` | string | Yes | ISO code, e.g. `ko` |
| `domain` | string | Yes | Must be `survival` |
| `levels` | string[] | Yes | Subset of `A1`, `A2` |
| `entries` | object[] | Yes | Pattern entries |

---

## 4. Pattern Entry Contract

每筆 `entries[]` 必填欄位：

| Field | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| `pattern_id` | string | Yes | `{lang}-{level}-{domain}-{nnn}` (lowercase lang/domain; level uppercase) |
| `level` | string | Yes | `A1` \| `A2` |
| `can_do` | string | Yes | Action sentence, measurable output |
| `frame` | string | Yes | Target-lang sentence frame with `{slot}` markers |
| `slots` | object[] | Yes | Slot definitions |
| `required_elements` | string[] | Yes | Elements needed for rubric pass |
| `acceptable_variants` | string[] | Yes | Canonical alternatives accepted |
| `constraints` | string[] | Yes | Grammar/register/pragmatic constraints |
| `transform_types` | string[] | Yes | Allowed transform operations |
| `repair_links` | string[] | Yes | Repair strategy IDs |
| `transfer_contexts` | string[] | Yes | Cross-scenario transfer list |
| `teaching_notes` | object | Yes | Must include `zh_tw`, reserve `en` |

`teaching_notes` contract:

| Field | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| `teaching_notes.zh_tw` | string | Yes | Non-empty pedagogical explanation |
| `teaching_notes.en` | string | Yes | Reserved field; empty string allowed as `TLG-007` stub in v1 |

`slots[]` contract:

| Field | Type | Required | Rule |
| :--- | :--- | :--- | :--- |
| `name` | string | Yes | snake_case |
| `description` | string | Yes | Slot intent in target-lang usage terms |
| `required` | boolean | Yes | Required in frame output |
| `value_type` | string | Yes | `word` \| `phrase` \| `time_expr` \| `place_expr` \| `quantity_expr` \| `clause` |
| `examples` | string[] | Yes | At least 1 target-lang example |

Special case:

- 固定公式句（例如 `안녕하세요.`）可使用 `slots: []`，但仍需提供 `required_elements` 與 `constraints`。

---

## 5. Enums and Naming Rules

### 5.1 `transform_types` enum

Allowed values (`v1`):

1. `politeness_shift`
2. `speech_level_shift`
3. `tense_shift`
4. `negation`
5. `question_statement`
6. `slot_substitution`
7. `time_expression_shift`
8. `context_retarget`
9. `connective_extension`
10. `modality_shift`

### 5.2 `repair_links` naming

Repair ID format: `R-{LANG}-{CATEGORY}-{NNN}`

- `LANG`: uppercase language code (e.g., `KO`)
- `CATEGORY`:
  - `HON` honorific/register
  - `FORM` morphology/form
  - `ORDER` word order
  - `PART` particle selection
  - `PRAG` pragmatic fit

Registry requirement:

- `repair_links` 必須對應 `docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json` 內存在的 `repair_id`。

### 5.3 `can_do` naming

- 必須以可觀測輸出描述，例如「能在餐廳用禮貌體點餐並指定數量」。
- 不可使用泛稱（如「理解韓文句型」）。

---

## 6. Skill Layering (A1/A2)

### 6.1 A1 Pattern Skill Profile

1. 單句功能優先（自介、點餐、問路、購物、時間）。
2. 單變項轉換為主（slot 代換、問句/陳述切換、否定）。
3. 語體目標：以 `-요` 禮貌體為默認輸出。

### 6.2 A2 Pattern Skill Profile

1. 跨子句與語用精度提升（原因/意圖/偏好/限制）。
2. 雙變項轉換（時態 + 語氣、場景 retarget + 句尾）。
3. 允許 more nuanced register shift（平語/禮貌體切換需受約束）。

---

## 7. Can-Do Mapping Rules

1. 每筆 pattern 僅綁定 1 個主要 `can_do`（可附次要用途但不入欄位）。
2. 同一 `can_do` 在同 level 建議 1-3 個 pattern entries。
3. `unit.skill_targets[].pattern_refs` 僅可引用存在的 `pattern_id`。
4. `can_do` 與 `transfer_contexts` 必須語意一致，不可脫鉤。

---

## 8. Slots / Constraints / Transformability / Repair Mapping

### 8.1 Slots

1. 每個 `{slot}` 必須在 `slots[]` 有同名定義。
2. `required=true` 的 slot 必須出現在 `required_elements` 說明中。
3. A1 pattern 建議 slot 數量 1-3；A2 建議 2-4。

### 8.2 Constraints

1. 必須包含至少 1 條語法或語體限制。
2. 若涉及敬語或終結語尾，需明示語境（陌生人/店員/朋友）。
3. `constraints` 不可只寫教材流程描述，需可驗證。

### 8.3 Transformability

1. 每筆至少 2 個 `transform_types`。
2. A2 至少包含一種非 `slot_substitution` 的結構轉換。
3. `pattern_transform` 任務檢核時需比對 `transform_types` 與輸出一致性。

### 8.4 Repair Mapping

1. 每筆至少 1 個 `repair_links`。
2. 若 pattern 含敬語/語體要求，必須含 `R-KO-HON-*`。
3. 若 pattern 含助詞依賴，必須含 `R-KO-PART-*`。

---

## 9. Transfer Contexts Spec

`transfer_contexts` 必須使用可枚舉場景字串，建議來源：

- `cafe_order`
- `restaurant_order`
- `convenience_store`
- `taxi_ride`
- `subway_navigation`
- `hotel_checkin`
- `airport`
- `classroom`
- `office`
- `friend_chat`
- `service_call`
- `online_message`
- `market`

Rules:

1. 每筆至少 2 個 transfer contexts。
2. 至少 1 個 context 應與原始語境不同（真正遷移）。
3. A2 pattern 建議至少 3 個 contexts。

---

## 10. Integration with TLG-003 Rubric

Pattern 欄位對接 rubric：

1. `required_elements` -> `payload.rubric.required_elements`
2. `acceptable_variants` -> `payload.rubric.acceptable_variants`
3. `transform_types` -> `pattern_transform` 節點的 `transform_type allowlist`
4. `repair_links` -> `P4(response_builder repair)` 的 `trigger_type/repair_goal` 參考
5. `constraints` -> `guided/review_retrieval` 的 `error_classes` 判定依據

Implementation note:

- Generator 在 P3/P4 節點必須回填 pattern metadata，確保 checker 可追溯。

---

## 11. Checker-Validatable Rules (TLG-006 pre-contract)

### 11.1 Blockers

1. `ERR_TLG_PATTERN_LIB_VERSION_INVALID`
- `version != target_lang_pattern_library_v1`

2. `ERR_TLG_PATTERN_ENTRY_MISSING_REQUIRED_FIELD`
- 任一 entry 缺少必填欄位。

3. `ERR_TLG_PATTERN_ID_DUPLICATED`
- `pattern_id` 重複。

4. `ERR_TLG_PATTERN_SLOT_FRAME_MISMATCH`
- frame 的 `{slot}` 與 `slots[].name` 不一致。

5. `ERR_TLG_PATTERN_EMPTY_ZH_TW_NOTE`
- `teaching_notes.zh_tw` 為空。

6. `ERR_TLG_PATTERN_NO_TRANSFER_CONTEXT`
- `transfer_contexts` 長度 < 2。

7. `ERR_TLG_PATTERN_NO_TRANSFORM_TYPE`
- `transform_types` 長度 < 2。

### 11.2 Warnings

1. `WARN_TLG_PATTERN_VARIANTS_EMPTY`
- `acceptable_variants` 為空。

2. `WARN_TLG_PATTERN_WEAK_REPAIR_LINK`
- 無 `R-{LANG}-*` 對應語系 repair ID。

3. `WARN_TLG_PATTERN_GENERIC_CAN_DO`
- `can_do` 為泛稱或不可驗證描述。

4. `WARN_TLG_PATTERN_LOW_CONTEXT_DIVERSITY`
- `transfer_contexts` 全屬同一 micro-domain。

5. `WARN_TLG_PATTERN_EN_NOTE_STUB`
- `teaching_notes.en` 為空字串（v1 允許；建議在 `TLG-007` 補齊）。

---

## 12. Definition of Done (TLG-004)

TLG-004 完成條件：

1. `TLG_004_TARGET_LANG_PATTERN_LIBRARY_SPEC.md` 已提交。
2. `docs/tasks/pattern_library/ko_survival_pattern_library_v1.json` 已提交。
3. 句型資料至少 40 筆，且 A1 >= 25、A2 >= 15。
4. 所有 entries 無未完成標記（例如 `TODO`、`TBD`）。
5. `TARGET_LANG_COURSE_FACTORY_TASKS.json` 將 `TLG-004` 標記為 `done`。
6. `TASK_INDEX.md` 進度同步更新。

---

## 13. Acceptance Commands

```bash
# 1) JSON syntax
jq empty /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json

# 2) Count and level distribution
jq '.entries | length' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json
jq '[.entries[] | select(.level=="A1")] | length' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json
jq '[.entries[] | select(.level=="A2")] | length' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json

# 3) Required fields sanity
jq -e '.entries[] | .pattern_id and .level and .can_do and .frame and .slots and .required_elements and .acceptable_variants and .constraints and .transform_types and .repair_links and .transfer_contexts and .teaching_notes.zh_tw and (.teaching_notes.en!=null)' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json >/dev/null

# 4) No incomplete-marker leakage in data
rg -n "TODO|TBD|placeholder" /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json

# 4.1) Repair links must be resolvable in KO registry
jq -r '.entries[].repair_links[]' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json | sort -u > /tmp/ko_repair_links.used.txt
jq -r '.entries[].repair_id' /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_repair_strategy_registry_v1.json | sort -u > /tmp/ko_repair_links.registry.txt
comm -23 /tmp/ko_repair_links.used.txt /tmp/ko_repair_links.registry.txt

# 5) JSON <-> Markdown round-trip (human-editable document)
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py json-to-md \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.json \
  --output /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.md

python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/pattern_library_codec.py md-to-json \
  --input /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/pattern_library/ko_survival_pattern_library_v1.md \
  --output /Users/ywchen/Dev/lingo/release-aggregator/staging/ko_survival_pattern_library_v1.roundtrip.json
```

---

## 14. Human-Readable Sync Format (v1)

為支援「可讀文件」與「可機器轉換」並存，TLG-004 指定 Markdown sync format：

1. `## Library` 區塊使用 `field/value` 二欄表。
2. 每筆 entry 使用 `## Entry: {pattern_id}`。
3. entry 主欄位使用 `field/value` 二欄表，陣列欄位以 JSON array 字串保存。
4. `### Slots` 使用固定欄位表（`name/description/required/value_type/examples`）。
5. 無 slot 時，使用 `(none)` sentinel row。

Codec script:

- `scripts/pattern_library_codec.py`
