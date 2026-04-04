# Asset Naming Policy (資產命名規範)

## Purpose (目的)
為了確保跨 Repo 之間資產索引的穩定性與自動化處理的準確性，所有產出的 JSON 資產檔案必須遵循特定的命名規範。

## Video Assets (影片資產 - Pattern 2)

適用於 `video/core/` 以及 `i18n/{target_lang}/video/` 資料夾下的檔案。

- **格式**: `{lang}_v{level}_{category}_{youtubeId}_{title}.json`
- **結構解析**:
  - `{lang}`: 來源語言代碼 (如 `ko`, `th`)
  - `v{level}`: 內容分級 (如 `v1`, `v2`, `v3`... 依據難度分別對應 TOPIK 1-6 / CEFR A1-C2)
  - `{category}`: 分類 (如 `vlog`, `music`, `social`)
  - `{youtubeId}`: YouTube 11 位字元 ID (如 `dpzJkC7hptY`)
  - `{title}`: 網頁友善的標題 (小寫，底線分隔)
- **範例**: `ko_v5_vlog_dpzJkC7hptY_seoul_walk.json`

## Dialogue Assets (對話資產 - Pattern 3)

適用於 `dialogue/` 或 `yarn/` 資料夾下的檔案。

- **格式**: `{lang}_l{level}_{category}_{id}.json`
- **結構解析**:
  - `{lang}`: 語言代碼
  - `l{level}`: 課堂分級 (如 `l0`, `l1`)
  - `{category}`: 分類 (如 `social`, `travel`)
  - `{id}`: 課堂 ID (如 `a1_01_greetings`)
- **範例**: `ko_l1_dialogue_a1_01.json`

## Enforcement (執行與驗證)

1. **Upstream (上游)**: `content-pipeline` 的 `integrity_gate.py` 會校驗 `dist/` 輸出。
2. **Downstream (下游)**: `lingo-frontend-web` 的 `asset_integrity_test.dart` 會作為預推檢核 (pre-push check)。

> [!IMPORTANT]
> 任何不符合上述規範的檔案將會導致 CI/CD 或 Pre-push 驗證失敗，阻斷合併與發佈。
