# How to Write "Unskippable" Agent Workflows

## 如何撰寫讓 Agent 乖乖聽話的工作流

您剛才觀察到的現象是 Agent 的通病：**過度優化 (Over-Optimization)**。預設情況下，Agent 會試圖用最少的步驟完成任務（例如一次生成所有語言），這通常會導致品質下降或產生「翻譯腔」。

要讓 Agent 像剛才那樣「一步一腳印」地執行，您需要在 Workflow Markdown 中使用以下 **4 個關鍵技巧**：

### 1. 設置明確的「停止閘門」 (The Stop Gate)

Agent 看到連續的指令會試圖並行處理。您必須在關鍵步驟間插入 **"Halt & Report"** 指令。

**❌ 錯誤寫法 (Bad):**

```markdown
1. 翻譯成中文
2. 翻譯成日文
3. 翻譯成西班牙文
```

*(Agent 會試圖在一個步驟內全部做完)*

**✅ 正確寫法 (Good):**

```markdown
1. **Translate to Chinese**: Generate `trans_zh_TW`.
2. **STOP & REVIEW (Gate 1)**: 🛑
   - You MUST `notify_user` to review the Chinese content.
   - DO NOT proceed to Japanese until User says "Approved".
```

### 2. 使用「專家角色」關鍵字 (Role Persona)

使用特定的形容詞來切換 Agent 的執行模式。避免使用 "Translate" 這種通用詞，改用更具體的指示。

- **Generic**: "Translate the text." (Agent 會用最快速度翻完)
- **Specific**: "Perform an **Expert Linguistic Review**. Act as a **Professional Poet**. Verify natural phrasing and remove any 'translationese'." (Agent 會切換到高耗能、高品質模式)

### 3. 強制拆分任務清單 (Forced Granularity)

在 Workflow 中明確要求 Agent 修改 `task.md`。如果 `task.md` 上只有一個大勾勾，Agent 就會想一次勾掉。如果拆成 5 個小勾勾，它就被迫分 5 次執行。

**✅ Workflow 指令範例:**
> "Before starting, you MUST update `task.md` to split the translation task into 5 separate items: [ ] JA, [ ] ES, [ ] RU, [ ] ID. check them off one by one."

### 4. 定義「失敗後果」 (Consequences)

告訴 Agent 如果偷懶會發生什麼事。

> **Rule**: If you generate all languages at once, the quality will be low and the User will reject it. You MUST do it sequentially to ensure quality.

---

## 推薦的 Workflow 模板範例

您可以將此結構用於未來的 `.agent/workflows/new_task.md`：

```markdown
# Workflow: High-Quality Multi-Lang Translation

## Phase 1: Preparation
- [ ] Read source content.
- [ ] **Task Split**: Update `task.md` to list each target language as a separate TODO item.

## Phase 2: Sequential Execution (Loop)
**Rule**: Execute one language at a time.

### Step 2.1: Traditional Chinese (zh-TW)
- Action: Translate to `trans_zh_TW`.
- Mode: **Creative Writer** (No machine literal translation).
- **GATE**: Call `notify_user`. Wait for approval.

### Step 2.2: Japanese (ja)
- Action: Translate to `trans_ja`.
- Mode: **Native Speaker**.
- **GATE**: Call `notify_user`. Wait for approval.

... (Repeat for others)
```

**總結：**
Agent 就像一個急著下班的實習生。您必須給它**打卡鐘 (Gates)** 和 **詳細的檢查表 (Split Tasks)**，它才會按部就班地把工作做好。
