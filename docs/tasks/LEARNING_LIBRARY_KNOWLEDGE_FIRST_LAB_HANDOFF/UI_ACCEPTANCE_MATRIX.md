# Knowledge-First Lab UI Acceptance Matrix

## Purpose

Define the frontend product acceptance gate for Knowledge Lab before implementation.
This matrix continues the existing multi-layer Learning Library architecture and does not
change the underlying content schema.

## Route / Entry Acceptance

| Area | Acceptance | Notes |
| :--- | :--- | :--- |
| Product entry | User-facing Knowledge Lab entry opens artifact-backed Knowledge-First Lab, not seed-only test data. | Artifact mode may still have a dev compare path, but product entry must not silently use seed mode. |
| Dev/test entry | Dev testbed may keep experimental labels and seed compare tools. | Dev-only surfaces must not be used as product acceptance proof. |
| Failure state | Missing optional feature packs should show scoped degraded UI only after a valid snapshot exists. | Required core/i18n pack failures should remain clear. |

## Home / Index Acceptance

| Capability | Acceptance |
| :--- | :--- |
| Category index | Home exposes first-class entry points for `grammar`, `pattern`, `usage`, `topic`, and `vocab` where data exists. |
| Counts | Home shows real artifact-backed counts for knowledge items, topics, vocab sets, and related sources/sentences. |
| Search | User can search knowledge/topic/vocab display fields from the composed snapshot. |
| Filters | User can filter by `kind`, `subcategory`, `level`, and tags when present. |
| Empty state | Empty categories are hidden or clearly marked as unavailable; they must not look like broken product areas. |

## Knowledge Detail Acceptance

| Capability | Acceptance |
| :--- | :--- |
| Canonical identity | Detail preserves canonical knowledge id, kind, subcategory, level, and tags from core. |
| Localized teaching | Detail uses selected i18n fields for title, summary, explanation, usage notes, and example gloss. |
| Examples | Detail shows related example sentences when refs exist. |
| Reverse lookup | Detail links back to related source items and source sentences when refs exist. |
| Related graph | Detail can show related topics and vocab sets without making them dictionary truth. |

## Topic Detail Acceptance

| Capability | Acceptance |
| :--- | :--- |
| Topic hierarchy | Detail shows parent/category/level metadata when present. |
| Related knowledge | Detail lists related knowledge items grouped by kind/subcategory when possible. |
| Related vocab | Detail lists vocab sets as teaching selections, not dictionary entries. |
| Related sources | Detail links to content-first source detail for sources that use this topic. |
| Related sentences | Detail shows example sentence references from the composed snapshot. |

## Vocab Detail Acceptance

| Capability | Acceptance |
| :--- | :--- |
| Teaching selection | Vocab UI describes why these words are taught for a source/topic. |
| Dictionary boundary | If `dictionary_atom_ref` exists, link to dictionary detail/disambiguation; otherwise show surface fallback. |
| No duplicate truth | Vocab UI must not become a second dictionary model. |
| Example refs | Vocab detail shows related sentences/sources when refs exist. |

## Data / Contract Acceptance

| Area | Acceptance |
| :--- | :--- |
| Composition boundary | Screens read a composed snapshot; screens do not merge core/i18n packs. |
| Required packs | Required core/i18n pack list is explicit and matches frontend artifact manifest. |
| Optional packs | Optional feature packs are explicitly marked optional and cannot crash unrelated UI. |
| Manifest | `library_manifest.json` lists every required pack and every available optional pack. |
| Provenance | Runtime should not read raw `content-ko/content_v2` paths directly. |

## Smoke Tests To Add With Implementation

| Test | Pass Condition |
| :--- | :--- |
| Knowledge Lab artifact home smoke | Product Knowledge Lab route renders real Korean artifact counts. |
| Knowledge index smoke | Index list renders more than seed sample size and exposes filters/search. |
| Knowledge detail smoke | Selecting a knowledge item opens detail and renders localized teaching fields. |
| Reverse lookup smoke | A knowledge/topic detail renders at least one related source or sentence where refs exist. |
| Optional vocab pack smoke | Missing or renamed optional vocab set data does not crash unrelated knowledge browsing unless contract marks it required. |

