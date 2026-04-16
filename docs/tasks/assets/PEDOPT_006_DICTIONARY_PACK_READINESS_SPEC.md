# PEDOPT-006 — Dictionary Pack Production-Readiness Spec

## 1. Goal
為 `dictionary_pack` 中的字典項建立一套「生產就緒標籤（Readiness Tags）」契約。目標是讓 PM、內容作者與發佈流程能明確區分哪些詞彙是「可直接展示/練習的生產內容」，哪些僅是「輔助 parsing 或參考用的草案輸入」。同時透過 `frame_refs` 與 `register_hints` 強化詞彙與教學場景、語氣層級的連結。

---

## 2. Tag Model (生命週期標籤)

每個字典項（Dictionary Item）必須包含一個 `readiness_tag` 欄位。

| 標籤名稱 | 定義 | 適用場景 |
| :--- | :--- | :--- |
| **`production_ready`** | **正式生產環境**。已完成翻譯校對、語氣分類與音檔關連，可直接用於課文展示、單字卡、練習題。 | 教學核心詞、生存高頻詞塊。 |
| **`input_only`** | **僅供內部輸入/參考**。作為機器翻譯、自動抓取或解析依賴存在，尚未通過人工教學審閱，不應直接展示給端使用者。 | 輔助解析的詞頭、低頻派生詞、尚未校對的草案。 |

### 狀態流轉 (Lifecycle States)
1. **Initial**: 所有自動生成的詞項預設為 `input_only`。
2. **Reviewing**: 內容作者進行校對、補全 `register_hints`。
3. **Promoted**: 通過校對後轉為 `production_ready`。
4. **Archived**: (Optional) 若不再使用，標記為 `input_only` 並移除 `frame_refs`。

---

## 3. Schema Requirements (欄位定義)

在字典項的 `metadata` 或核心 Payload 中新增以下欄位：

### 3.1 `readiness_tag`
- **Type**: `enum`
- **Values**: `["production_ready", "input_only"]`
- **Default**: `input_only`

### 3.2 `frame_refs` (教學框架引用)
定義該詞項支援哪些教學環節。
- **Type**: `array<string>`
- **Namespace Design**:
  - `lesson:[UNIT_ID]:[SLOT]` (例：`lesson:A1_U04:main_dialogue`)
  - `grammar:[GRAMMAR_ID]` (例：`grammar:ko:n_j_topic`)
  - `retrieval:[STRATEGY]` (例：`retrieval:survival_ordering`)
- **Purpose**: 追蹤詞彙的教學覆蓋率，避免生產「孤兒詞」（無人引用的詞）。

### 3.3 `register_hints` (語氣提示)
定義詞項的社會語義屬性，對韓文等具備敬語體系的語言至關重要。
- **Type**: `object`
- **Fields**:
  - `formality`: `["formal", "informal", "neutral"]`
  - `politeness`: `["polite", "casual", "honorific"]`
  - `context_note_zh_tw`: 簡短的用法備註（例：「用於點餐對店員說」、「對平輩朋友用」）。

---

## 4. Promotion Rules (晉升準則)

從 `input_only` 轉為 `production_ready` 的強制條件 (Blockers)：

1. **[ ] 意義明確**：具備正確的 `zh_tw` 對應意義，非機器直譯。
2. **[ ] 語氣標註**：`register_hints` 必須填寫（對 A1/A2 生存場景尤為重要）。
3. **[ ] 框架關連**：必須至少有關連到一個 `frame_refs`，證明該詞在課程中有教學用途。
4. **[ ] 形態穩定**：若是動詞/形容詞，已確認基本階（Dictionary Form）正確，且支援預設的變化規則。

---

## 5. QA / Review Checks

### 作者自檢清單 (Author Checklist)
- [ ] 我是否已將本單元「必學」的詞塊標記為 `production_ready`？
- [ ] `frame_refs` 是否精準指向了當前單元的 `target_unit_id`？
- [ ] 對於點餐等生存任務，我是否標註了 `register_hints` 為 `polite`（避免學習者對陌生人用半語）？

### PM 審閱清單 (PM Checklist)
- [ ] **雜訊檢查**：是否有過多 `input_only` 詞項混入生產包？（會增加無謂的維護成本）。
- [ ] **語氣一致性**：`production_ready` 的詞項語氣是否與該單元的教學情境相符？
- [ ] **孤兒詞掃描**：有無 `production_ready` 但 `frame_refs` 為空的詞項？

---

## 6. A1/A2 Examples

### 範例 1：A1 - 點餐請求句 (Production Ready)
- **Foreign (KO)**: `주세요` (juseyo)
- **Meaning (zh-TW)**: `請給我...`
- **Readiness**: `production_ready`
- **Register Hints**:
  - `formality`: `informal` (口語常用)
  - `politeness`: `polite` (非正式敬語)
  - `context_note_zh_tw`: `標準點餐回應語氣。`
- **Frame Refs**: `["lesson:A1_U04:ordering", "retrieval:survival_request"]`
- **Rationale**: 核心功能詞，教學目標明確，應立即進入生產。

### 範例 2：A1 - 原始動詞解析 (Input Only)
- **Foreign (KO)**: `주다` (juda)
- **Meaning (zh-TW)**: `給` (基本階)
- **Readiness**: `input_only`
- **Frame Refs**: `[]`
- **Rationale**: A1 生存階段學習者僅需掌握 `주세요` 詞塊。`주다` 作為解析用的詞頭存在，不應直接出現在 A1 單字卡中增加認知負擔。

### 範例 3：A2 - 委婉婉拒 (Production Ready)
- **Foreign (KO)**: `괜찮습니다` (gwaenchanseumnida)
- **Meaning (zh-TW)**: `沒關係 / 不用了（客氣婉拒）`
- **Readiness**: `production_ready`
- **Register Hints**:
  - `formality`: `formal`
  - `politeness`: `polite`
  - `context_note_zh_tw`: `用於較正式場合或店員詢問是否需要其他服務時的禮貌拒絕。`
- **Frame Refs**: `["lesson:A2_U02:declining_offer"]`
- **Rationale**: A2 開始引入 Formal 語氣，需明確標註與 Informal Polite 的區別。

### 範例 4：A2 - 特定專業詞彙 (Input Only)
- **Foreign (KO)**: `유통기한` (yutonggihan)
- **Meaning (zh-TW)**: `有效期限`
- **Readiness**: `input_only`
- **Frame Refs**: `["reference_only"]`
- **Rationale**: 在藥局單元中可能在對話中提到，但非 A2 學習者必須精通的產出性詞彙。先作為輸入參考，不標記為生產就緒。

---

## 7. Consistency Alignment
- **Terminlogy**: 與 `PEDOPT-001~005` 一致，使用 `frame_refs` 取代舊有的 `can_do_links` 以整合更大的教學框架。
- **Adapter Safety**: `register_hints` 結構與前端 Adapter 預留欄位對齊，確保 UI 能根據 `politeness` 自動切換視覺提示（如：敬語色塊標記）。
