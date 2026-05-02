# Release Aggregator GPT Review Packet

Date: 2026-05-02
Sources: Gemini repo mapper output, `cleanup_inventory.md`, local verification.

## Project Goal

Prepare an architecture decision for the `release-aggregator` refactor.
The target is a reliable release control tower that can aggregate validated `content-pipeline` artifacts, produce a trustworthy global manifest, preserve cross-repo ownership boundaries, and expose working agent / human operational entry points.

## Current Architecture

- `release-aggregator` is the Lingo control tower and release staging repo.
- Docs are centralized under `docs/`, with `docs/index.md` as the human and agent navigation hub.
- Repo ownership is defined in `docs/owners.md`.
- Agent workflow shims live in `.agent/workflows/`.
- The release executable is `scripts/release.py`.
- The release wrapper is `scripts/release.sh`.
- `scripts/release.sh` defaults to sibling repos: `../content-pipeline/dist` and `../core-schema`.
- Release assembly walks the pipeline dist tree, copies `.json`, `.ogg`, and `.mp3` files into a staging directory, hashes each file, and emits `global_manifest.json`.
- Manifest validation shells out to `core-schema/validators/validate.py` against `core-schema/schemas/manifest.schema.json`.
- Quality gating is run through `scripts/check_quality.py`.
- `Makefile` exposes operational targets including `gsd`, `sync-tasks`, `ingest-ko`, `check`, and TLG validation/generation tasks.
- The documented data flow is `lllo` -> `content-ko` -> `content-pipeline` -> `release-aggregator` -> `lingo-frontend-web`.
- Current code stages release artifacts locally; no implemented promotion or rollback automation was found.

## Pain Points

### P0

- `scripts/release.py` blindly copies artifacts from `content-pipeline/dist` without freshness, source manifest, or clean-build checks.
  Evidence: `scripts/release.py:63-103`.
  Risk: stale artifacts can enter `global_manifest.json` and ship to frontend consumers.

- `make gsd` is broken because `Makefile:23-24` calls `scripts/gsd_shim.py`, which does not exist.
  Evidence: `Makefile:23-24`; no `scripts/gsd_shim.py` found.
  Risk: documented orchestration entry point fails.

### P1

- Release and package versions are hardcoded in `scripts/release.py`.
  Evidence: `scripts/release.py:49`, `scripts/release.py:89`, `scripts/release.py:95-96`.
  Risk: release manifest cannot prove actual release, pipeline, or schema provenance.

- `scripts/release.sh` accepts `--version` but does not pass it to `scripts/release.py`.
  Evidence: `scripts/release.sh:33-35`, `scripts/release.sh:83-88`.
  Risk: staged directory may be versioned, but manifest content is not.

- `scripts/release.sh` hardcodes quality scope to `A1`.
  Evidence: `scripts/release.sh:79-81`.
  Risk: non-A1 releases can pass the wrong quality gates.

- Docs claim promotion / rollback ownership, but implementation only stages artifacts.
  Evidence: `docs/owners.md`, `docs/runbooks/release_cut_and_rollback.md`, `scripts/release.py`, `scripts/release.sh`.
  Risk: architecture contract is broader than implemented behavior.

- `lllo` role is inconsistent between docs.
  Evidence: `GEMINI.md` describes it as a viewer; `docs/owners.md` describes it as writer/source input.
  Risk: unclear upstream/downstream ownership.

### P2

- Duplicate or overlapping validation / scaffold tools exist.
  Evidence: `scripts/mockup_check.py`, `scripts/validate_mockup_fixture.py`, `scripts/scaffold_unit_blueprint.py`, `scripts/generate_multilingual_scaffold.py`, `scripts/tlg005_generate_unit_v1.py`.
  Risk: teams may use the wrong schema-era tool.

- `scripts/prg/` contains prototype release assembly logic not integrated into Makefile.
  Evidence: `scripts/prg/assembler_prototype.py`, `scripts/prg/seed_release_manifest.py`.
  Risk: unclear whether this is future release architecture or dead prototype code.

- `tools/content_candidate_generation/bin/` overlaps with top-level `scripts/`.
  Evidence: cleanup inventory duplicate table.
  Risk: unclear ownership and schema version drift.

### Corrected Finding

DeepSeek reported `.agent/workflows/*.md` as missing. Local verification shows this is false:

- `.agent/workflows/start.md`
- `.agent/workflows/wrap.md`
- `.agent/workflows/gsd.md`
- `.agent/workflows/handoff.md`

Do not treat `.agent/workflows` existence as a P0 unless link targets are later proven broken from rendered docs.

## Relevant Files

- `scripts/release.py`: core aggregation, hashing, manifest generation, schema validation.
- `scripts/release.sh`: release wrapper, output directory selection, quality gate invocation.
- `Makefile`: public dev / CI command surface; currently references missing `gsd_shim.py`.
- `docs/owners.md`: cross-repo responsibility contract.
- `docs/runbooks/release_cut_and_rollback.md`: documented release / rollback behavior.
- `GEMINI.md`: project context and repo role descriptions.
- `.agent/workflows/start.md`: agent startup shim.
- `.agent/workflows/gsd.md`: local GSD workflow shim.
- `scripts/prg/assembler_prototype.py`: possible future release assembly prototype.
- `scripts/prg/seed_release_manifest.py`: possible manifest seeding prototype.
- `cleanup_inventory.md`: DeepSeek cleanup and consistency inventory.

## Cross-Repo Boundaries

- Source / authoring: `lllo`, `content-ko`.
- Schema / contract: `core-schema`.
- Build / validation pipeline: `content-pipeline`.
- Release staging / control tower: `release-aggregator`.
- Runtime consumer: `lingo-frontend-web`.

## Decision Needed

1. Should immediate refactor focus on hardening `scripts/release.py` and `scripts/release.sh`, or should the PRG prototype path replace them?
2. Should `release-aggregator` implement promotion / rollback, or should docs narrow its ownership to staging only?
3. What is the correct manifest provenance contract: release version, package version, pipeline version, schema version, source repo, source commit, build timestamp?
4. Should artifact freshness be enforced by requiring upstream build metadata, deleting output before copy, verifying against a source manifest, or all of the above?
5. Should cross-repo sibling path assumptions remain documented convention, or move to explicit repo config / environment variables?
6. Which cleanup candidates are safe before architecture migration, and which should wait?

## Known Risks

- Risk: stale artifacts ship.
  Evidence: `release.py` walks all files in dist and copies them.
  Proposed mitigation: require a source build manifest, clean staging before copy, and validate package list against expected build metadata.

- Risk: manifest provenance is not trustworthy.
  Evidence: hardcoded release, package, pipeline, and schema versions.
  Proposed mitigation: thread `--version` into `release.py`; read pipeline and schema versions from metadata or explicit CLI args.

- Risk: docs promise rollback that code cannot execute.
  Evidence: owners and rollback runbook vs. staging-only scripts.
  Proposed mitigation: choose one: implement rollback / promotion workflow, or revise ownership docs to staging-only.

- Risk: command surface is broken.
  Evidence: `make gsd` calls missing `scripts/gsd_shim.py`.
  Proposed mitigation: either implement the shim or remove / redirect the Makefile target to existing `.agent/workflows/gsd.md` workflow.

## Acceptance Criteria

- `make gsd` either works or is intentionally removed from help and `.PHONY`.
- `scripts/release.sh --version <tag>` results in manifest version matching `<tag>`.
- Release provenance contains non-hardcoded pipeline and schema version values.
- Release assembly has a staleness / cleanliness guard.
- Quality gate scope is configurable and not always `A1`.
- Docs and code agree on promotion / rollback responsibility.
- Cross-repo path configuration is documented and testable.

## Out Of Scope

- Editing archived docs under `docs/archive/universal/**`.
- Refactoring active TLG pipeline scripts unless directly required by release hardening.
- Consolidating `tools/content_candidate_generation/bin/` before GPT decides ownership.
- Replacing frontend runtime intake behavior.

## Requested GPT Output

1. Verdict: approve / approve with changes / reject for starting a release hardening refactor.
2. Severity-ordered architecture findings.
3. Migration plan with step order and validation after each step.
4. Decision on `scripts/release.py` versus `scripts/prg/` prototype direction.
5. Decision on promotion / rollback ownership.
6. Required tests or validation commands before merge.
7. Cleanup items that can proceed now versus must wait.

## Prompt To GPT

```text
You are reviewing the Lingo release-aggregator architecture. Use the review packet above as the source of truth.

Please judge whether the next refactor should harden the current release path (`scripts/release.py` + `scripts/release.sh`) or pivot toward the prototype PRG release path under `scripts/prg/`.

Return:
1. Verdict: approve / approve with changes / reject.
2. Findings ordered by severity.
3. A migration plan that can be implemented in small Codex tasks.
4. Required validation gates.
5. Which cleanup items are safe now.
6. Which issues require direct file inspection before a final decision.

Constraints:
- Do not request the full repo unless evidence is contradictory or insufficient.
- Keep release behavior changes separate from cleanup-only changes.
- Preserve cross-repo ownership boundaries.
- Treat stale artifact leakage, manifest provenance, and rollback ownership as the highest-risk areas.
```
