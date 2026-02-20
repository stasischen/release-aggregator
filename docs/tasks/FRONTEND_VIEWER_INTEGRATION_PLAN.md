# Frontend Viewer Integration Plan

> **目標**：將 Aggregator `core_i18n_viewer` 已驗證的三大功能整合進 `lingo-frontend-web` 穩定版。
> **目標語言**：中文學韓文 (zh_tw → ko)

## 現狀盤點

### Aggregator Viewer 已有（HTML/JS 驗證通過）

| 功能 | 資料來源 | Viewer 實作位置 |
|---|---|---|
| 預錄音檔播放 | `line.audio` → `./data/audio/{file}.mp3` | `playLine()` |
| 句子時間軸高亮 | `line.audio_metadata` → `.sentences.json` (start_ms/duration_ms) | `isSentenceActive()` + `timeupdate` |
| Grammar Notes (Markdown) | `course.grammar_notes[lessonId]` → `[{title, explanation_md}]` | `renderGrammar()` → `marked.parse()` |
| Token 辭典查詢 | `dictionary_core.json` + `dict_ko_zh_tw.json` | `renderDictionary()` |

### Flutter 前端現狀

| 元件 | 狀態 | 落差 |
|---|---|---|
| `Turn` model | ✅ 已有 `audio` 欄位 (String?) | 目前沒被使用，`_playTurnAudio()` 直接用 TTS |
| `EventContent` | ✅ 已有 `bgm` 欄位 | 沒有 `grammar_notes` 欄位 |
| `ConfigLoader` | ✅ 從 `manifest.json` 讀課程 | 沒有載入 `.sentences.json` 或 grammar JSON |
| `EventOccurrenceScreen` | ✅ 有 TTS 播放、辭典查詢 | 沒有預錄音檔邏輯、沒有句子高亮、沒有 Grammar 面板 |
| 音檔 assets | ❌ 前端目前沒有打包音檔 | content-ko 有 A1-01~A1-02 的 Edge-TTS MP3 (70 檔，A1-01 共 1.0MB) |
| grammar JSON | ❌ 前端完全沒有 | content-ko 有 333 個 grammar note JSON (~150KB) |

---

## 格式落差分析

### 1. 音檔路徑：需要橋接

**Viewer 格式**（`course.package.json` 每行）：
```json
{
  "id": "L01-D1-01",
  "audio": "A1-01/L01-D1-01_민수.mp3",
  "audio_metadata": "A1-01/L01-D1-01_민수.sentences.json"
}
```

**Flutter Turn 格式**（`event.dart`）：
```dart
const factory Turn({
  String? audio,    // ← 已有欄位，但未使用
  // ❌ 缺少 audio_metadata 欄位
})
```

**需要的調整**：
- `Turn` model 加入 `audioMetadata` 欄位 (`@JsonKey(name: 'audio_metadata')`)
- Yarn JSON 的 turn 需要寫入 `audio` 和 `audio_metadata` 路徑
- 或者用命名規則推導：從 turn ID + speaker 直接組出路徑（無需改 model）

**建議方案**：**命名規則推導**（零 schema 變動）
```
Turn ID = "L01-D1-01", speaker = "민수"
→ audio = "assets/audio/A1-01/L01-D1-01_민수.ogg"
→ metadata = "assets/audio/A1-01/L01-D1-01_민수.sentences.json"
```
這樣上游不用動，前端用 convention-over-configuration。

### 2. Grammar Notes：需要新的載入路徑

**Viewer 格式**：
```json
// course.package.json
{ "grammar_notes": { "A1-01": [{ "title": "...", "explanation_md": "..." }] } }
```

**Flutter 對應**：
- `EventContent` 沒有 `grammar_notes`
- 不建議塞進 EventContent（會讓 Event JSON 膨脹）

**建議方案**：**獨立 Service 按需載入**
```
GrammarNoteService.loadForLesson("A1-01")
→ 掃描 assets/content/grammar/ko__g__a1__l01__*.json
→ 回傳 List<GrammarNote>
```

### 3. 句子時間軸：格式已對齊，零調整

`.sentences.json` 格式在 content-ko 和 viewer 完全一致：
```json
{
  "sentences": [
    { "text": "안녕하세요!", "start_ms": 100.0, "duration_ms": 2187.5 }
  ]
}
```

---

## 音檔格式策略

### 實測數據 (content-ko/assets/audio/A1-01)

| 項目 | 數值 |
|---|---|
| 檔案數 | 35 個 MP3 + 35 個 .sentences.json |
| 資料夾總大小 | **1.0 MB** |
| 單檔平均大小 | ~25 KB |
| 單檔平均長度 | 3~5 秒 |
| 目前格式 | MP3, 48 kbps, 24 kHz, Mono |

### 格式比較（語音場景）

| | **Opus (.ogg)** ✅ 選定 | AAC (.m4a) | MP3 (現有) |
|---|---|---|---|
| 設計目的 | 專為語音+音樂雙用途設計 | 通用音樂壓縮 | 通用音訊（1990s） |
| 低 bitrate 語音品質 | 24 kbps 已接近自然語音 | 24 kbps 會明顯失真 | 48 kbps 才堪用 |
| 同品質所需 bitrate | **24 kbps** | 48~64 kbps | 48 kbps |
| 延遲 | 極低 (5ms)，適合互動 | ~100ms | ~100ms |
| 授權 | 完全免費開源 (BSD) | 專利授權（Apple 平台免費） | 專利已過期 |
| Flutter 支援 | `just_audio` ✅ `audioplayers` ✅ | ✅ 全平台 | ✅ 全平台 |
| Web 支援 | Chrome ✅ Firefox ✅ Safari 17+ ✅ | ✅ 全平台 | ✅ 全平台 |
| macOS 原生 | ✅ (AVFoundation 支援) | ✅ | ✅ |
| **體積估算 (A1 全 25 課)** | **~12 MB** | ~20 MB | ~25 MB |

### 決定：**Opus (.ogg) 24kbps**

**理由**：
1. 語音場景 Opus 在同品質下體積只有 MP3 的一半
2. 專為語音設計的 codec，低 bitrate 下品質遠優於 AAC
3. 完全開源免費，無授權風險
4. Safari 17 (2023) 起已支援，無相容性顧慮

### 轉換指令

```bash
# 單檔轉換
ffmpeg -i input.mp3 -c:a libopus -b:a 24k -ar 24000 -ac 1 output.ogg

# 批次轉換 A1-01
for f in assets/audio/A1-01/*.mp3; do
  ffmpeg -i "$f" -c:a libopus -b:a 24k -ar 24000 -ac 1 "${f%.mp3}.ogg"
done
```

### 體積預估

| 範圍 | MP3 (現在) | Opus (轉換後) | 節省 |
|---|---|---|---|
| A1-01 (1 課) | 1.0 MB | **~0.5 MB** | 50% |
| A1 全部 (25 課) | ~25 MB | **~12 MB** | 52% |
| A1+A2+B1 (75 課) | ~75 MB | **~36 MB** | 52% |

> **結論**：Opus 格式讓「A1 全部內建 + A2/B1 按需下載」策略更可行。

---

## 實作計畫

### Phase 1：預錄音檔 + 句子高亮

**觸及 Repo**：`lingo-frontend-web`、`content-ko`（資產搬運）

| Task ID | 工作項目 | Repo | 估計量 |
|---|---|---|---|
| FVI-01 | 建立 `AudioTimelineModel` — 解析 `.sentences.json` | frontend | S |
| FVI-02 | 建立 `PrerecordedAudioService` — 播放 Opus + 發射 `Stream<SentenceState>` | frontend | M |
| FVI-03 | 修改 `_playTurnAudio()` — 偵測有無預錄音檔，有則用 `PrerecordedAudioService`，fallback TTS | frontend | M |
| FVI-04 | 建立 `SentenceHighlightWidget` — 依 `SentenceState` 高亮對應句段（參考 viewer 的 `.sentence-wrap.highlight`） | frontend | M |
| FVI-05a | 批次轉換 A1 音檔 MP3 → Opus (.ogg) | content-ko | S |
| FVI-05b | 將 Opus 音檔 + sentences.json 打包進 Flutter assets | content-ko → frontend | S |

**依賴鏈**：FVI-01 → FVI-02 → FVI-03 + FVI-04（可並行）← FVI-05a → FVI-05b

### Phase 2：Grammar Notes 面板

**觸及 Repo**：`lingo-frontend-web`、`content-ko`（資產搬運）

| Task ID | 工作項目 | Repo | 估計量 |
|---|---|---|---|
| FVI-06 | 建立 `GrammarNote` model + `GrammarNoteService` — 用 lesson ID 載入對應的 grammar JSON | frontend | S |
| FVI-07 | 建立 `GrammarNotesPanel` — 用 `flutter_markdown` 渲染 `explanation_md`，Accordion 展開 | frontend | M |
| FVI-08 | 在 `EventOccurrenceScreen` 加入 Grammar 入口 — TopBar 📝 按鈕 → BottomSheet 或 Side Panel | frontend | S |
| FVI-09 | 將 grammar zh_tw JSON 打包進 Flutter assets | content-ko → frontend | S |

**依賴鏈**：FVI-06 → FVI-07 → FVI-08 ← FVI-09

### Phase 3：資產打包策略

| Task ID | 工作項目 | Repo | 估計量 |
|---|---|---|---|
| FVI-10 | 建立 `AssetResolver` — 統一處理本地 assets vs 遠端下載的路徑解析 | frontend | M |
| FVI-11 | 實作按需下載機制 — A1 內建，A2/B1 按需從 Firebase Storage 下載 | frontend | L |

**依賴鏈**：Phase 1+2 驗證通過後才啟動

---

## 分工建議

| 角色 | 負責 Phase | 說明 |
|---|---|---|
| **Agent A (Frontend)** | Phase 1 (FVI-01~04) + Phase 2 (FVI-06~08) | 純 Flutter 開發，不需動上游 |
| **Agent B (Content Ops)** | FVI-05a/b + FVI-09 | 音檔轉檔、搬運資產、更新 pubspec.yaml |
| **Human Review** | Phase 3 設計決策 | 打包 vs 下載策略需要決定體積/體驗取捨 |

---

## 技術決策記錄

### 決策 1：音檔路徑 — Convention over Configuration
- **選擇**：用命名規則推導，不改 Turn model
- **理由**：避免 schema 變動引發跨 repo 連鎖修改
- **規則**：`{lesson_folder}/{turn_id}_{speaker}.ogg`

### 決策 2：Grammar Notes — 獨立 Service
- **選擇**：不塞進 EventContent，建立獨立的 GrammarNoteService
- **理由**：Grammar 是輔助資訊，不應綁定在課程播放流程中

### 決策 3：句子高亮 — Stream-based
- **選擇**：`PrerecordedAudioService` 透過 `Stream<SentenceState>` 推送狀態
- **理由**：跟 Viewer 的 `timeupdate` event 概念相同，但用 Dart reactive pattern

### 決策 4：音檔格式 — Opus (.ogg) 24kbps
- **選擇**：從 Edge-TTS 生成的 MP3 48kbps 轉換為 Opus 24kbps
- **理由**：語音場景下 Opus 品質優於 AAC/MP3、體積減半、開源免費
- **轉換**：`ffmpeg -i {input}.mp3 -c:a libopus -b:a 24k -ar 24000 -ac 1 {output}.ogg`
- **Safari 相容**：Safari 17+ (2023) 已原生支援

### 待決策
- [x] ~~A1 音檔全部打包進 assets 還是只打包 A1-01 做 PoC？~~ → **全部打包**（Opus 格式下 A1 全部約 10MB，可接受）
- [x] ~~Grammar Panel 用 BottomSheet 還是 TabBar？~~ → **BottomSheet**（`DraggableScrollableSheet`，不中斷課程播放，桌面可 auto-pin 為側欄）
- [x] ~~是否需要加入 `flutter_markdown` 依賴？~~ → **是**（Flutter 官方維護，~100KB，Grammar 表格渲染必需）
