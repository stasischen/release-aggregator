# PEDOPT-008 — Listening Discrimination Micro-node Spec

## 1. Goal
定義一個輕量級、具備生產可行性的「聽辨（Listening Discrimination）」微節點規格。目標是在 A1/A2 單元中針對具備「生存風險」或「高頻誤導」的聽力特徵點，進行精確的聽辨檢查，且不增加語音製作流水線的沉重負荷。

本節點應能直接對接現有 Edge-TTS 流程，不依賴 ASR（語音辨識）或高品質聲學處理。

---

## 2. Node Purpose & Boundaries (用途與邊界)

### 2.1 用途 (Purpose)
- **Discrimination Only**: 專注於「區分」相似發音或高度相關的聽力特徵，而非「全篇聽力理解（Comprehension）」。
- **Survival Bottlenecks**: 針對生存場景中極易造成溝通誤會的點，如：
    - **Minimal Pairs**: 相似音（例如：韓文的 ㄱ/ㄲ/ㅋ 在單詞開頭）。
    - **Honorific/Formality**: 句尾階稱的聽辨（口語 vs 敬語）。
    - **Frequent Acoustic Confusions**: 數字（1 vs 2, 3 vs 4）、時間、方位词。

### 2.2 邊界 (Boundaries)
- **TTS-first**: 預設支援文字轉語音（TTS），不要求專門錄音。
- **Low Cognitive Load**: 每題只專注於 1 個區分點，不進行長對話聽力。
- **No Production Overhead**: 使用現有的 `practice_card` 或 `path_node` 結構擴展。

---

## 3. Payload Spec (資料結構)

```json
{
  "id": "Uxx-Lxx-LD",
  "node_type": "listening_discrimination_micro",
  "payload": {
    "discrimination_target": "minimal_pair | formality | numeral | particle",
    "prompt_zh_tw": "題目說明（例如：請問你聽到了哪個數字？）",
    "context_ko": "(選填) 輔助聽辨的前情提要",
    "audio_refs": [
      {
        "id": "audio_A",
        "text": "選項 A 播出的韓文文本",
        "tts_config": { "speed": 1.0, "voice": "standard" }
      }
    ],
    "options": [
      {
        "id": "opt_1",
        "text": "選項 1 文本 (中文或韓文)",
        "is_correct": true,
        "distractor_rationale": "敘述為何學習者可能會選錯（給 PM/作者看）",
        "feedback_zh_tw": "答錯時的回饋內容，需強調聽覺差異"
      }
    ],
    "correct_option_id": "opt_1",
    "difficulty_level": "A1 | A2",
    "fallback_zh_tw": "當音源不可用時的替代提示"
  }
}
```

---

## 4. Placement Rules (放置規則)

- **時機 (When)**: 
    - 緊接在核心 Pattern 第一次暴露 (`first_exposure`) 之後的一個或兩個節點。
    - 在進行大規模變體練習 (`transform_practice`) 之前。
- **頻率 (Frequency)**: 
    - 每個 Lesson 單元建議不超過 1-2 個 LD 節點。
    - 避免連續出現 LD 節點導致認知疲勞。
- **邏輯地位**: 作為「聽→認」的橋樑，確保在「認→說」之前地基是穩固的。

---

## 5. Scoring & Feedback (評分與回饋)

- **Scoring**: 
    - 二進位（True/False）。
    - 允許 Retry，但第二次答錯應直接顯示正確答案與「聽覺標註」（例如：highlight 差異音節）。
- **Immediate Corrective Feedback**: 
    - 答錯時，應提供對比分析。例如：「聽起來像 __，但尾音是 __ 代表這是複數形式。」
- **Feedback Style**: 
    - **A1**: 使用中文與簡單韓文標註。
    - **A2**: 加入簡單的語法意義說明。

---

## 6. Operational Constraints (運作約束)

- **TTS Compatibility**: 所有 `audio_refs` 必須在本地 pipeline 可直接通過 `tts_gen` 生成。
- **No Premium Dependency**: 設計時不應依賴特定角色音色，應以「中性辨識」為主。
- **Offline Fallback**: 若離線緩存未命中心，節點應顯示「文本閱讀」模式，並加註「視覺化聽辨提示」。

---

## 7. A1/A2 Examples

### 範例 1：A1 - Minimal Pair (咖啡廳)
- **Target**: ㄱ (G) vs ㅋ (K) 區分。
- **Scenario**: 點咖啡時，「兩杯 (두 개)」 vs 「四杯 (네 개)」的數字聽辨（針對 A1 基礎）。
- **Payload Sketch**:
    - `prompt_zh_tw`: 「請聽聽看，客人最後點了多少？」
    - `audio_ref`: 「네 개 주세요.」
    - `options`: 
        - `opt_1`: { "text": "四個", "is_correct": true }
        - `opt_2`: { "text": "三個", "is_correct": false }
    - `feedback_zh_tw`: 「聽到了 'ㄴ' (n) 的發音，所以是 '네' (4) 而非 '세' (3)。」
- **Signal**: 學習者是否能分辨高頻數字的發音差異。

### 範例 2：A1 - Formality (問候)
- **Target**: `-요` (結尾) vs `-ㅂ니다` (結尾) 的聽感區分。
- **Payload Sketch**:
    - `prompt_zh_tw`: 「這段話聽起來是在跟誰說話？」
    - `audio_ref`: 「만나서 반갑습니다.」
    - `options`: 
        - `opt_1`: { "text": "第一次見面的長輩 (正式)", "is_correct": true }
        - `opt_2`: { "text": "親近的朋友 (非正式)", "is_correct": false }
    - `feedback_zh_tw`: 「聽到了 '-습니다'，這是在正式場合常用的敬語。」
- **Signal**: 學習者對於韓文階稱環境的初步聽感。

### 範例 3：A2 - Tense (昨日行程)
- **Target**: 過去式雙收音 `ㅆ` 的聽辨。
- **Payload Sketch**:
    - `prompt_zh_tw`: 「這件事情發生了嗎？」
    - `audio_ref`: 「시장에 갔어요.」
    - `options`: 
        - `opt_1`: { "text": "已經去了 (過去)", "is_correct": true }
        - `opt_2`: { "text": "正要去 (現在/未來)", "is_correct": false }
    - `distractor_rationale`: 學習者容易忽略過去式的 `-았/었-` 聽感。
- **Signal**: 對於時態標記的聲音敏感度。

### 範例 4：A2 - Honorific Subject (關於父母)
- **Target**: `께서` vs `이/가` 助詞聽辨。
- **Payload Sketch**:
    - `prompt_zh_tw`: 「主角在談論誰？」
    - `audio_ref`: 「어머니께서 오셨어요.」
    - `options`: 
        - `opt_1`: { "text": "受尊敬的人物 (如：母親)", "is_correct": true }
        - `opt_2`: { "text": "平輩或自己", "is_correct": false }
- **Signal**: 學習者能否聽出「敬語助詞」所帶來的身分暗示。

---

## 8. PM Review Checklist

- [ ] **生產可行性**: 題目是否能僅靠 TTS 就達成教學目的？（不需要演員特定的情緒表演）
- [ ] **目標精確點**: `discrimination_target` 是否真的屬於該級別的 bottleneck？
- [ ] **反饋價值**: `feedback_zh_tw` 是否解釋了「怎麼聽出差異」？
- [ ] **干擾項設計**: `distractor_rationale` 是否合理？（不是隨機湊數，而是真的會混淆的音）
