# Rule-Engine Fix Backlog (KO-GEMINI-04)

Derived from:
- `KO_SEGMENTATION_ENGINE_BLOCKERS_2026-02-16.md`
- `qa_report_A1_A2_B1_B2_C1_Validation_20260222_230004.md`
- `audit_report.txt`

## 1. Rule Family: Honorific Formal (ㅂ니다 / ㅂ니까)

**Priority: HIGH**

- **Symptom**: Common formal endings in A1-A2 content are currently unresolved or require manual overrides.
- **Target Patterns**:
  - `-(스)ㅂ니다`: `아닙니다`, `있습니다`, `계십니다`, `됩니다`.
  - `-(스)ㅂ니까`: `어떻습니까`, `있습니까`, `계십니까`, `않습니까`.
- **Proposed Rule**:
  - `verb_formal_bnida`: `(.+)([ㅂ습])니다$` -> `ko:v:{stem}다` + `ko:e:ㅂ니다`.
  - `verb_formal_bnikka`: `(.+)([ㅂ습])니까$` -> `ko:v:{stem}다` + `ko:e:ㅂ니까`.
- **Expected Impact**: Substantial reduction in unresolved ratio for formal/polite content (levels B1/B2/C1).

## 2. Rule Family: Polite Command (십시오)

### Priority: MEDIUM (Family 2)

- **Symptom**: `주십시오` (top unresolved in recent reports).
- **Target Patterns**:
  - `-십시오`: `주십시오`, `가십시오`.
- **Proposed Rule**:
  - `verb_polite_sipsio`: `(.+)([시스])십시오$` -> `ko:v:{stem}다` + `ko:e:시` + `ko:e:ㅂ시오` (or atomic mapping).
- **Expected Impact**: Cleanly handles polite requests without manual mapping.

## 3. Rule Family: Conjecture & Modality

### Priority: MEDIUM (Family 3)

- **Symptom**: `듯합니다`, `텐데`, `된다면` clustered in unresolved lists.
- **Target Patterns**:
  - `-듯하다` (Conjecture)
  - `-ㄴ/은/ㄹ 텐데` (Background info/Assumption)
  - `-ㄴ/은/면` (Conditionals)
- **Proposed Rule**:
  - Add specific productive rules in `35_productive_morphology.json`.

## 4. Architectural Fixes (Regression Prevention)

### Priority: CRITICAL (Architecture)

- **Status Check**:
  - `suffix_yo` (B2 blocker) has been REMOVED from `70_modifiers_fallback.json`.
  - `dictionary_exact` priority is `110`.
- **Action**: Verify if `dictionary_exact` should be lowered below productive rules (e.g. to `10`) to allow segmentation to take precedence over exact dictionary match for productive forms.

## 5. Metadata & POS Synchronization

### Priority: HIGH (Data Sync)

- **Finding**: `-되다` verbs are often tagged as adjectives in dictionary.
- **Action**: Execute bulk move as part of `MAPPING_DICTIONARY` track.
- **Evidence**: `KO-GEMINI-05` audit findings.

## 6. Redundancy Elimination (Override Clean-up)

### Priority: LOW (Maintenance)

- **Finding**: Over 100+ instances of `있어요`, `해요`, `저는` in manual overrides.
- **Action**: Once rules are stable, purge these from `surgery_*.json` and `mapping_accepted.jsonl` to reduce technical debt.

---

### Status: Ready for Implementation (feeds into `KO-MAP-03`)
