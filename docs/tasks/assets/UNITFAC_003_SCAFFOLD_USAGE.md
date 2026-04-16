# UNITFAC-003: Unit Blueprint Scaffold Usage Guide

This document describes how to use the `scaffold_unit_blueprint.py` script to generate a production-ready unit skeleton for the Lingourmet platform.

## Overview

The scaffold generator creates a full unit skeleton (12–15 nodes) aligned with the **UNITFAC-002** specification. It includes all necessary learning roles, structured sequencing, and placeholder payloads with clear `TODO` markers for authors.

## Prerequisites

- Python 3.x

## Command Usage

Run the script from the root of the `release-aggregator` repository:

```bash
python scripts/scaffold_unit_blueprint.py \
    --unit_id <UNIT_ID> \
    --title_zh_tw <TITLE> \
    --level <A1|A2> \
    --theme_zh_tw <THEME> \
    --output <OUTPUT_PATH>
```

### Arguments

| Argument | Description | Example |
| :--- | :--- | :--- |
| `--unit_id` | Unique identifier for the unit. | `A1-U06` |
| `--title_zh_tw` | Unit title in Traditional Chinese. | `旅館入住` |
| `--level` | CEFR level. | `A1` |
| `--theme_zh_tw` | Brief theme description. | `預約確認與入住手續` |
| `--output` | Target file path for the JSON output. | `docs/tasks/mockups/a1_u06_unit_blueprint_v0.json` |
| `--target_language` | (Optional) Target language code. | `ko` (default) |
| `--learner_locale_source` | (Optional) Learner's native locale. | `zh-TW` (default) |

## Example

Generating a new unit for "Hotel Check-in":

```bash
python scripts/scaffold_unit_blueprint.py \
    --unit_id A1-U06 \
    --title_zh_tw "旅館入住" \
    --level A1 \
    --theme_zh_tw "預約確認、入住手續與填寫資料" \
    --output docs/tasks/mockups/a1_u06_unit_blueprint_v0.json
```

## Output Structure (Sequence Summary)

The generated skeleton contains 15 nodes structured for a "Linear-Spiral" progression:

1.  **{id}-L1**: Immersion Input (Dialogue)
2.  **{id}-L2**: Comprehension Check (Question)
3.  **{id}-L3**: Immersion Input (Notice/Document)
4.  **{id}-D1**: Structure: Dictionary (Functional Chunks)
5.  **{id}-G1**: Structure: Grammar (Pattern Card)
6.  **{id}-G2**: Structure: Grammar (Explanation Note)
7.  **{id}-P1**: Controlled Output (Chunk Assembly)
8.  **{id}-P2**: Controlled Output (Response Builder)
9.  **{id}-P3**: Pattern Transform (Productive Practice)
10. **{id}-P4**: Repair Practice (Communication Resilience)
11. **{id}-P5**: Guided Output (Speaking Roleplay)
12. **{id}-P6**: Guided Output (Writing Message)
13. **{id}-R1**: Review Retrieval (Final Recall)
14. **{id}-X1**: Scheduled Followup (+1 unit)
15. **{id}-X2**: Scheduled Followup (+3 units)

## Authoring Workflow

1.  **Generate**: Run the scaffold command.
2.  **Author**: Open the JSON file and look for `"TODO"` fields in the `payload` of each node.
3.  **Verify**: Run the `mockup-check` (implemented in UNITFAC-004) to ensure schema and quality compliance.
4.  **Preview**: Register the fixture in `fixtures.json` and view it in the Modular Viewer.
