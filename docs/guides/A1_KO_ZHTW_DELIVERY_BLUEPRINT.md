# A1 KO:ZH-TW Delivery Blueprint

## 1. 完整度判斷 (A1 ko:zh-TW)

目前不是「只差補辭典翻譯」而已，還有一個對齊點：

- `content-ko` core dictionary atom IDs: `489`
- `content-ko` i18n dictionary atom IDs: `489`
- 但 `missing_i18n = 9`, `extra_i18n = 9`（POS 分類命名不一致）

典型差異：
- core: `ko:count:개`, `ko:det:무슨`
- i18n: `ko:num:개`, `ko:m:무슨`

結論：
1. 補齊辭典翻譯內容是必要條件。
2. 但還要先把這 9 個 ID 對齊（core/i18n 同 atom_id），前端查字才不會 miss。

---

## 2. 目標流程 (固定)

`content -> content-translate -> tokenize -> dict-translate -> speech`

---

## 3. Repo 職責與目錄

### 3.1 `content-ko` (Source of Truth)

```text
content-ko/
├─ content/
│  ├─ core/
│  │  ├─ dialogue/A1/*.json
│  │  ├─ article/*.json
│  │  └─ dictionary/atoms/**/*.json
│  └─ i18n/zh_tw/
│     ├─ dialogue/*.json
│     ├─ article/*.json
│     ├─ dictionary/*.json
│     └─ mapping.json
└─ scripts/ops/
   ├─ export_content_handoff.py
   └─ export_tokenize_handoff.py
```

產出到 handoff:
- `01-content/content.items.json`
- `03-tokenize/tokenize.items.json`
- `03-tokenize/dictionary.json`

### 3.2 `content-pipeline` (Translator/Packager)

```text
content-pipeline/
└─ scripts/handoff/
   ├─ run_handoff_stage.py
   └─ export_frontend_intake.py
```

產出到 handoff:
- `02-content-translate/content.translations.json`
- `04-dict-translate/dictionary.translations.json`
- `05-speech/timeline.json`
- `05-speech/audio/**/*`

額外產出前端可吃包:
- `staging/frontend_intake/<run_id>/packages/ko/course/*`
- `staging/frontend_intake/<run_id>/packages/ko/i18n/*`
- `staging/frontend_intake/<run_id>/packages/ko/manifest.json`

### 3.3 `core-schema` (Contract)

```text
core-schema/
├─ schemas/handoff_manifest.schema.json
└─ examples/handoff_manifest.json
```

### 3.4 `release-aggregator` (Control Tower)

```text
release-aggregator/
├─ staging/handoffs/<run_id>/01..05/
├─ staging/frontend_intake/<run_id>/packages/ko/
└─ docs/
```

---

## 4. 前端最終吃的包 (重點)

```text
packages/ko/
├─ course/
│  ├─ course.package.json
│  └─ timeline.json
├─ i18n/
│  ├─ dict_ko_zh_tw.json
│  ├─ Strings_zh_tw.json
│  └─ mapping.json
├─ core/                      # 相容層，避免舊路徑斷掉
│  ├─ course.package.json
│  └─ dictionary_core.json
└─ manifest.json
```

說明:
- 你要的兩塊是 `course/` + `i18n/`。
- `core/` 先保留相容，避免前端既有 `dictionary_core.json` 讀取路徑失效。

---

## 5. A1 KO:ZH-TW 交付門檻

1. A1 課程內容齊全（dialogue/article/subtitle）。
2. `dict-translate` 完整且 `mapping.json` 可解析。
3. core/i18n atom_id 零差異（目前差 9 需要修）。
4. `packages/ko/course` 與 `packages/ko/i18n` 可被 frontend ingest。
5. `manifest.json` 與 `handoff_manifest.schema.json` 驗證通過。
