# Walkthrough: Dictionary-to-Grammar Deep Linking UI (kg-ui-019)

This document tracks the stabilization of design specifications and implementation progress for the Dictionary Grammar Linking feature.

## Status Summary

| Phase | Description | Status | Owner |
| :--- | :--- | :--- | :--- |
| **Logic & Spec** | Format and mapping logic stabilization | In Progress | mac |
| **UI Design** | Component and interaction design | Todo | m5pro |
| **FE Implementation** | Drawer and overlay execution | Todo | m5pro |

## Accomplishments (mac)

### Spec Stabilization
- Aligned `KG-UI-019` requirements with the latest **V5 Frozen Spec**.
- Verified that `surface_ko` -> `ko` and `translation_zh_tw` -> `translation` transitions are reflected in related normalization plans.
- Task indexed in `TASK_INDEX.md` under Layer 2.

## Next Steps
- [ ] `m5pro`: Propose UI design for the "文法詳解" chip.
- [ ] `m5pro`: Define Drawer behavior for Web vs. Mobile.
- [ ] `mac`: Finalize `dict_grammar_mapping.json` schema validation.
