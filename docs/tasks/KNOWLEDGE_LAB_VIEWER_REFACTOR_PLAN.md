# Knowledge Lab Viewer 重構計畫

## 技術對齊 (已完成階段：文法、句型、視覺優化、自動化導入、內容對齊)

### 0. 自動化數據導入與對齊 (Phase KLABVIEW-005) - 已完成

- **動態 Manifest 生成**：編寫 `scripts/generate_library_manifest.py`，全量掃描 `content-ko` 內容。
- **自動掛載**：開發期間可用 `scripts/watch_library_manifest.py` 監看 `content-ko`，新條目一出現就重生 `library_manifest.json`。
- **閱讀器功能強化**：
  - **分級顯示**：支援 A1/A2/B1 標籤渲染。
  - **音檔播放**：實作「例句銀行」音檔按鈕，支援實體檔案與 Browser TTS 回退機制。
- **內容對齊 (Alignment)**：
  - **例句承接**：成功對齊「全域 `example_sentence` 引用」與「過渡期 `example_bank`」。
  - **Markdown Profile**：對齊 [Markdown Profile](../guides/KNOWLEDGE_LAB_MARKDOWN_PROFILE_V1.md)，支援 Bento UI (📐, ⚠️, 💬) 及 `[ko:|zh:]` 行內積木。

### 開發期運行方式

若要讓新條目在本機開發時自動掛進 manifest，請同時開啟：

```bash
python3 scripts/watch_library_manifest.py
```

這會持續監看 `content-ko/content/core/learning_library/knowledge` 與 `example_sentence` 目錄，並自動重生 `docs/tasks/mockups/modular/data/library_manifest.json`。

### 1. 視覺與體驗優化 (Phase KLABVIEW-004) - 已完成

- **適應性書卷佈局 (Adaptive Book Layout)**：
  - 轉向**全局目錄模式**，支援「文法」、「句型」、「連接詞」等主題式導航。
  - **行動端適應**：實作側邊欄抽屜 (Sidebar Drawer) 與手機閱讀器。
  - **Premium 渲染**：整合 `content-ko` 原始數據，支援 Markdown 詳盡解析與例句銀行。

### 1. 輔助詳情介面覆蓋 (文法/用法)

- **文法/用法支援 (Grammar/Usage Support)**：採用結構化的 `sections` 與頂層欄位，支援 Markdown 並具備舊版相容性。
  - **回退優先順序 (Fallback Precedence)**：
    - **內容渲染**：`explanation_md_i18n` > `explanation_md_zh_tw` > `explanation_i18n` > `explanation_zh_tw`。
    - **例句渲染**：`example_sentence_refs` (Canonical) > `example_bank` (Transitional)。
  - **Fail-soft**：若 payload 結構無效，顯示「資料檢視 (Data Inspection)」視圖。

### 2. 句型支援與狀態持久化 (句型)

- **句型支援 (Pattern Lab Support)**：實作 `builder_id` 範疇的狀態持久化。

### 2. Adapter 範疇與正規化

- **Adapter 角色**：嚴格限定在 **安全性與正規化 (Safety & Normalization)**。
    - 透過 `resolveExamples` 正規化例句來源。
    - 確保 `payload` 至少為 `{}`。
    - 正規化陣列欄位，並優雅處理缺失的 i18n 欄位解析。

### 3. 安全失敗 (Fail-Soft) 區分

- **情境：有效但為空 (Valid but Empty)**：若 `sections` 與頂層 `points` 均缺失或為空，但 `content_form` 已被識別，則顯示優雅的「無相關詳情」提示。
- **情境：格式錯誤 (Malformed Payload)**：若 payload 結構無效或關鍵鍵值缺失，則顯示原始 JSON 以利除錯。

## 驗證方式 (已完成)

### 手動驗證案例
1. **僅 Canonical**：驗證 `kg.grammar.particle.*` 成功承接全域例句。
2. **僅 Transitional**：驗證 `kg.connector.*` 成功顯示過渡期例句。
3. **共存 (Coexistence)**：驗證 Markdown 與 Resolved Examples 同時呈現。
4. **安全失敗**：驗證無內容或無效 payload 時的顯示正常。

### 測試資料
- **主測試件**：`kg.grammar.particle.also` (Canonical), `kg.connector.cause.geuraeseo` (Transitional)。
- **安全失敗測試件**：`A1-U04` (節點 G2)。

## 後續階段 (計畫中)

- **單字支援 (Vocab Support)**：預留位 (Reserved Slot) / 安全失敗處理。
- **內容正規化 (Normalization)**：依據 [Content Normalization Plan](./KNOWLEDGE_LAB_CONTENT_NORMALIZATION_PLAN_V1.md) 逐步將 Bucket B 提取至 Canonical。

## 內容規約收斂 (Spec Convergence)

- **Markdown Profile 凍結**：已完成。
- **Content Normalization**：計畫中。
- **Emoji Marker 定位**：確認作為 UI 示範樣式。
