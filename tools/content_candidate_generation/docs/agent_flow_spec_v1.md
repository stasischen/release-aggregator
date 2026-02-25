# Agent Flow Specification (v1)

本文定義 `CONTENT_CANDIDATE_GENERATION_FRAMEWORK` 中 Agent Flow 的執行規格，包含 Gap Analysis、Generation 與 Self-Review 階段。

## 1. Gap Analysis Spec (AGG-GEN-009)

Agent 在生成前需分析現有內容，產出 `gap_report.json`。

### Output Schema: `gap_report.json`
- `summary_zh_tw`: (必填) 繁體中文總結調查結果。
- `gaps`: (列表)
    - `gap_id`: 唯一識別碼。
    - `description_zh_tw`: (必填) 具體的缺口描述。
    - `priority`: `high` | `med` | `low`。
    - `target_unit`: 目標單元 ID。
    - `missing_concepts`: (必填) 缺失的概念或關鍵字列表。

## 2. Agent Generation Spec (AGG-GEN-010)

Agent 產出的候選內容需包含以下「必填中文審核欄位」：

| 欄位名 | 說明 | 範例 |
| :--- | :--- | :--- |
| `title_zh_tw` | 課程/項目名稱 | `A1-U04 基礎問候變體` |
| `subtitle_zh_tw` | 副標題/簡短說明 | `學習如何用非正式語氣打招呼` |
| `can_do_zh_tw` | 學完後能做什麼 (List) | `["能使用安寧哈瑟喲以外的問候語"]` |
| `review_summary_zh_tw` | 中文摘要 (給審核員) | `本課程補充了三種常見的非正式問候...` |
| `placement_rationale_zh_tw` | 位置編排考量 | `放在 U04-L2 之後，因為銜接了主詞助詞的用法。` |

## 3. Agent Self-Review Spec (AGG-GEN-011)

Agent 需對生成的內容進行自我評量，產出評分與建議。

### 評量指標 (Score 0-1)
- `fit`: 教學目標契合度。
- `novelty`: 內容新鮮度/是否與舊有重複。
- `learnability`: 易讀性/教學難度適中性。
- `reuse`: 內容可複用性。
- `engagement`: 趣味性/情節吸引力。
- `cost`: 製作成本 (1 表示成本極低，0 表示成本極高)。

### 審核欄位
- `agent_recommendation`: `accept` | `revise` | `reject`。
- `novelty_rationale_zh_tw`: 新鮮度理由（為什麼不是重複的？）。
- `risk_flags_zh_tw`: 風險標記 (例如：使用了未教過的進階單字)。

## 4. Agent Raw Output Format (For Normalization)

Agent 產出的 `candidate_packs.agent.raw.json` 結構範例：

```json
{
  "batch_id": "20260225_A1_U04_agent_v1",
  "candidates": [
    {
      "internal_id": "agent-001",
      "type": "lesson",
      "planning": {
        "title": "韓文初音：不同的問候",
        "rationale": "現有單元過於死板",
        "placement": "after A1-U04-L2"
      },
      "pedia": {
        "summary": "介紹多種問候語",
        "can_do": ["學會正式語與非正式語"],
        "novelty": "使用了當代潮流用語"
      },
      "validation": {
        "scores": {
          "fit": 0.9,
          "novelty": 0.8,
          "learnability": 0.9,
          "reuse": 0.7,
          "engagement": 0.8,
          "cost": 0.9
        },
        "recommendation": "accept",
        "risk": ["包含 A2 單字"]
      },
      "payload": {
        "foreign_preview": "안녕, 반가워..."
      }
    }
  ]
}
```

這將由 `normalize_candidates.py` 轉換為 Canonical Schema。
