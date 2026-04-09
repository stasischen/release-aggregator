# Example Sentence Bank Schema (V1)

## Status: Draft / Under Review (Pending freeze via kg-spec-011)

This document defines the V1 schema for `example_sentence` assets in `content-ko`. All extracted and manually authored example sentences must adhere to this contract to gate development of downstream features.

---

## 1. Core Structure (Core Repo)

Stored in: `content-ko/content/core/learning_library/example_sentence/`

### Required Fields

- `id` (string): Unique identifier. Pattern: `ex.[lang].[family].[desc].[version]`.
- `target_lang` (string): Usually `ko`.
- `surface_ko` (string): The literal Korean text. Must be clean (no markdown highlighting or mixed scripts).
- `level` (string): CEFR levels (`A1`, `A2`, `B1`, etc.).
- `source_type` (enum): 
  - `knowledge_item_extraction`: Extracted from structured example blocks in a Knowledge Item.
  - `youtube_reference`: Derived from a video transcript.
  - `dialogue_reference`: Derived from a course dialogue.
  - `article_reference`: Derived from a course article.
  - `legacy_bootstrap`: Imported from older content-ko datasets.
  - `curated`: Hand-written by content experts.

### Provenance & Quality (Conditional Requirements)

#### Required for all `source_type` != `curated`:
- `provenance` (object):
  - `original_ki_ref` (string): **Required** if `source_type` is `knowledge_item_extraction`. ID of the originating Knowledge Item.
  - `source_sentence_ref` (string): **Required** if `source_type` is `youtube_reference`, `dialogue_reference`, or `article_reference`. Optional otherwise.
  - `extraction_date` (string): **Required**. ISO timestamp of when this record was created/extracted.

#### Recommended:
- `register` (enum): `polite`, `formal`, `casual`.
- `quality_flags` (object):
  - `segmentation_ready` (boolean)
  - `reviewed_by_native` (boolean)
  - `audio_verified` (boolean)
- `knowledge_refs` (array of strings): IDs of grammar/pattern items this sentence exemplifies.
- `topic_refs` (array of strings): IDs of topics.

---

## 2. I18N Structure (I18N Repo)

Stored in: `content-ko/content/i18n/[locale]/learning_library/example_sentence/`

### Fields

- `id` (string): Must match the Core ID.
- `translation_[locale]` (string): e.g., `translation_zh_tw`.
- `explanation_[locale]` (string, optional): Contextual note on why this specific sentence was used.

---

## 3. Pattern Alignment (`frame_projection`)

Only used if the sentence is a valid instance of a `pattern_frame`.

```json
{
  "frame_projection": {
    "pattern_frame_ref": "kp.time.today_is_weekday",
    "slot_projection": [
      {
        "slot_id": "weekday",
        "slot_surface": "토요일",
        "slot_refs": ["kv.time.weekday.saturday"]
      }
    ]
  }
}
```

### Constraints:
1. `pattern_frame_ref` must point to a valid `pattern_frame` item.
2. `slot_id` must be declared in the target frame.
3. `slot_refs` (Optional) can link to a specific vocabulary atom or knowledge value.

---

## 4. Quality Gate Rules

1. **Bare String Rule**: `surface_ko` must NOT contain `<b>`, `*`, or `[ ]`. Highlight information belongs in UI-layer projection or metadata.
2. **Translation Rule**: Every production-grade example MUST have at least one valid translation in the preferred support language.
3. **No Invented Fields**: Do not add ad-hoc metadata fields (e.g., `difficulty_score: 5`) until they are formally added to the schema and accepted by the ingestor.
