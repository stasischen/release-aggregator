# KNOWLEDGE_SCHEMA_EXTENSION_PROPOSAL_V1

## Goal
To improve the traceability, pedagogical flexibility, and searchability of Knowledge Items by extending the V5 schema with `aliases`, `source_refs`, and `teaching_blocks`.

## Proposed Schema Extensions

### 1. Aliases and Variants
We distinguish between morphological variants (Core) and localized mapping/search aliases (I18n).

#### [CORE] `surface_variants`: `Array<string>`
- **Purpose**: Store exact Korean text variants that refer to the same concept (e.g., `-아서`, `-어서`, `-해서` are variants of the same cause-and-effect grammar item).
- **Validation**: Must be a non-empty array of non-empty strings.

#### [I18n] `aliases`: `Array<string>`
- **Purpose**: Store localized names, common Chinese translated titles, or keywords used by learners to find this item (e.g., "原因", "因為", "A/V-아서").
- **Validation**: Unique items within the array. Locality is determined by the `locale` field.

### 2. Source Traceability

#### [CORE] `source_refs`: `Array<SourceRef>`
- **Purpose**: Establish a link back to the curriculum source or historical evidence. 
- **Migration Note**: This proposal introduces a richer `SourceRef` object for knowledge-item schema extension. It does **not** change existing manifest-level `source_refs: string[]` conventions in other contracts.
- **Structure**:
  ```json
  {
    "source_id": "string",
    "role": "primary | mention | historical",
    "fragment": "string (optional, e.g., 'v_001', 'p.123')"
  }
  ```
- **Rationale**: Unlike `example_bank` which links to specific sentences, `source_refs` links the *concept* to the lesson or video where it was taught.

### 3. Pedagogical Structure

#### [I18n] `teaching_blocks`: `Array<TeachingBlock>`
- **Purpose**: Allow explanations to be broken down into structured "cards" or "sections" rather than one giant `explanation_md`. This supports interactive "drawer" UIs.
- **Structure**:
  ```json
  {
    "title": "string",
    "content_md": "string (markdown allowed)",
    "usage_tag": "string (optional, e.g., 'form_rule', 'register_note')"
  }
  ```

---

## Sample Implementation

### Core Item Asset
`content-ko/content/core/learning_library/knowledge/grammar/ending/kg.grammar.ending.reason_aseo.json`

```json
{
  "id": "kg.grammar.ending.reason_aseo",
  "kind": "grammar",
  "subcategory": "ending",
  "surface": "아서/어서/해서",
  "surface_variants": ["아서", "어서", "해서"],
  "source_refs": [
    {
      "source_id": "video:79Pwq7MTUPE",
      "role": "primary",
      "fragment": "v_015"
    },
    {
      "source_id": "lesson:KO-A1-L05",
      "role": "historical"
    }
  ],
  "level": "A1"
}
```

### I18n Item Overlay
`content-ko/content/i18n/zh_tw/learning_library/knowledge/grammar/ending/kg.grammar.ending.reason_aseo.json`

```json
{
  "id": "kg.grammar.ending.reason_aseo",
  "locale": "zh_tw",
  "title": "아서/어서/해서 (原因/原因語尾)",
  "aliases": ["原因", "因為", "連結子"],
  "summary": "用於表示前後內容的因果關係。",
  "explanation_md": "...",
  "teaching_blocks": [
    {
      "title": "變化規則 (Form Rules)",
      "content_md": "- 陽性母音 (ㅏ, ㅗ) -> `-아서` \n- 陰性母音 (其他) -> `-어서` \n- `하다` -> `-해서`",
      "usage_tag": "form_rule"
    },
    {
      "title": "語用限制 (Constraints)",
      "content_md": "後句不能使用命令式或建議式語尾（如 -세요, -읍시다）。",
      "usage_tag": "pragmatic_note"
    }
  ]
}
```

---

## Impact and Migration Path

1. **Pipeline Support**: The artifact generator must be updated to concatenate `teaching_blocks` or preserve them as a structured field for the frontend.
2. **Modular Viewer**: Update the renderer to support a "Expandable Blocks" view for `teaching_blocks`.
3. **Migration Pack 003**: The next batch of 10-20 items should be used to field-test these new schema fields before full curriculum ingestion.
