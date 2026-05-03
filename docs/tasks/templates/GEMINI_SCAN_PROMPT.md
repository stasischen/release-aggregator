# Gemini Scan Prompt

Objective:
掃描 repo 或跨 repo 範圍，產出給 GPT 5.5 決策用的濃縮架構材料。

Scope:
- Repo:
- Target domain / feature:
- Related repos:

Inspect:
- Entry points
- Core modules
- Data models and schemas
- Build, validation, and release scripts
- Runtime consumers
- Docs that describe intended architecture

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

