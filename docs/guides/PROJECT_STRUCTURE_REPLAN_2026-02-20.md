# Project Structure Replan (2026-02-20)

目標: 讓內容、翻譯(兩階段)、分詞、語音產線可獨立重跑、可追蹤、可發版，且可跨多個 repo 穩定交接。

## 0) 多 Repo 邊界 (新增)

| Repo | 角色 | 可寫入階段 | 主要產物 |
|---|---|---|---|
| `lllo` | 上游教材來源 | 無（唯讀） | 課程原文、對話稿、文章素材 |
| `content-ko` (或 `content-<lang>`) | 語言內容真相來源 | 01-content, 03-tokenize | `dialogue/article/youtube_subtitle` + `*.pos.json` + `dictionary.json` |
| `core-schema` | 契約與驗證法律條文 | 契約更新時 | JSON Schema, 版本規範 |
| `content-pipeline` | 通用 build/validate/translate/speech 引擎 | 02-content-translate, 04-dict-translate, 05-speech | `content.translations.json`, `dictionary.translations.json`, TTS 音檔, `timeline.json` |
| `release-aggregator` | 發版控制塔與清單聚合 | release cut 時 | `manifest.json`, 版本包, 發版紀錄 |
| `lingo-frontend-web` | 資產接收與執行 | intake 時 | `assets/content/*` production package |

### 0.1 Stage 與 Repo 對照

1. Stage 01 內容生產 (`content`): `content-<lang>`（由 `lllo` 匯入/生成）
2. Stage 02 內容翻譯 (`content-translate`): `content-pipeline`（只翻譯對話/文章/字幕）
3. Stage 03 分詞與詞典 (`tokenize`): `content-<lang>`（語言專用 tokenizer 與 POS）
4. Stage 04 詞典翻譯 (`dict-translate`): `content-pipeline`（只翻譯詞典 entries）
5. Stage 05 語音 (`speech`): `content-pipeline`（TTS 與時間軸）
6. Release 聚合: `release-aggregator`（整包並驗證契約）
7. Frontend Intake: `lingo-frontend-web`（接收 production assets）

### 0.2 Repo 交接規則

1. 只交接「版本化 artifacts」，不交接暫存中間檔。
2. 每次交接都必須帶 `run_id` 與 `schema_version`。
3. Schema 若有變更，先改 `core-schema`，再改下游 repo。
4. `release-aggregator` 不生成語言資料，只聚合、驗證、發版。

## 1) 建議目錄

註: 此處為「邏輯總覽」，實作時應依 `0) 多 Repo 邊界` 拆分到各自 repo，不應全部塞在同一 repo。

```text
release-aggregator/
├─ package.json
├─ yarn.lock
├─ tsconfig.json
├─ .env
├─ configs/
│  ├─ languages.json                    # 來源語言/目標語言設定
│  ├─ providers.json                    # LLM/TTS provider 設定
│  └─ pipeline.json                     # 批次大小、重試、輸出策略
├─ src/
│  ├─ cli/
│  │  └─ index.ts                       # yarn pipeline:* 入口
│  ├─ pipelines/
│  │  ├─ content/
│  │  │  ├─ dialogue.ts                 # 生產對話
│  │  │  ├─ article.ts                  # 生產文章
│  │  │  └─ youtube_subtitle.ts         # 生產 youtube 字幕
│  │  ├─ tokenize/
│  │  │  ├─ dialogue_pos.ts             # 對話分詞+POS
│  │  │  ├─ article_pos.ts              # 文章分詞+POS
│  │  │  ├─ subtitle_pos.ts             # 字幕分詞+POS
│  │  │  └─ dictionary.ts               # 產生辭典表
│  │  ├─ translate/
│  │  │  ├─ dialogue.ts                 # 對話翻譯
│  │  │  ├─ article.ts                  # 文章翻譯
│  │  │  ├─ subtitle.ts                 # 字幕翻譯
│  │  │  └─ dictionary.ts               # 辭典翻譯
│  │  └─ speech/
│  │     ├─ tts.ts                      # 產生 TTS 音檔
│  │     └─ timeline.ts                 # 產生時間軸
│  ├─ services/
│  │  ├─ llm.ts
│  │  ├─ tokenizer.ts
│  │  ├─ translator.ts
│  │  ├─ tts.ts
│  │  └─ youtube.ts
│  ├─ contracts/
│  │  ├─ content.ts
│  │  ├─ token.ts
│  │  ├─ translation.ts
│  │  ├─ dictionary.ts
│  │  └─ timeline.ts
│  └─ utils/
│     ├─ io.ts
│     ├─ id.ts
│     └─ logger.ts
├─ data/
│  ├─ runs/
│  │  └─ <run_id>/
│  │     ├─ 01-content/
│  │     │  ├─ dialogue.json
│  │     │  ├─ article.json
│  │     │  └─ youtube_subtitle.json
│  │     ├─ 02-tokenize/
│  │     │  ├─ dialogue.pos.json
│  │     │  ├─ article.pos.json
│  │     │  ├─ subtitle.pos.json
│  │     │  └─ dictionary.json
│  │     ├─ 03-translate/
│  │     │  ├─ dialogue.translations.json
│  │     │  ├─ article.translations.json
│  │     │  ├─ subtitle.translations.json
│  │     │  └─ dictionary.translations.json
│  │     └─ 04-speech/
│  │        ├─ audio/
│  │        │  ├─ dialogue/
│  │        │  ├─ article/
│  │        │  └─ subtitle/
│  │        └─ timeline.json
│  └─ releases/
│     └─ <release_tag>/
│        ├─ manifest.json
│        ├─ content/
│        ├─ tokenize/
│        ├─ translate/
│        └─ speech/
├─ tests/
│  ├─ contracts/
│  ├─ pipelines/
│  └─ fixtures/
└─ docs/
   ├─ guides/
   └─ runbooks/
```

## 2) 產線對應 (你提供的需求)

- 內容:
  - 生產 `dialogue/article/youtube_subtitle` (由 `yarn pipeline:content` 觸發)
- 分詞:
  - 產生三種內容的 `*.pos.json`
  - 產生 `dictionary.json`
- 翻譯:
  - 產生三種內容的 `*.translations.json`
  - 產生 `dictionary.translations.json`
- 語音:
  - 產生 TTS 音檔
  - 產生 `timeline.json`

## 2.1 跨 Repo 交接檔案

- `content-<lang>` -> `content-pipeline` (for Stage 02)
  - `01-content/*.json`
- `content-<lang>` -> `content-pipeline` (for Stage 04/05)
  - `03-tokenize/*.pos.json`
  - `03-tokenize/dictionary.json`
- `content-pipeline` -> `release-aggregator`
  - `02-content-translate/content.translations.json`
  - `04-dict-translate/dictionary.translations.json`
  - `05-speech/audio/**/*`
  - `05-speech/timeline.json`
- `release-aggregator` -> `lingo-frontend-web`
  - `releases/<release_tag>/manifest.json`
  - `releases/<release_tag>/{content,tokenize,translate,speech}/**/*`

## 3) 檔名與欄位最小契約

### 3.1 content JSON

```json
{
  "run_id": "20260220_ko_zhTW",
  "source_lang": "ko",
  "items": [
    {
      "id": "dlg_0001",
      "type": "dialogue",
      "text": "...",
      "meta": {}
    }
  ]
}
```

### 3.2 POS JSON

```json
{
  "run_id": "20260220_ko_zhTW",
  "source": "dialogue",
  "items": [
    {
      "id": "dlg_0001",
      "tokens": [
        { "surface": "...", "lemma": "...", "pos": "NOUN", "start": 0, "end": 2 }
      ]
    }
  ]
}
```

### 3.3 dictionary JSON

```json
{
  "run_id": "20260220_ko_zhTW",
  "entries": [
    { "lemma": "...", "pos": "NOUN", "freq": 12, "sources": ["dialogue", "article"] }
  ]
}
```

### 3.4 translations JSON

```json
{
  "run_id": "20260220_ko_zhTW",
  "target_lang": "zh-TW",
  "items": [
    { "id": "dlg_0001", "text": "...", "translation": "..." }
  ]
}
```

### 3.5 timeline JSON

```json
{
  "run_id": "20260220_ko_zhTW",
  "audio_root": "./audio",
  "segments": [
    {
      "id": "dlg_0001",
      "audio": "dialogue/dlg_0001.mp3",
      "start_ms": 0,
      "end_ms": 1820,
      "text": "..."
    }
  ]
}
```

## 4) Yarn scripts (最小可用)

```json
{
  "scripts": {
    "pipeline:content": "tsx src/cli/index.ts content",
    "pipeline:content-translate": "tsx src/cli/index.ts content-translate",
    "pipeline:tokenize": "tsx src/cli/index.ts tokenize",
    "pipeline:dict-translate": "tsx src/cli/index.ts dict-translate",
    "pipeline:speech": "tsx src/cli/index.ts speech",
    "pipeline:all": "yarn pipeline:content && yarn pipeline:content-translate && yarn pipeline:tokenize && yarn pipeline:dict-translate && yarn pipeline:speech",
    "test": "vitest run"
  }
}
```

## 4.1 建議拆分到各 Repo 的 scripts

### `content-<lang>/package.json`

```json
{
  "scripts": {
    "pipeline:content": "tsx src/cli/index.ts content",
    "pipeline:tokenize": "tsx src/cli/index.ts tokenize",
    "pipeline:prepare-handoff": "tsx src/cli/index.ts prepare-handoff"
  }
}
```

### `content-pipeline/package.json`

```json
{
  "scripts": {
    "pipeline:content-translate": "tsx src/cli/index.ts content-translate",
    "pipeline:dict-translate": "tsx src/cli/index.ts dict-translate",
    "pipeline:speech": "tsx src/cli/index.ts speech",
    "pipeline:validate-handoff": "tsx src/cli/index.ts validate-handoff"
  }
}
```

### `release-aggregator/package.json`

```json
{
  "scripts": {
    "release:aggregate": "python scripts/release.py aggregate",
    "release:verify": "python scripts/release.py verify",
    "release:cut": "python scripts/release.py cut"
  }
}
```

## 5) 執行順序與邊界

1. `content-<lang>` 的 `content` 只寫 `01-content/`。
2. `content-pipeline` 的 `content-translate` 只讀 `01-content/`，只寫 `02-content-translate/`。
3. `content-<lang>` 的 `tokenize` 只讀 `01-content/`，只寫 `03-tokenize/`。
4. `content-pipeline` 的 `dict-translate` 只讀 `03-tokenize/dictionary.json`，只寫 `04-dict-translate/`。
5. `content-pipeline` 的 `speech` 只讀 `01-content/` 或 `02-content-translate/`（依產品需求），只寫 `05-speech/`。
6. `release-aggregator` 只做聚合、驗證、封版，不回寫上游。
7. 每個 stage 不覆蓋前一 stage 檔案，失敗可重跑單一 stage。

## 6) 兩階段導入

1. Phase A (先穩定跨 repo 交接): 先固定 `run_id + schema_version + 01~05 artifacts` 的交接規格。
2. Phase B (再優化品質): 補齊 POS 標準、字典去重策略、翻譯術語表、TTS 對齊規則。
3. Phase C (自動化 release): 在 `release-aggregator` 實作自動 manifest 與 frontend intake 檢核。
