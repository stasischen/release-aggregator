# Phase 2 Atoms Checklists

## 🟢 Pre-Audit

- [ ] **Validation Passed**: `validation.py` returns PASSED.
- [ ] **JSON Valid**: No syntax errors in `atoms_json` column.

## 🟡 Linguistic Audit (Segmentation & Lemma)

_Always refer to the Expert Audit Guide for specific segmentation rules:_

- [[linguistics/audit_ko_content.md]]
- [[linguistics/audit_th_content.md]]
- [[linguistics/audit_de_content.md]]

* [ ] **Expert Guide Consulted**: Checked segmentation/lemma rules for the target language.
* [ ] **Segmentation**:
  - **Compound Nouns**: Treated as one atom or split? (Consistency check)
  - **Phrasal Verbs**: Rule = **Single Atom** (e.g., "give up", not "give", "up").
* [ ] **POS Accuracy**:
  - [ ] No Noun/Verb confusion.
  - [ ] Particles tagged as `PART` or `ADP` correctly.
* [ ] **Lemma Accuracy**:
  - [ ] Irregular verbs mapped to correct root.
  - [ ] Plural nouns mapped to singular.

## 🔴 Final Gate

- [ ] **All Rows Parsable**: No errors when loading into game engine (simulated by validation script).
