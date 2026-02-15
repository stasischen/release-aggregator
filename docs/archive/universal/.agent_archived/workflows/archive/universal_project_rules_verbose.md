---
description: Universal Project Rules / 通用項目規則
---

# Universal Project Rules (通用項目規則)

所有參與 Lingourmet Universal 的 Agent 必須遵守以下規則。
All agents participating in Lingourmet Universal must follow these rules.

## 🗣️ 0. 溝通規範 (Communication Standards)

### A. 雙語對照 (Bilingual Requirement)

所有與使用者的對話、Artifacts (Task/Plan/Walkthrough) 必須使用 **中英對照** 格式。
All conversations and user-facing artifacts must use **Bilingual (Chinese/English)** format.

- **Chat**: Chinese first, then English (or interleaved).
- **Artifacts**: Titles and key descriptions must be bilingual.
- **Code**: Comments and Commit Messages remain in **English** only.

### B. 確認與回應規範 (Confirmation & Response Standards)

- **Confirmation Cap (確認上限)**: 標準指令確認上限為 **1 次**。禁止像鸚鵡般重複使用者指令 (No parrot-like echoing).
- **Critical Exception**: 針對高風險操作 (刪除、大規模重構)，確認次數上限為 **2 次**。
- **Directness**: Tell me the result/status, not what I just told you.

## 🏗️ 1. 技術棧與架構 (Tech Stack & Architecture)

### A. 核心前端 (Core Frontend)

- **Framework**: Flutter (Dart)
- **State Management**: Riverpod (Generator preferred)
- **Models**: Freezed 3.x (Must use `abstract class`)
- **Navigation**: GoRouter

### B. 代碼規範 (Code Standards)

- **Naming**: `snake_case` for files, `PascalCase` for classes, `camelCase` for variables.
- **Logger**: Always use `Logger` for game/error logging. Avoid `print` in production code.
- **Const**: Use `const` constructors wherever possible for performance optimization.
- **Const**: Use `const` constructors wherever possible for performance optimization.
- **Linting**: Strict linting enabled. Run `flutter analyze` before committing.

### C. 語言完整性與品質檢查 (Mandatory Linguistic Quality Review) ⚠️

- **全階段審查**: 每個涉及文字的階段 (Phase 1, 2, 4) 完成後，**必須** 對 **所有文字內容** 進行語義、風格與準確度稽核。
- **Full Content Review**: For Phases 1, 2, and 4, a **Mandatory** audit of **all text content** (semantics, style, accuracy) must be performed.
- **零容忍品質控管**: 僅檢查結構 (Metadata) 是不足夠的。Agent 必須逐行確認：
  - Phase 1: 譯文是否自然、是否符合角色語氣、Big 5 翻譯是否一致、有無誤譯。
  - Phase 2: 分詞是否符合語義邊界、詞性 (POS) 標註是否對應語義。
  - Phase 4: 詞典解釋是否精確、例句是否能正確展示詞彙用法。
- **Gate**: If content quality is not verified, the phase is NOT considered complete.

### D. 工具重用原則 (Tool Reuse Policy) ⚠️

- **Check First**: Before writing a new script, check `tools/v4/`.
- **Reuse**: Prefer modifying existing validation/repair tools over creating one-off scripts.
- **Sanitize**: Use `sanitize_dictionary.py` for any data cleanup tasks.
- **One-off Scripts**:
  - **Storage**: Must be placed in `tools/temp_scripts/`. NEVER create them in the root directory.
  - **Lifetime**: DELETE them immediately after use and verification. Do not commit unless essential.
  - **Cleanup**: Regularly purge content in `tools/temp_scripts/`.

### E. 自動化翻譯安全規約 (Strict Automation Policy for Translation) ⚠️

- **Manual Default (預設手動)**: 所有涉及翻譯的流程（Phase 1 翻譯, Phase 4 詞典等），預設一律採用 **人工手動檢查 (Manual Audit)**。
- **Approval Required (需批准)**: 任何自動化翻譯工具（如 `batch_translate`, LLM Client, 外部 API）在執行前，**必須** 獲得使用者的 **明確批准**。嚴禁擅自自動執行。
- **Deterministic Scripts**: 若需批量處理，應優先撰寫確定性的 Python Script 進行規則化替換，而非依賴 AI 生成。

## 🧪 2. 測試策略 (Testing Strategy)

### A. Shift-Left Testing

在部署前驗證邏輯。
Verify logic before deployment.

- **Unit Tests**: Test core logic and models.
- **Widget Tests**: Test UI behavior and components.
- **Golden Tests**: Visual regression protection.

## 📦 3. 內容管線 (Content Pipeline - V5 Modular)

### A. 雙重真值來源 (Dual Source of Truth)

V5 架構將結構與內容分離，以支援高頻變更：
V5 architecture separates structure from content for high-frequency updates:

1.  **Structure (Atoms)**:
    - Source: `0_yarn/` (.yarn files)
    - Storage: `2_atoms/`
    - **Rule**: NEVER edit `2_atoms` manually. Change the `.yarn` file and run sync.
2.  **Content (Translations)**:
    - Source: `1_translation/`
    - **Rule**: This is the editable zone for copywriters.

### B. V5 核心流程 (Core V5 Flow)

標準作業程序必須遵循以下階段 (詳見 `skill:v5_content_pipeline`)：
SOP must follow these phases (see `skill:v5_content_pipeline`):

1.  **Sync (更新)**: `python -m tools.v5.core.update_db {lang}`
    - _Action_: Parses Yarn, updates `2_atoms`, and fills `1_translation` from TM.
2.  **Merge (合併)**: `python -m tools.v5.core.merger {lang}`
    - _Action_: Combines Atoms + Translations -> `5_full_view`.
3.  **Build (構建)**: `python -m tools.v4 build {lang}`
    - _Action_: Compiles `5_full_view` into App Assets.

### C. 嚴格管線執行 (Strict Pipeline Execution)

- **禁止手動編輯 Full View**: `5_full_view` 是自動生成的。任何編輯都會在下次 Merge 時丟失。
- **No Manual Edit on Full View**: `5_full_view` is auto-generated. Edits will be lost.
- **修復上游**: 若在 Preview 發現錯誤：
  - 結構/邏輯錯誤 -> 修改 `0_yarn`
  - 錯字/翻譯 -> 修改 `1_translation`

### D. Agent Content Safeguards (Self-Check)

- **Must Read**: `.agent/workflows/agent_content_guardrails.md`
- **Rule**: Agents must verify the "Target Language First" principle before any content extraction or atomization.

## 🚀 4. 功能移植 (Feature Porting)

從 Legacy (`lingourmet_flutter`) 移植到 Universal 時：
When porting from Legacy:

1. **Analysis**: 檢查依賴項。
2. **Models**: 修復 Freezed 語法與 JSON 轉換。
3. **Screen**: 適配 Universal 的特定 API (TTS/Logger/Colors)。
4. **Verification**: 確保通過靜態分析。

## 🧠 6. 工作流標準 (Workflow Standards - Skills) ⚠️

本項目採用 **Progressive Disclosure (漸進式揭露)** 架構管理 Agent 工作流 (Skills)。
This project uses **Progressive Disclosure** architecture for Agent Workflows.

### A. 三層架構 (Three-Layer Architecture)

所有新建立或重構的工作流必須遵循以下分層：
All workflows must follow these layers:

1.  **Metadata Layer** (入口文件):
    - 位於 `.agent/workflows/{command}.md`。
    - 包含 YAML `description`（~100 tokens）供 Agent 識別。
    - 僅包含大方向 (Direction) 與資源索引 (Resource Index)。
2.  **Instruction Layer** (執行手冊):
    - 位於 `.agent/workflows/{command}/SOP.md`。
    - 包含具體執行指令與核心邏輯，控制在 5000 tokens 以內。
3.  **Resource Layer** (按需資源):
    - 位於 `.agent/workflows/{command}/resources/`。
    - 包含 `troubleshooting.md`, `checklists.md`, `prompts/` 等資料，僅在需要時讀取。

### B. 按需加載與強制閱讀原則 (On-Demand Loading & Mandatory SOP Reading) ⚠️

1.  **Mandatory Reading (強制閱讀)**: 在開始任何 Phase (N) 的任務前，Agent **必須** 使用 `view_file` 讀取對應的 `.agent/workflows/v5_content_pipeline/{N}_{Phase}/SOP.md`。嚴禁僅憑記憶或常識操作。
2.  **On-Demand (按需加載)**: Agent 在執行任務時，應優先讀取入口文件，確認目標後再主動請求讀取 `SOP.md` 或資源文件。嚴禁一次性讀取整個目錄內容以免撐爆 Context Window。

## 🛡️ 7. 階段性強制驗證 (Strict Phase-by-Phase Execution) ⚠️

為了確保品質並防止錯誤累積，Agent 必須嚴格遵守「階段門禁 (Gatekeeping)」原則：
To ensure quality and prevent error accumulation, Agents must strictly follow "Gatekeeping" principles:

### A. 零容忍原則 (Zero Tolerance Policy)

- **禁止跳級**: 除非當前階段 (Phase N) 達到 **100% Pass (0 Errors, 0 Warnings)**，否則嚴禁進入下一階段 (Phase N+1)。
- **No Skipping**: DO NOT proceed to the next phase until the current phase passes with **Zero Errors and Zero Warnings**.
- **例外排除**: 只有在使用者明確指令「忽略警告」或「手動覆核後通行」的情況下，方可繼續。
- **Exception**: Only proceed if the user explicitly says "ignore warnings" or "proceed anyway".

### B. 單一語言優先 (Single-Language Focus)

- **一次一個**: 執行管線或是稽核任務時，必須採取 `th -> ko -> de` 的順序，完成一個語言的所有階段 (0-5) 並通過驗證後，才開啟下一個語言。
- **Focus**: Process one language at a time. Complete all phases (0-5) for one language before starting the next.

### C. 顯式報告 (Explicit Reporting)

- 在切換 `task_boundary` 的 `TaskName` 之前，必須在 `TaskSummary` 中條列出當前階段的驗證結果，證明已無懸留問題。
- You must explicitly list verification results in the `TaskSummary` before moving to a new `TaskName`.

### D. 配置與數據完整性門禁 (Configuration & Data Integrity Gate) ⚠️

為了防止自動化工具在同步（Sync）時誤刪手動新增的內容：
To prevent automated tools from deleting manually added content during sync:

1.  **Mandatory Registration (強制註冊)**: 任何在 Phase 1 手動新增的翻譯欄位（例如 `trans_id`），**必須** 先在 `tools/v4/core/generate.py` 的 `STRATEGIC_LEARNER_LOCALES` 中註冊。
2.  **Validation First**: 嚴禁在未確認 `generate.py` 配置與 CSV Header 100% 吻合前執行 Phase 2 的 `update_db.py`。
3.  **Conservative Tools**: 工具開發者應確保 `update_db.py` 在發現未知欄位且內含數據時，應拋出錯誤（Error）而非預設刪除。

### E. 實體簽收文件要求 (Physical Sign-off Artifact Requirement) ⚠️

為了防止 Master Script 或 Agent 自動「跳級」：
To prevent Master Scripts or Agents from "skipping" phases:

1.  **Artifact Presence**: Master Script 在進入 Phase N+1 之前，**必須** 物理性地檢查 `verified_pN.txt` 是否存在。
2.  **Verification Checkbox**: 簽收文件必須包含「配置對齊 (Config Alignment)」與「數據完整性 (Data Integrity)」的檢查項。
3.  **No Artifact, No Proceed**: 即使代碼門禁（Gate Script）通過，若缺少人類（或 Agent 模擬手動檢查後的）實體簽收文件，管線必須強制中止。

---

## ⚡ 8. Action Bias (Avoid Hesitation Loops)

1.  **Trust Your Tools**: If you need information (file path, line number), verify it immediately with `find_by_name` or `grep_search`. Do NOT enter a "thinking loop" of verifying without acting.
2.  **Fail Fast**: It is better to try a `find` command and fail (then correct) than to sit in a cycle of "Wait, I should check...".
3.  **Sequential Execution**: If you have a clear plan (Find -> Edit -> Run), execute the first step immediately. Do not buffer too many mental steps if they depend on the first step's output.

### F. Windows Safe Write Protocol (WSWP) ⚠️

- **Why**: Standard tools like `write_to_file` or `replace_file_content` frequently cause encoding corruption (e.g., mangled emojis, BOM issues) on Windows environments.
- **Rule**: For any non-trivial file update (especially those containing non-ASCII characters or emojis), **PREFER** executing a Python script to perform the update.
- **Implementation**:
  - Create a temporary script (e.g., `tools/temp_scripts/update_file.py`).
  - Use `open(path, 'w', encoding='utf-8')` or `encoding='utf-8-sig'` (if BOM is required).
  - Execute the script using `run_command`.
  - This ENSURES consistent encoding and prevents the "weird characters" () bug.

### G. Audit Accountability (Table Requirement) ⚠️

Whenever performing an Audit (Phase 5 or Phase 2), the Agent MUST:

1.  **Maintain a Progress Table**: Create/Update an `audit_report.md` in the relevant phase directory (e.g., `.agent/workflows/5_build/audit_reports/`).
2.  **Format Compliance**: 必須嚴格遵守資源目錄中的 `audit_template.md` 格式。禁止自行創立簡易清單。
3.  **Evidence-Based Reporting (證據導向報告)**:
    - **Verification Logs**: 在報告中必須附上驗證工具 (如 `audit_view.py --scan`) 的執行日誌路徑或掃描摘要。
    - **No False Greens**: 🟢 (Verified) status MUST ONLY be assigned after a HUMAN semantic cross-check (Source vs Translation vs Atom).
4.  **Cross-Language Verification**: Auditing one language is INSUFFICIENT. All supported target languages (EN, ZH_TW, JA, KO, RU) must be verified before a file is marked complete.
5.  **Traceability**: Every fixed item must be linked back to its Phase (e.g., Fix in Phase 4 Dictionary -> Re-run Phase 5 Merger).

---

## 🛑 Appendix: Case Study - The 'Pass' Illusion (2026-01-15)

**Scenario**:
During the V5 Thai rollout, the pipeline reported "Green" (Success) for Phase 4 Dictionary.
However, a later Manual Audit (Phase 5) revealed major issues:

1.  **Extract Bug**: Homonyms (e.g., `th_PREP_กับ` vs `th_CONJ_กับ`) were silently deduplicated, losing data.
2.  **Missing Definitions**: Common words (`th_N_วัน`) existed in Dictionary but had empty translations (`[MISSING]`), yet Sync didn't flag them as error.
3.  **Hallucinations**: Auto-translation treated Tags (`{$th_end}`) as text ("Yes"), creating content bugs.

**Root Cause**:
The Agent trusted the `status="reviewed"` column and the exit code `0` of the script, without looking at the **Actual Content** line-by-line.

**Lesson**:

- **Automated Checks are Insufficient**: Scripts only check syntax (JSON valid?), not semantics (Is translation correct?).
- **Strict Manual Audit is Mandatory**: You CANNOT skip Phase 5 Audit. You must read the CSV rows.
- **Trust No One**: Even if previous file says `reviewed`, assume it is `draft` until YOU verify it.

**Preventive Rule**:
All Agents must execute `audit_view` and verify at least one file **visually** before declaring a task complete.

---

**Last Updated**: 2026-01-15
