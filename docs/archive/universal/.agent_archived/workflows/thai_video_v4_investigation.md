# Thai Video V5 Pipeline Investigation Report

## 問題
泰語影片 `th_v1_music_6f5sozKp0R0_fade_jeff.json` 使用舊的 V4 格式（`lines` 陣列），而不是 V5 格式（`nodes/turns` 結構）。

## 根因
泰語影片沒有經過完整的 V5 pipeline 處理，直接從 Phase 0 (writer) 複製到 production。

## 正確流程

### Phase 0: Writer (已完成)
- 位置：`lingostory_universal/content/0_writer/video/th/th_v1_music_6f5sozKp0R0_fade_jeff.json`
- 格式：V4 (lines 陣列)

### Phase 2: Atoms (需要執行)
**步驟 1：創建 atoms CSV**
```bash
# 手動分詞或使用 LLM
# 輸出：lingostory_universal/content/2_atoms/th/video/th_v1_music_6f5sozKp0R0_fade_jeff_atoms.csv
```

**CSV 格式**：
```csv
line_id,text_source,atoms_json
th_v1_music_6f5sozKp0R0_000,"ต้องนานเท่าไร","[{\"id\":\"th_V_ต้อง\",\"text\":\"ต้อง\"},{\"id\":\"th_ADJ_นาน\",\"text\":\"นาน\"}...]"
```

**步驟 2：合併 atoms 與時間戳**
```bash
cd /Users/ywchen/Dev/Lingourmet_universal
python -m tools.v5.8_staging.merge_video_atoms --src th --target zh-TW --id th_v1_music_6f5sozKp0R0_fade_jeff
```

輸出：`tools/v5/2_atoms/video/th/zh-TW/th_v1_music_6f5sozKp0R0_fade_jeff.json`

### Phase 8: Staging (需要執行)
```bash
python -m tools.v5.8_staging.video_builder --src th --target zh-TW --id th_v1_music_6f5sozKp0R0_fade_jeff
```

輸出：`tools/v5/8_staging/video/th/zh-TW/th_v1_music_6f5sozKp0R0_fade_jeff.json` (V5 格式)

### Phase 9: Deploy (需要執行)
```bash
python -m tools.v5.9_deploy.video_deploy --src th --id th_v1_music_6f5sozKp0R0_fade_jeff
```

輸出：`lingostory_universal/content/production/packages/th/video/th_v1_music_6f5sozKp0R0_fade_jeff.json` (V5 格式)

## 臨時解決方案
已在 `VideoRepository.loadSubtitles()` 中添加 V4 格式向後兼容性，但這只是臨時措施。

## 建議
1. **立即**：為泰語影片執行完整的 V5 pipeline
2. **長期**：確保所有新影片都經過 Phase 2-8-9 流程
3. **移除**：在所有影片轉換為 V5 後，移除 V4 兼容性代碼

## 參考
- Video Pipeline: `tools/v5/video_pipeline.py`
- Merge Atoms: `tools/v5/8_staging/merge_video_atoms.py`
- Builder: `tools/v5/8_staging/video_builder.py`
- Deploy: `tools/v5/9_deploy/video_deploy.py`
