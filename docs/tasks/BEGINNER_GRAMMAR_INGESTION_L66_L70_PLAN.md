# Ingest Beginner Korean Grammar L66–L70 (Source 067–071)

This plan covers the systematic ingestion of 5 beginner Korean grammar lessons from the YouTube curriculum source into the `content-ko` production library.

## User Review Required

> [!IMPORTANT]
> **Sentence Count Clarification**: The user request mentioned "生成 10 句全新的原創例句", but usually each lesson in this series requires 10 sentences (total 50 for 5 lessons). I will proceed with **10 sentences per lesson (Total 50)** to maintain consistency with the existing library, unless instructed otherwise.

> [!WARNING]
> **L66 (067) ID Assignment**: Item 067 `(으)로 하다` was not explicitly listed in the family mapping draft. I have assigned it to `kg.grammar.ending.choice_euro_hada`.

## Proposed Changes

### 1. Knowledge Item Ingestion (Core & i18n)

I will create 5 Knowledge Items (KIs) with their corresponding `zh_tw` localizations.

- **L66 (Item 067)**: `(으)로 하다` (Decision/Choice)
    - Core ID: `kg.grammar.ending.choice_euro_hada`
    - Title: `(으)로 하다 (決定/選擇)`
- **L67 (Item 068)**: `았/었/했으면 좋겠다` (Wish/Hope)
    - Core ID: `kg.grammar.ending.wish_ass_eumyeon_jokgetda`
    - Title: `았/었/했으면 좋겠다 (希望/願望)`
- **L68 (Item 069)**: `기로 하다` (Decision/Promise)
    - Core ID: `kg.grammar.ending.promise_gi_ro_hada`
    - Title: `기로 하다 (決定/約定)`
- **L69 (Item 070)**: `자` (Banmal Suggestion)
    - Core ID: `kg.grammar.ending.propose_banmal_ja`
    - Title: `자 (提議 - 非敬語)`
- **L70 (Item 071)**: `지 말자` (Banmal Negative Suggestion)
    - Core ID: `kg.grammar.ending.propose_prohibit_banmal_ji_malja`
    - Title: `지 말자 (否定提議 - 非敬語)`

### 2. Example Sentence Generation

I will generate 50 original, context-rich example sentences (10 per KI) starting from `ex.ko.s.000657` up to `ex.ko.s.000706`.

- **Originality**: All sentences will be rewritten from the source for better pedagogy and to avoid duplication.
- **Batchim Safety**: Strict review of conjugation rules (e.g., `으로` vs `로`, vowel harmony for `았으면`).
- **Pedagogy**: Focused on A1/A2 beginner level vocabulary and natural contexts (ordering at cafes, personal resolutions, friend suggestions).

### 3. Repository Integrity & Sync

#### [MODIFY] [BEGINNER_GRAMMAR_INGESTION_AUDIT.md](file:///e:/Githubs/lingo/content-ko/docs/reports/BEGINNER_GRAMMAR_INGESTION_AUDIT.md)
Update the audit report to reflect the completion of L66-L70.

#### [MODIFY] [STATE.md](file:///e:/Githubs/lingo/content-ko/STATE.md)
Mark L66-L70 as completed.

## Open Questions

- **Total Sentence Count**: Should I stick to exactly 10 sentences for the whole batch, or 10 sentences per lesson? I highly recommend 10 per lesson.
- **ID Names**: Are the proposed KI IDs acceptable?

## Verification Plan

### Automated Tests
- `python scripts/tools/generate_knowledge_sentence_index_v0.py`: Ensure `broken_refs=0`.
- `python scripts/tools/check_json_validity.py`: Validate syntax.
- `python scripts/tools/validate_learning_library_schema.py`: Ensure V5 schema compliance for all new files.
- `python scripts/ops/export_learning_library_runtime.py`: Sync to `release-aggregator`.

### Manual Verification
- Review the generated `zh_tw` explanations for naturalness and clarity.
- Verify the `explanation_md` skeleton complies with the `·` dot-point requirement and uses backticks for Korean fragments.
