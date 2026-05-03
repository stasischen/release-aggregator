# DeepSeek Decision Note

Objective:
記錄 DeepSeek 對某個任務做出的結論，通常在 `deepseek-v4-pro` 下產生。

Default model:
- `deepseek-v4-pro`

Use when:
- 需要把 inventory 轉成明確建議
- 需要對候選方案做排序
- 需要判定風險、是否升級、是否交 GPT 5.5 做最終決策

Input:
- `docs/tasks/<TASK_ID>/DEEPSEEK_INVENTORY.md`
- `docs/tasks/<TASK_ID>/TASK_BRIEF.md`

Output format:
1. Recommendation:
   - Choose: flash / pro / defer / split / needs GPT
   - Why:
2. Key risks:
   - Risk
   - Evidence
   - Severity
3. Suggested next action:
   - Exact next step
4. Escalation notes:
   - What should go to GPT 5.5
   - What can stay on DeepSeek / Codex

Constraints:
- Do not change code.
- Do not expand scope.
- Keep the answer decision-oriented, not exploratory.

