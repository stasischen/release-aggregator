# Tools Manifest (V5 Content Pipeline)

This document serves as the **Inventory of Truth** for required tooling.
If a tool listed here is missing for your target language, you MUST build it using the reference implementation.

## 🟢 Phase 1: Translation

- `tools/v5/core/update_db.py` (Universal)
- `tools/v5/core/update_db.py` (Universal)
- `tools/v5/audit/audit_lang.py` (Universal Phase 1 Audit)
- `tools/v5/qa/integrity_guard_universal.py` (Universal Strict Guard)

## 🟡 Phase 2: Atoms

- `tools/v5/2_atoms/create_atoms_{lang}.py` (Intelligent Generator)
  - Status:
    - [x] ko (`create_atoms_ko.py`)
    - [ ] de (Use `create_atoms_de.py` or generic fallback)
- `tools/v5/2_atoms/validation` (Universal Module)

## 🟠 Phase 3: Mapping

- `tools/v5/core/extract.py` (Universal)
- `tools/v5/qa/check_mapping_collisions.py` (Universal)

## 🟣 Phase 4: Dictionary

- `tools/v5/core/sync.py` (Universal)
- `tools/v5/4_dictionary/enrich.py` (Universal)

## 🏁 Phase 5: Build

- `tools/v5/core/merger.py` (Universal)
- `tools/v5/5_build/builder.py` (Universal)
- `tools/v5/5_build/audit_view.py` (Universal)
