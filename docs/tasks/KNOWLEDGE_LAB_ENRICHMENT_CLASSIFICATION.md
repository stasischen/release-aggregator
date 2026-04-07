# Knowledge Lab Enrichment: V1 Alignment & Classification Rules

## Goal

To safely prepare the existing `KNOWLEDGE_LAB_ENRICHMENT` v1 content for example sentence bank extraction, graph enrichment (e.g., `kg-mig-010`), and strict schema boundaries. 
This document defines how to classify current knowledge items and example blocks so we differentiate between global reusable examples and item-specific teaching content.

---

## Content Extradition Types

When inspecting an existing knowledge item's `i18n` examples or `core` sentences, the content MUST be classified into one of the following states:

### 1. Reusable Example Sentence (Extractable)
**Definition:** A complete, grammatically sound, context-independent sentence that demonstrates the target grammar/pattern.
**Criteria:**
- Standalone: Makes sense without the surrounding teaching explanation.
- Clean Segmentation: Does not mix instructional meta-text (e.g., brackets, highlighting notation `*`) directly into the bare Korean string `ko` if that string is meant to be a literal target sentence.
- Source Quality: Good quality human translation and correct target language usage.
**Alignment Action:** Mark as ready for `example_bank` extraction. Will be extracted globally.

### 2. Item-Local Teaching Commentary (Do Not Extract)
**Definition:** Examples or text fragments that only make sense within the context of learning this specific grammar/pattern.
**Criteria:**
- Highly Contextual: Often contrastive (e.g., "See how this is different from X...").
- Fragmented: Phrase snippets or incomplete sentences used for structural breakdown (e.g., "학교 + 에서").
- Mixed Notation: Uses intentional invalid syntax with strikethroughs to show common mistakes.
**Alignment Action:** Do not extract. Keep these trapped entirely within the `explanation_md_i18n` or existing teaching metadata fields. Any future dedicated block for local commentary must be defined in a separate schema review.

### 3. Ambiguous / Needs Review
**Definition:** Sentences that look like reusable examples but suffer from formatting issues, unclear canonical meaning, or mixed constraints.
**Criteria:**
- Contains conversational fragments (like "A: Hello, B: Hello") stuffed into a single string.
- Has complex morphological changes that might trip up a clean extraction script without manual review.
**Alignment Action:** Flag for PM/Author review. Do not extract to the global bank until clarified.

### 4. Candidate Only / Not Ready
**Definition:** Placeholder content, highly experimental drafts, or low-quality AI-generated snippets that haven't passed human QA.
**Criteria:**
- Found in items still explicitly marked with `candidate` or `staging_only`.
- Examples that don't match the required `A1/A2` competency level of the current module.
**Alignment Action:** Exclude from `kg-mig-010`. Retain only as `staging` for internal review.

---

## Alignment Check Rules

When aligning an existing item to these classifications:

1. **Separate Commentary from Examples:**
   Ensure that the arrays holding example sentences do not contain "teaching notes". Move teaching notes into the Markdown explanation block.
2. **Stable References:**
   Verify `source_ref` or links point to actual existing items, otherwise mark as `Ambiguous`.
3. **No Mixed Scripts:**
   The `ko` target string should be 100% Korean (plus standard punctuation). Any English/Chinese metadata must be moved to the `zh_tw` or `en` translations, or `annotation` fields, not inside the core string.

