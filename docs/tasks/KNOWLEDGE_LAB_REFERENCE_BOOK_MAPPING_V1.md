# Knowledge Lab Reference Book Mapping V1

## 1. Mapping Grammar Items (Beginner / Endings)

Source: `reports/youtube_beginner_grammar/clean_md/*.md`
Source: `reports/youtube_connective_endings/clean_md/*.md`

| Source Field | Learning Lab `core.json` Field | Learning Lab `i18n/{support}/knowledge.json` Field |
| :--- | :--- | :--- |
| **# Title** | `id` (Semantic Slug) | `title_zh_tw` |
| **Description** | N/A | `summary_zh_tw` |
| **Usage Rules** | N/A | `explanation_md_zh_tw` (Markdown formatted) |
| **Examples (KO)** | N/A | `example_bank.ko` |
| **Examples (ZH)** | N/A | `example_bank.zh_tw` |
| **Other Tags** | `tags` | N/A |

## 2. Mapping Connector Items

Source: `reports/youtube_connectors/clean_md/*.md`

- **Knowledge Kind**: `connector`.
- **Mapping**: Same as Grammar items.
- **Fields**: Use `title_zh_tw`, `summary_zh_tw`, `explanation_md_zh_tw`.

## 3. Mapping Survival Patterns

Source: `ko_survival_pattern_library_v1.json`

| Source Field | Learning Lab `core.json` Field | Learning Lab `i18n/{support}/pattern.json` Field |
| :--- | :--- | :--- |
| **`pattern_id`** | `id` (Normalized) | N/A |
| **`frame`** | `frame` | N/A |
| **`slots`** | `slots` | N/A |
| **`can_do`** | N/A | `summary_zh_tw` |
| **`acceptable_variants`** | `tags` (as alt_info) | N/A |
| **`teaching_notes`** | N/A | `explanation_md_zh_tw` |

## 4. Reference Metadata (Provenance Layer)

The following fields from the source are NOT added to the JSON artifacts but are kept in the mapping notes for ingestion scripts:

- **`media_id`**: Relegated to `source_ref` in `example_bank` or mapping database.
- **`playlist_index`**: Internal sorting hint only.

## 5. Normalization Rules

1. **Strict Contract**: No nested objects like `metadata` or `explanation.summary`.
2. **Semantic Slugs**: Names like `sumndia_formal_ending` instead of `001_...`.
3. **Markdown Ingestion**: Ensure usage rules from source MD are properly escaped and formatted for `explanation_md_zh_tw`.
