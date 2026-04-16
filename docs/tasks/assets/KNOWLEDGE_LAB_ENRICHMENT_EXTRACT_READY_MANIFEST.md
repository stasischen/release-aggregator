# Knowledge Lab Enrichment: Extraction-Ready Manifest

## Goal
Inventory and classify existing KLab enrichment v1 content for example extraction readiness, separating reusable examples from item-local commentary for the Batch 001 pilot.

## Scope (Wave 1)
- `kg.grammar.particle.*`
- `kg.connector.*`
- `kp.daily.greeting.*`

---

## 1. Inventory & Classification Manifest

| Item ID | Kind | Status | Example Count | Classification | Note / Skip Reason |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **kg.grammar.particle.subject** | grammar | READY | 8 | Reusable | subject marker (이/가) |
| **kg.grammar.particle.object** | grammar | READY | 10 | Reusable | object marker (을/를) |
| **kg.grammar.particle.topic_eunneun** | grammar | READY | 8 | Reusable | topic marker (은/는) |
| **kg.grammar.particle.at_time_place** | grammar | READY | 5 | Reusable | time/place (에) |
| **kg.grammar.particle.at_place_action** | grammar | READY | 5 | Reusable | action location (에서) |
| **kg.grammar.particle.also** | grammar | READY | 5 | Reusable | also (도) |
| **kg.grammar.particle.and_with_hago** | grammar | READY | 4 | Reusable | with/and (하고) |
| **kg.grammar.particle.wagwa** | grammar | READY | 5 | Reusable | with/and (와/과) |
| **kg.grammar.particle.boda** | grammar | READY | 5 | Reusable | comparative (보다) |
| **kg.grammar.particle.man** | grammar | READY | 5 | Reusable | only (만) |
| **kg.grammar.particle.euro_dir** | grammar | READY | 5 | Reusable | direction (로) |
| **kg.grammar.particle.euro_tool** | grammar | READY | 5 | Reusable | tool/means (로) |
| **kg.connector.cause.geuraeseo** | connector | READY | 5 | Reusable | so/therefore |
| **kg.connector.cause.geureomeuro** | connector | READY | 5 | Reusable | hence/therefore (formal) |
| **kg.connector.cause.geureonikka** | connector | READY | 5 | Reusable | so/as/since |
| **kg.connector.cause.ttaraseo** | connector | READY | 5 | Reusable | accordingly |
| **kg.connector.condition.geureomyeon** | connector | READY | 5 | Reusable | if so / then |
| **kg.connector.contrast.hajiman** | connector | READY | 5 | Reusable | but (neutral) |
| **kg.connector.contrast.geureochiman** | connector | READY | 5 | Reusable | but/however |
| **kg.connector.contrast.geureona** | connector | READY | 5 | Reusable | but (formal) |
| **kg.connector.contrast.geureonde** | connector | READY | 5 | Reusable | but/well (contrast) |
| **kg.connector.contrast.geuraedo** | connector | READY | 5 | Reusable | even so |
| **kg.connector.conversion.geureonde** | connector | READY | 5 | Reusable | by the way (topic change) |
| **kg.connector.sequence.geurigo** | connector | READY | 5 | Reusable | and/then |
| **kg.connector.sequence.geureom** | connector | READY | 5 | Reusable | then/well |
| **kg.connector.sequence.gedaga** | connector | READY | 5 | Reusable | besides/furthermore |
| **kp.daily.greeting.annyeong** | pattern | READY | 3 | Reusable | Anyo/Hello |
| **kp.daily.greeting.bangawoyo** | pattern | SKIP | 0 | No Examples | Item exists but has no example_bank entries. |

---

## 2. Extraction Quality Check (Batch 001)

- **Total Items Evaluated**: 28
- **Total Ready for Extraction**: 27
- **Total Skipped**: 1 (No examples in JSON)
- **OCR/Mixed-Script Check**: 100% clean Korean strings in `example_bank.ko`.
- **Instructional Metadata Check**: No highlighting (`*`, `[]`) found in `example_bank.ko`.

---

## 3. Pilot Extraction Slice Selection (12 Items)

| Selection Rank | Item ID | Type | Reason |
| :---: | :--- | :--- | :--- |
| 1 | `kg.grammar.particle.subject` | Core Grammar | High frequency, very stable. |
| 2 | `kg.grammar.particle.object` | Core Grammar | High frequency, very stable. |
| 3 | `kg.grammar.particle.topic_eunneun` | Core Grammar | High frequency, very stable. |
| 4 | `kg.grammar.particle.at_time_place` | Core Grammar | High frequency, very stable. |
| 5 | `kg.connector.cause.geuraeseo` | Connector | Pillar of cause/effect. |
| 6 | `kg.connector.contrast.hajiman` | Connector | Pillar of contrast. |
| 7 | `kg.connector.sequence.geurigo` | Connector | Pillar of sequence. |
| 8 | `kg.connector.contrast.geureonde` | Connector | Stable contrast/transition. |
| 9 | `kg.grammar.particle.and_with_hago` | Particle | Oral usage indicator. |
| 10 | `kg.grammar.particle.also` | Particle | Stable additive particle. |
| 11 | `kp.daily.greeting.annyeong` | Greeting | Foundation of phrases. |
| 12 | `kg.connector.sequence.geureom` | Connector | Simple transition. |

---

## 4. Skip List (Rationale)

| Item ID | Reason | Automated Detection Rule |
| :--- | :--- | :--- |
| `kp.daily.greeting.bangawoyo` | No `example_bank` found in i18n JSON. | `len(item.example_bank) == 0` |
| `kg.grammar.ending.*` | Out of scope for this thread. | `startswith("kg.grammar.ending")` |
| `kg.grammar.tense.*` | Out of scope for this thread. | `startswith("kg.grammar.tense")` |
| `kp.pattern.social_basic.*` | Out of scope for this thread. | `startswith("kp.pattern.social_basic")` |

---

## 5. Verification Checklist (Completed)

- [x] Extraction manifest created.
- [x] No Wave 2 items included.
- [x] No bulk ingestion performed.
- [x] Example bank vs commentary separation verified for pilot list.
- [x] `source_ref` hygiene check (pilot items have no raw media IDs in bank).
