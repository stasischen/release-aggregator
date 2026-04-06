# Knowledge Lab Reference Book Mapping V1

## 1. Mapping Grammar Items (Beginner / Endings)

Source: `reports/youtube_beginner_grammar/clean_md/*.md`
Source: `reports/youtube_connective_endings/clean_md/*.md`

| Reference Book Field | Learning Lab `core.json` Field | Learning Lab `i18n/{support}/knowledge.json` Field |
| :--- | :--- | :--- |
| **# Title** | `knowledge_id` (Slugified) | `title` |
| **Description** | N/A | `explanation.summary` |
| **Usage Rules** | N/A | `explanation.details` (Normalized from prose) |
| **母音/子音 Rules** | `attributes.ending_type` (Ref) | N/A (Keep as notes) |
| **Examples (KO)** | N/A | `example_bank.target_text` |
| **Examples (ZH)** | N/A | `example_bank.translation` |
| **Video ID** | `metadata.media_id` | N/A |
| **Playlist Index** | `metadata.source_order` | N/A |

## 2. Mapping Connector Items

Source: `reports/youtube_connectors/clean_md/*.md`

- **Knowledge Kind**: `connector`.
- **Mapping**: Same as Grammar items, but emphasis on `contrastive_notes` in `i18n` if present.

## 3. Mapping Survival Patterns

Source: `ko_survival_pattern_library_v1.json`

| Reference Book Field | Learning Lab `core.json` Field | Learning Lab `i18n/{support}/pattern.json` Field |
| :--- | :--- | :--- |
| **`pattern_id`** | `pattern_id` (Normalized) | N/A |
| **`frame`** | `frame` | N/A |
| **`slots`** | `slots` | N/A |
| **`can_do`** | N/A | `summary` |
| **`acceptable_variants`** | `acceptable_alt_frames` | N/A |
| **`teaching_notes`** | N/A | `explanation.learner_tips` |

## 4. Reference Book Browse Hierarchy (Topics)

Topics are NOT canonical; they are the browsing layer.

- **`topic.grammar.particle`**: Grouping for all particles.
- **`topic.grammar.ending`**: Grouping for all connective endings.
- **`topic.connector.causal`**: Grouping for `그래서`, `따라서`.
- **`topic.pattern.survival.greeting`**: Grouping for "Survival: Greetings".

## 5. Normalization Rules

1. **Slugification**: Titles like `敬語結尾正式敘述 -습니다/ㅂ니다` should be mapped to `sumndia_formal_ending`.
2. **Example Cleanup**: Metadata emojis (🗣, 📘) should be removed from pure text fields but can be kept in `summary` if desired.
3. **Media Link**: Ensure `media_id` is stored so the frontend can retrieve the specific YouTube segment.
