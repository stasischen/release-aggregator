# Knowledge Lab Markdown Profile V1

本文件定義了 Knowledge Lab (知識文庫) 教學內容所使用的 Markdown 子集規範。為了確保內容能在多端（Web Viewer, Flutter App）一致呈現且具備高度互動性，作者應嚴格遵守此 Profile，避免使用未定義的擴充語法。

## 1. Canonical Markdown Subset (標準子集)

以下為 Viewer 穩定支援且正式列入 canonical 的語法：

### A. 標題 (Headings)
*   支援 `H1` (#), `H2` (##), `H3` (###)。
*   `H1`, `H2` 通常用於大章節或頁面標題；`H3` 常配合 Bento UI Style 做區塊分割。

### B. 列表 (Lists)
*   **無序列表**：使用 `- ` 或 `* `。
*   **有序列表**：使用 `1. `, `2. ` 等。

### C. 文字格式 (Text Styling)
*   **粗體**：`**text**`
*   **斜體**：`*text*`
*   **行內程式碼**：`` `code` `` (用於標注韓文拼寫或文法成分)

### D. 表格 (Tables)
*   支援標準 GFM 表格語法：
    ```markdown
    | 表頭 | 表頭 |
    | :--- | :--- |
    | 內容 | 內容 |
    ```

### E. 連結 (Links)
*   `[顯示文字](URL)`：僅限外部參考連結。

---

## 2. Interactive Tokens (互動擴充語法)

這是 Lingourmet 專屬的互動標記，屬於 canonical 規範：

### A. 行內例句積木 (Inline Sentence Chips)
*   **語法**：`[ko:韓文原文|zh:中文翻譯|id:例句ID(可選)]`
*   **功能**：在 UI 中呈現為可點擊、可發音的藥丸狀積木。
*   **建議**：短語、單詞對照、或教學內文中的關鍵短句應優先使用此格式。

---

## 3. Demonstrative UI Styles (示範 UI 樣式)

以下標籤用於觸發特定的 UI 容器效果（Bento Boxes），但在內容儲存層級，它們應視為「樣式暗示」而非「語義標籤」：

*   `### 📐 標題`：觸發「句型公式」樣式（通常帶有尺規圖示與藍色外框）。
*   `### ⚠️ 標題`：觸發「注意事項」樣式（通常帶有警告圖示與黃色外框）。
*   `### 💬 標題`：觸發「語境說明」樣式。

**註記**：這些 Emoji Marker 僅供示範 UI 渲染效果。若不帶 Emoji，Viewer 將以一般 `H3` 標題樣式呈現。

---

## 4. Non-Canonical / Forbidden (非正式或禁止語法)

以下語法目前 **不建議** 或 **嚴格禁止** 使用於 Knowledge Lab 正式內容中：

*   ❌ **GitHub Admonitions**：例如 `> [!NOTE]`，Viewer 不保證正確渲染。
*   ❌ **自訂 HTML 標籤**：例如 `<module:...>`、`<div>`。
*   ❌ **複雜嵌入 (Embeds)**：如 YouTube Iframe、Iframe 嵌入等。
*   ❌ **多層嵌套表格**：表格內不可包含表格。

---

## 5. Content Hierarchy (內容層級建議)

1.  **Explanatory Markdown (說明文本)**：使用上述規範撰寫的文字、列表、表格。
2.  **Inline Sentence Chips (行內積木)**：嵌入在說明文本中的 `[ko:|zh:]` 積木，供即時點擊。
3.  **Global Example Refs (全域引用)**：在 JSON 中的 `example_sentence_refs` 引用全域 `example_sentence` 銀行的例句。

---
