# Project Review Packet Template

Use this packet when asking GPT to judge a refactor, migration, or architecture decision.
Keep it short enough to review directly, but concrete enough that the decision is auditable.

```text
Project goal:
- What are we trying to change?
- What should the system look like after this work?
- Which repo or domain owns the target state?

Current architecture:
- 20-50 lines from Gemini.
- Include module boundaries, entry points, data flow, persistence format, release path, and runtime consumers.
- State what is known versus inferred.

Pain points:
- P0:
- P1:
- P2:
- P3:

Relevant files:
- path/to/file: why it matters, current responsibility, risk level.
- path/to/file: why it matters, current responsibility, risk level.

Current diff or proposed patch:
- Link or paste the smallest useful diff.
- Separate behavior changes from cleanup changes.

Cross-repo boundaries:
- Source repo:
- Schema / contract repo:
- Build / pipeline repo:
- Release repo:
- Runtime consumer repo:

Decision needed:
- Should this refactor proceed?
- Are the proposed boundaries correct?
- What is the safest migration order?
- What must be tested before merge?

Known risks:
- Risk:
  Evidence:
  Proposed mitigation:

Acceptance criteria:
- Functional:
- Schema / contract:
- Validation command:
- Rollback condition:

Out of scope:
- Items deliberately not being solved in this round.

Requested GPT output:
- Verdict: approve / approve with changes / reject.
- Architecture risks, severity ordered.
- Migration plan, step ordered.
- Required tests or validation.
- Files that need closer review.
```

## Packet Rules

- Keep relevant files to 5-15 unless GPT asks for more.
- Prefer summaries plus exact file paths over full file dumps.
- Include full diffs only for the patch under review.
- If evidence is contradictory, show both versions and label the source.
- Never mix speculative cleanup with required migration work.
