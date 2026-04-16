# TLG-001 — Unit Blueprint v1 Contract (Target-Language-First)

| Field | Value |
| :--- | :--- |
| **Contract Name** | Target-Language Unit Blueprint Protocol |
| **Version** | `unit_blueprint_v1` |
| **Status** | **FROZEN (Draft Freeze for TLG Track)** |
| **Effective Date** | 2026-03-01 |
| **Scope** | release-aggregator mockups, generator pipeline, checker, frontend adapter |

---

## 1. Goal

定義 `unit_blueprint_v1` 的最小可執行契約，支援：

1. 先以 **目標語內容** 完成教學流程（target-lang first）。
2. 再補齊 **zh_tw / en 教學層**（support languages）。
3. 可被 script 轉換成前端可渲染的 unit flow。

---

## 2. Contract Principles

1. **Pedagogy-first**: 保留既有 `sequence` 教學節點順序與角色語意。
2. **Target-lang canonical**: `payload` 內目標語字串是 canonical source。
3. **Support-lang additive**: `zh_tw/en` 為補充層，不可改寫 target-lang 意圖。
4. **Adapter-safe**: metadata 必須足夠讓 `blueprint -> frontend flow` 無損投影。

---

## 3. Required Top-Level Fields

以下欄位在 `unit_blueprint_v1` 為必填：

| Path | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `version` | string | Yes | Must be `unit_blueprint_v1` |
| `adapter_version` | string | Yes | Must be `frontend_unit_adapter_v1` |
| `unit.unit_id` | string | Yes | e.g., `A1-U04` |
| `unit.level` | string | Yes | `A1`/`A2`... |
| `unit.target_lang` | string | Yes | e.g., `ko`, `ja`, `en` |
| `unit.support_langs` | string[] | Yes | Must include `zh_tw` and `en` in current phase |
| `unit.default_support_lang` | string | Yes | Must be one of `support_langs` |
| `unit.can_do` | string[] | Yes | Unit-level can-do outcomes |
| `unit.skill_targets` | object[] | Yes | Pattern skill targets (see 4.1) |
| `sequence` | object[] | Yes | Node sequence |
| `scheduled_followups` | object[] | Yes | Spaced review / transfer |

---

## 4. Required Metadata Additions

### 4.1 `unit.skill_targets[]`

每個 skill target 必須包含：

| Field | Type | Required |
| :--- | :--- | :--- |
| `skill_id` | string | Yes |
| `can_do` | string | Yes |
| `pattern_refs` | string[] | Yes |
| `success_criteria` | string[] | Yes |
| `transfer_contexts` | string[] | Yes |

### 4.2 Sequence Node Metadata

以下欄位是 v1 必填（Node-level）：

| Path | Required | Notes |
| :--- | :--- | :--- |
| `sequence[].node_id` | Yes | Unique |
| `sequence[].learning_role` | Yes | Existing allowlist |
| `sequence[].content_form` | Yes | Existing + TLG extensions |
| `sequence[].output_mode` | Yes | `none` or interaction mode |
| `sequence[].summary_target_lang` | Yes | Target language summary |
| `sequence[].summary_zh_tw` | Yes | zh_tw support summary |
| `sequence[].summary_en` | Yes | en support summary |
| `sequence[].payload` | Yes | Content payload |

### 4.3 Followup Metadata

`scheduled_followups[]` 必須包含：

| Field | Type | Required |
| :--- | :--- | :--- |
| `timing` | string | Yes (`+1_unit`/`+3_units`) |
| `followup_type` | string | Yes (`review`/`transfer`) |
| `goal_target_lang` | string | Yes |
| `goal_zh_tw` | string | Yes |
| `goal_en` | string | Yes |
| `retrieval_targets` | string[] | Yes |

---

## 5. Checker Rules (for `scripts/mockup_check.py`)

### 5.1 Blockers

1. `ERR_UNSUPPORTED_VERSION_V1`  
   - Trigger: `version != unit_blueprint_v1`
2. `ERR_MISSING_TARGET_LANG`  
   - Trigger: missing/empty `unit.target_lang`
3. `ERR_MISSING_SUPPORT_LANGS`  
   - Trigger: missing `unit.support_langs` or not including `zh_tw` and `en`
4. `ERR_MISSING_SKILL_TARGETS`  
   - Trigger: `unit.skill_targets` empty
5. `ERR_SKILL_TARGET_INCOMPLETE`  
   - Trigger: missing any required fields in 4.1
6. `ERR_MISSING_SUMMARY_LOCALES`  
   - Trigger: missing `summary_target_lang`/`summary_zh_tw`/`summary_en`

### 5.2 Warnings

1. `WARN_EMPTY_CAN_DO`  
   - Trigger: can-do present but too generic/placeholder text
2. `WARN_TODO_LEAKAGE_V1`  
   - Trigger: any `TODO` in learner-facing fields
3. `WARN_WEAK_TRANSFER_CONTEXT`  
   - Trigger: skill target exists but `transfer_contexts` count < 2

---

## 6. Migration Rules (v0 -> v1)

1. Keep old keys (`unit`, `sequence`, `payload`) unchanged to protect renderers.
2. Add v1 metadata fields incrementally; do not rename legacy fields in-place.
3. For old fixtures, allow temporary compatibility via adapter fallback, but v1 freeze requires all blockers resolved.

---

## 7. Definition of Done (TLG-001)

TLG-001 is complete when all are true:

1. This contract file is committed.
2. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-001` as `done`.
3. `TASK_INDEX.md` reflects updated progress.
4. Team can author a v1 fixture skeleton without field ambiguity.

---

## 8. Validation Commands

```bash
# JSON syntax check
jq empty /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TARGET_LANG_COURSE_FACTORY_TASKS.json

# Confirm index wiring
rg -n "TARGET_LANG_COURSE_FACTORY" /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TASK_INDEX.md
```

