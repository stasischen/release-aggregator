# Task: Legacy Content V5 Standardization (L0)

## Overview
- **Status**: PLANNED
- **Priority**: HIGH
- **Assignee**: AI Agent / Content Team
- **Description**: Migrate legacy Korean content (Level 0) to the V5 standardized format, including atomic dictionary decomposition and Yarn-format dialogues.

## Background
V5 standardization for A1 (Level 1) is complete and deployed. However, legacy content (L0 Travel/Social/etc.) still uses the V4 ID format (`ko_POS_lemma`), which causes dictionary lookup failures in the new V5-compatible frontend. To maintain app integrity, these have been temporarily un-shipped from the 9_production build.

## Objectives
1. [ ] **Content Restructuring**: Split legacy L0 dialogues into `core` and `i18n` (zh_tw) components.
2. [ ] **Atomic Decomposition**: Perform POS tagging and atom segmentation for all L0 sentences.
3. [ ] **Dictionary Mapping**: Map all L0 tokens to V5 dictionary atoms.
4. [ ] **Gold Standard Generation**: Produce `gold_standards/dialogue/A0/*.jsonl` for regression testing.
5. [ ] **Automated Build Integration**: Ensure L0 content successfully passes through the `content-pipeline` V5 build.

## Target Lessons
- ko_l0_social_001_intro
- ko_l0_travel_001_airport
- ko_l0_travel_008_shopping
- (Other L0 modules)

## Next Steps
1. Run `content-ko/scripts/ops/restructure_content.py` adapted for L0.
2. Trigger Stage-02 (Tokenization) and Stage-03 (Atom Mapping) for L0 lessons.
3. Verify via `lllo` viewer before promoting to `9_production`.
