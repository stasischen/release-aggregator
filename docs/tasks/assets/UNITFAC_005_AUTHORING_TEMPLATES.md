# UNITFAC-005 — Authoring Template Pack (Fixture Production)

本文件提供 Lingourmet 課程單元 Fixture（Mockup Blueprint）的作者指引、填寫模板與 QA 核查清單。

> [!NOTE]
> 所有 Fixture 在提交前必須通過 `release-aggregator/scripts/mockup_check.py` 驗證。

---

## 1. Mockup-Check 驗證規則 (Blockers & Warnings)

在填寫時，請務必遵守以下規則，否則工具會回報錯誤或警告。

### 🚫 Blocker (Error) - 必須修正否則無法過關
- **JSON_INVALID**: 檔案必須是標準 JSON 格式。
- **MISSING_FIELD**: Top-level 必須包含 `version`, `unit`, `sequence`。
- **MISSING_UNIT_FIELD**: `unit` 物件必須包含 `unit_id`, `level`, `target_language`, `title_zh_tw`。
- **INVALID_SEQUENCE**: `sequence` 必須是陣列（List）。
- **MISSING_NODE_ID**: 每個 sequence 節點必須有唯一的 `id` (例如 `U04-L1`)。
- **MISSING_NODE_FIELD**: 每個節點必須包含 `candidate_type`, `content_form`, `learning_role`, `title_zh_tw`。
- **DUPLICATE_NODE_ID**: 單元內不可有重覆的 Node ID。
- **INVALID_CANDIDATE_TYPE / INVALID_CONTENT_FORM / INVALID_LEARNING_ROLE / INVALID_OUTPUT_MODE**: 只能使用 Allowlist 中定義的值。
- **ERR_MIN_NODE_COUNT**: 成熟單元（Production-Ready）至少需要 10 個節點。
- **ERR_MISSING_ROLE**: 必須包含 `immersion_input`, `structure_pattern`, `review_retrieval` 這三類角色。
- **ERR_ORDER_VIOLATION**: 練習與產出節點（Output）不可出現在教學節點（Input）之前。
- **ERR_MISSING_COMPREHENSION (New Pilot Only)**: 在新開發的 Pilot（如 A1-U05）中，此項為 **Blocker**。第一個 Input 之後必須緊接一個 `comprehension_check`。

### ⚠️ Warning (Warning) - 強烈建議修正，除非有特殊理由
- **ERR_MISSING_COMPREHENSION (Legacy)**: 對於既有舊單元（如 A1-U04），暫時視為 Warning。
- **MISSING_PAYLOAD_FIELD**: 
    - `content_form: dialogue` 應包含 `payload.dialogue_turns`。
    - `content_form: pattern_card` 應包含 `payload.frames`。
- **LANG_EXPECTATION_MISS**:
    - `sample_lines` 應該包含韓文字符（[\uac00-\ud7af]）。
    - 欄位名為 `zh_tw` 或以 `_zh_tw` 結尾者，不應只包含韓文（可能填錯欄位）。
- **MIXED_SCRIPT_GUARD**:
    - 欄位名為 `text` 或以 `_ko` 結尾者，若包含中文字符，必須同時包含韓文字符（避免只有翻譯卻放在原文欄位）。

---

## 2. 核心欄位規範 (Allowlist)

為了確保橫向相容性，請僅使用以下定義的值。

### Candidate Type
- `lesson`: 主要教學內容節點。
- `grammar_note`: 語法說明或焦點節點。
- `dictionary_pack`: 詞彙包、短語包。
- `path_node`: 練習、任務或測驗節點。

### Content Form
- `dialogue`: 對話流。
- `notice`: 公告、指示、短看板。
- `message_thread`: 通訊軟體對話。
- `comparison_card`: 兩者比較選擇。
- `pattern_card`: 句型模板卡。
- `grammar_note`: 純文字/圖文語法說明。
- `functional_phrase_pack`: 功能性詞彙包。
- `practice_card`: 練習題型。
- `roleplay_prompt`: 口說角色扮演任務。
- `message_prompt`: 寫作任務（訊息）。
- `review_card`: 複習與存檔節點。

### Learning Role
- `immersion_input`: 純沉浸輸入（聽/讀）。
- `structure_pattern`: 句型與詞組模式建立。
- `structure_grammar`: 語法解析。
- `controlled_output`: 受控產出（組裝、選擇）。
- `immersion_output`: 沉浸產出（角色扮演、訊息撰寫）。
- `review_retrieval`: 複習回扣。

### Output Mode
- `none`: 無需使用者產出（純顯示）。
- `frame_fill`: 句框填空。
- `chunk_assembly`: 詞塊組裝。
- `response_builder`: 多選一回應組裝。
- `guided_typing`: 導引式打字練習。
- `guided_speaking`: 導引式口說練習。
- `guided`: (Legacy) 舊版導引式任務。
- `review_retrieval`: 複習擷取。

---

## 3. Payload 寫作模板

### Dialogue (對話)
```json
"payload": {
  "dialogue_turns": [
    {
      "speaker": "角色名",
      "text": "韓文原文",
      "zh_tw": "繁體中文翻譯"
    }
  ]
}
```

### Comprehension Check (理解檢查)
```json
"payload": {
  "question_type": "info_extract | intent | next_response | sequence",
  "prompt_zh_tw": "題目描述",
  "options": [
    { "text": "對的選項", "is_correct": true, "feedback_zh_tw": "對的解析" },
    { "text": "錯的選項", "is_correct": false, "feedback_zh_tw": "錯的提示" }
  ]
}
```

### Pattern Card (句型卡)
```json
"payload": {
  "frames": [
    {
      "frame": "___ (item) 주세요.",
      "use_zh_tw": "使用場景描述",
      "slots_zh_tw": ["槽位 1 說明", "槽位 2 說明"]
    }
  ],
  "grammar_help_zh_tw": "畫面上方的快速指引"
}
```

### Pattern Transform (變體練習)
```json
"payload": {
  "transform_type": "slot | scenario | function | politeness | correction",
  "base_sentence_ko": "저는 커피를 마셔요.",
  "instruction_zh_tw": "請換成「茶」來練習",
  "tasks": [
    {
       "prompt_zh_tw": "換成：茶 (차)",
       "target_examples": ["저는 차를 마셔요."]
    }
  ]
}
```

### Review Retrieval (複習檢索)
```json
"payload": {
  "target_type": "form | function | mixed",
  "retrieval_focus": "本次檢索的核心重點",
  "context_zh_tw": "情境描述",
  "prompt_zh_tw": "提示文字",
  "target_examples": ["標準答案"]
}
```

### Practice Card (詞塊組裝題)
```json
"payload": {
  "mode": "chunk_assembly",
  "tasks": [
    {
      "prompt_zh_tw": "題目描述",
      "chunks": ["詞塊 A", "詞塊 B", "詞塊 C"],
      "chunk_gloss_by_ko": { "詞塊 A": "翻譯 A" },
      "target_examples": ["標準完整答案"],
      "target_examples_zh_tw": ["標準答案翻譯"]
    }
  ]
}
```

---

## 4. CMOD 模組化元數據 (Modular Metadata)

對於已遷移至 CMOD 架構的內容，應包含以下擴展欄位以解耦內容與互動。

### Interaction Modes (回答路徑集)
```json
"interaction_modes": ["response_builder", "guided_typing", "guided_speaking"],
"default_interaction_mode": "response_builder"
```

### Completion Rules (完成判準)
```json
"completion_rules": {
  "required_modes": ["guided_typing"],
  "min_attempts": 1,
  "pass_policy": "manual_mark_after_required_modes"
}
```

### Review Policy (複習策略)
```json
"review_policy": {
  "enabled": true,
  "card_source": {
    "prefer_carrier": true,
    "include_support": ["pattern_card"]
  },
  "spacing_semantics": {
    "profile": "same_day_plus_1_plus_3",
    "intensity": "high"
  },
  "card_policies": {
    "recognition": { "priority": 10, "cue_type": "audio_first" },
    "recall": { "priority": 20, "cue_type": "meaning_first" },
    "response": { "priority": 30, "cue_type": "scenario_context" }
  },
  "cue_source_preference": ["carrier_context", "sentence_surface", "grammar_rule"]
}
```

---

## 5. 教育品質核查清單 (Educational QA Checklist)

#### 骨架結構 (Unit Skeleton)
- [ ] **Scaffolding**: 單元安排是否遵循從沉浸輸入 -> 句型建模 -> 受控練習 -> 自由產出的順序？
- [ ] **Balance**: 聽、讀、說、寫的比例是否平衡？(Target `output_ratio_target` 應介於 0.3 - 0.6)
- [ ] **Retrieval**: 單元末尾是否有 `review_card` 進行無提示回想？
- [ ] **Pedagogy Metadata**: 所有 `comprehension_check`, `pattern_transform`, `repair_practice`, `review_card` 是否都填寫了對應的 `type` 標籤？

#### 內容質量 (Content Quality)
- [ ] **CC Diversity**: 理解檢查題型是否多樣（不只有資訊提取）？
- [ ] **Transform Transfer**: 變體練習是否包含 `scenario` 或 `function` 遷移，而非單純換名詞？
- [ ] **Followup Semantics**: `scheduled_followups` 是否標明了 `followup_type` (review/transfer)？
- [ ] **Bilingual**: 所有 `zh_tw` 翻譯是否準確且符合台灣用語習慣（非機器直譯）？
- [ ] **Honorifics**: 韓文敬語等級在單元內是否一致（例如 A1 預設使用 해요體）？
- [ ] **Authenticity**: 對話是否自然？（避免像機器人般的課本對話）

### 資源連接 (Resources)
- [ ] **Lexicon**: 重要的 `dictionary_terms` 是否都有在節點中定義，以便後續關聯解析？
- [ ] **Grammar**: 每個 `path_node` 的 `resource_links` 是否連結了正確的語法說明？

---

## 5. 交付定義 (Minimum Definition of Done)

作者在執行量產任務時，需達到以下里程碑方可進入下一階段：

### 🟢 Milestone 1: Scaffold-complete
- [ ] 執行 `scaffold_unit_blueprint.py` 生成骨架。
- [ ] 所有節點 ID 與基礎教育地圖（Learning Role）已填寫完畢。
- [ ] `mockup-check` 通過，無 **Blocker**。

### 🔵 Milestone 2: Authoring-complete
- [ ] 所有節點的 `payload` 已填寫完成（文本、翻譯、選項）。
- [ ] `dictionary_terms` 與核心句型已對齊課程內容。
- [ ] `mockup-check` 通過，且無重大 **Warning**。

### 🟣 Milestone 3: PM-review-ready
- [ ] 課程已註冊至 `fixtures.json`。
- [ ] 在 Modular Viewer 中可流暢試玩，無渲染錯誤。
- [ ] 自會審核：已核對第 4 節的教育品質核查清單。
