---
description: Phase 2 Atoms (Segmentation & POS Tagging)
---

# Phase 2: Atoms (Atomization)

Phase 2: Atoms (原子化)

本階段負責將句子切分為最小語義單位（Atoms），並標註詞性（POS）與原形（Lemma）。
This phase breaks sentences into minimal semantic units (Atoms) and tags them with POS and Lemma.

## 🎯 Goal

- **Segmentation**: Confirm words are split correctly (e.g. "bus stop" vs "bus", "stop").
- **POS Tagging**: Verify correct Part of Speech (Noun, Verb, etc.).
- **Lemma**: Ensure dictionary form is correct (e.g. "went" -> "go").

## 🛑 Gatekeeper Protocol (嚴格把關協議)

**Warning**: This phase requires a mandatory "Gate 2 Pass" before proceeding to Phase 3.
**警告**：此階段必須通過「Gate 2 檢核」才能進入 Phase 3。

### Gate 2 Requirements

1. **Automated Check (自動檢查)**:
   - **Perfect Reconstruction**: Atoms concatenated MUST match source exactly.
   - **Segmentation**: No illegal suffixes inside atoms (e.g., `습니다`, `요` attached to stems).
   - **Structure**: No `null` or empty atoms.
2. **Manual Verification (人工驗證)**:
   - **Word-for-Word Inspection (逐字檢查)** of `atoms_json` for linguistic accuracy.
   - **Linguistic Logic**: Verify separable verb splits (DE) or particle attachments (KO).
3. **Data Integrity (數據完整性)**:
   - **P1 vs P2 Source Sync**: Ensure `text_source` in Phase 1 (Translation) matches Phase 2 (Atoms) exactly.
   - **Translation Alignment**: Confirm Big 5 columns (en, zh_TW, ko, ja, ru) are correctly populated without shifts.
4. **Sign-off (簽核)**:
   - Update `lingostory_universal/content/1_translation/{lang}/audit_report_p2.md` with "DATA INTEGRITY: 🟢 PASSED".
   - Commitment of verified CSVs is the final proof.

## 🛠 Tools

- **Generator**: `python tools/v5/2_atoms/create_atoms_{lang}.py` (Generates initial structure)
- **Validation**: `python -m tools.v5.2_atoms.validation {lang}` (Syntax Check)
- **Integrity**: `python tools/v5/qa/integrity_guard_universal.py {lang}` (Universal Strict Guard)

## 📚 Resources

- [Atoms Design Principles (SPACE atoms)](file:///d:/Githubs/Lingourmet_universal/docs/v5_atomization_principles.md)
- [[2_atoms/2_atoms_sop.md]]
- [[2_atoms/resources/checklists.md]]
- [Golden Sample](file:///d:/Githubs/Lingourmet_universal/.agent/workflows/2_atoms/resources/sample_atoms.csv)
