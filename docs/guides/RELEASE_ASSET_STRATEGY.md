# System Asset & Release Strategy

本文件定義了 Lingo 內容資產（Assets）的追蹤與發佈策略。

## Environment Distribution Strategy (穩定版與測試版分離策略)

為了兼顧用戶體驗的穩定性與開發功能的完整性，Lingo 採行以下資產發佈策略：

### 1. 穩定版 (Stable - `production`)
- **適用環境**：Production App / App Store Releases.
- **資產範圍**：
  - **僅保留** 完整通過 V5 數據大修、原子化拆解 (Atomic Decomposition)、且獲准發佈的語系。
  - **目前唯一語系**：`ko` (Korean) -> `zh_tw` (Traditional Chinese)。
- **清理原則**：所有非必要、未大修或實驗中的語系（如 `de`, `th`, `id` 等）必須從資產包中完全剔除。

### 2. 測試版 (Experimental/Beta)
- **適用環境**：內部 Preview / LLlo Viewer / Experimental Branches.
- **資產範圍**：
  - **全語系支援**：包含 `ko`, `de`, `th`, `ja`, `id` 等所有管線開發中的內容。
  - **全功能預覽**：開啟所有實驗性功能門控，包含未完成轉碼的音檔與測試中辭典。

## 1. 資產追蹤模式 (Asset Tracking Modes)

系統在穩定性與靈活性之間平衡，定義了兩種模式：

### A-Mode: Tracked Assets (穩定模式 - 當前使用)
- **規範**: 最終編譯後的 Production JSON/Assets 會被 commit 進前端 Repo (`lingo-frontend-web`)。
- **優點**:
    - **Zero-Setup CI**: CI 跑測時無需外部同步資產。
    - **確定性**: Pull code 即可獲得完整的開發環境。
    - **可追蹤**: 內容變更與程式碼變更在 Git History 中同步。
- **操作**: `import_lllo_raw.py` 或建置管線產出的產物必須 commit。

### B-Mode: External Assets (解耦模式 - 計畫中)
- **規範**: 資產在 Git 中被 ignore，透過 Artifact Registry 或 Firebase 分發。
- **切換標準**: 當 Pipeline 達成 100% 成功率且維持 2 個發佈週期後切換。

## 2. 單向資料流 (One-Way Data Flow)
資產應遵循以下路徑流動，嚴禁逆向：
1. `lllo` (Raw Markdown/Yarn)
2. `content-<lang>` (Atomic Source)
3. `content-pipeline` (Build & Package)
4. `release-aggregator` (Release Orchestration)
5. `lingo-frontend-web` (Customer Intake)

---
**備註**: 修改 A-Mode 策略屬於重大計畫變更，需跨團隊核准。
