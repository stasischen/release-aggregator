# Knowledge Migration Pack 003 Plan

## Goal

Plan and execute the third bounded knowledge migration pack for Korean learning-library content.
This pack focuses on **Core Tenses, Negation, and Ability Endings**, which are essential for A1 students to form basic sentences.

---

## Pack 003 Scope

### 1. Basic Tense (Grammar > Tense)

| Canonical ID | Surface | Source Report | Notes |
| :--- | :--- | :--- | :--- |
| `kg.grammar.tense.past_ass_oss` | `~았/었/했-` | `031_過去式了 았었했.md` | Standard past tense suffix. |
| `kg.grammar.tense.future_geoyeyo` | `~ㄹ/을 거예요` | `030_將會 打算 ㄹ을 거예요.md` | Common future/probability ending. |

### 2. Negation (Grammar > Negation)

| Canonical ID | Surface | Source Report | Notes |
| :--- | :--- | :--- | :--- |
| `kg.grammar.negation.short_an` | `안 ~` | `041_不口語否定 안 動詞 形容詞.md` | Short-form negation (adverb). |
| `kg.grammar.negation.long_ji_anta` | `~지 않다` | `040_不否定 지 않다.md` | Long-form/formal negation. |
| `kg.grammar.negation.short_mot` | `못 ~` | `047_不能沒辦法 副詞 못.md` | "Cannot" (lack of ability/circumstance). |

### 3. Ability (Grammar > Ability)

| Canonical ID | Surface | Source Report | Notes |
| :--- | :--- | :--- | :--- |
| `kg.grammar.ability.can` | `~ㄹ/을 수 있다` | `045_會可以 能力可能性 ㄹ을 수 있다.md` | Ability/Possibility. |
| `kg.grammar.ability.cannot` | `~ㄹ/을 수 없다` | `046_不會不能 不可能無能力 ㄹ을 수 없다.md` | Inability/Impossibility. |

---

## Normalization Strategy

1.  **Taxonomy**: Use `grammar > tense`, `grammar > negation`, and `grammar > ability` subcategories.
2.  **ID Standards**: Follow `kg.grammar.<subcategory>.<slug>` format.
3.  **Title/Summary**: Rename source titles for clarity (e.g., `031_過去式了 았었했` -> `過去式 (~았/었/했)`).
4.  **Example Selection**: Extract 3-5 clean examples from reports.

---

## Tasks

- [ ] Create core JSON files in `content-ko/content/core/learning_library/knowledge/grammar/{tense,negation,ability}/`
- [ ] Create i18n JSON files in `content-ko/content/i18n/zh_tw/learning_library/knowledge/grammar/{tense,negation,ability}/`
- [ ] Verify build artifacts
- [ ] Link to existing A1 dialogues if applicable (e.g., A1-01)
