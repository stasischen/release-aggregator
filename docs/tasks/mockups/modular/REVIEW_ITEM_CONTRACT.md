# Review Item Contract v1

This document defines a reusable review-item shape for beginner grammar mockups so that the same source sentence can drive multiple review modes.

## Goal

One canonical sentence item should be reusable across:

- `chunk_assembly`: see the translation, build the Korean sentence from chunks
- `flashcard_review`: hear/see the Korean sentence, flip for the answer, then rate recall

The review system should not require each lesson author to manually duplicate the same sentence into multiple unrelated payload shapes.

## Delivery Boundary

For the current mockup stage:

- `P1` in the modular mockup viewer should support **chunk assembly only**
- sentence-reading practice and typed sentence input are intentionally deferred to the frontend runtime

For the later frontend stage, the same canonical review item may also project into:

- `shadowing` / repeat-after-audio style speaking practice
- `typed_input` sentence production

This keeps the mockup focused on validating sentence contract quality first, without prematurely expanding interaction complexity.

## Canonical Review Item

```json
{
  "item_id": "bg_l01_identity_polite_yuna",
  "source_node_id": "A1-BG-L01-L1",
  "source_builder_id": "identity-register-switch",
  "pattern_family": "identity_switch",
  "register": "polite",
  "ko_surface": "저는 유나예요.",
  "tts_text": "저는 유나예요.",
  "meaning_i18n": {
    "zh_tw": "我是 Yuna。",
    "en": "I am Yuna."
  },
  "note_i18n": {
    "zh_tw": "第一次見面先用 해요체 最安全。",
    "en": "In a first meeting, 해요체 is the safest starting point."
  },
  "chunks": ["저는", "유나예요."],
  "distractors": ["안녕하세요.", "민수예요."],
  "review_modes": ["chunk_assembly", "flashcard_review"],
  "tags": ["a1", "identity", "polite", "first_meeting"]
}
```

## Required Fields

- `item_id`: stable unique id
- `ko_surface`: canonical Korean sentence shown in review
- `meaning_i18n`: learner-facing translation
- `review_modes`: supported review projections

## Strongly Recommended Fields

- `source_node_id`: trace back to lesson node
- `source_builder_id`: trace back to sentence family / builder
- `pattern_family`: normalized family name for grouping
- `register`: `formal | polite | casual`
- `tts_text`: explicit speech text if different from `ko_surface`
- `note_i18n`: short teaching note shown on answer side
- `tags`: filter/search/recommendation support

## Mode-Specific Projection Rules

### 1. `chunk_assembly`

Required extra fields:

- `chunks`: the correct chunks in target order
- `distractors`: optional distractor chunks

Projection shape:

```json
{
  "prompt_zh_tw": "請組出：我是 Yuna。",
  "chunks": ["저는", "유나예요.", "안녕하세요.", "민수예요."],
  "target_examples": ["저는 유나예요."],
  "target_examples_zh_tw": ["我是 Yuna。"]
}
```

Rules:

- `chunks` in the projected task can be `correct chunks + distractors`
- chunk gloss should be omitted in the learner UI by default
- task order may be randomized at runtime
- use only one canonical answer in v1 unless the author explicitly provides alternates

### 2. `flashcard_review`

Required extra fields:

- none beyond canonical fields

Projection shape:

```json
{
  "front_ko": "저는 유나예요.",
  "prompt_i18n": {
    "zh_tw": "先聽這句，想想它是什麼意思。",
    "en": "Listen to this sentence first and think about what it means."
  },
  "answer_i18n": {
    "zh_tw": "我是 Yuna。",
    "en": "I am Yuna."
  },
  "back_ko": "저는 유나예요.",
  "note_i18n": {
    "zh_tw": "第一次見面先用 해요체 最安全。",
    "en": "In a first meeting, 해요체 is the safest starting point."
  }
}
```

Rules:

- front side should prioritize `ko_surface`
- answer side should show `meaning_i18n`
- rating buttons (`Again/Hard/Good/Easy`) are interaction metadata, not item data

## Derivation Rules from Existing Mockup Content

### Can be derived automatically

From `pattern_builder_demos` or fixed dialogue turns:

- `source_node_id`
- `source_builder_id`
- `pattern_family`
- `register`
- `ko_surface`
- `tts_text`
- part of `meaning_i18n` if the builder already has clean `translation_templates`

### Usually needs author input

- `note_i18n`
- `chunks`
- `distractors`
- explicit alternate correct answers
- review prioritization / tags

## Authoring Constraints

- `ko_surface` must be a complete sentence, not a fragment
- `meaning_i18n` must be natural learner-facing copy, not schema fragments
- no unresolved template tokens are allowed in projected items
- `chunk_assembly` should avoid ambiguous chunking for v1
- if a sentence has more than one acceptable beginner answer, either:
  - provide one canonical answer only, or
  - explicitly declare alternates in a future v2 shape

## A1-BG-L01 Mapping Table

### Directly reusable now

| Source | Example surface | `chunk_assembly` | `flashcard_review` |
|---|---|---:|---:|
| `A1-BG-L01-L1` formal intro | `저는 유나입니다.` | yes | yes |
| `A1-BG-L01-L1` polite intro | `저는 유나예요.` | yes | yes |
| `A1-BG-L01-L1` casual intro | `나는 유나야.` | yes | yes |
| `A1-BG-L01-L2` thing demonstrative | `이건 사과예요.` | yes | yes |
| `A1-BG-L01-L2` time question | `지금 몇 시예요?` | yes | yes |
| `A1-BG-L01-L3` verb slot | `카페에 가요.` | yes | yes |
| `A1-BG-L01-L3` verb slot | `커피를 마셔요.` | yes | yes |
| `A1-BG-L01-G1` identity register | `저는 학생입니다.` | yes | yes |
| `A1-BG-L01-G1` place topic | `여기는 카페예요.` | yes | yes |
| `A1-BG-L01-G1` core verb ending | `책을 읽어요.` | yes | yes |

### Better as flashcard-only for now

| Source | Reason |
|---|---|
| long explanatory contrasts in `G2` | better as review notes than assembly tasks |
| open roleplay prompts in `P5` | not a single canonical sentence |

## Recommended Next Step

For each lesson node that contains sentence-bearing content, add a lightweight export layer:

```json
{
  "review_items": [
    {
      "item_id": "...",
      "ko_surface": "...",
      "meaning_i18n": { "zh_tw": "...", "en": "..." },
      "review_modes": ["chunk_assembly", "flashcard_review"]
    }
  ]
}
```

This keeps sentence authoring close to the source node while allowing multiple review projections to be generated downstream.

## P1 Scope Decision

For `A1-BG-L01` and the next beginner grammar mockups:

- `P1` = `chunk_assembly`
- do not add speaking-repeat or typed-input logic to the mockup viewer yet
- keep `ko_surface`, `tts_text`, and `meaning_i18n` in the source item so frontend can add those modes later without changing sentence source data

## Auto-Derivation Strategy v2

The long-term target is that every lesson can auto-derive review items from sentence-bearing source content.

### Principle

Do not author `P1` and `R2` as primary content.

Instead:

- lesson nodes remain the primary sentence source
- `review_items` are derived from lesson nodes
- `P1` (`chunk_assembly`) and `R2` (`flashcard_review`) are generated from `review_items`

### Eligible Source Nodes

Sentence-bearing nodes that should be able to auto-derive review items:

- `dialogue` turns in `L1`
- fixed output examples from `pattern_lab` builders in `L2 / L3 / G1`
- canonical contrast sentences in `grammar_note` only if explicitly tagged for review export

### Required Export Layer per Lesson

Each lesson should expose a lightweight sentence export bundle:

```json
{
  "review_items": [
    {
      "item_id": "...",
      "ko_surface": "...",
      "meaning_i18n": { "zh_tw": "...", "en": "..." },
      "review_modes": ["chunk_assembly", "flashcard_review"]
    }
  ]
}
```

### Derivation Sources by Content Type

#### 1. Dialogue

From each fixed dialogue turn:

- `ko_surface` = turn text
- `meaning_i18n` = turn translation
- `tts_text` = turn text
- `register` = turn register if present
- `pattern_family` = normalized from `pattern_ref`

Author must still decide:

- export priority
- whether the sentence is suitable for chunk assembly
- distractor policy

#### 2. Pattern Lab

From each builder, derive one or more canonical surfaces from predefined presets.

A builder must declare export presets if it wants auto-derived review items.

Example:

```json
{
  "builder_id": "basic-verb-slot-switch",
  "review_export_presets": [
    {
      "preset_id": "go_cafe_polite",
      "control_values": {
        "verb_pack": "go",
        "slot_phrase": "카페",
        "register": "polite"
      },
      "meaning_i18n": {
        "zh_tw": "去咖啡廳。",
        "en": "Go to a cafe."
      },
      "chunks": ["카페에", "가요."],
      "distractors": ["학교에", "마셔요."]
    }
  ]
}
```

This avoids trying to brute-force every possible builder combination.

### Variation Policy

Variation should come from controlled generation, not random nonsense.

Allowed variation sources:

- random task order
- random chunk order
- random subset selection from the lesson's eligible review items
- multiple export presets per builder
- level-appropriate distractor pools from the same lesson

Not allowed in v1/v2:

- unconstrained combinatorial generation across all builder controls
- runtime dictionary-based sentence guessing
- generating sentences with no author-approved `meaning_i18n`

### Recommended Generation Pipeline

For each lesson:

1. collect sentence-bearing sources
2. derive or read explicit `review_items`
3. filter to the requested review mode
4. sample a subset for the current session
5. shuffle task order and interaction order

### Minimal Session Generation Config

```json
{
  "review_generation": {
    "chunk_assembly": {
      "sample_size": 8,
      "shuffle_task_order": true,
      "shuffle_chunk_order": true
    },
    "flashcard_review": {
      "sample_size": 8,
      "shuffle_card_order": true
    }
  }
}
```

### Why This Scales Better

With this model:

- every lesson can expose a common sentence source
- variation increases without hand-authoring every review node from scratch
- frontend can consume the same `review_items` contract across units
- mockup viewer remains simple while still validating the data model needed for scale

## First Implementation Target

For the next implementation step, use `A1-BG-L01` as the pilot lesson.

### Pilot Rule

- keep the current hand-authored `P1` as a temporary fallback
- start adding `review_export_presets` to `L2 / L3 / G1` builders
- derive a parallel `review_items` list from those presets
- once stable, replace the hand-authored `P1` task list with generated output

### Why Start with Builder Presets

This is the smallest credible path to auto-derivation because:

- `L2 / L3 / G1` already contain structured control data
- preset-based export keeps content authoring deterministic
- we avoid trying to derive infinite combinations from free-form builders

### Suggested Engineering Sequence

1. add `review_export_presets` to eligible builders
2. write a local generator that turns presets into `review_items`
3. write a projector from `review_items -> chunk_assembly tasks`
4. write a projector from `review_items -> flashcard cards`
5. swap `P1` and `R2` from hand-authored payloads to generated payloads
