# Knowledge Lab Enrichment Plan V0

## Goal

In response to the gaps identified in `A1-01` (A1-1 level), this plan outlines the systematic enrichment of topics, knowledge items, and internal links without modifying the underlying artifact schema or blocking the content migration mainline.

## Proposed Changes

### 1. Topic Taxonomy (New Families)

Establish missing topic families to group related vocabulary and grammar from early dialogues.
- **`topic.identity.occupation`**: `선생님` (Teacher), `의사` (Doctor), `학생` (Student).
- **`topic.place.institutional`**: `학교` (School), `컴퓨터실` (Computer Lab).
- **`topic.family.relation`**: `아버지` (Father), `어머니` (Mother).

### 2. Knowledge Item Backfill

Address high-frequency items used in Dialogue A1-01.
- **Honorific Grammar**: Add `~으시` suffix and honorific copula form `~이사/가`.
- **Essential Expressions**: Add `안녕하세요` (Hello) and `감사합니다` (Thank you) with dedicated teaching notes.
- **Echo Questions**: Add `~요?` conversational pattern (e.g., `부산요?`).

### 3. Source Enrichment (A1-01)

Increase the information density of the primary A1-1 dialogue.
- **Vocab Set Expansion**: Increase from 4 to ~12 items (verbs like `오다`, `살다`, `이다`, and high-frequency nouns).
- **Link Completion**: Add missing links for `~에` (at), `~에서` (from/at), and Object Particle `~을/를`.

### 4. Teaching Depth (i18n)

Enhance the educational value of existing items.
- **Learner Tips**: Add a `usage_notes` or `summary` layer in `zh_tw` to explain the social context of honorifics vs. polite informal forms used in the dialogue.

## Verification Plan

### Automated

- `npm run validate:learning-library`: Verify JSON schema compliance.
- `python scripts/check_links.py`: Ensure all new `origin_id` and `target_id` pairs are resolvable.

### Manual

- **Modular Viewer**: Verify that new knowledge items and links are correctly surfaced in the UI for Lesson A1-01.
- **Pack Emission**: Verify that `core` and `i18n` packs are emitted separately as per the current contract.
