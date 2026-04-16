# UNITFAC-008: Batch Production Playbook (Unit Assembly Line)

本文檔定義了 Lingourmet 課程單元的**批次量產 (Batch Production)** 標準作業程序。透過「單元工廠」模式，確保多位 Agent 或作者能平行產出高品質、符合教育規範的單元的內容。

---

## 1. 生產模型與目的 (Production Model)

### 1.1 什麼是「單元工廠」？

「單元工廠」是指一套標準化的流水線流程：從自動生成骨架 (Scaffold) 開始，經過內容填寫 (Authoring)、自動化檢核 (Lint)、PM 試玩 (Trial)，最後凍結 (Freeze) 入庫。

### 1.2 批次定義 (Production Batch)

一個**生產批次**通常包含 2–5 個單元。

* **基準參考 (References)**：
  * **A1-U04 (Baseline)**: 已達到 PR-ready 標準，作為結構與表現的基準。
  * **A1-U05 (Pilot)**: 完整量產流程生成的試點單元，包含最新的動態句型轉換。
  * **A1-U06 (Scaffold)**: 範例腳手架狀態，用於對比開發中與完工之差異。

---

## 2. 角色與職責 (Roles & Responsibilities)

| 角色 | 職責描述 | 交付物 |
| :--- | :--- | :--- |
| **Author (作者)** | 根據 Template 填寫 Fixture 的 `payload`（中韓文、選項、詞塊）。 | 內容完備的 JSON Fixture |
| **Lint/QA (檢核者)** | 執行 `mockup_check` 與 Schema 驗證，確保無遺失欄位或格式錯誤。 | 檢核報告 (Passed with 0 Blockers) |
| **PM Reviewer (評審)** | 使用 Modular Viewer 進行試玩，核對教育品質與 UX 通順度。 | PM 驗證報告 (UNITFAC-007) |
| **Fixer (修正者)** | 根據 Lint 或 PM 的反饋修正內容或結構錯誤。 | 修正後的 JSON Fixture |
| **Freeze (整合者)** | 更新 `fixtures.json` 索引，更新任務狀態，凍結版本。 | 合併至 Git 且狀態標記為 Done |

---

## 3. 標準工作流 (Standard Workflow)

### Stage 0: 批次規劃與派工 (Batch Setup)

* 確定本次批次的 Unit ID 名單。
* 分配 Author 與主要 Reviewer。

### Stage 1: 骨架生成 (Scaffold Generation)

* 使用 `scaffold_unit_blueprint.py` 生成 initial skeleton。
* 參考：[UNITFAC-003 Scaffold Usage](./UNITFAC_003_SCAFFOLD_USAGE.md)。

### Stage 2: 內容填寫 (Authoring)

* 根據 [UNITFAC-005 Authoring Templates](./UNITFAC_005_AUTHORING_TEMPLATES.md) 填充 `TODO` 欄位。
* 確保所有目標語 (KO) 都有對應的繁體中文 (ZH-TW)。

### Stage 3: 自動化門檻 (Validation Gate)

* 執行 `mockup_check`。
* 參考：[UNITFAC-004 Mockup Check Usage](./UNITFAC_004_MOCKUP_CHECK_USAGE.md)。
* **Gate**: 必須達到 **0 Blockers**。

### Stage 4: PM 試玩與驗收 (PM Trial)

* 將 Fixture 註冊至 `modular/data/fixtures.json`。
* PM 執行 [UNITFAC-007 PM Trial Guide](./UNITFAC_007_MULTI_UNIT_PM_TRIAL_GUIDE.md)。

### Stage 5: 反饋循環 (Fix Loop)

* Fixer 修正 PM 提出的內容問題（如：翻譯不自然、題目太難）。
* 重複 Stage 3 確保修正後未引入語法錯誤。

### Stage 6: 凍結與登記 (Freeze & Registry)

* 更新 `docs/tasks/mockups/modular/data/fixtures.json` 中的狀態標籤。
* 提交 Git Commit 併入主線。

---

## 4. 進場與出場準則 (Entry/Exit Criteria)

### 4.1 Blocker vs Warning 政策

* **PR-Ready (生產完畢)**：必須 **Zero Blockers** 且 **Zero Warnings**（除非 Warning 已被 PM 核准忽略）。
* **Scaffold/Draft (開發中)**：允許存在 `TODO` 相關的 Warnings，但不可有 `JSON_INVALID` 或 `MISSING_FIELD` 等 Blockers。

### 4.2 出場清單 (Exit Checklist)

* [ ] 通過 `scripts/mockup_check.py` 且無 Blocker。
* [ ] 在 Modular Viewer 中完成全單元試玩。
* [ ] `unit_id` 符合規範且 Node ID 無重覆。

---

## 5. 文件與 Commit 規範 (Conventions)

### 5.1 檔案命名

* 路徑：`docs/tasks/mockups/`
* 格式：`a1_u{NN}_unit_blueprint_v0.json` (小寫，底線分隔)

### 5.2 Commit 信息

* 新單元生成：`feat(content): add scaffold for A1-U07`
* 內容完工：`feat(content): complete authoring for A1-U07`
* 修復反饋：`fix(content): address PM findings for A1-U07`

---

## 6. 批次追蹤格式 (Batch Tracking Table)

| Unit ID | Owner | 當前階段 (Stage) | Blockers | PM 狀態 | 備註 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A1-U06 | Agent-A | Stage 2: Authoring | 0 | N/A | 填充對話中 |
| A1-U07 | Agent-B | Stage 4: PM Trial | 0 | Pending | 等待 PM 試玩 |
| A1-U08 | Agent-A | Stage 1: Scaffold | 2 | N/A | 待補齊骨架 |

---

## 7. 品質門檻 (Quality Gates)

### 提交 PM 試玩前 (Pre-Trial)

```bash
python scripts/mockup_check.py docs/tasks/mockups/a1_uXX_...json
```

* 必須確保所有 `payload` 欄位已非空。

### 最終凍結前 (Pre-Freeze)

```bash
python scripts/mockup_check.py --index docs/tasks/mockups/modular/data/fixtures.json
```

* 確保批次內所有單元均通過檢核，無副作用。

---

## 8. 常見故障與排除 (Common Failure Modes)

| 現象 | 可能原因 | 排除方法 |
| :--- | :--- | :--- |
| **Lint 通過但 Viewer 空白** | Payload 結構層次錯誤（如多了一層 `payload.payload`）。 | 檢查 JSON 巢狀結構。 |
| **TTS 不發音** | `sample_lines` 或 `text` 包含中文字符。 | 修正為純韓文，翻譯放入 `zh_tw` |
| **ID 衝突** | 手工複製 Node 時忘記更改 ID。 | 執行 `mockup_check` 會報 `DUPLICATE_NODE_ID`。 |
| **狀態不持久** | localStorage 緩存舊資料。 | 點擊 Viewer 介面的「重置」按鈕。 |

---

## 9. 完工定義 (Definition of Done)

符合以下條件即視為批次完成：

1. 本批次所有單元 Fixture 通過 `mockup_check` (Zero Blockers)。
2. 本批次所有單元在 Modular Viewer 中試玩無誤。
3. `fixtures.json` 的 meta 資訊已更新為最新的 Title 與狀態。
4. 交付報告中包含每個單元的驗證報告連結。

---

## ⚡ 快速通道 (Fast Lane) — 現有 PR 單元微調

若僅為修正現有 PR 單元（如 A1-U04）的錯字，流程可簡化為：

1. **Edit** JSON 直接修正。
2. **Lint** 跑單檔 `mockup_check`。
3. **Smoke Review** 在 Viewer 確定該節點修正正確。
4. **Commit** 提交。
