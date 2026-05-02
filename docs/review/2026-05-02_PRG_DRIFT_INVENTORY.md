# PRG Phase 2 Drift Inventory & Promotion Readiness
# date: 2026-05-02
# scope: promotion-readiness audit before rename/deploy of PRG prototype

---

## 1. DRIFT INVENTORY

Each finding maps to one of the 7 drift categories from the audit brief.

---

### D1: Docs that say PRG should scan raw content-ko or raw staging directories in production mode

#### D1.1 — P1 — docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:13

**Current wording:**
`| **Scope** | All content in \`content-ko\` (including B1+ segmentation-in-progress) | Only \`production-ready\` units and lessons. |`

**Why stale/risky:**
The Staging Catalog scope column says "All content in `content-ko`". Post Phase-1/Phase-2 architecture decision, the staging catalog scope must be Phase 1 staging output (from `release.py`), not the raw `content-ko` repo. Presenting `content-ko` as the staging scope encourages bypassing the hardened provenance pipeline.

**Recommended disposition:**
Change to `"All content in Phase 1 staging output (release.py + global_manifest.json)"`.

---

#### D1.2 — P1 — docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:28

**Current wording:**
```
A[content-ko / source truth] -->|Pipeline Build| B[Staging Candidate Artifacts]
B --> C[Staging Catalog / Full Inventory]
C -->|Inst. Review & QA| D{Release Decision}
D -->|Allowlist| E[Production Release Manifest]
E -->|Production Assembler| F[Production Bundle / Frontend Assets]
```

**Why stale/risky:**
The Mermaid diagram starts from `content-ko / source truth` and shows a single "Pipeline Build" -> "Staging Candidate Artifacts" -> "Production Assembler" chain. This collapses Phase 1 (release.py, global_manifest.json, provenance) into an invisible step. It also implies PRG receives candidate artifacts directly from `content-ko`, which contradicts the architecture decision that PRG must consume Phase 1 staging output.

**Recommended disposition:**
Redraw to show: `content-pipeline/dist` -> `Phase 1: release.py + global_manifest.json` -> `Phase 2: PRG assembler` -> `Production artifacts`.

---

#### D1.3 — P1 — docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:9

**Current wording:**
`It MUST NOT directly scan \`content-ko\` repositories or candidates to determine "what to release."`

**Why stale/risky:**
This is the correct rule, but it says "content-ko repositories" when the current architecture concern is that PRG must also not scan raw Phase 1 staging directories or `content-pipeline/dist` directly. The scope should be broader: PRG must consume `global_manifest.json` or a derived candidate inventory, not any raw directory. Contrast: the code itself does reference `content-ko/dist_unified/staging/ko` as a default path (lines 503, 566 of assembler_prototype.py).

**Recommended disposition:**
Broaden: `"must not directly scan any raw content repository, content-pipeline/dist, or raw staging directory. Must consume \`global_manifest.json\` or a typed candidate inventory derived from Phase 1 staging."`

---

### D2: Docs that omit global_manifest.json as Phase 1 provenance source

#### D2.1 — P0 — docs/human-handbook/08_PRG_ARTIFACT_MAP.md:186-192

**Current wording:**
```
source truth
  -> staging candidate inventory
  -> release manifest
  -> production assembler
  -> production manifest / lesson catalog / bundles
```

**Why stale/risky:**
`global_manifest.json` — the hardened provenance artifact from Phase 1 (release.py) — is completely absent from the PRG artifact flow. This is the canonical human-handbook entry for PRG, so it defines the mental model for anyone working on release gating. Without `global_manifest.json` in the flow, readers will assume PRG assembler can scan staging candidate directories directly.

**Recommended disposition:**
Insert `global_manifest.json` as the bridge between "staging candidate inventory" and "release manifest":
```
content-pipeline/dist
  -> Phase 1: release.py staging + global_manifest.json
  -> Phase 2: release manifest + candidate inventory (from global_manifest.json)
  -> production assembler
  -> production manifest / lesson catalog / bundles
```

---

#### D2.2 — P0 — docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:186-192

**Current wording:**
Identical text flow diagram as D2.1 above.

**Why stale/risky:**
Same issue — the task-level artifact map is a working document for implementers. Omitting `global_manifest.json` means task authors may design PRG features that bypass Phase 1 provenance.

**Recommended disposition:**
Same fix as D2.1.

---

#### D2.3 — P1 — docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:26-34

**Current wording:**
The Mermaid diagram (detailed in D1.2 above).

**Why stale/risky:**
In addition to the `content-ko` origin problem (D1.2), the diagram does not show `global_manifest.json` anywhere in the flow. The transition from "Staging Candidate Artifacts" to "Production Assembler" happens without a provenance checkpoint.

**Recommended disposition:**
Add `global_manifest.json` as an explicit node between staging artifacts and the release decision.

---

#### D2.4 — P2 — docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:19

**Current wording:**
`| Staging Candidate Inventory | \`content-pipeline/staging/**\` or prototype staging outputs in \`staging/prototype_output/**\` |`

**Why stale/risky:**
Lists `content-pipeline/staging/**` as the staging candidate inventory path, but omits `global_manifest.json` as the authoritative index of what is in staging. This path reference is ambiguous — it could mean raw content-pipeline staging.

**Recommended disposition:**
Add `global_manifest.json` as the authoritative staging index: `"Phase 1 staging output, indexed by global_manifest.json"`.

---

### D3: Docs that describe PRG outputs incorrectly after recent changes

#### D3.1 — P1 — docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:28

**Current wording:**
`3. **Asset Bundles**: The actual JSON artifacts and audio referenced by the allowlisted lessons.`

**Why stale/risky:**
The PRG contract lists three outputs: `manifest.json`, `lesson_catalog.json`, and "Asset Bundles." The actual code (assembler_prototype.py:492-495) outputs three files: `manifest.json`, `lesson_catalog.json`, and **`production_plan.json`**. The production plan contains gaps, allowlisted lessons, packaged artifacts, provenance — but it does NOT output asset bundles (the actual lesson JSON and audio files). The contract promises a deliverable the code does not produce.

**Recommended disposition:**
Update the contract to list the actual three outputs: `manifest.json`, `lesson_catalog.json`, `production_plan.json`. Add a note that "Asset bundles are Phase 2 future scope."

---

#### D3.2 — P2 — docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:25

**Current wording:**
`The Production Assembler outputs the following files into the production directory (e.g., \`lingo-frontend-web/assets/content/production/\`):`

**Why stale/risky:**
The contract says the output directory is `lingo-frontend-web/assets/content/production/`. The actual default output directory is `staging/prototype_output/` (assembler_prototype.py:527). For a prototype, `staging/prototype_output/` is correct. But the contract reads as if PRG already writes directly into the frontend production path, which overstates its readiness.

**Recommended disposition:**
Clarify that the current output path is `staging/prototype_output/` and that `lingo-frontend-web/assets/content/production/` is the future target after promotion.

---

#### D3.3 — P2 — docs/runbooks/release_cut_and_rollback.md:29

**Current wording:**
`PRG remains prototype until it preserves provenance from \`global_manifest.json\` into its \`production_plan.json\` and rejects raw directory scanning in strict production mode.`

**Why stale/risky:**
The runbook lists these as promotion blockers. But the code already does BOTH: (a) provenance carry-through from global_manifest.json into production_plan.json (see test_prg_provenance_bridge.py:93-97, assembler_prototype.py:131-132, 331-339), and (b) strict mode rejects raw directory scanning (assembler_prototype.py:576-580). The runbook is behind the code on these two criteria. However, other blockers (old default paths, missing Makefile wiring) remain valid.

**Recommended disposition:**
Update to reflect that provenance carry-through and strict-mode directory rejection are now implemented, but list remaining blockers: old default path `content-ko/dist_unified/staging/ko`, test gap, Makefile gap.

---

### D4: Tests missing from Makefile or runbook validation commands

#### D4.1 — P1 — Makefile (entire file)

**Current behavior:**
The Makefile has zero test targets. Neither `test_prg_frontend_contract.py` nor `test_prg_provenance_bridge.py` appear. There is no `make test`, `make test-prg`, or `make validate` target.

**Why stale/risky:**
PRG tests exist but are not discoverable or runnable through the standard command surface. CI pipelines, reviewers, and future developers have no documented way to run them. The review packet (2026-05-02_RELEASE_AGGREGATOR_GPT_REVIEW_PACKET.md:67-69) already flagged this.

**Recommended disposition:**
Add `make test-prg` target that runs both test files via `python -m pytest tests/ -v` or `python -m unittest discover -s tests/`.

---

#### D4.2 — P2 — docs/runbooks/release_cut_and_rollback.md (section 4, line 36)

**Current wording:**
`- **Command**: \`npm run test:content\` (in frontend)`

**Why stale/risky:**
The runbook's validation section only references the frontend content test. It does not mention PRG contract tests or provenance bridge tests as validation gates for the release cut.

**Recommended disposition:**
Add a validation step: "Run `make test-prg` in release-aggregator to verify PRG contract and provenance bridge before promotion."

---

### D5: Old paths presented as production defaults

#### D5.1 — P0 — scripts/prg/assembler_prototype.py:503, 566

**Current path:**
`content_ko_staging = aggregator_root.parent / "content-ko/dist_unified/staging/ko"` (line 503)
`expected_default = aggregator_root.parent / "content-ko/dist_unified/staging/ko"` (line 566)

**Why stale/risky:**
This is a raw `content-ko` repo path with a legacy `dist_unified/staging/ko` subdirectory structure. The current Phase 1 architecture produces staging output under `release-aggregator/staging/<version>/`, indexed by `global_manifest.json`. The default path points to a sibling repo directory that may or may not exist, and even if it does, it represents unvalidated raw pipeline output that has not passed through the release.py provenance gate.

**Recommended disposition:**
Change the default to consume `global_manifest.json` from Phase 1 staging. Remove the `content-ko/dist_unified/staging/ko` fallback entirely. The `--candidate-source` default should be `staging/<version>/global_manifest.json` or absent (requiring explicit CLI specification).

---

#### D5.2 — P1 — scripts/prg/assembler_prototype.py:563

**Current wording:**
`# Explicit path from requirement: e:\Githubs\lingo\content-ko\dist_unified\staging\ko`

**Why stale/risky:**
Contains a developer machine-specific Windows path (`e:\Githubs\...`) as a code comment. This is not portable and references the old architecture.

**Recommended disposition:**
Remove or replace with repo-relative path reference.

---

#### D5.3 — P3 — docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:19

**Current wording:**
`| Staging Candidate Inventory | \`content-pipeline/staging/**\` or prototype staging outputs in \`staging/prototype_output/**\` |`

**Why stale/risky:**
Mentions `content-pipeline/staging/**` as a staging path. This was valid before Phase 1 staging was introduced, but post-architecture, staging candidates should be referenced through Phase 1 staging output under `release-aggregator/staging/`.

**Recommended disposition:**
Replace with `"Phase 1 staging output (release-aggregator/staging/<version>/** + global_manifest.json)"`.

---

### D6: Wording that implies assembler_prototype.py is production-ready

#### D6.1 — P1 — docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md (title + entire document)

**Current wording:**
Title: `PRG-004: Production Assembler Contract Specification`
L1: "Define the new role and responsibilities of the **Production Assembler**"

**Why stale/risky:**
The document title and throughout refers to "Production Assembler" as if it already exists as a production component. The actual file is named `assembler_prototype.py`, and the architecture review (2026-05-02_PRG_PHASE2_REVIEW_DECISION.md) explicitly says "Promote later" and "Do not rename assembler_prototype.py yet." The contract language is ahead of implementation reality.

**Recommended disposition:**
Retitle sections to "Prototype Assembler Contract" or add a prominent disclaimer at the top: "This spec is aspirational. The current implementation is `assembler_prototype.py` and is not yet promoted to production."

---

#### D6.2 — P2 — docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:18-22

**Current wording:**
The table lists "Production `manifest.json`", "Production `lesson_catalog.json`", "Production bundles" as if these are live artifacts from PRG.

**Why stale/risky:**
These are described as the outputs of the PRG flow, but the PRG assembler is a prototype outputting to `staging/prototype_output/`, not to the frontend production paths. The artifact map table makes no distinction between current reality (prototype_output) and future target (frontend production paths).

**Recommended disposition:**
Add a status column or note: "Currently generated to `staging/prototype_output/`; future target is `lingo-frontend-web/assets/content/production/`."

---

#### D6.3 — P2 — docs/tasks/PRG_005_PILOT_PLAN.md:3

**Current wording:**
`Establish a small, production-ready allowlist slice using **exactly-matched** content`

**Why stale/risky:**
The phrase "production-ready" applied to the PRG-005 pilot scope is misleading. After the architecture review, PRG is "promote later" — the pilot validates the approach but the assembler is still a prototype.

**Recommended disposition:**
Change to: "Establish a small pilot allowlist slice" — remove "production-ready" from this document.

---

### D7: Mismatch between PRG contract docs and actual current code behavior

#### D7.1 — P0 — assembler_prototype.py:503 vs docs/runbooks/release_cut_and_rollback.md:28

**Contract says (runbook line 28):**
`PRG must consume validated staging artifacts from Step 1 or a candidate inventory derived from them. It must not bypass Step 1 by reading raw source repositories as a production input.`

**Code does (assembler_prototype.py:503):**
`content_ko_staging = aggregator_root.parent / "content-ko/dist_unified/staging/ko"` — this is the default candidate source in `parse_args()`.

**Risk:**
If `content-ko/dist_unified/staging/ko` exists on disk, PRG will silently use raw content-ko pipeline output as its default candidate source, completely bypassing Phase 1 provenance. This is the single highest-risk drift item.

**Recommended disposition:**
Remove the default. Require explicit `--candidate-source` with a `global_manifest.json` for strict mode. Add a check in `main()` that warns if the candidate source is not a `global_manifest.json` in strict mode.

---

#### D7.2 — P1 — assembler_prototype.py:576-581 vs docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:40

**Contract says (PRG_002 line 40):**
`Production Assembler should NEVER scan \`core/dialogue\` or \`core/video\` directly for production releases.`

**Code does (assembler_prototype.py:576-581):**
In strict mode, rejects directory scanning with a clear error. In planning mode, allows it via `CandidateInventory.scan_directory()`. This is CORRECT behavior (strict mode guard), but the `scan_directory` method (lines 138-179) still exists and works in planning mode.

**Risk:**
Low risk for promotion since strict mode blocks it. But `scan_directory` as a code path creates maintenance risk — a future refactor could accidentally re-enable it.

**Recommended disposition:**
Add a comment above `scan_directory` marking it as planning-only / deprecated for production. Consider moving it to a separate module.

---

#### D7.3 — P1 — assembler_prototype.py:492-495 vs docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:26-28

**Contract says (PRG_004 lines 26-28):**
Outputs: `manifest.json`, `lesson_catalog.json`, and "Asset Bundles."

**Code does (assembler_prototype.py:492-495):**
Outputs: `manifest.json`, `lesson_catalog.json`, `production_plan.json` — no asset bundles.

**Risk:**
The contract and code disagree on what the third output is. This misalignment means the contract is not usable as an acceptance test.

**Recommended disposition:**
Either implement asset bundle output, or update the contract to list `production_plan.json` as the third output with a note that asset bundles are a future deliverable.

---

#### D7.4 — P1 — test_prg_frontend_contract.py:65 vs intended Phase 2 architecture

**Contract/architecture says:**
PRG in production mode must use `global_manifest.json` as its candidate source.

**Test does (line 65):**
`inventory = assembler.CandidateInventory.scan_directory(candidate_root)` — uses the directory scanner path.

**Risk:**
The frontend contract test validates the legacy scanning path, not the `load_from_global_manifest` path. If the scanning path is removed, this test breaks but with the wrong signal (it should test the new path).

**Recommended disposition:**
Add a parallel test case that exercises `load_from_global_manifest` and validates the same frontend contract fields. Keep the `scan_directory` test but mark it as planning-mode coverage.

---

#### D7.5 — P2 — review doc 2026-05-02_PRG_PHASE2_REVIEW_DECISION.md:59 vs actual code

**Review doc says (line 59):**
`the script does not yet preserve or link back to Phase 1 provenance hashes from \`global_manifest.json\`.`

**Code does (assembler_prototype.py:131-132, 331-339, test_prg_provenance_bridge.py:93-97):**
Provenance IS preserved — `load_from_global_manifest` extracts provenance, `build_packaged_artifact` includes it, and `production_plan.json` contains `packaged_artifacts` with hashes and provenance.

**Risk:**
The review document is stale on this point. The provenance carry-through was likely added in commit `708c8a8` ("Harden release aggregation workflow") after the review was written. This stale finding could mislead the next reviewer into thinking provenance is still missing.

**Recommended disposition:**
Update the review document to note that provenance carry-through from `global_manifest.json` is now implemented. The Codex-ready task #3 ("Add provenance carry-through") can be marked done.

---

## 2. PROMOTION READINESS CHECKLIST

### Ready

- [x] `load_from_global_manifest` method exists and carries provenance/hash into inventory (assembler_prototype.py:105-135)
- [x] `build_packaged_artifact` preserves provenance into production_plan.json (assembler_prototype.py:331-339)
- [x] Strict mode rejects raw directory scanning (assembler_prototype.py:576-580)
- [x] Provenance bridge test passes: provenance flows global_manifest -> production_plan (test_prg_provenance_bridge.py:93-97)
- [x] Strict mode correctly fails on missing packages in global_manifest (test_prg_provenance_bridge.py:99-117)
- [x] CLI rejection of raw directory scan in strict mode tested (test_prg_provenance_bridge.py:119-144)
- [x] Frontend contract test validates manifest.json and lesson_catalog.json field shapes (test_prg_frontend_contract.py:78-94)

### Not Ready

- [ ] Old default path `content-ko/dist_unified/staging/ko` still hardcoded as default candidate source (P0)
- [ ] Windows dev-machine path `e:\Githubs\lingo\content-ko\dist_unified\staging\ko` in code comment (P1)
- [ ] No `make test-prg` or any test target in Makefile (P1)
- [ ] Contract document (PRG_004) lists "Asset Bundles" as output but code produces `production_plan.json` (P1)
- [ ] Human-handbook PRG artifact map omits `global_manifest.json` from the flow (P0)
- [ ] PRG_002 Mermaid diagram starts from `content-ko` instead of Phase 1 staging (P1)
- [ ] PRG_002 scope column says "All content in content-ko" (P1)
- [ ] Test `test_prg_frontend_contract.py` uses `scan_directory` instead of `load_from_global_manifest` (P1)
- [ ] Contract language (PRG_004) uses "Production Assembler" throughout; code is still a prototype (P1)
- [ ] Runbook block description (D3.3) is stale about provenance carry-through being unimplemented (P2)
- [ ] PRG_005 pilot plan uses "production-ready" language (P2)
- [ ] Artifact map table shows production paths as current reality (P2)
- [ ] Review document 2026-05-02_PRG_PHASE2_REVIEW_DECISION.md is stale on provenance carry-through (P2)

### Needs GPT Review

- Whether `scan_directory` should be removed entirely or moved to a separate planning/analysis module
- Whether `production_plan.json` is the correct final output contract or if asset bundles should be added before promotion
- Whether the PRG_004 contract should be split into "prototype contract" and "future production contract" documents
- Whether `lingo-frontend-web/assets/content/production/` or `release-aggregator/staging/production/` is the correct target output path for Phase 2

---

## 3. SAFE CODEX ACTIONS (can do immediately, no architecture review needed)

### Docs fixes (text-only changes, zero code impact):

1. **docs/human-handbook/08_PRG_ARTIFACT_MAP.md:186-192** — Add `global_manifest.json` to the flow diagram text; show Phase 1 / Phase 2 boundary.

2. **docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:186-192** — Same flow diagram fix as above.

3. **docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:28** — Change "Asset Bundles" to "production_plan.json" (match current code output). Add footnote about asset bundles as future scope.

4. **docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md:25** — Add note: "Current output: staging/prototype_output/. Future target: lingo-frontend-web/assets/content/production/."

5. **docs/tasks/assets/PRG_004_PRODUCTION_ASSEMBLER_CONTRACT.md — top** — Add disclaimer: "Current implementation is assembler_prototype.py (prototype). This spec is aspirational for post-promotion."

6. **docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:13** — Change scope from "All content in content-ko" to "All content in Phase 1 staging output."

7. **docs/tasks/assets/PRG_ARTIFACT_MAP_OVERVIEW.md:19** — Add `global_manifest.json` reference to staging candidate inventory description.

8. **docs/runbooks/release_cut_and_rollback.md:29** — Update the promotion blocker text to reflect that provenance carry-through is implemented; list remaining blockers (default path, Makefile).

9. **docs/tasks/PRG_005_PILOT_PLAN.md:3** — Remove "production-ready"; use "pilot" language.

10. **docs/review/2026-05-02_PRG_PHASE2_REVIEW_DECISION.md:59, 82-83** — Mark provenance carry-through task (#3) as done; note that tasks #1 and #2 are now also implemented in code.

### Makefile fix:

11. **Makefile** — Add:
    ```makefile
    test-prg:
    	python -m unittest discover -s tests/ -p "test_prg*.py" -v
    ```
    Add `test-prg` to `.PHONY` and `help` list.

### Code comment fix:

12. **scripts/prg/assembler_prototype.py:563** — Remove Windows-specific path from comment. Replace with generic repo-relative description.

### Test augmentation:

13. **tests/test_prg_frontend_contract.py** — Add a second test method that exercises `load_from_global_manifest` path and validates the same frontend contract fields (manifest.json and lesson_catalog.json shape). Keep existing `scan_directory` test but label it as planning-mode coverage.

---

## 4. MUST NOT TOUCH (requires architecture review first)

1. **scripts/prg/assembler_prototype.py:503, 566** — Do NOT change the `content-ko/dist_unified/staging/ko` default path until the team confirms what the replacement default should be. Options: (a) remove default entirely and require explicit `--candidate-source`, (b) default to `staging/<version>/global_manifest.json`, or (c) default to a config file path. This is intertwined with how `scripts/release.sh` names staging directories.

2. **scripts/prg/assembler_prototype.py** — Do NOT rename the file from `assembler_prototype.py` to `assembler.py` or remove `scan_directory`. The review decision explicitly says "Do not rename assembler_prototype.py yet."

3. **scripts/prg/assembler_prototype.py:138-179** — Do NOT delete `CandidateInventory.scan_directory`. It is used by planning mode and the frontend contract test. Removal requires consensus that planning-mode scanning is no longer needed.

4. **docs/tasks/assets/PRG_002_STAGING_VS_PRODUCTION_BOUNDARY.md:26-34** — Do NOT redraw the Mermaid diagram without confirming the correct Phase 1 / Phase 2 flow with the team. The diagram implies architectural relationships that affect how staging and PRG interact.

5. **docs/tasks/assets/PRG_004 line 28 "Asset Bundles"** — Do NOT add asset bundle output code to the assembler. The decision of whether PRG should produce asset bundles or whether that belongs to a separate tool requires architecture discussion.

6. **scripts/prg/assembler_prototype.py:527 (default output-dir)** — Do NOT change the output directory default without confirming the target. The current `staging/prototype_output/` is correct for a prototype; changing to `lingo-frontend-web/assets/content/production/` would prematurely couple PRG to frontend deployment.

7. **Makefile** — Do NOT add a `make release-prg` or `make promote` target that replaces `scripts/release.sh` / `scripts/release.py`. The architecture review says PRG should not replace Phase 1.

---

## 5. SUMMARY COUNTS

| Severity | Count | Category |
|----------|-------|----------|
| P0       | 4     | Default path bypasses provenance (D5.1, D7.1); flow diagrams omit global_manifest.json (D2.1, D2.2) |
| P1       | 13    | Contract/code mismatch, stale docs, missing Makefile, test uses scanner path |
| P2       | 7     | Stale review doc finding, "production-ready" wording, output path descriptions |
| P3       | 1     | Minor path reference (D5.3) |

Total: 25 drift items across 7 categories.
