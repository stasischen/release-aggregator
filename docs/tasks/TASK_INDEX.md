# Task Index (任務索引)

本檔案是所有 Task 的人類可讀索引。Agent 開工時**必須先讀此檔案**。

> [!IMPORTANT]
> 新增或完成任務時，必須同步更新此索引。

---

## 🗺️ Execution Roadmap (執行路線圖)

```
Phase A: Viewer + 辭典（content-ko 內部閉環）
│  ├── A1: Viewer 增強 — 辭典彈出、多義詞顯示     [VIEWER-01]
│  ├── A2: 辭典品質驗證 — Viewer 逐課檢查 688 字   [MAPPING_DICTIONARY]
│  └── A3: 多義詞標記 — senseIndex 機制 + Yarn 標記 [KO_RESOLUTION_100PCT]
│
Phase B: Pipeline Build（content-ko → content-pipeline）
│  ├── B1: 確認 build output 格式（JSON schema）    [CONTENT_PIPELINE_SEPARATION]
│  └── B2: 跑完整 build，輸出 production assets
│
Phase C: 前端整合（lingo-frontend-web）
│  ├── C1: 對照 build output，確認前端 parser
│  ├── C2: 導入新資產，flutter test
│  └── C3: 驗證多義詞在 App 內顯示效果
```

**原則：上游先定義格式 → 驗證完畢 → 才往下游推送。**

---

## Active Tasks (進行中)

### Phase A — 當前優先

| Task ID | 描述 | Phase | 進度 | 檔案 |
|---|---|---|---|---|
| VIEWER_ENHANCEMENT | Viewer 辭典彈出 + 舊課程顯示 | A1 | 0/3 tasks | [JSON](VIEWER_ENHANCEMENT_TASKS.json) |
| MAPPING_DICTIONARY | 字典映射標準化 + 品質驗證 | A2 | 0/8 tasks | [JSON](MAPPING_DICTIONARY_TASKS.json) |
| KO_RESOLUTION_100PCT | 韓語 Token + 多義詞標記 | A3 | 7/8 tasks | [JSON](KO_RESOLUTION_100PCT_TASKS.json) |

### Phase B/C — 待 Phase A 完成後啟動

| Task ID | 描述 | Phase | 進度 | 檔案 |
|---|---|---|---|---|
| CONTENT_PIPELINE_SEPARATION | 職責分離 + Build 格式 | B1 | 0/6 phases | [JSON](CONTENT_PIPELINE_SEPARATION_TASKS.json) |

---

## Completed Tasks (已完成)

_目前無已完成的 epic。_
