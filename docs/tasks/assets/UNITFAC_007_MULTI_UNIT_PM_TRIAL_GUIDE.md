# UNITFAC-007: Multi-Unit PM Trial Guide (Modular Viewer)

本文檔旨在引導產品經理 (PM) 或產品審核人員使用 **Modular HTML Viewer** 進行多單元課程內容的驗證與試玩。

---

## 1. 目的與對象 (Purpose & Audience)

* **對象**：產品經理 (PM)、教學設計審核人、內容品質保證 (QA)。
* **目的**：
  * 驗證「量產等級」(Production-Ready, PR) 單元是否符合教育骨架與互動品質。
  * 區分「量產等級」單元與「開發中腳手架」(Scaffold) 單元的差異。
  * 在進入 Flutter 實作前，於 HTML 環境確認內容邏輯與翻譯正確性。

---

## 2. 準備工作 (Prerequisites)

在開始試玩前，請確保已完成以下步驟：

### 2.1 啟動本地伺服器

由於網頁瀏覽器的安全性限制（CORS），直接雙擊 `index.html` 可能無法載入地圖資料。請在專案根目錄執行：

```bash
# 使用 Python 啟動伺服器
python -m http.server 8000
```

隨後在瀏覽器訪問：`http://localhost:8000/docs/tasks/mockups/modular/index.html`

### 2.2 運行自動化檢核

在人工審看前，作者應先運行 `mockup_check` 以排除低級錯誤：

```bash
python scripts/mockup_check.py --index docs/tasks/mockups/modular/data/fixtures.json
```

* **預期結果**：A1-U04/U05 應為 `PASS (0 errors, 0 warnings)`；A1-U06 允許存在 `TODO` 警告。

---

## 3. 測試單元集定義 (Trial Set)

本次試玩包含三個具有代表性的狀態單元：

| 單元 ID | 主題 | 準備狀態 (Readiness) | 試玩重點 |
| :--- | :--- | :--- | :--- |
| **A1-U04** | 咖啡廳點餐 | **PR-Ready (Baseline)** | 驗證完整教學循環、多輸入形式、回想練習。 |
| **A1-U05** | 在藥局買藥 | **PR-Ready (Pilot)** | 驗證 `pattern_transform` 與 `repair_practice` 新模型。 |
| **A1-U06** | 旅館入住 | **Scaffold (Reference)** | 觀察開發中狀態（含 TODO），建立「非 PR」的辨識標準。 |

---

## 4. 推薦試玩路徑 (Recommended Walkthrough) — 15~20 分鐘

建議按照以下順序進行，以建立品質基準感：

### 第一站：A1-U04 (量產基準線)

1. **切換單元**：在左側下拉選單選擇 `A1-U04`。
2. **觀察輸入多樣性**：從 `U04-L1` (對話) 到 `U04-L3` (公告) 到 `U04-L4` (通訊訊息)，確認頁面渲染是否清晰。
3. **驗證骨架**：確保在第一個對話後出現了 `U04-L2` (理解度檢核)。
4. **終點對應**：跳到 `U04-R1` (單元回想)，確認題目是否能覆蓋單元核心功能（點餐、付款、約時間）。

### 第二站：A1-U05 (新量產試點)

1. **切換單元**：選擇 `A1-U05`。
2. **重點檢查 P3/P4**：
   * `A1-U05-P3` (結構轉換)：檢查是否能清楚引導學習者從「頭痛」轉換為「喉嚨痛」。
   * `A1-U05-P4` (溝通修復)：確認是否包含如「請再說一次」等生存必備語句。
3. **TTS 測試**：點擊右上角「韓文語音 (TTS)」測試按鈕，確認發音流暢度。

### 第三站：A1-U06 (腳手架比對)

1. **切換單元**：選擇 `A1-U06`。
2. **辨識 Blockers**：你會看到大量 `TODO` 文字。這在 PM 試玩階段是正常的，但在「發佈」階段則屬於 Blocker。

---

## 5. 多單元驗證清單 (Acceptance Checklist)

當 PM 標記某單元為 **PASS (PR-ready)** 時，應符合以下所有檢查項：

### A. 教學結構與序列 (Structure & Sequencing)

* [ ] **序列完整性**：必須包含「輸入 -> 解析/結構 -> 受控輸出 -> 引導輸出 -> 結案回想」的循環。
* [ ] **理解度門檻**：第一個大型 Input 之後必須緊跟一個 `comprehension_check`。
* [ ] **輸出遞進**：輸出練習順序必須是「組裝 (Assembly) -> 轉換 (Transform) -> 角色扮演 (Guided)」。
* [ ] **非對話輸入**：至少包含一個非對話形式的輸入（如：公告、簡訊、卡片）。

### B. 內容與可用性 (Content & Usability)

* [ ] **雙語完整性**：所有韓文內容均有對應的繁體中文翻譯，且無 `TODO` 或空值。
* [ ] **詞塊化傾向**：字典檔 (Dictionary Pack) 內容應以「詞塊 (Chunks)」為主（如：아침을 먹다），而非孤立單字（아침）。
* [ ] **互動一致性**：點選練習後，UI 反饋明確（例如：顯示正確答案）。
* [ ] **TTS 覆蓋**：所有 `dialogue` 與 `sample_lines` 均能觸發 TTS 語音。

### C. 系統穩定性 (System Stability)

* [ ] **切換隔離**：切換 U04 與 U05 時，狀態（進度、標記）應互不干擾。
* [ ] **狀態持久化**：重新整理網頁後，已標記的「標記完成」或「待回看」狀態應保留 (localStorage)。
* [ ] **響應式布局**：在手機視窗大小或平板視窗大小下，側選單與內容區塊不應重疊。

---

## 6. 問題分類指引 (Issue Triage Guide)

若發現問題，請按以下類別進行歸類回報：

| 類別 | 描述 | 範例 | 責任方 |
| :--- | :--- | :--- | :--- |
| **Fixture Content** | 內容錯誤、翻譯不通、標題錯字。 | 「美式咖啡」譯為「拿鐵」。 | Content Agent / Author |
| **Fixture Contract** | 欄位缺失、JSON 格式錯誤、ID 重複。 | 遺失 `learning_role` 欄位。 | Content Pipeline / Lint |
| **Viewer Renderer** | HTML/JS 渲染錯誤、排版跑掉、按鈕無效。 | 點擊「下一節」沒反應。 | Mockup Dev |
| **TTS/System** | 語音唸法錯誤、瀏覽器不支援發音。 | 某些字唸成日文。 | Browser / TTS Engine |

---

## 7. PM 驗證回報模板 (Reporting Template)

請 PM 在試玩結束後填寫以下表單（範例）：

> **單元驗證報告**
>
> * **試玩日期**：2026-02-25
> * **受測單元**：A1-U04, A1-U05
> * **總體結論**：[PASS / FAIL / PASS with minor issues]
>
> **具體反饋**：
>
> 1. [PASS] A1-U04 對話流暢，理解度檢核位置正確。
> 2. [ISSUE] A1-U05-P3 的中文題目描述略顯生硬，建議改為...
> 3. [SUGGEST] 建議 Viewer 的 TTS 可以加上發音速度調整。
> 4. [FIXED] U04 之前的 ID 重複問題已在本次試驗中確認修正。
