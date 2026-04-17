# CMOD-011: 內容下鑽與錨點連結開發規範 (Anchor Linking Spec)

## 1. 任務目標 (Goal)

實作課程內容的「語義分段（Segmentation）」與「行內錨點連結（Inline Anchor Linking）」契約。
讓學習者在閱讀句子時，能點擊特定的單字、詞組或句子片段，精準導向 Dictionary 或 Knowledge Lab 的對應條目。

## 2. 核心架構 (Core Architecture)

本規範擴展 `interaction_contract.knowledge_dive` 結構，引入位移（Offsets）機制以支援精確的行內標記。

### 2.1 實施位置
所有支援句子級下鑽的載體（Dialogue, Video Transcript, Article Sentence）應在 `interaction_contract.knowledge_dive` 中包含 `anchors` 陣列。

### 2.2 錨點資料結構
```json
{
  "interaction_contract": {
    "knowledge_dive": {
      "anchors": [
        {
          "surface": "생일카드",
          "offset": 7,
          "length": 4,
          "level": "chunk",
          "target": "topic_ref",
          "ref": "topic:ko:birthday"
        },
        {
          "surface": "오늘",
          "offset": 0,
          "length": 2,
          "level": "token",
          "target": "dictionary_atom_ref",
          "ref": "ko:n:오늘"
        }
      ]
    }
  }
}
```

## 3. 欄位定義 (Field Definitions)

| 欄位 (Field) | 類型 (Type) | 說明 (Description) |
| :--- | :--- | :--- |
| `surface` | string | 原始文本中的片段字串。用於前端渲染與容錯比對。 |
| `offset` | integer | 片段在母字串中的起始位移 (0-indexed)。 |
| `length` | integer | 片段字元長度。 |
| `level` | enum | 錨點層級：`token` (單字), `chunk` (詞組), `sentence` (全句)。 |
| `target` | enum | 下鑽目標類型：`dictionary_atom_ref`, `topic_ref`, `grammar_ref`。 |
| `ref` | string | 目標項目的唯一 ID。 |

### 3.1 錨點層級 (Anchor Levels)
- **`token`**: 最細顆粒度，對應 V5 字典中的原子（Atomic Word）。
- **`chunk`**: 語義區塊，由多個單字組成（如：複合名詞、固定搭配），通常連結至 Knowledge Lab 的 Topic。
- **`sentence`**: 覆蓋整句的錨點，通常用於連結至整句的語法解釋或情境分析。

### 3.2 下鑽目標 (Link Targets)
- **`dictionary_atom_ref`**: 指向 `content-ko` 的 V5 原子字典。ID 格式：`ko:pos:lemma` (例如 `ko:n:친구`)。
- **`topic_ref`**: 指向 Knowledge Lab 的主題條目（如：星期、數字）。ID 格式：`topic:<domain>:<id>`。
- **`grammar_ref`**: 指向語法知識點。ID 格式：`grammar:<lang>:<id>`。

## 4. 整合與驗證 (Integration & Validation)

### 4.1 與 CMOD-013 整合
- `CMOD-013` (Sentence Action Contract) 應優先使用 `anchors` 進行行內渲染。
- 若舊有資料僅包含 `dictionary_atom_refs` 或 `grammar_refs`（無位移資訊），前端應回退至「列表式下鑽」或嘗試進行全文檢索匹配（不推薦長期使用）。

### 4.2 驗證規範 (mockup_check.py)
`mockup_check.py` 應實施以下硬性校驗：
1. **邊界檢查 (Boundary Check)**: `offset + length` 必須小於等於所屬內容節點的文字長度。
2. **Ref 命名規範 (ID Naming)**:
   - `dictionary_atom_ref`: 必須符合 `core-schema` 的 `atom.schema.json` regex。
   - `topic_ref`: 必須以 `topic:` 為前綴。
   - `grammar_ref`: 必須以 `grammar:` 為前綴。
3. **重複性檢查**: 避免在相同位移範圍內出現多個完全重複的 `token` 錨點（不同 level 的重疊是允許的）。

## 5. 範例場景 (Example Scenario)

**輸入文字**: `오늘은 제가 생일카드를 가져왔어요.`

| Surface | Offset | Length | Level | Target | Ref |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 오늘 | 0 | 2 | token | dictionary_atom_ref | ko:n:오늘 |
| 생일카드 | 7 | 4 | chunk | topic_ref | topic:ko:birthday |
| 가져왔어요 | 12 | 10 | token | grammar_ref | grammar:ko:v-past-polite |

## 6. 後續執行 (Next Steps)
1. **更新驗證器**: 修改 `release-aggregator/scripts/mockup_check.py` 以支援 `anchors` 校驗。
2. **更新模板**: 在 `UNITFAC_005_AUTHORING_TEMPLATES.md` 中加入 `anchors` 範例。
3. **Pilot Data**: 將 `A1-U05` 的句子下鑽部分遷移至 `anchors` 格式。
