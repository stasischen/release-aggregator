# TLG-003 — Output Mastery Rubric Spec (Target-Language-First)

## 1. Goal

定義 A1/A2 在 `unit_blueprint_v1` 的輸出節點完成門檻，讓：

1. Author 知道每種 output_mode 何時算完成。
2. PM/QA 可一致判定是否達到教學目標。
3. Checker 可檢查 rubrics 欄位完整性與最低門檻。

---

## 2. Scope

本規格涵蓋以下 output modes：

1. `chunk_assembly`
2. `response_builder`
3. `pattern_transform`
4. `guided` (speaking/writing)
5. `review_retrieval`

---

## 3. Rubric Contract Fields

每個可互動輸出節點 (`output_mode != none`) 在 `payload.rubric` 必須提供：

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `completion_policy` | string | Yes | `pass_on_threshold` \| `complete_on_attempt` |
| `min_attempts` | number | Yes | Minimum attempts required before completion |
| `pass_threshold` | number | Yes | 0.0 - 1.0 |
| `max_hints_for_pass` | number | Yes | Maximum hint usage allowed for PASS |
| `required_elements` | string[] | Yes | Target-lang elements to include |
| `acceptable_variants` | string[] | Optional | Valid non-canonical variants |
| `feedback_policy` | string | Yes | `strict`, `supportive`, `coach` |

For `guided`/`review_retrieval`, add:

| Field | Type | Required |
| :--- | :--- | :--- |
| `error_classes` | string[] | Yes |
| `revise_allowed` | boolean | Yes |

---

## 4. Mastery Thresholds by Level

### 4.1 A1 Defaults

| Output Mode | min_attempts | pass_threshold | max_hints_for_pass | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `chunk_assembly` | 2 | 0.80 | 2 | 重點是組裝成功與詞塊順序。 |
| `response_builder` | 2 | 0.75 | 2 | 可接受多個正確語境回應。 |
| `pattern_transform` | 2 | 0.70 | 2 | 以單變項轉換為主。 |
| `guided` | 1 | 0.60 | 3 | 先鼓勵完成，不追求完美。 |
| `review_retrieval` | 2 | 0.65 | 2 | 檢索回想優先於精緻語法。 |

### 4.2 A2 Defaults

| Output Mode | min_attempts | pass_threshold | max_hints_for_pass | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `chunk_assembly` | 2 | 0.85 | 1 | 減少提示依賴。 |
| `response_builder` | 2 | 0.80 | 1 | 要求語用判斷更精準。 |
| `pattern_transform` | 2 | 0.78 | 1 | 可要求雙變項轉換。 |
| `guided` | 2 | 0.70 | 2 | 增加語氣/時態檢核。 |
| `review_retrieval` | 2 | 0.72 | 1 | 提高 recall 穩定度。 |

---

## 5. Mode-Specific Completion Rules

1. `chunk_assembly`
- PASS requires exact or allowed variant match in `target_lang`.
- If using hints > `max_hints_for_pass`, downgrade to REVISE.

2. `response_builder`
- PASS if selected/constructed response is in `accepted_responses`.
- At least one item should support multiple accepted answers to avoid overfitting.

3. `pattern_transform`
- PASS only if transformed output satisfies both:
  - target constraint (`transform_type`)
  - structural integrity (required elements present)

4. `guided` (roleplay/message)
- Can mark `REVISE` when semantics are correct but form/register is weak.
- Must provide actionable feedback in zh_tw and optional en support.

5. `review_retrieval`
- PASS can accept partial recall if core functional intent is preserved.
- Must include reference answers for self-check and PM review.

---

## 6. Error Classes (Minimum Set)

`guided` and `review_retrieval` should use:

1. `missing_element`
2. `semantic_mismatch`
3. `register_mismatch`
4. `form_mismatch`

If target language needs more granularity (e.g., Korean honorific mismatch), add language-specific subclasses in `TLG-006`.

---

## 7. Checker Mapping

### Blockers
- `ERR_TLG_RUBRIC_MISSING`: interactive node missing `payload.rubric`.
- `ERR_TLG_THRESHOLD_INVALID`: thresholds out of range or missing.
- `ERR_TLG_REQUIRED_ELEMENTS_EMPTY`: `required_elements` empty.

### Warnings
- `WARN_TLG_VARIANTS_EMPTY`: no acceptable variants provided.
- `WARN_TLG_GUIDED_NO_ERROR_CLASSES`: guided/retrieval without error classes.
- `WARN_TLG_PASS_TOO_LOW`: pass threshold below A1/A2 default floor.

---

## 8. DoD (TLG-003)

TLG-003 is complete when:

1. This rubric spec is committed.
2. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-003` as `done`.
3. `TASK_INDEX.md` progress is updated.
4. Spec is reference-ready for `TLG-005` generator payload templates and `TLG-008` QA checks.

