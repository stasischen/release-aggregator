# Knowledge Lab 內容撰寫規範 (Content Specification)

本文件定義了 Knowledge Lab (知識文庫) 內容的撰寫標準，旨在確保所有知識點（文法、句型、慣用語等）具備一致的優質視覺呈現與良好的初學者互動體驗。

## 1. 核心結構：教學模組與 UI 樣式

Knowledge Lab 內容主要由 `explanation_md_zh_tw` (或各語系對應欄位) 構成。為了提供結構化且具備視覺引導的體驗，建議使用以下 Markdown 結構。

### UI 樣式與 Emoji 標記 (Demonstrative Style)
下表列出的標籤可用於觸發 Viewer 的 Bento UI 容器。這些 Emoji 標記僅為「UI 樣式暗示 (Style Hint)」，不應視為內容的硬性語義欄位。

| 樣式區塊 | UI 提示 (Demonstrative) | 建議內容 |
| :--- | :--- | :--- |
| **句型公式 (Formula)** | `### 📐` | 描述文法的形態變化規則（母音/子音結尾）。 |
| **注意事項 (Alert)** | `### ⚠️` | 提醒易錯點、敬語差異、常見陷阱。 |
| **實戰語境 (Context)** | `### 💬` | 說明此文法最常出現的場景（餐廳、機場、面試等）。 |

> [!TIP]
> **作者建議**：儘量保持標題文字簡潔。即使不使用 Emoji，內容依然會以標準 Markdown 標題呈現，具備完全的相容性。

---

## 2. 內容呈現層次

Knowledge Lab 的例句呈現分為三個層次，作者需根據教學目的選擇適合的層次：

### A. 全域例句引用 (Global Example Refs) - **Canonical**
*   **欄位**：JSON 中的 `example_sentence_refs` 陣列。
*   **用途**：引用 `example_sentence` 銀行中的標準例句。
*   **視覺**：顯示在頁面下方的「精選例句」區域。
*   **優點**：可重用、具備完整音檔與 POS 解析。

### B. 互動式行內例句 (Inline Sentence Chips) - **Authoring-convenient**
*   **語法**：`[ko:韓文|zh:中文|id:ID]`
*   **用途**：直接嵌入在 Markdown 說明中。
*   **視覺**：可點擊的藥丸形積木。
*   **場景**：用於形態變化示範 (e.g. `가요` -> `갈 거예요`) 或簡短對話片段。

### C. 純說明文本 (Plain Markdown)
*   **用途**：一般的解說文字。
*   **限制**：不具備互動播放功能，僅作為輔助說明。

---

## 3. 最佳實踐與檢查單 (Checklist)

- [ ] 標題是否使用了語意清晰的 Markdown Heading (H3)？
- [ ] 內文中的關鍵變形或對照是否已包裹為 `[ko:...|zh:...]` 格式？
- [ ] 形態變化規則是否已使用表格 (Table) 或清單 (List) 清晰呈現？
- [ ] 是否已從 `example_sentence_refs` 引用了至少 2-3 個「例句銀行」中的全域例句？
- [ ] 內容是否符合 [Knowledge Lab Markdown Profile](./KNOWLEDGE_LAB_MARKDOWN_PROFILE_V1.md) 規範？

---

## 4. 向後相容性 (Backward Compatibility)
- 舊版內容若未使用 Emoji 關鍵字，檢視器將以「一般 Markdown」模式呈現。
- **Migration Note**: 舊內容中的 `example_bank` (陣列) 應視為過渡期產物，未來將全數轉化為 A 層級 (Global Refs) 與 B 層級 (Inline Chips)。

