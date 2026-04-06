# Knowledge Lab Reference Book Inventory

## 1. Source Families

### A. `youtube_beginner_grammar` (141 items)

- **Format**: Markdown / YouTube Metadata.
- **Content**: 141 core items from "Teacher Kim's Korean" (金老師的韓國語).
- **Structure**: Title, description, usage rules (e.g., vowel vs consonant endings), example sentences with translations.
- **Suitability**: **High**. Primary source for core grammar reference book.

1. **Slugification**: Titles like `敬語結尾正式敘述 -습니다/ㅂ니다` should be mapped to `sumndia_formal_ending`.
2. **Example Cleanup**: Metadata emojis (🗣, 📘) should be removed from pure text fields but can be kept in `summary` if desired.
3. **Media Link**: Ensure `media_id` is stored so the frontend can retrieve the specific YouTube segment.

### B. `youtube_connectors` (113 items)

- **Format**: Markdown / YouTube Metadata.
- **Content**: 113 high-frequency connectors (e.g., `그리고`, `그래서`).
- **Structure**: Semantic meaning, sample uses, contrastive notes.
- **Suitability**: **High**. Transitions naturally to `connector` kind in Learning Lab.

### C. `youtube_connective_endings` (112 items)

- **Format**: Markdown / YouTube Metadata.
- **Content**: 112 intermediate/advanced endings (e.g., `~기에`, `~느라고`).
- **Structure**: Grammatical context, reasoning, sample dialogues.
- **Suitability**: **Med/High**. Better suited for Wave 5 due to semantic complexity.

### D. `ko_survival_pattern_library_v1.json` (180+ entries)

- **Format**: Structured JSON.
- **Content**: 188 functional patterns tagged by `level` (A1, A2).
- **Structure**: `frame`, `slots`, `can_do`, `acceptable_variants`, `teaching_notes`.
- **Suitability**: **High**. Perfect for `kp.pattern` items.

### E. `language/ko` (Reference Tables)

- **Format**: JSON (`can_do_catalog_v1.json`, `topic_taxonomy_v1.json`).
- **Content**: Domain-level tagging (e.g., `Self-Intro`, `Shopping`).
- **Suitability**: **Low (as content)** / **High (as metadata)**. Use these to tag and group the above sources.

## 2. Ineligible Sources (Discarded for Lab)

- **`raw` directories**: Unstructured data requiring heavy pre-processing.
- **`youtube_idioms` (Initial scan)**: Idioms require a different `idiom` schema or `expression` mapping that is currently not the focus of the "Reference Book" structure.
- **YouTube Playlists (as items)**: Playlists are not knowledge items; their constituents are.

## 3. Data Integrity & Mapping Considerations

- **OCR/Translation Flaws**: Early clean MDs might have mixed-script or minor OCR errors from video transcriptions.
- **Mapping Gaps**: Usage rules in MD are prose; mapping them to a structured `explanation_md_zh_tw` in the Lab requires careful formatting but stays within the current i18n contract.
- **Provenance Layer**: Metadata like `media_id` and `source_order` are valuable for debugging but will not be added to the knowledge JSON core at this stage. They remain as internal mapping notes.
