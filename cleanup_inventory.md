# release-aggregator Cleanup & Consistency Inventory

Generated: 2026-05-02 | Analyst: DeepSeek | For: GPT architecture review packet assembly

---

## 1. Pain-Point Inventory

### P0

**P0-1: `scripts/release.py` blindly aggregates stale artifacts with no freshness check**

- Evidence: `scripts/release.py` lines 63-103 walk `pipeline_dist` and copy all `.json`, `.ogg`, `.mp3` files to staging. No timestamp check, no `generated_at` comparison against manifest, no checksum verification of source vs. staged. If `content-pipeline/dist/` contains artifacts from a prior failed run, they get aggregated silently.
- Files: `scripts/release.py:63-103`
- Why it matters: A stale artifact entering the release manifest can ship outdated content to production. The aggregator is the last gate before frontend intake; it currently has no staleness guard.
- Recommended disposition: Fix now

**P0-2: `.agent/workflows/` directory is referenced extensively but contains no populated `.md` files**

- Evidence: `GEMINI.md:18` says agents must read `.agent/workflows/start.md`. `docs/index.md:39` links to `../../.agent/workflows/start.md`. `.planning/codebase/ARCHITECTURE.md:18` references `.agent/workflows/start.md`. A glob for `.agent/**/*.md` under this repo returns 0 files. The `.planning/codebase/STACK.md` also references `.agent/workflows/start.md` and `.agent/workflows/wrap.md`. `docs/runbooks/codex_antigravity_orchestration.md:30` references `.agent/workflows/gsd.md`.
- Files: `GEMINI.md:18-21`, `docs/index.md:39`, `.planning/codebase/STACK.md:20`, `.planning/codebase/ARCHITECTURE.md:18`, `docs/runbooks/codex_antigravity_orchestration.md:30`
- Why it matters: Agents following startup protocol will hit dead links. The entire agent onboarding chain is broken.
- Recommended disposition: Fix now (populate or remove references)

**P0-3: `scripts/gsd_shim.py` referenced in Makefile does not exist**

- Evidence: `Makefile:24` calls `$(PYTHON) $(SCRIPTS)/gsd_shim.py` for `make gsd`. The file does not exist on disk. Grep across the entire repo finds no `gsd_shim.py` file, only the Makefile reference.
- Files: `Makefile:23-24`
- Why it matters: `make gsd` is the primary orchestration entry point per the Makefile help text ("Run the GSD protocol shim"). It is broken out of the box.
- Recommended disposition: Fix now

### P1

**P1-1: `scripts/release.py` has hardcoded MVP version constants**

- Evidence: `scripts/release.py:49` hardcodes `"version": "1.0.0"` for the release version. Line 89 hardcodes `"version": "1.0.0"` for each package entry. Line 95 hardcodes `"pipeline_version": "v1.0.0-alpha"` with comment "# MVP constant". Line 96 hardcodes `"schema_version": "1.0.0"` with comment "# MVP constant".
- Files: `scripts/release.py:49,89,95-96`
- Why it matters: Schema version should be read from `core-schema` (which is already passed as `--core-schema` arg). Pipeline version should be read from pipeline build metadata. Package versions should come from the artifact source, not be hardcoded. Version drift between manifest and reality is inevitable.
- Recommended disposition: Fix now

**P1-2: Multiple scripts hardcode `f:/Githubs/` or `e:\Githubs\` Windows paths**

- Evidence: `scripts/audit_phrases.py:5` hardcodes `Path("f:/Githubs/lingo/content-ko")`. `scripts/inject_phrases.py:5` hardcodes `Path("f:/Githubs/lingo/content-ko")`. `scratch/find_ids.py:10` hardcodes `r'e:\Githubs\lingo\content-ko\...'`. `scripts/prg/assembler_prototype.py:467` references `e:\Githubs\lingo\content-ko\dist_unified\staging\ko`.
- Files: `scripts/audit_phrases.py:5`, `scripts/inject_phrases.py:5`, `scratch/find_ids.py:10`, `scripts/prg/assembler_prototype.py:467`
- Why it matters: These scripts are non-portable. They will fail on any machine that doesn't have the exact Windows drive letter and path structure.
- Recommended disposition: Fix now (use relative path resolution like other scripts do)

**P1-3: `scripts/migrate_universal_docs_to_control_tower.sh` and `scripts/ops/start_lingo_control_tower.sh` hardcode user-local macOS paths**

- Evidence: `scripts/migrate_universal_docs_to_control_tower.sh:14` hardcodes `SRC="/Users/ywchen/Dev/Lingourmet_universal"`. Line 15 hardcodes `DST="/Users/ywchen/Dev/lingo/release-aggregator/docs/archive/universal"`. `scripts/ops/start_lingo_control_tower.sh:5` hardcodes a layout file under `/Users/ywchen/Dev/lingo/...`.
- Files: `scripts/migrate_universal_docs_to_control_tower.sh:14-15`, `scripts/ops/start_lingo_control_tower.sh:5`
- Why it matters: These are non-portable. The migration script should be parameterized or moved to a historic archive since it appears to already have been executed (universal docs already exist under `docs/archive/universal/`).
- Recommended disposition: Delete candidate (migration script) / fix now (zellij layout)

**P1-4: `lllo` role description contradicts between `GEMINI.md` and `docs/owners.md`**

- Evidence: `GEMINI.md:11` says "lllo: LLLO Viewer，用於預覽課程內容" (a viewer/preview tool). `docs/owners.md:17` says "lllo is writer/source input" (an authoring tool). These are incompatible descriptions: a viewer consumes content; a writer produces it.
- Files: `GEMINI.md:11`, `docs/owners.md:17-19`
- Why it matters: Agents reading these docs will get conflicting guidance on whether lllo is upstream (authoritative source) or downstream (preview consumer). The `docs/owners.md:19` rule "No direct release from lllo" only makes sense if lllo is a source, not a viewer.
- Recommended disposition: Fix now (align to owners.md: lllo is writer/source input)

**P1-5: `docs/runbooks/release_cut_and_rollback.md` claims release-aggregator owns promotion/rollback, but code only stages artifacts**

- Evidence: `docs/owners.md:12` assigns release-aggregator "release promotion/rollback" responsibility. `docs/runbooks/release_cut_and_rollback.md:28-30` describes an emergency rollback procedure ("Revert staged global_manifest.json..."). However, `scripts/release.py` only copies artifacts and generates `global_manifest.json` in a staging directory. There is no promotion script (pushing to frontend), no rollback script (reverting), and no release versioning mechanism in code. The `scripts/release.sh:69-71` wrapper only creates a versioned staging directory but does not promote.
- Files: `docs/owners.md:12`, `docs/runbooks/release_cut_and_rollback.md:28-30`, `scripts/release.py`, `scripts/release.sh`
- Why it matters: The documented capability does not exist in code. The handoff to frontend (`release-aggregator -> lingo-frontend-web`) has no implementation.
- Recommended disposition: Needs GPT review (gap between architecture docs and implementation)

### P2

**P2-1: Duplicate mockup validation scripts with overlapping checks**

- Evidence: `scripts/mockup_check.py` (626 lines) is a comprehensive checker with modular contract validation, CMOD checks, pedagogy metadata, anchor validation. `scripts/validate_mockup_fixture.py` (112 lines) is a lightweight checker with mixed-script typo scans, alias checks, bilingual list length validation. Both share the identical `MIXED_PATTERNS` regex list (e.g., `7時`, `二\s*잔`, `하端`, `外部\s*음식`). Both check for `answers_ko` legacy alias.
- Files: `scripts/mockup_check.py:14-19` (MIXED_PATTERNS), `scripts/validate_mockup_fixture.py:26-31` (MIXED_PATTERNS), `scripts/mockup_check.py:256` (answers_ko check), `scripts/validate_mockup_fixture.py:81-84` (answers_ko check)
- Why it matters: Duplicated logic risks divergence. The lightweight script validates a single hardcoded fixture path (`a1_u04_unit_blueprint_v0.json`) while the full checker accepts arbitrary files.
- Recommended disposition: Delete candidate for lightweight script (consolidate into mockup_check.py)

**P2-2: Two unit scaffold generators with version drift**

- Evidence: `scripts/scaffold_unit_blueprint.py` generates `unit_blueprint_v0` with 15 hardcoded node blocks and ~56 TODO placeholders. `scripts/generate_multilingual_scaffold.py` generates from a profile + template registry, supporting locale/language overrides. The v0 scaffold has extensive TODO placeholders rendering it a template, not usable output. Neither is referenced in the Makefile.
- Files: `scripts/scaffold_unit_blueprint.py`, `scripts/generate_multilingual_scaffold.py`
- Why it matters: Two generators producing incompatible schema versions. No clear documentation on when to use which. The v0 generator creates v0 output but the TLG-005/006 pipeline expects v1 format.
- Recommended disposition: Delete candidate for v0 scaffold (scaffold_unit_blueprint.py) or mark as legacy

**P2-3: `scripts/prg/` contains prototype code with hardcoded paths and no Makefile integration**

- Evidence: `scripts/prg/assembler_prototype.py` references `e:\Githubs\lingo\...` (line 467), defaults to `content-ko/dist_unified/staging/ko` (line 418) which assumes a specific sibling repo structure. `scripts/prg/seed_release_manifest.py` defaults to `lingo-frontend-web/assets/content/production/manifest.json` (line 191) assuming a specific frontend sibling. Neither is wired into the Makefile. Both are marked "prototype" in their filenames.
- Files: `scripts/prg/assembler_prototype.py`, `scripts/prg/seed_release_manifest.py`
- Why it matters: Prototype code with hardcoded cross-repo paths that uses sibling-directory assumptions. If promoted to production, these need parameterization and integration into the Makefile.
- Recommended disposition: Needs GPT review (are these the future release pipeline or dead prototypes?)

**P2-4: `tools/content_candidate_generation/bin/` contains 8 Python scripts that duplicate release/scaffold logic**

- Evidence: `tools/content_candidate_generation/bin/` includes `normalize_candidates.py`, `normalize_agent_candidates.py`, `scaffold_unit.py`, `export_review_bundle.py`, `export_backlog_seed.py`, `export_catalog_draft.py`, `qa_candidates.py`, `run_api_batch.py`, `mockup_check.py`. Some of these overlap with scripts/ functionality (e.g., another `scaffold_unit.py`, another `mockup_check.py`, normalization that overlaps with `tlg005_normalize_blueprint_v1.py`).
- Files: `tools/content_candidate_generation/bin/scaffold_unit.py`, `tools/content_candidate_generation/bin/mockup_check.py`, `tools/content_candidate_generation/bin/normalize_candidates.py`, `tools/content_candidate_generation/bin/normalize_agent_candidates.py`
- Why it matters: Multiple normalization and scaffold scripts scattered across directories without clear ownership. Risk of using wrong tool for a given schema version.
- Recommended disposition: Needs GPT review

**P2-5: `release.sh` hardcodes quality gate scope to A1**

- Evidence: `scripts/release.sh:81` always runs `check_quality.py --scope A1` regardless of what content is being released. The `--scope` is not parameterized through the shell script.
- Files: `scripts/release.sh:81`
- Why it matters: If releasing B1/B2 content, A1 quality gates are run instead. False confidence in quality.
- Recommended disposition: Fix now

### P3

**P3-1: `.gemini/commands/gsd/new-project.md.bak` is a stale backup file**

- Evidence: File has `.bak` extension indicating it's a backup. Content appears to be a GSD new-project command definition.
- Files: `.gemini/commands/gsd/new-project.md.bak`
- Why it matters: Stale backup in the command definitions directory. Could confuse agent command discovery.
- Recommended disposition: Delete candidate

**P3-2: `scratch/find_ids.py` is a one-off script with hardcoded Windows path**

- Evidence: `scratch/find_ids.py:10` hardcodes `r'e:\Githubs\lingo\content-ko\content\core\learning_library\example_sentence'`. The file is in `scratch/` directory suggesting it was temporary/exploratory.
- Files: `scratch/find_ids.py`
- Why it matters: Scratch scripts with hardcoded paths shouldn't remain in the repo.
- Recommended disposition: Delete candidate

**P3-3: `scripts/ops/audit_mixed_script.py` and `scripts/ops/verify_reports.py` have no Makefile targets**

- Evidence: Neither script appears in the Makefile. Both are in `scripts/ops/` subdirectory suggesting operational/ad-hoc use. `audit_mixed_script.py` assumes sibling repo layout (`current_dir.parents[1]`).
- Files: `scripts/ops/audit_mixed_script.py`, `scripts/ops/verify_reports.py`
- Why it matters: Unclear if these are actively used or abandoned. Without documentation or Makefile integration, they risk bitrot.
- Recommended disposition: Needs GPT review or add to Makefile if still used

**P3-4: `scripts/migrate_universal_docs_to_control_tower.sh` appears to be a one-time migration already executed**

- Evidence: The target directory `docs/archive/universal/` already exists and is populated. The script hardcodes source/destination paths specific to `ywchen`'s machine. Worklog `docs/worklogs/2026-02-15.md:32` confirms the migration was done.
- Files: `scripts/migrate_universal_docs_to_control_tower.sh`, `docs/worklogs/2026-02-15.md:32`
- Why it matters: One-time migration script is dead code after execution.
- Recommended disposition: Delete candidate

**P3-5: Multiple TODO placeholders in `scaffold_unit_blueprint.py`**

- Evidence: `scripts/scaffold_unit_blueprint.py` contains approximately 56 TODO strings across lines 33-383. Every node in the generated scaffold has TODO placeholders for content.
- Files: `scripts/scaffold_unit_blueprint.py` (56+ TODO occurrences)
- Why it matters: If this scaffold is meant to be used as a starting template, having TODOs is acceptable. But the volume suggests the scaffold is not being actively used as a template — it's more of a schema illustration.
- Recommended disposition: Defer (acceptable if this is intentionally a template generator)

---

## 2. Duplicate Logic Table

| File A | File B | Shared behavior | Difference that matters | Suggested owner |
|:---|:---|:---|:---|:---|
| `scripts/mockup_check.py` (626 lines) | `scripts/validate_mockup_fixture.py` (112 lines) | Mixed-script pattern scanning (identical MIXED_PATTERNS list), answers_ko legacy alias detection, bilingual list length checks | mockup_check.py is comprehensive (CMOD contracts, anchors, completion rules, review policies). validate_mockup_fixture.py validates a single hardcoded fixture path. | Consolidate into mockup_check.py; delete validate_mockup_fixture.py |
| `scripts/scaffold_unit_blueprint.py` | `scripts/generate_multilingual_scaffold.py` | Both generate unit blueprint JSON scaffold with node sequences (L1-L3, D1, G1-G2, P1-P6, R1) | scaffold produces v0 schema with hardcoded TODO templates. generate_multilingual uses profile + template registry, supports locale overrides, produces v1-compatible format. | Delete scaffold_unit_blueprint.py or flag as legacy v0 template |
| `scripts/tlg005_generate_unit_v1.py` | `scripts/scaffold_unit_blueprint.py` | Both generate unit blueprints with learning role sequences | tlg005 uses external pattern library, lang profiles, and registration system. scaffold_unit_blueprint hardcodes everything inline. tlg005 produces v1; scaffold produces v0. | Scaffold is superseded by TLG-005 |
| `scripts/prg/assembler_prototype.py` | `scripts/prg/seed_release_manifest.py` | Both handle release manifest creation/assembly with candidate inventory, lesson catalog, unit assignment | seed generates initial manifest from legacy assets. assembler consumes a manifest and assembles a production plan from candidates. Different pipeline stages. | Keep both if prototype becomes production; otherwise archive both |
| `tools/content_candidate_generation/bin/normalize_candidates.py` | `scripts/tlg005_normalize_blueprint_v1.py` | Both normalize content/blueprint payloads (setdefault for missing fields, field migration) | normalize_candidates likely works on candidate-level data; tlg005_normalize works on unit-level blueprints. Different schemas but overlapping normalization pattern. | Needs GPT review |
| `tools/content_candidate_generation/bin/mockup_check.py` | `scripts/mockup_check.py` | Both validate mockup/fixture files | The tools/ version is part of the content_candidate_generation toolchain; scripts/ version is a standalone checker. | Needs GPT review for consolidation |
| `scripts/check_quality.py` | `scripts/ops/verify_reports.py` | Both scan for Korean/Chinese mixed script, placeholder detection | check_quality.py is comprehensive (dictionary, POS, LLLO, atom integrity). verify_reports.py is focused on report files only. | OK to keep both (different scope) |

---

## 3. Dead-Code Candidates

| File or symbol | Why it appears unused | Confidence | Verification needed before removal |
|:---|:---|:---|:---|
| `scripts/gsd_shim.py` (referenced but missing) | Makefile:24 references it; grep finds no file | High | Confirm no other build system references it |
| `scripts/migrate_universal_docs_to_control_tower.sh` | One-time migration; target already exists; worklog confirms completed 2026-02-15 | High | Verify all docs are in archive; check no automation calls it |
| `scratch/find_ids.py` | In `scratch/` directory; hardcoded Windows path; appears to be ad-hoc debugging script | High | Check if referenced by any workflow doc |
| `scripts/audit_phrases.py` | Hardcoded `f:/Githubs/` path; no Makefile target; no imports from other scripts | Medium | Verify it's not called manually as part of content audit workflow |
| `scripts/inject_phrases.py` | Hardcoded `f:/Githubs/` path; no Makefile target; appears to be content injection utility | Medium | Verify it's not used in content-ko ingestion pipeline |
| `.gemini/commands/gsd/new-project.md.bak` | Backup file with `.bak` extension | High | Confirm the active `new-project.md` exists and is functional |
| `scripts/scaffold_unit_blueprint.py` | Produces v0 schema; no Makefile target; superseded by TLG-005 v1 pipeline | Medium | Verify no docs reference it as the recommended scaffold tool |
| `scripts/validate_mockup_fixture.py` | Validates single hardcoded path; superseded by more comprehensive `mockup_check.py` | Medium | Verify the hardcoded fixture path is not used in CI |
| `scripts/prg/assembler_prototype.py` | "Prototype" in name; hardcoded Windows path reference; not in Makefile | Low (may be future pipeline) | Confirm with architecture plan whether PRG is the future release pipeline |

---

## 4. Stale or Contradictory Docs

| Doc file | Claim | Contradicting code or doc | Severity | Recommended disposition |
|:---|:---|:---|:---|:---|
| `GEMINI.md:11` | "lllo: LLLO Viewer，用於預覽課程內容" | `docs/owners.md:17` says "lllo is writer/source input". `docs/owners.md:19` says "No direct release from lllo" (implies lllo produces content, not just views it) | P1 | Fix GEMINI.md to match owners.md |
| `docs/owners.md:12` | release-aggregator owns "release promotion/rollback" | `scripts/release.py` only stages artifacts to a directory; has no promotion (push-to-frontend) or rollback (revert-to-previous) logic | P1 | Needs GPT review — either add promotion/rollback code or narrow the ownership claim |
| `docs/runbooks/release_cut_and_rollback.md:9-10` | Command reference: `./scripts/release.sh --version vX.Y.Z` | `scripts/release.sh` supports `--version` flag (line 33-35) but the release.sh default behavior runs `check_quality.py --scope A1` regardless of version tag | P2 | Fix to pass scope from version context or parameterize |
| `docs/runbooks/release_cut_and_rollback.md:29` | "Revert staged global_manifest.json..." as emergency rollback | No script implements this. Rollback is described as a manual git operation but has no automation, verification, or smoke-test step | P2 | Needs GPT review |
| `GEMINI.md:18` | "啟動後必須先讀取 release-aggregator/.agent/workflows/start.md" | `.agent/workflows/start.md` and `wrap.md` are referenced but a glob for `.agent/**/*.md` returns 0 files. The files may exist but were not returned by the glob; the directory structure is uncertain. | P0 | Verify and fix |
| `docs/index.md:39` | Links to `../../.agent/workflows/start.md` as "入口指令 shim" | Same as above — the link target may not exist | P0 | Verify and fix |
| `docs/runbooks/agent_reference_order.md:23` | Hardcoded session start prompt containing `/Users/ywchen/Dev/lingo/release-aggregator/docs/**` | This is a user-local path that won't work for other developers | P3 | Replace with relative or variable path |
| `docs/runbooks/release_cut_and_rollback.md:14` | Default `pipeline-dist` is `../content-pipeline/dist` | `scripts/release.sh:7` has same default. This works with sibling repo layout but breaks if repos are cloned elsewhere | P2 | Needs GPT review |
| `docs/human-handbook/03_STAGE_CHECKLISTS.md:77` | References `./scripts/release.sh` with `--version` flag | The `--version` flag is parsed but not used for version stamping in `release.py` (which hardcodes "1.0.0") | P2 | Fix to thread version through to release.py |

---

## 5. Hardcoded Config Inventory

| File | Value or path | Should become env/config/build metadata? | Risk if left as-is |
|:---|:---|:---|:---|
| `scripts/release.py:49` | `"version": "1.0.0"` | Yes — should come from `--version` arg or pipeline metadata | All releases stamped with same version |
| `scripts/release.py:89` | `"version": "1.0.0"` per package | Yes — should come from artifact metadata | Package version drift undetected |
| `scripts/release.py:95` | `"pipeline_version": "v1.0.0-alpha"` (MVP) | Yes — should come from pipeline build metadata | Cannot trace which pipeline version produced an artifact |
| `scripts/release.py:96` | `"schema_version": "1.0.0"` (MVP) | Yes — should come from core-schema | Manifest validation uses wrong schema version if core-schema updates |
| `scripts/release.sh:81` | `--scope A1` (hardcoded) | Yes — should be parameterized from version or config | Wrong quality gates run for non-A1 content |
| `scripts/release.sh:7` | `../content-pipeline/dist` (relative sibling) | Could be env var PIPELINE_DIST (already supports this) | Low — env var override exists |
| `scripts/audit_phrases.py:5` | `Path("f:/Githubs/lingo/content-ko")` | Yes — should use AGGREGATOR_ROOT.parent pattern | Non-portable; breaks on non-Windows or different directory layouts |
| `scripts/inject_phrases.py:5` | `Path("f:/Githubs/lingo/content-ko")` | Yes — should use AGGREGATOR_ROOT.parent pattern | Non-portable |
| `scratch/find_ids.py:10` | `r'e:\Githubs\lingo\content-ko\...'` | Should be deleted (scratch script) | Non-portable |
| `scripts/migrate_universal_docs_to_control_tower.sh:14-15` | `/Users/ywchen/Dev/...` paths | Should be deleted (one-time migration done) | Non-portable |
| `scripts/ops/start_lingo_control_tower.sh:5` | `/Users/ywchen/Dev/lingo/...` | Yes — should be relative to repo root | Non-portable |
| `scripts/ingest_ko.py:10-11` | `DEV_ROOT / "lllo"`, `DEV_ROOT / "content-ko"` | Acceptable as convention, but should be documented | Low if sibling layout is guaranteed |
| `scripts/check_quality.py:13-14` | `DEV_ROOT / "lllo"`, `DEV_ROOT / "content-ko"` | Acceptable as convention | Low if sibling layout is guaranteed |
| `scripts/prg/assembler_prototype.py:418` | `content-ko/dist_unified/staging/ko` | Yes — should be parameterized | Path may not exist; prototype only |
| `scripts/prg/seed_release_manifest.py:191` | `lingo-frontend-web/assets/content/production/manifest.json` | Yes — should be parameterized | Assumes specific frontend sibling path |
| `scripts/release.py:118-119` | `core-schema/validators/validate.py`, `core-schema/schemas/manifest.schema.json` | Acceptable — derived from `--core-schema` arg | Low |
| `scripts/viewer/sync_core_i18n_viewer_data.py:15-20` | Frontend intake package paths (REQUIRED dict) | Could be configurable | Low if these paths are stable |
| `scripts/tlg_gemini_emit_prompts.py:43` | `docs/tasks/prompts/gemini` (relative) | Acceptable | Low |
| `scripts/tlg_gemini_run_unit_demo.py:25-26` | `docs/tasks/pattern_library/...`, `docs/tasks/pattern_library/...` (relative to REPO_ROOT) | Acceptable | Low |
| `scripts/tlg005_generate_unit_v1.py:89` | `docs/tasks/lang_profiles/{target_lang}_generation_profile_v1.json` | Acceptable as convention | Low |
| `scripts/validate_mockup_fixture.py:21-23` | `docs/tasks/mockups/a1_u04_unit_blueprint_v0.json`, `unit_blueprint_v0.schema.json` (hardcoded) | Should be parameterized | Validates only one fixture |

---

## 6. Cleanup Batch Proposal

### Safe cleanup now (low risk, high confidence)

1. **Delete `scratch/find_ids.py`** — one-off debug script with hardcoded Windows path
2. **Delete `.gemini/commands/gsd/new-project.md.bak`** — stale backup
3. **Delete `scripts/migrate_universal_docs_to_control_tower.sh`** — one-time migration already executed (confirmed in worklogs)
4. **Fix `GEMINI.md:11`** — change lllo description from "LLLO Viewer，用於預覽課程內容" to "LLLO Writer/Source Input，用於編寫課程內容" to match owners.md
5. **Remove `make gsd` from Makefile** or create the missing `scripts/gsd_shim.py` — currently a broken entry point
6. **Fix `scripts/release.sh:81`** to accept `--scope` parameter instead of hardcoding A1
7. **Replace hardcoded `f:/Githubs/` paths** in `scripts/audit_phrases.py` and `scripts/inject_phrases.py` with relative resolution (same pattern as `scripts/check_quality.py`)
8. **Fix `scripts/ops/start_lingo_control_tower.sh:5`** to use relative path from repo root instead of `/Users/ywchen/Dev/lingo/`
9. **Delete `scripts/validate_mockup_fixture.py`** — superseded by `scripts/mockup_check.py`; duplicated MIXED_PATTERNS logic
10. **Delete `scripts/scaffold_unit_blueprint.py`** or mark as `_legacy` — produces v0 schema; superseded by TLG-005 v1 pipeline; 56 TODO placeholders
11. **Fix `scripts/release.py`** — replace hardcoded "1.0.0" version, "v1.0.0-alpha" pipeline_version, and "1.0.0" schema_version with values from CLI args or source metadata
12. **Fix hardcoded path in `scripts/audit_phrases.py:5` and `scripts/inject_phrases.py:5`**

### Needs GPT architecture review (medium risk, architectural implications)

1. **`scripts/prg/assembler_prototype.py` and `scripts/prg/seed_release_manifest.py`** — are these the future release pipeline? Should they replace `scripts/release.py`? They handle manifest-driven assembly, candidate inventory, and production plans, which is more sophisticated than the current `release.py`.
2. **`tools/content_candidate_generation/bin/`** — is this a separate toolchain or should it be consolidated into `scripts/`? Contains 8 scripts with overlapping normalization, scaffold, and mockup validation.
3. **Release promotion/rollback gap** — `docs/owners.md` claims release-aggregator owns promotion/rollback but no code implements it. GPT should decide: add promotion code, narrow ownership docs, or designate a different repo for promotion.
4. **`.agent/workflows/` directory** — docs extensively reference it but files may be missing or empty. GPT should decide: populate with actual workflow files, remove references from docs, or restructure the agent entry point.
5. **Schema version drift** — coexistence of `unit_blueprint_v0`, `v0.1`, `v1`, `frontend_unit_adapter_v0`, `v1`. Which is canonical? Should v0 support be dropped?
6. **Cross-repo path convention** — multiple scripts assume `AGGREGATOR_ROOT.parent / "content-ko"` sibling layout. Should this be formalized as a `DEV_ROOT` env var or repo config?

### Defer (non-critical, no immediate risk)

1. **`scripts/scaffold_unit_blueprint.py` TODO placeholders** — acceptable if this is intentionally a template generator
2. **`docs/runbooks/agent_reference_order.md:23` hardcoded user path** — only affects copy-paste workflow; fix when addressing agent entry point restructuring
3. **`scripts/ops/audit_mixed_script.py` and `scripts/ops/verify_reports.py`** — add to Makefile if still used; otherwise archive
4. **`scripts/audit_phrases.py` and `scripts/inject_phrases.py`** — after fixing hardcoded paths, determine if these should have Makefile targets

### Do not touch

1. **`docs/archive/universal/**`** — marked as reference-only by `agent_reference_order.md:20`. Do not modify archived docs.
2. **`.gemini/get-shit-done/**`** — GSD framework templates and references; third-party framework files
3. **`tools/modular-viewer/` and `tools/core_i18n_viewer/`** — actively used viewer tools with their own data dependencies
4. **`scripts/tlg*` scripts** — active TLG pipeline; all appear to be in active use with consistent naming conventions
5. **`scripts/pattern_library_codec.py`** — core library used by multiple TLG scripts; well-structured
6. **`scripts/check_quality.py`** — comprehensive quality gate; wired into Makefile
7. **`scripts/ingest_ko.py`** — wired into Makefile as `make ingest-ko`
8. **`scripts/sync_task_index.py`** — wired into Makefile as `make sync-tasks`
9. **`scripts/generate_library_manifest.py` and `scripts/watch_library_manifest.py`** — active manifest generation pipeline for modular viewer
