# Example Extraction Policy (V1)

## Status: Frozen

## Goal
To prevent "pollution" of the global `example_sentence` bank with instructional fragments, contrastive snippets, or invalid syntax. This policy governs the behavior of `kg-mig-010`.

---

## 1. Scope of Extraction

### Allowed Targets (Extractable)
- **Standalone Sentences**: Must be grammatically complete and interpretable without the sibling explanation.
- **Structured JSON Arrays**: Content already contained in `example_bank` or `sentences` arrays in V5 knowledge items.
- **Audio-Synced Blocks**: Any block that already has an assigned `source_ref` pointing to a video or dialogue.

### Disallowed Targets (Stay in Item-Local)
- **Contrastive Fragments**: e.g., "은/는 (X) vs 이/가 (O)".
- **Phrase Snippets**: "학교 + 에서" (used for morphological breakdown).
- **Explanation Markdown**: Freeform text inside `explanation_md_i18n` or `summary_zh_tw` must NEVER be parsed for sentences unless flagged for manual review.
- **Mistake Patterns**: Sentences used to show "what not to do".

---

## 2. Hard Constraints

1. **No Invented Fields**: The extraction script must not generate "synthetic" metadata (e.g., guessing the level or register) unless it can be derived from the source knowledge item's metadata.
2. **Provenance Preservation**: Every extracted sentence MUST carry the ID of its source Knowledge Item in `provenance.original_ki_ref` (as required by the V1 Schema for `knowledge_item_extraction`).
3. **Clean String Guarantee**: Any highlighting notation (e.g., brackets `[]`, asterisks `*`) must be stripped during extraction to ensure the `surface_ko` is a pure target-language string.

---

## 3. Extraction Alignment Pass Outputs

The result of the alignment pass (before actual file modification) should be:

1. **Classification Report**:
   - `Ready`: Clean items for auto-extraction.
   - `Context-Bound`: Items to be left in-situ as commentary.
   - `Ambiguous`: Items requiring human review.
2. **Extraction Manifest**: A mapping of `Original_KI_ID -> Proposed_Sentence_ID`.
3. **Reviewed Inventory**: A list of sentences successfully staged for the bank.

---

## 4. Execution Guardrails

- **Dry-Run Mandatory**: No write operations without a classification summary.
- **ID Stability**: Once a sentence is extracted from a KI, its ID must remain stable even if the KI changes.
- **Link Replacement**: When a sentence is extracted, the KI's internal example block must be replaced with an `example_sentence_refs` entry to maintain the link.
