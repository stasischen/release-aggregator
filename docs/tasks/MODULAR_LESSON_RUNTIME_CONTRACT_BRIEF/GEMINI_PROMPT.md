# Gemini Prompt

```text
Repo context:
- Frontend repo: /Users/ywchen/Dev/lingo/lingo-frontend-web
- Control repo: /Users/ywchen/Dev/lingo/release-aggregator

Please first read these control docs:
- /Users/ywchen/Dev/lingo/release-aggregator/AGENTS.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/index.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/agent_reference_order.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/runbooks/multi_model_task_orchestration.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/TASK_INDEX.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/MODULAR_LESSON_RUNTIME_PRODUCT_BRIEF/HANDOFF_SUMMARY.md
- /Users/ywchen/Dev/lingo/release-aggregator/docs/tasks/MODULAR_LESSON_RUNTIME_CONTRACT_BRIEF/TASK_BRIEF.md

Task:
Run a read-only modular lesson runtime contract options inventory.

Important constraints:
- Do NOT modify files.
- Do NOT define the final contract yourself.
- Do NOT modify or propose concrete lesson schema changes.
- Do NOT touch content-ko or content-pipeline.
- Do NOT collapse domain adapter semantics into one generic adapter.
- Do NOT propose removing compatibility/cache behavior such as mapping_v2 origin cache.
- Treat lesson runtime as not final unless proven otherwise.

Inspect these areas:
- Modular lesson runtime screens/routes
- ULV primary surface adapters
- ULV support surface adapters and support panel switcher
- Article/video/dialogue/sentence/vocab/pattern/usage rendering paths
- Current fail-soft/fallback behavior
- Preview/testbed routes and whether production navigation can reach them
- Existing tests around modular runtime, support panels, article/video surfaces, and route exposure
- Existing completed architecture/mock verification artifacts if referenced by TASK_INDEX

Questions to answer:
1. Article surface:
   - What renderer options are implied by the current code?
   - What minimum production behavior is possible without schema changes?
   - What behavior requires a product/runtime contract decision?
   - What fail-soft states should remain dev-only?

2. Support panels:
   - For pattern / usage / vocab, what data or component ownership options exist?
   - Can existing Knowledge Lab / Dictionary / Sentence Bank components be reused safely?
   - What are the risks of lesson-local renderers vs shared domain components?

3. Video runtime:
   - What data dependencies and builder assumptions exist today?
   - Which paths are already production-safe?
   - Which paths are pilot/fail-soft?

4. Route exposure:
   - Which modular runtime, preview, and dev/testbed routes exist?
   - Which are user-facing through normal navigation?
   - Which labels or placeholders are acceptable if internal-only?

5. Validation:
   - What smoke-test matrix should gate article/support/video runtime production exposure?
   - Which existing tests can be reused?
   - Which tests are missing?

Required output:
1. Findings sorted P0/P1/P2/P3.
2. Decision matrix:
   - Surface
   - Option A/B/C
   - Pros
   - Risks
   - Requires schema/content change? yes/no/unknown
   - Requires product decision? yes/no
   - Recommended by Gemini as input only, not final
3. Route exposure table:
   - Route
   - Entry point
   - User-facing or internal
   - Placeholder/pilot markers
   - Recommended disposition
4. Smoke-test matrix:
   - Surface
   - Test file to add/update
   - Fixture/data needed
   - Pass condition
5. Suggested implementation task split after Codex/user approval.

Output only analysis and recommendations. Do not edit the repo.
```
