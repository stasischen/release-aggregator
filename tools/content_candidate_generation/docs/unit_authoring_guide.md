
# Unit Blueprint Authoring Guide (v0)

這份文件說明如何撰寫與維護 `unit_blueprint_v0` 格式的單元清單 (Fixture)，供 HTML Mockup Viewer 使用。

## 1. 快速開始：生成骨架

使用以下命令為新單元生成基礎 JSON 檔案：

```bash
python3 tools/content_candidate_generation/bin/scaffold_unit.py \
  --id A1-UXX \
  --title "單元名稱" \
  --output docs/tasks/mockups/a1_uxx_unit_blueprint_v0.json
```

## 2. 核心結構說明

### `unit` (單元中繼資料)
- `unit_id`: 單元編號 (例如 `A1-U04`)。
- `level`: 難度等級 (`A1`, `A2`...)。
- `target_language`: 目標語言 (`ko`)。
- `can_do_zh_tw`: 學習者完成本單元後應能達到的能力描述。

### `sequence` (學習節點序列)
每個節點代表學習流程中的一個步驟。

- `id`: 節點唯一 ID (建議格式 `{UNIT_ID}-{TYPE}{NUM}`)。
- `candidate_type`: 內容類別 (`lesson`, `grammar_note`, `dictionary_pack`, `path_node`)。
- `content_form`: 呈現形式 (`dialogue`, `notice`, `pattern_card`, `functional_phrase_pack`, `practice_card`, `review_card`)。
- `learning_role`: 學習角色，決定渲染時的色調與分類：
  - `immersion_input`: 沉浸輸入 (對話、訊息、公告)
  - `structure_pattern`: 句型結構 (句型卡、詞塊包)
  - `structure_grammar`: 最小語法 (語法解說)
  - `controlled_output`: 可控輸出 (拼句練習、反應建構)
  - `immersion_output`: 任務輸出 (自由口說、訊息撰寫)
  - `review_retrieval`: 總結複習
- `payload`: 實際內容，結構取決於 `content_form`。
- `adapter_hints`: 前端渲染提示：
  - `content_renderer_key`: 指定 Body 區域使用的渲染器。
  - `interaction_renderer_key`: (選填) 指定互動區域使用的渲染器。

## 3. 欄位檢驗與 QA

在提交前，請務必執行 `mockup-check` 工具：

```bash
python3 tools/content_candidate_generation/bin/mockup_check.py docs/tasks/mockups/your_unit.json --verbose
```

## 4. 最佳實踐與檢查清單 (Checklist)

- [ ] **ID 唯一性**: 單元內所有節點 ID 不得重複。
- [ ] **語言一致性**: `text` 或 以 `_ko` 結尾的欄位應放置韓文；以 `_zh_tw` 結尾的欄位放置中文。
- [ ] **Renderer 映射**: 確保 `content_form` 與 `adapter_hints` 設置正確，否則 Viewer 可能無法顯示內容。
- [ ] **樣例句**: `sample_lines` 雖非渲染必備，但供 Agent 或 PM 快速預覽，請盡量提供。
- [ ] **邏輯順序**: 確保 `sequence` 的佈排符合學習路徑 (Input -> Structure -> Output -> Review)。
