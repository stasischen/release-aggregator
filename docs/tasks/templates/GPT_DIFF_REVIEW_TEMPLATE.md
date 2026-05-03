# GPT 5.5 Diff Review Prompt

請 review 這次 diff。

## Input

- Task Brief:
- GPT Decision:
- Diff:
- Test output:

## Review Focus

1. 有沒有破壞既有架構。
2. 有沒有過度修改或 scope creep。
3. 有沒有漏測。
4. 有沒有安全、資料流、schema、release path 問題。
5. 是否符合原本 Task Brief。

## Required Output

### 必修問題

- Severity:
- File:
- Issue:
- Required fix:

### 建議問題

- Issue:
- Suggested fix:

### 可以接受的 Tradeoff

- Tradeoff:
- Why acceptable:

### 下一步修正指令

- 給 Codex 的精準修正指令。

