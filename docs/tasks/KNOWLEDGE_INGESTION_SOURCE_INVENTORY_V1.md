# Knowledge Ingestion Source Inventory V1 (kg-mig-015A)

This document provides a comprehensive inventory and assessment of new knowledge content from `lingo-curriculum-source/reports` for the upcoming ingestion wave.

## 1. Scan Summary

- **Total Scanned**: 349 items
- **Scan Date**: 2026-04-12
- **Source Scope**:
    - `youtube_beginner_grammar/clean_md` (126 files)
    - `youtube_connective_endings/clean_md` (109 files)
    - `youtube_connectors/clean_md` (114 files)

### Overall Classification

| Status | Count | Description |
| :--- | :--- | :--- |
| **Ready** | 184 | Fresh concepts and examples, no conflicts found. |
| **Skip** | 120 | Already exists in `content-ko` knowledge or internal source duplicate. |
| **Shared Usage** | 19 | New concept but overlaps with existing example surfaces. |
| **Needs Review** | 26 | Polysemous or complex taxonomy (e.g., `는데`, `으니까`). |

---

## 2. Shared Usage Analysis (Policy Application)

In accordance with `KNOWLEDGE_BANK_SHARED_USAGE_POLICY_V1.md`, items in the **Shared Usage** bucket have been identified as having surfaces identical to existing canonical examples.

| Source Item | Shared Canonical Example(s) | Recommendation |
| :--- | :--- | :--- |
| `009_對象標記 에게 한테` | `ex.ko.grammar.dative.call_sibling.v1`, `ex.ko.grammar.dative.feed_dog.v1` | **Merge**: Same parsing and function. |
| `023_給 에게 한테 께` | `ex.ko.grammar.dative.give_friend.v1` | **Merge**: Surface match on dative particle usage. |
| `015_在地點存在 에 있다` | `ex.ko.grammar.particle.at_time_place.at_home.v1` (implied) | **Merge**: Symmetrically link to existing items. |

> [!NOTE]
> 19 items are marked as `shared_usage`. Most are basic particles (`에`, `에서`) or polite endings (`습니다`) that were already partially extracted during prior waves.

---

## 3. Per-Family Detailed Classification

### 3.1. youtube_beginner_grammar (Ready List - Sample)
- `015_在地點存在 에 있다`
- `031_過去式了 았었했`
- `032_形容詞修飾名詞 ㄴ은 名詞`
- `043_不要口語 지 마`
- `049_必須 義務 書面正式 아야어야해야 하다`
- `055_要不要 我想要 ㄹ을래요`
- `069_決定要 約定決定 기로 하다`

### 3.2. youtube_connective_endings (Ready List - Sample)
- `001_...-기-일쑤다-總是經常-負面習慣`
- `002_...-지경이다-到了的地步--快要`
- `004_...-았었더라면-如果當時的話-後悔假設`
- `006_...-으ㄹ까-말까-猶豫要不要`
- `015_...-기-나름이다-全看怎麼做`

### 3.3. youtube_connectors (Ready List - Sample)
- `001_...-하필-偏偏-為什麼是`
- `002_...-공교롭게도-不巧-偏偏---巧合`
- `005_...-도리어-反而-反倒---與預期相反`
- `006_...-차라리-寧願-倒不如`

---

## 4. Ingestion Readiness & Recommendation

### 4.1. Preferred Pilot Batch: `youtube_connectors`
**Rationale**: 
- Connectors have the simplest structure (surface + meaning + examples).
- Lower risk of taxonomy overlap compared to grammar endings.
- High "Ready" ratio.

### 4.2. Recommended Next Wave: `youtube_beginner_grammar` (Partial)
**Rationale**:
- Focus on `Ready` items only to minimize ingestion friction.
- A pilot batch of 15-20 items from the `Ready` list is recommended.

### 4.3. Deferred Items
- **Needs Review** (26 items): Postpone until Wave 5+ or after manual vetting of `는데/은데` usage clusters.
- **Skip** (120 items): No action required except for potential cross-linking of metadata.

---

## 5. Next Steps

1. [ ] **Pilot Ingestion Plan**: Select 10 Connectors and 5 Beginner Grammars for formal ingestion.
2. [ ] **Cross-Link Update**: Update existing KIs in `Skip` list with `source_refs` pointing to these YouTube reports for better provenance.
3. [ ] **Shared Usage Formalization**: Apply merges to the 19 identified items.

---
**Status**: INVENTORY COMPLETE
**Reference**: `content-ko/scratch/kg_mig_015A_inventory.py`
