# Phase 1 Translation Checklists

## 🟢 Pre-Audit

- [ ] **Dependencies**: Python environment is active.
- [ ] **Latest Source**: `0_yarn` is up to date (git pull).
- [ ] **DB Updated**: Ran `python -m tools.v5.core.update_db` recently.

## 🟡 Content Audit (CSV)

- [ ] **No Invisible Empty Lines**: Ensure no rows where `text_source` exists but `trans_{lang}` is empty/whitespace.
- [ ] **Header Integrity**: `line_id`, `text_source`, `trans_{lang}`, `trans_en` columns are present.
- [ ] **Tags Clean**: Ensure no HTML/Yarn tags leaked into the translation text.
- [ ] **BOM Fix**: Files are `utf-8-sig` (Excel compatible) or standard `utf-8`.

## 🟣 Linguistics (Language Specific)

_Always refer to the Expert Audit Guide for the target language:_

- [[linguistics/audit_ko_content.md]]
- [[linguistics/audit_th_content.md]]
- [[linguistics/audit_de_content.md]]

- [ ] **Expert Guide Consulted**: Checked the specific rules (e.g. KO speech levels) in the expert guide.
- [ ] **Type-Specific Checks**:
  - **Scenario (Dialogue)**:
    - [ ] **Tone**: Matches character personality (Polite/Casual/Formal).
    - [ ] **Spoken Style**: Particles allowed (thai `krub/ka` ok).
  - **Article (Narrative)**:
    - [ ] **KO**: Plain form (해라체) ONLY.
    - [ ] **DE**: Präteritum for narrative.
    - [ ] **TH**: No spoken particles in narrative.

## 🔴 Final Gate

- [ ] **Validation Script**: `python -m tools.v5.1_translation.validation {lang}` returns **PASSED**.
