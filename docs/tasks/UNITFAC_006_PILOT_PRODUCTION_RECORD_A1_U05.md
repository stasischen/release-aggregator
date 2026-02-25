# UNITFAC-006 Pilot Production Record: A1-U05 (Pharmacy)

## Overview
- **Unit ID**: A1-U05
- **Title**: 在藥局買藥 (At the Pharmacy)
- **Status**: Production-Ready
- **Date**: 2026-02-25
- **Author**: Antigravity (AI Agent)

## Structural Compliance
| Requirement | Status | Node ID(s) |
| :--- | :--- | :--- |
| Min 10 Nodes | ✅ (13 seq nodes) | - |
| Immersion Input (Dialogue) | ✅ | A1-U05-L1 |
| Immersion Input (Non-Dialogue) | ✅ | A1-U05-L3 (Message Thread) |
| Comprehension Check | ✅ | A1-U05-L2 |
| Structure Pattern | ✅ | A1-U05-G1, A1-U05-D1 |
| Output - Controlled (Assembly) | ✅ | A1-U05-P1, A1-U05-P4 |
| Output - Controlled (Response) | ✅ | A1-U05-P2 |
| Output - Transform | ✅ | A1-U05-P3 |
| Output - Guided (Roleplay) | ✅ | A1-U05-P5 |
| Output - Guided (Message) | ✅ | A1-U05-P6 |
| Review Retrieval | ✅ | A1-U05-R1 |
| Scheduled Followups | ✅ (2 nodes) | A1-U05-X1, A1-U05-X2 |

## Content Highlights
- **Patterns**: `___가/이 아파요` (Something hurts), `___ 주세요` (Please give me ___), `-(으)세요` (Direction/Command).
- **Survival Chunks**: Covered cold medicine, headache medicine, digestive medicine, and fever reducers.
- **Repair Layer**: Added phrases for asking for repetition (`다시 말씀해 주세요`) and expressing confusion (`잘 모르겠어요`).
- **Review Strategy**: Retrieval focuses on translating clinical symptoms and pharmacists' directions back into Korean from target language prompts.

## Validation Results
- **Tool**: `tools/content_candidate_generation/bin/mockup_check.py`
- **Errors**: 0
- **Warnings**: 0
- **Status**: Verified

## Next Steps
- PM Trial in Modular Viewer.
- Freeze for batch production reference.
