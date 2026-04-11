# KG_MIG_010 Bucket C2 Dry-Run Report

## 1. Batch Overview
- **Batch ID**: `kg-mig-010-bucket-c2-dry-run`
- **Execution Date**: 2026-04-11
- **Scope**: Remaining Bucket C items (after C1 batch 17+2+1 resolution)
- **Target**: High-confidence standalone sentences

## 2. Statistics
- **Total Candidates Reviewed**: 15
- **Ready for Extraction**: 13
- **Duplicate (Existing Bank)**: 2
- **Context-Bound / Fragment**: 0 (all selected items were verified as standalone)
- **Manual Review Required**: 0

## 3. Collision Analysis

### 3.1. Existing Bank Collisions
The following items were found to have literal index collisions with the existing `content-ko` bank:

| Surface KO | Knowledge Item Ref | Reason | Action |
| :--- | :--- | :--- | :--- |
| `할 수 있다` | `kg.grammar.ability.can` | Found in bank as `ex.ko.grammar.ability.can.v1` | Merge |
| `먹을 수 없다` | `kg.grammar.ability.cannot` | Found in bank as `ex.ko.grammar.ability.cannot.v1` | Merge |

### 3.2. Internal Batch Collisions
- No internal duplicates within the C2 batch were detected.

## 4. Extraction Candidates (C2 Highlights)

The following candidates are proposed for extraction into the bank:

| Proposed ID | Surface KO | Knowledge Item | Classification |
| :--- | :--- | :--- | :--- |
| `ex.ko.grammar.tense.future_geoyeyo.study_tomorrow.v1` | `저는 내일 공부할 거예요.` | `kg.grammar.tense.future_geoyeyo` | Ready |
| `ex.ko.pattern.payment.bargaining.v1` | `할인 가능해요?` | `kp.pattern.payment.bargaining` | Ready |
| `ex.ko.pattern.question.asking_name.informal_polite.v1` | `이름이 뭐예요?` | `kp.pattern.question.asking_name` | Ready (Unique Register) |
| `ex.ko.pattern.transport.subway_query.v1` | `지하철역이 어디예요?` | `kp.pattern.question.location_query` | Ready |
| `ex.ko.grammar.ending.additive_eulppunderseo.interesting_useful.v1` | `재미있을뿐더러 유益해요` | `kg.grammar.ending.additive_eulppunderseo` | Ready |

## 5. Risks & Ambiguities
- **Register Sensitivity**: Items like `이름이 뭐예요?` are functionally identical to `성함이 어떻게 되세요?` (C1) but differ in politeness level. We are maintaining both as separate records to support variegated learning paths.
- **Normalization Stability**: Some items in the inventory contain Hanja placeholders or mixed scripts (e.g., `유益해요`). These will be fully normalized to pure Hangul (`유익해요`) during the formal extraction phase.

## 6. Files Output
- [Inventory JSON](file:///e:/Githubs/lingo/release-aggregator/docs/tasks/KG_MIG_010_BUCKET_C2_REVIEWED_INVENTORY_V1.json)
- [Extraction Manifest JSON](file:///e:/Githubs/lingo/release-aggregator/docs/tasks/KG_MIG_010_BUCKET_C2_EXTRACTION_MANIFEST_V1.json)
