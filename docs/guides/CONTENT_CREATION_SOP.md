# Content Creation & Quality Assurance SOP

本文件定義了 Lingo 所有語言課程內容產出的標準作業流程（SOP），包含編寫、在地化與品質審計。

## 1. 目錄結構標準
內容應遵循 「Course First」 結構，路徑固定為 `data/courses/{lang}/{level}/`。

- `ko/`: 韓語課程
- `th/`: 泰語課程
- `locales/zh-TW/`: 繁體中文在地化內容

## 2. 課程編寫流程 (Transcreation)

### 步驟 1: 定義單元 (Preparation)
- 確認該級別的 **Persona (人物誌)**：角色集合、角色關係、說話調性。
- 確認 **Speech Level (語體)**：例如韓語的 Banmal, Haeyo-che, Hapsyo-che。

### 步驟 2: 編寫對話 (Dialogue - Yarn)
- 使用 `.yarn` 格式。
- 每行必須包含唯一的 ID 標籤：`#line:Lxx-Dxx-xx`。
- 對話中 100% 使用目標語言，不夾雜翻譯。

### 步驟 3: 語法說明 (Grammar Article - Markdown)
- 在 `locales/{lang}/{level}/` 下編寫 Markdown 說明。
- 優先使用模組化標籤（例如 `<module:conjugation-polite>`）以減少重複。

### 步驟 4: 在地化翻譯 (Localization - CSV)
- 在 `locales/{lang}/{level}/` 下編寫 `Lxx.csv`。
- 欄位固定為 `id, text`。

## 3. 品質檢查清單 (QA Checklist)
在提交任何內容批次前，必須檢查：

- [ ] **人物一致性**：角色名稱與關係是否符合 Persona 定義。
- [ ] **語體一致性 (Register Hygiene)**：結尾、代名詞（我/我）是否統一。
- [ ] **技術驗證**：
    - 目錄命名符合 `^L[0-9]{2}-[A-Za-z0-9-]+$`。
    - 跑 `python tools/content_builder.py` 通過 Build。
- [ ] **Git 衛生**：嚴禁提交生成的 `content.js` 等開發中產物。

---
**備註**: 本文件整合自 `lllo` 倉庫的實踐規範。
