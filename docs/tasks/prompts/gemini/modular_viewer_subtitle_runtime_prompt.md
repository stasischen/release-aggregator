請依照 `plan-delegate-review` 模式執行任務。

你當前的執行緒目標是：**擴展 Modular Viewer 以承接字幕類（Subtitle-bearing）內容**。

## 核心任務：MODULAR_VIEWER_REFACTOR (Subtitle Runtime Phase)

本階段的目標是讓 Modular Viewer 能夠讀取並渲染真實的韓語對話（Dialogue）與影片（Video）字幕內容，同時嚴格遵守現有的 **Adapter-Renderer** 分離架構。

### 🚨 核心規範（Hard Constraints）

1. **禁止直接移植**：不要直接從 `lllo/tools/viewer.html` 移植程式碼。僅將其作為資料呈現與互動的參考。
2. **遵守 ULV 合約**：必須對齊 `UNIFIED_LESSON_RUNTIME_CONTRACT.md` 的規範，尤其是選取狀態與 Support Panel 的連動。
3. **小步迭代**：每一輪只做一個「最小可驗證切片」（Minimum Verifiable Slice）。
4. **Adapter 優先**：所有原始資料（Source/Build Artifact）的標準化邏輯應在 Adapter 中實現，Renderer 應保持對原始欄位（如 legacy `*_zh_tw`）的無知。

---

## 📖 必讀文件與現況 (Required Context)

### 1. 任務計畫與規範
- `release-aggregator/docs/tasks/MODULAR_VIEWER_REFACTOR_PLAN.md`
- `release-aggregator/docs/tasks/MODULAR_VIEWER_SUBTITLE_RUNTIME_BRIEF.md`
- `release-aggregator/docs/tasks/mockups/modular/UNIFIED_LESSON_RUNTIME_CONTRACT.md`

### 2. 程式碼現況
- `release-aggregator/docs/tasks/mockups/modular/js/adapter.js` (資料標準化入口)
- `release-aggregator/docs/tasks/mockups/modular/js/renderers/dialogue.js` (既有對話渲染器)
- `release-aggregator/docs/tasks/mockups/modular/js/state.js` (全域狀態管理)

### 3. 真實資料樣板
- `content-ko/content/core/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json`
- `content-ko/content/i18n/zh_tw/video/ko_v1_vlog_79Pwq7MTUPE_easy_listening_lesson.json`

---

## 🛠️ 目標資料模型 (Target Runtime Model)

在 Adapter 內部引入統一的字幕片段模型：

```json
{
  "surface_type": "dialogue|video",
  "segments": [
    {
      "segment_id": "stable-id",
      "speaker": "optional",
      "ko": "韓文文本",
      "translation": "運行時解析出的翻譯 (Bilingual)",
      "start_ms": 0,
      "end_ms": 0,
      "anchor_refs": ["knowledge-id"],
      "source_meta": {}
    }
  ]
}
```

---

## 🎯 本輪建議任務 (Recommended Slice)

請從以下切片中選擇一個開始：
- **切片 A (Dialogue)**：建立 Dialogue 專用的字幕化 Adapter。讓 `lesson_01~03` 的對話節點使用標準化的 `translation` 解析邏輯，而非直接讀取 legacy 欄位。
- **切片 B (Video)**：實作一個最小的 Video Subtitle Renderer。使用 `/video/ko_v1_vlog_79Pwq7MTUPE` 作為資料源，在 Web Mockup 中渲染出帶時間戳記的字幕清單。

---

## 📝 回報格式規範 (Required Feedback)

每一輪完成後，你必須回報：
- **Current State**: 目前實作到哪裡。
- **Changes Made**: 修改了哪些檔案。
- **How To Test**: 如何在本地開啟 `modular/index.html` 驗證。
- **What I Should Look For**: 驗收重點（預期效果）。
- **Next Step**: 建議下一輪的切片。
