# TTS Generation RunBOOK (語音生成操作手冊)

本手冊說明如何使用 `content-pipeline` 中的工具自動生成高品質的韓語語音檔 (TTS)。

## 1. 核心工具

- **基礎語音生成**: `content-pipeline/scripts/tts/generate_edge_tts.py`
- **帶時間軸生成 (推薦)**: `content-pipeline/scripts/tts/generate_edge_tts_sentences.py`
- **技術棧**: Python + [Edge-TTS](https://github.com/rany2/edge-tts)

## 2. 環境安裝

```bash
# 建議在 content-pipeline 目錄下執行
python -m pip install edge-tts
```

## 3. 使用方法

### 單課生成 (推薦使用帶時間軸版本)

執行腳本時指定輸入的 V5 格式 JSON 及輸出目錄。

```bash
# 產生音檔 (.mp3) 與段落時間軸 (.sentences.json)
python scripts/tts/generate_edge_tts_sentences.py --input <JSON_PATH> --output <OUTPUT_DIR>
```

### 批次生成範例 (Batch Processing)

如果你有多個 A1 課文（A1-01, A1-02...），可以使用簡單的 PowerShell 或 Bash 迴圈：

**PowerShell:**

```powershell
$lessons = "01", "02", "03" # 依此類推
foreach ($no in $lessons) {
    python scripts/tts/generate_edge_tts_sentences.py `
      --input "e:/Githubs/lingo/content-ko/content/core/dialogue/A1/A1-$no.json" `
      --output "e:/Githubs/lingo/content-ko/assets/audio/A1-$no"
}
```

## 4. 產出物說明

執行後在輸出目錄會看到兩個對應檔案：

- `ID_ROLE.mp3`: 語音檔。
- `ID_ROLE.sentences.json`: **句子級別時間軸**（包含每句話的 `start_ms` 與 `duration_ms`）。

## 5. 整合至 Dict Viewer

生成音檔後，回到 `content-ko` 重跑資料聚合腳本：

```bash
# 在 content-ko 目錄下執行
python scripts/ops/prepare_viewer_data.py
```

這會自動執行以下動作：

1. 檢測 `assets/audio/` 下是否有對應音檔與 Metadata。
2. 將數據注入 `data/content.js`。
3. 將音檔同步更新到 Viewer 的內部路徑。

## 7. Premium TTS (Qwen3TTS) - 實驗性功能

為了提供更高品質的語音，我們引入了 Local Qwen3TTS 支援。

### 安裝環境

所需資源較大，建議在具備 GPU 的環境執行：

```bash
pip install -U qwen-tts
```

### 使用方法

使用 `generate_qwen_tts.py`。該腳本支援自動回退機制，若本地未偵測到 Qwen 環境，預設會自動切換回 Edge-TTS。

```bash
# 使用 Premium 模式生成 (具備回退設計)
python scripts/tts/generate_qwen_tts.py --input <JSON_PATH> --output <OUTPUT_DIR>

# 強制不使用回退 (只用 Qwen)
python scripts/tts/generate_qwen_tts.py --input <JSON_PATH> --output <OUTPUT_DIR> --no-fallback
```

### 時間軸提取 (Word/Chunk Level)

Premium 語音支援更細緻的單詞級時間軸提取：

```bash
python scripts/tts/extract_qwen_timestamps.py --audio <AUDIO_PATH> --text "<TEXT>" --output <JSON_PATH>
```

產出的 `.words.json` 包含 `start_ms` 與 `duration_ms`。
