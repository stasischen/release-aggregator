# Model Input Specs

These specs define what to ask each model for during a project review.
They are designed to produce inputs that can be assembled into `PROJECT_REVIEW_PACKET_TEMPLATE.md`.

## Gemini: Repo Mapper

Use Gemini when the task needs broad repo or cross-repo understanding.

```text
Objective:
Scan the repo and produce an architecture map for this project review.

Scope:
- Repo:
- Target domain / feature:
- Related repos, if known:

Inspect:
- Entry points
- Core modules
- Data models and schemas
- Build, validation, and release scripts
- Runtime consumers
- Docs that describe the intended architecture

Output format:
1. Architecture summary, 20-50 lines.
2. Module map table:
   - Module
   - Responsibility
   - Inputs
   - Outputs
   - Key files
3. Data flow:
   - Source
   - Transform
   - Validate
   - Release
   - Consume
4. Dependency and ownership risks:
   - Risk
   - Evidence
   - Files
   - Severity P0-P3
5. Relevant files:
   - 5-15 files with one-line reason each.

Constraints:
- Do not propose the final refactor plan.
- Separate observed facts from inference.
- Call out contradictory docs or stale flows.
```

## DeepSeek: Cleanup Analyst

Use DeepSeek for bulk inventory and consistency checks.

```text
Objective:
Find cleanup and consistency issues that may affect the refactor.

Scope:
- Repo:
- Target directories:
- Known migration goal:

Find:
- Duplicate logic
- Dead code or unused scripts
- Old data structures or legacy adapters
- Naming drift
- TODO / FIXME / XXX
- Docs that conflict with current code
- Files that appear related but are no longer called

Output format:
1. Pain-point inventory:
   - Issue
   - Evidence
   - Files
   - Severity P0-P3
   - Recommended disposition: fix now / defer / delete candidate / needs review
2. Duplicate logic table:
   - File A
   - File B
   - Shared behavior
   - Difference that matters
3. Dead-code candidates:
   - File or symbol
   - Why it appears unused
   - Verification needed before removal
4. Cleanup batch proposal:
   - Safe cleanup
   - Risky cleanup
   - Should not touch

Constraints:
- Do not decide architecture boundaries.
- Do not delete or rewrite code.
- Mark confidence for dead-code claims.
```

## GPT: Architecture Judge

Use GPT after Gemini and DeepSeek have produced the condensed evidence packet.

```text
Objective:
Review the project review packet and decide whether the proposed refactor or migration is architecturally sound.

Input:
- Project goal
- Gemini architecture summary
- DeepSeek pain-point inventory
- Relevant files summary
- Current diff or proposed patch
- Cross-repo boundaries
- Acceptance criteria

Questions:
1. Is the target architecture correct for the stated goal?
2. Are module and repo boundaries respected?
3. What are the P0/P1 risks?
4. What migration order is safest?
5. Which tests or validation gates are mandatory?
6. Which files require direct review before merge?

Output format:
1. Verdict:
   - approve / approve with changes / reject
2. Findings:
   - Severity
   - Risk
   - Evidence
   - Required change
3. Migration plan:
   - Ordered steps
   - Validation per step
   - Rollback condition
4. Review focus:
   - Files to inspect directly
   - Questions to resolve before implementation
5. Implementation constraints:
   - What Codex / DeepSeek may change
   - What must stay out of scope

Constraints:
- Do not request the full repo unless the packet has contradictions or insufficient evidence.
- Keep cleanup-only work separate from behavior or schema changes.
- Prefer a migration path that can be validated one step at a time.
```
