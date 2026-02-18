# TTS Generation RunBOOK (語音生成操作手冊)

本手冊說明如何使用 `content-pipeline` 中的工具自動生成高品質的韓語語音檔 (TTS)。

## 1. 核心工具

- **腳本路徑**: `content-pipeline/scripts/tts/generate_edge_tts.py`
- **技術棧**: Python + [Edge-TTS](https://github.com/rany2/edge-tts) (Microsoft Edge 高品質神經網路發音)

## 2. 環境安裝

在使用前，請確保已安裝 `edge-tts` 依賴套件：

```bash
# 建議在 content-pipeline 目錄下執行
python -m pip install edge-tts
```

## 3. 使用方法

### 基本指令

執行腳本時需要指定輸入的 JSON 檔案（符合 Lingo V5 格式）以及輸出的目標資料夾。

```bash
python scripts/tts/generate_edge_tts.py --input <JSON_PATH> --output <OUTPUT_DIR>
```

### 範例：生成 A1-01 課文語音

```bash
python scripts/tts/generate_edge_tts.py \
  --input "e:/Githubs/lingo/content-ko/content/core/dialogue/A1/A1-01.json" \
  --output "e:/Githubs/lingo/content-ko/assets/audio/A1-01"
```

## 4. 功能特性

### 角色音色映射 (Role Mapping)

腳本會根據 JSON 內容中的 `role` 欄位自動切換適當的音色：

| 角色 (Role) | 性別 | 語音 ID |
|---|---|---|
| `민수` | 男 | `ko-KR-InJoonNeural` |
| `지수` | 女 | `ko-KR-SunHiNeural` |
| `teacher` (或預設) | 女 | `ko-KR-SunHiNeural` |

### 命名規範

生成的檔案名稱將嚴格遵循 JSON 中的 `id`：

- 格式: `{id}_{role}.mp3`
- 範例: `L01-D1-01_민수.mp3`

## 5. 注意事項

1. **網路連接**: Edge-TTS 本質上是存取 Microsoft 的線上服務，執行時需保持網路連線。
2. **輸出路徑**: 輸出的音檔目前存放在 `content-ko/assets/audio/`，未來發佈時需同步至 `lingo-frontend-web/assets/content/9_production/`。
3. **字元編碼**: 傳送給 TTS 的文字必須為 UTF-8 編碼。
