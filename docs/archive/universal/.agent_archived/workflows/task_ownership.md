---
description: Task Ownership & Cross-Task Modification Protocol
---

# Task Ownership & Cross-Task Modification Protocol

## 核心原則

**Rule 1: 檔案所有權優先**
- 每個任務的 `context.files` 列表定義了該任務的**主要責任範圍**
- Agent 應優先處理自己任務範圍內的檔案

**Rule 2: Lint 修復的特殊情況**
- 如果 IDE 回報的 lint 錯誤**不在**你的任務 `context.files` 範圍內：
  1. 檢查該檔案是否被其他 Agent 的任務 claim
  2. 如果是，**不要修改**，讓負責的 Agent 處理
  3. 如果沒有人 claim，可以修復，但需在 commit message 中註明 `[cross-task]`

**Rule 3: 依賴性修改**
- 如果你的任務**必須**修改其他任務範圍的檔案（例如刪除舊檔案導致測試失效）：
  1. 在 commit message 中明確說明原因
  2. 在 `AGENT_TASKS.json` 的 `history` 中記錄跨界修改
  3. 通知相關 Agent（透過 heartbeat 或 history）

## 檢查清單

在修改任何檔案前，問自己：

```
1. 這個檔案在我的 task.context.files 中嗎？
   ├─ YES → 可以修改
   └─ NO  → 繼續檢查

2. 這個檔案被其他 IN_PROGRESS 任務 claim 了嗎？
   ├─ YES → 不要修改，除非有依賴性
   └─ NO  → 可以修改，但標記 [cross-task]

3. 這是我刪除的檔案導致的連鎖影響嗎？
   ├─ YES → 可以修改，但記錄在 history
   └─ NO  → 謹慎評估是否真的需要修改
```

## 範例

### ❌ 錯誤示範
```
Task: v3-task-3 (Mini-Game 遷移)
修改: video_player_controller_test.dart (屬於 v3-task-1)
原因: 看到 lint 就順手修了
結果: 跨界修改，可能與 Agent-Home-Desktop 衝突
```

### ✅ 正確示範
```
Task: v3-task-3 (Mini-Game 遷移)
修改: mini_game_state_controller_test.dart (刪除)
原因: 我刪除了 mini_game_state_controller.dart，這個測試檔案已失效
Commit: "chore: remove obsolete test after mixin deletion"
```

### ⚠️ 可接受但需註明
```
Task: v3-task-3 (Mini-Game 遷移)
修改: video_player_controller_test.dart (屬於 v3-task-1)
原因: 我新增的 mockito 依賴導致需要重新生成 mocks
Commit: "[cross-task] fix: regenerate mocks after adding mockito dependency"
History: 在 v3-task-3 的 history 中記錄此跨界修改
```

## 自動化檢查（未來改進）

可以在 `.agent/scripts/` 中加入 pre-commit hook：

```python
# check_task_ownership.py
def check_modified_files(task_id, modified_files):
    task = load_task(task_id)
    owned_files = task['context']['files']
    
    for file in modified_files:
        if file not in owned_files:
            owner = find_file_owner(file)
            if owner and owner['status'] == 'IN_PROGRESS':
                print(f"⚠️  Warning: {file} is owned by {owner['assignee']}")
                print(f"   Consider letting them handle it.")
```

## 總結

**記住：多人協作時，清晰的邊界比快速修復更重要。**
