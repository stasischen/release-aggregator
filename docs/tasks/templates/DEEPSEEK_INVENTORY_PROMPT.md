# DeepSeek Inventory Prompt

Objective:
整理問題、cleanup candidates、方案草稿，產出給 GPT 5.5 決策用的材料。

Scope:
- Repo:
- Target directories:
- Known goal:

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
2. Proposed solutions:
   - Option A
   - Option B
   - Option C
3. Duplicate logic table:
   - File A
   - File B
   - Shared behavior
   - Difference that matters
4. Dead-code candidates:
   - File or symbol
   - Why it appears unused
   - Verification needed before removal
5. Cleanup batch proposal:
   - Safe cleanup
   - Risky cleanup
   - Should not touch

Constraints:
- Do not decide architecture boundaries.
- Do not delete or rewrite code.
- Mark confidence for dead-code claims.

