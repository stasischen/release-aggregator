# Handoff: Korean Dialogue Dictionary Mapping & Curriculum Fix (2026-02-28)

## Context
Currently working on resolving the "fallback no mapping" warning and missing word definitions in the Korean dialogue component of the `lingo-frontend-web` app. This started with lesson A1-01 but affects all lessons. Also fixed a curriculum catalog issue where B1-C1 lessons were not loading correctly.

## Accomplishments
1. **Curriculum Catalog Fix**:
   - Updated `/Users/ywchen/Dev/lingo/lingo-frontend-web/assets/content/production/packages/ko/curriculum/lesson_catalog.json`.
   - Fixed lesson IDs (e.g., `B1-01`) and titles for B1, B2, and C1 levels.
2. **Sync Automation (V5 to App)**:
   - Updated and used `/tmp/final_sync_merge_v7.py`.
   - **Key Change**: Switched from splitting morphemes into separate atoms to **aggregating** them into tokens (Eojeols) using the `+` separator (e.g., `ko:n:신입생+ko:cop:이다+ko:e:에요`).
   - This aggregation prevents the App's `SmartTextSegmenter` from overlapping atoms on the same surface text, which previously caused "fallback" warnings.
3. **Manifest Update**:
   - Rebuilt `manifest.json` using `/tmp/update_manifest.py` for all 125 lessons.

## Current State & Remaining Issues
- **Residual Fallback**: "안녕하세요" and "혹시" in A1-01 (and likely others) still show "fallback no mapping" even though they have IDs (`ko:phrase:안녕하세요` and `ko:adv:혹시`).
- **Research Findings**:
  - `mapping.json` has `"안녕하세요": "ko:adj:안녕하다+ko:e:시+ko:e:어요"`.
  - The `yarn` JSONs now have `"id": "ko:phrase:안녕하세요"`.
  - The App might be looking for `ko:phrase:안녕하세요` in the mapping AND in the dictionary. It is in the dictionary, but if it fails to resolve via the mapping or if the ID mismatch causes the `ParsedText` widget to fail safety checks, it falls back.
- **Hypothesis**: We need to either:
  1. Add `ko:phrase:안녕하세요` as a key in `mapping.json`.
  2. Change the `yarn` ID to match the mapping's value: `ko:adj:안녕하다+ko:e:시+ko:e:어요`. (Matching the mapping Value is usually better for "phrase" expansion).

## Next Steps for Successor
1. **Injection into mapping.json**: Modify `mapping.json` to include any missing phrase/atom IDs used in the `yarn` files as keys.
2. **Yarn ID Alignment**: Check if `ko:phrase:안녕하세요` should be replaced with its decomposition `ko:adj:안녕하다+ko:e:시+ko:e:어요` in the `yarn` files to satisfy the `DictionaryResolver`.
3. **Verify A1-01**: Ensure the first turn of A1-01 has ZERO fallback warnings.

## Infrastructure
- **Script**: `/tmp/final_sync_merge_v7.py` (Unified sync script).
- **Staging**: `lingo-frontend-web/assets/content/production/packages/ko/yarn/` (All 125 lessons).

(Handoff: Continued in next session)
