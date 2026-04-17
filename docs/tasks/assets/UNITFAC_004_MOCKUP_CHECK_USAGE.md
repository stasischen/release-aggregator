# UNITFAC-004: Mockup Check Usage Guide

This document describes how to use the `mockup_check.py` script to validate unit fixtures for schema compliance, data hygiene, and educational structure rules.

## Overview

The `mockup_check.py` tool is a unified validator designed to catch errors before PM reviews. it distinguishes between **Blocker Errors** (must fix to be Production-Ready) and **Warnings** (non-critical hygiene or TODO items).

## Prerequisites

- Python 3.x

## Command Usage

### 1. Validate Single or Multiple Files
```bash
python scripts/mockup_check.py docs/tasks/mockups/a1_u04_unit_blueprint_v0.json
```

### 2. Validate All Fixtures in Index (Recommended)
This command automatically finds all fixtures listed in the modular viewer index.
```bash
python scripts/mockup_check.py --index docs/tasks/mockups/modular/data/fixtures.json
```

### 3. Validate with Schema
```bash
python scripts/mockup_check.py --index docs/tasks/mockups/modular/data/fixtures.json --schema docs/tasks/mockups/unit_blueprint_v0.schema.json
```

### 4. Legacy v0.1 Regression Fixture
Use this file to confirm that older `unit_blueprint_v0.1` assets without modular metadata still pass validation:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/legacy_v0_1_compat_unit_blueprint.json
```

### 5. TTS-Only Sentence Contract Regression Fixture
Use this file to confirm that `interaction_contract` can rely on `tts_text` without `audio_ref`:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/tts_only_sentence_contract_unit_blueprint.json
```

### 6. Article Carrier Regression Fixture
Use this file to confirm that article-style sentence carriers are scanned for nested `interaction_contract` entries:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/article_sentence_contract_missing_target_surface.json
```

### 7. Missing output_mode Regression Fixture
Use this file to confirm that a missing `output_mode` stays visible as an error and does not collapse into `none` during dispatch checks:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/missing_output_mode_dispatch_unit_blueprint.json
```

### 8. Anchor Multi-Level Overlap Regression Fixture
Use this file to confirm that identical spans can be shared across `token` / `chunk` / `sentence` anchors without triggering duplicate rejection:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/anchor_multilevel_overlap_allowed.json
```

### 9. Anchor Duplicate Same-Level Rejection Regression Fixture
Use this file to confirm that identical spans with the **same level** (e.g., two `token` anchors for the same word) trigger `CMOD_DUPLICATE_ANCHOR`:
```bash
python scripts/mockup_check.py docs/tasks/assets/mockups/regression/anchor_duplicate_same_level_rejected.json
```

## Validation Rules

### Blocker Errors (Exit Code 1)
- **ERR_MIN_NODE_COUNT**: Unit has fewer than 10 nodes (PR standard is 12-18).
- **ERR_ORDER_VIOLATION**: Output nodes appear before input or structure nodes.
- **ERR_MISSING_COMPREHENSION**: No `comprehension_check` node found after the initial input.
- **PED_FOLLOWUP_INCONSISTENT**: `followup_type: transfer` but `transfer_pattern_refs` is empty.
- **CMOD_DUPLICATE_ANCHOR**: Detects identical spans (offset/length) at the same anchor level.
- **Unsupported Values**: Use of unknown `learning_role`, `content_form`, or `output_mode`.
- **Mixed-Script**: Detects Chinese characters accidentally mixed into Korean strings (e.g., `7時` instead of `7시`).

### Warnings
- **PED_MISSING_TYPE**: `comprehension_check` or `pattern_transform` missing type label (e.g. `question_type`).
- **PED_MISSING_RETRIEVAL_FOCUS**: `review_card` nodes missing `retrieval_focus` description.
- **PED_LISTENING_NO_RATIONALE**: `listening_discrimination` missing `distractor_rationale` or `feedback_zh_tw`.
- **PED_LOW_CC_DIVERSITY**: All CC nodes in a unit have the same `question_type`.
- **Missing zh-TW**: Detects empty or `TODO` markers in Chinese translation fields.
- **Legacy Aliases**: Detects use of `answers_ko` (deprecated) instead of `reference_answers_ko`.
- **Bilingual Mismatch**: Detects cases where the number of Korean items doesn't match the number of Chinese translations.

## Allowlisted Values (Upgraded)

The checker intentionally supports the following new values introduced in the UNITFAC cycle:
- **Content Forms**: `comprehension_check`, `notice`, `message_thread`, `comparison_card`, `pattern_card`, `grammar_note`, `functional_phrase_pack`, `practice_card`, `roleplay_prompt`, `message_prompt`, `review_card`, `article`, `video_transcript`.
- **Output Modes**: `pattern_transform`, `chunk_assembly`, `frame_fill`, `response_builder`, `guided`, `review_retrieval`.
- **Learning Roles**: `cross_unit_transfer`.

## Exit Codes
- `0`: Success (All blockers passed, warnings may exist).
- `1`: Blocker failure (One or more files failed validation).
- `2`: System/Parse error (JSON failure or missing files).
