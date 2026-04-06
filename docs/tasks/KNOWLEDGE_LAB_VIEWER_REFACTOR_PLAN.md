# Knowledge Lab Viewer 重構計畫

## 技術對齊 (已完成階段：文法、句型)

### 1. 輔助詳情介面覆蓋 (文法)

- **文法支援 (Grammar Support)**：採用結構化的 `sections`，支援 Markdown 並具備舊版相容性。
  - **回退優先順序 (Fallback Precedence)**：
    - **優先級 1**：`payload.sections` (若存在)。
      - 每個 section：先渲染 `explanation_md_i18n` (Markdown)，再渲染 `points_i18n` (清單)。兩者可共存。
    - **優先級 2**：`payload.points_i18n` 或 `payload.points_zh_tw` (舊版頂層回退)。
    - **優先級 3**：安全失敗 (Fail-soft，見下文)。

### 2. 句型支援與狀態持久化 (句型)

- **句型支援 (Pattern Lab Support)**：實作 `builder_id` 範疇的狀態持久化。
  - **動態合成 (Dynamic Synthesis)**：支援多個切換式句型生成器。
  - **狀態隔離 (State Scoping)**：使用 `builderId` 作為 key，確保存儲在 `interactionStateByNodeId` 中的選擇在跨節點導覽或頁面重新整理後能正確恢復。
  - **語系對齊 (Locale Alignment)**：確保切換控制項的使用者介面標籤與註解 (gloss) 均對齊教學語系 (Teaching Locale)。

### 2. Adapter 範疇與正規化

- **Adapter 角色**：嚴格限定在 **安全性與正規化 (Safety & Normalization)**。
    - 不進行語義變更，不發明新的文法專用結構。
    - 確保 `payload` 至少為 `{}`。
    - 正規化陣列欄位，並優雅處理缺失的 i18n 欄位解析。

### 3. 安全失敗 (Fail-Soft) 區分

- **情境：有效但為空 (Valid but Empty)**：若 `sections` 與頂層 `points` 均缺失或為空，但 `content_form` 已被識別，則顯示優雅的「無相關詳情」提示。
- **情境：格式錯誤 (Malformed Payload)**：若 payload 結構無效或關鍵鍵值缺失，則顯示「資料檢視 (Data Inspection)」視圖（原始 JSON），以利除錯。

## 驗證方式

### 手動驗證案例
1. **僅 sections**：驗證僅含標題與文字的 section 渲染。
2. **共存 (Coexistence)**：驗證同時含 `explanation_md_i18n` 與 `points_i18n` 的 section。
3. **舊版回退**：驗證僅含頂層 `points_i18n` 的 payload。
4. **有效但為空**：使用 `A1-U04-G2` 驗證優雅的「無詳情」狀態。
5. **格式錯誤**：測試注入無效 payload（如 `sections` 為字串）時的資料檢視視圖。

### 測試資料
- **主測試件**：`A1-GRAMMAR-L01` (節點 L1, L2, L3)。
- **安全失敗測試件**：`A1-U04` (節點 G2)。

## 後續階段 (第一階段不包含)

- **句型支援 (Pattern Support)**：實作 `builder_id` 範疇的狀態持久化。
- **用法支援 (Usage Support)***：與 `notice` / `support-module` 保持一致。
- **單字支援 (Vocab Support)**：預留位 (Reserved Slot) / 安全失敗處理。
