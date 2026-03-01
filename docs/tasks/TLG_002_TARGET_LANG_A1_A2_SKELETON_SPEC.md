# TLG-002 — Target-Language-First A1/A2 Skeleton Spec

## 1. Goal

定義 `unit_blueprint_v1` 在 A1/A2 survival 課程的標準骨架，作為：

1. `TLG-005` 生成器的固定輸出序列。
2. `TLG-006/TLG-008` checker 規則來源。
3. `TLG-010` 前端 adapter 的可預期節點合約。

---

## 2. Design Principle: Target-Language-First

1. 每一節點先定義 `target_lang` 教學任務（canonical content）。
2. `zh_tw` / `en` 僅做教學支持，不反向主導內容設計。
3. 句型、修復、轉換任務必須基於目標語真實語用（register, syntax, morphology）。

---

## 3. Mandatory Skeleton (A1/A2)

每單元主序列固定 **13 nodes**，並有 **2 followups**（共 15 element）：

| Order | Node ID Suffix | Learning Role | Content Form | Output Mode | Required |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `-L1` | immersion_input | dialogue | none | Yes |
| 2 | `-L2` | immersion_input | comprehension_check | response_builder | Yes |
| 3 | `-L3` | immersion_input | notice or message_thread | none | Yes |
| 4 | `-D1` | structure_pattern | functional_phrase_pack | chunk_assembly | Yes |
| 5 | `-G1` | structure_pattern | pattern_card | frame_fill | Yes |
| 6 | `-G2` | structure_grammar | grammar_note | none | Yes |
| 7 | `-P1` | controlled_output | practice_card | chunk_assembly | Yes |
| 8 | `-P2` | controlled_output | practice_card | response_builder | Yes |
| 9 | `-P3` | controlled_output | practice_card | pattern_transform | Yes |
| 10 | `-P4` | controlled_output | practice_card | response_builder (repair) | Yes |
| 11 | `-P5` | immersion_output | roleplay_prompt | guided | Yes |
| 12 | `-P6` | immersion_output | message_prompt | guided | Yes |
| 13 | `-R1` | review_retrieval | review_card | review_retrieval | Yes |

`scheduled_followups`:
- `-X1`: `+1_unit`, `followup_type: review`
- `-X2`: `+3_units`, `followup_type: transfer`

---

## 4. Sequencing Constraints (Blocker-Level)

1. `L2` must immediately follow `L1`.
2. No output node (`P*`) can appear before `D1/G1/G2` are present.
3. `P3` must be `pattern_transform`; cannot downgrade to `frame_fill`.
4. `P4` must be repair-oriented (must include repair metadata).
5. `R1` must be final node in `sequence`.
6. Followups must be outside `sequence` and include retrieval/transfer references.

---

## 5. Node Payload Minimums

### 5.1 Input Layer
- `L1 dialogue`: target-lang turns + zh_tw/en gloss support.
- `L2 comprehension_check`: at least 2 tasks, each with accepted responses.
- `L3 notice/message_thread`: non-dialogue document-style input.

### 5.2 Structure Layer
- `D1 functional_phrase_pack`: chunk-oriented items, not isolated nouns only.
- `G1 pattern_card`: at least 1 frame with slot description.
- `G2 grammar_note`: minimal grammar note tied to `G1` pattern usage.

### 5.3 Output Layer
- `P1 chunk_assembly`: at least 2 tasks.
- `P2 response_builder`: at least 2 scenario prompts.
- `P3 pattern_transform`: at least 2 transformations with explicit constraints.
- `P4 repair`: must include `trigger_type` and `repair_goal`.
- `P5/P6 guided`: must include task constraints and required pattern hints.

### 5.4 Review Layer
- `R1 review_card`: must include retrieval prompts and reference answers.
- Followups: must include timing, goal (target_lang/zh_tw/en), and pattern refs.

---

## 6. A1/A2 Output Ratio Guidance

1. A1 recommended output node share: `>= 40%` of sequence.
2. A2 recommended output node share: `>= 45%` of sequence.
3. Guided nodes (`P5/P6`) are mandatory in both levels.

---

## 7. Target-Language Quality Guards

1. No `TODO` or placeholder text in learner-facing target-lang fields for PR units.
2. `pattern_transform` must reflect target-lang grammar constraints (not pure lexical swap only).
3. Repair phrases must match local pragmatic norms (politeness/register).

---

## 8. Checker Rule Mapping

Proposed checker rules for this spec:

### Blockers
- `ERR_TLG_MISSING_MANDATORY_NODE`
- `ERR_TLG_ORDER_VIOLATION`
- `ERR_TLG_MISSING_PATTERN_TRANSFORM`
- `ERR_TLG_MISSING_REPAIR_METADATA`
- `ERR_TLG_MISSING_FOLLOWUP_TIMING`

### Warnings
- `WARN_TLG_LOW_OUTPUT_RATIO`
- `WARN_TLG_WEAK_NON_DIALOGUE_INPUT`
- `WARN_TLG_LOW_TRANSFORM_COMPLEXITY`

---

## 9. Definition of Done (TLG-002)

TLG-002 is complete when:

1. This skeleton spec is committed.
2. `TARGET_LANG_COURSE_FACTORY_TASKS.json` marks `TLG-002` as `done`.
3. `TASK_INDEX.md` progress is updated.
4. The spec can be directly consumed by scaffold/checker implementation tasks.

