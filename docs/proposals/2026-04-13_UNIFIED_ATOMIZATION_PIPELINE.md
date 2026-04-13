# Unified Content Atomization Pipeline

**Date**: 2026-04-13
**Status**: Proposal → Execution Spec (V2)
**Goal**: All sentence-level containers (dialogue lines, video turns, article sentences) must pass the same `surface → atoms` canonical validation contract.

---

## 1. Core Principle: Engine Is the Validator, Not the Author

The Engine (`engine/tokenizer.py` + `engine/rules_engine.py`) is the **canonical validator and formatter**.
It is NOT an unconditional auto-rewriter that silently overrides authoring decisions.

### What the Engine Decides (Law)
- POS taxonomy: `pos_taxonomy.py` CANONICAL_POS is the only valid set.
- Ending decomposition: composite endings MUST be recursively split per `KO_DATA_STANDARDIZATION_PROTOCOL.md`.
- Atom ID format: `ko:<pos>:<lemma>` with NFC normalization.
- Reversibility: `join(atom.text for atom in atoms) == surface`.

### What the Engine Does NOT Decide
- Whether a specific word is a noun vs. a verb when both are linguistically valid.
- Whether a novel compound word should be split or kept whole.
- Domain-specific annotation choices (e.g., colloquial contractions in video subtitles).

These are **human review decisions**, not engine overrides.

---

## 2. Container Unit vs. Atomization Unit

These are two distinct layers that MUST NOT be conflated.

### Container Unit (Domain-Specific)
The outer wrapper differs by content type:

| Domain | Container Name | ID Field | Domain Metadata |
|:---|:---|:---|:---|
| `dialogue` | line | `line_id` | `lesson_id`, `role`, `eojeol_index` |
| `video` | turn | `turn_id` | `video_id`, `time_start`, `time_end` |
| `article` | sentence | `sentence_id` | `article_id`, `paragraph_id` |

Container names, schemas, and upstream source formats **do not** need to be unified.

### Atomization Unit (Universal)
The inner validation payload is **identical** across all domains:

```json
{
  "surface": "가져왔어요",
  "gold_final_atom_id": "ko:v:가져오다+ko:e:았+ko:e:어요"
}
```

This is the shape that `lint_gold.py`, `remediate_gold.py`, and `qa_gate.py` operate on.

### Bridge: Normalized Validation Item

To feed domain-specific containers into the unified validation pipeline, each tool must normalize items to this common shape:

```json
{
  "domain": "dialogue|video|article",
  "container_id": "A1-01:L01-D1-02:3",
  "surface": "맞아요",
  "gold_final_atom_id": "ko:v:맞다+ko:e:아요",
  "source_hash": "sha256:..."
}
```

Domain metadata is preserved in the source file but stripped for validation purposes.

---

## 3. Auto-Fix vs. Manual-Review Matrix

### ✅ Auto-Fixable (Engine Normalizer can apply without human approval)

| Category | Example | Justification |
|:---|:---|:---|
| POS alias normalization | `ko:Verb:가다` → `ko:v:가다` | Pure formatting; `pos_taxonomy.py` canonical mapping |
| Atom ID casing | `ko:N:사람` → `ko:n:사람` | Pure formatting |
| Jamo normalization | NFD `ᄇ니다` → NFC `ㅂ니다` | Unicode normalization; no semantic change |
| Space atom → canonical form | `ko:space` → `ko:space:SPACE` or vice versa | Format alignment between domains |
| Known ending template split | `았어요` → `ko:e:았+ko:e:어요` | Deterministic; defined in SOP mapping table |
| Known ending template split | `셨어요` → `ko:e:시+ko:e:었+ko:e:어요` | Deterministic; defined in SOP mapping table |
| Known ending template split | `세요` → `ko:e:시+ko:e:어요` | Deterministic; defined in SOP mapping table |
| Surgery heuristic exact match | `했어요` → `ko:v:하다+ko:e:었+ko:e:어요` | Confidence 1.0 in `surgery_heuristics.json` |
| Punct atom insertion/removal | Add/strip `ko:punct:*` atoms | Structural alignment to domain spec |

### 🔴 Manual-Review Required (Engine reports but MUST NOT auto-apply)

| Category | Example | Why Manual |
|:---|:---|:---|
| Dictionary unknown | New word not in any mapping | Requires human to define lemma + POS |
| Competing valid segmentations | `차가` = `차+가` (car+subj) vs. `차갑다` stem | Semantic ambiguity; context-dependent |
| Surface ≠ source | Atom surface doesn't match original text | Possible hallucination; must verify against source |
| Engine reconstruction fail | Engine can't uniquely reconstruct | Irregular form; needs lexical override |
| POS dispute (v vs. adj) | `있다` as adj vs. v in context | Both POS exist in dictionary; context-dependent |
| Novel compound word | Should `김치볶음밥` be 1 atom or 3? | Domain/pedagogical decision |
| Phrase decomposition choice | `안녕하세요` as phrase vs. `안녕하다+세요` | Gold decomposes; dictionary keeps phrase. Video currently uses phrase. |

### ⚠️ Escalation Policy

If `normalize_video_atoms.py` encounters a case not covered by either list above:
1. **Default to manual-review** (conservative).
2. Log the case to `reports/normalize_escalations.jsonl`.
3. A human decides; if the pattern recurs, add it to the appropriate list.

---

## 4. Unified Pipeline Flow

### For Dialogue (Existing — No Change)
```
Source Text → Engine Tokenizer → Auto Remediation → Lint → Human Surgery → QA Gate → Gold
```

### For Video (Proposed — Aligned)
```
Source Subtitle → Gemini Initial Atomization → Engine Normalizer → Auto Remediation → Lint → Human Review → QA Gate → Gold
                                                    ↑                    ↑                ↑
                                              Auto-fix only      Engine-fixable     Report only
                                              (Section 3 ✅)     (remediate_gold)   (lint_gold)
```

### For Article (Schema Reserved — Phase 2)
Same flow as Dialogue. Container schema defined now; implementation deferred.

---

## 5. Implementation Roadmap

### Phase 1: Spec + Tooling Foundation
- [x] Write `UNIFIED_ATOMIZATION_PIPELINE.md` (this document)
- [ ] Create `normalize_video_atoms.py` with explicit auto-fix / manual-review boundary
- [ ] Extend `lint_gold.py` to accept `--content-type video` and normalize video JSON items
- [ ] Extend `remediate_gold.py` to accept `--content-type video`
- [ ] Update `build_gemini_video_atom_bundle.py` prompt with V5 ending decomposition rules

### Phase 2: Pilot Alignment
- [ ] Run normalizer on `BWINkN8QbkU_atoms.json` (dry-run first)
- [ ] Diff review: human inspects auto-fix results + escalation log
- [ ] Run lint + remediate on normalized atoms
- [ ] Full-pass human review of residuals

### Phase 3: Stabilize + Scale
- [ ] Retroactively normalize all existing video atoms
- [ ] Add `--content-type video` mode to `qa_gate.py`
- [ ] Define Article container schema + reserve pipeline slot
- [ ] Document and commit final auto-fix / manual-review matrix as SOP

---

## 6. Resolved Open Questions

| # | Question | Decision |
|:---|:---|:---|
| Q1 | Engine as sole validator? | **Yes.** All domains must pass the same `surface → atoms` validation. |
| Q2 | Engine can auto-rewrite? | **Format normalization only.** Segmentation judgment differences → manual review. |
| Q3 | Article included now? | **Schema yes, implementation Phase 2.** Prevents schema redesign later. |
| Q4 | Video attestation? | **Yes, simplified.** Per-video attestation (`video_review_attest.json`), not per-turn. |
| Q5 | Retroactive normalization? | **Yes.** Batch normalize → human diff review. Low effort for existing 3 videos. |

---

*V2 revised based on design review feedback. Core changes: (1) explicit container/atomization separation, (2) engine authority boundary, (3) auto-fix vs manual-review matrix.*
