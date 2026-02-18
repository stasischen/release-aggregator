# Session Handoff: Task Sync & Golden Split (2026-02-18)

## 📌 Status at Session End
- **Task Alignment**: `TASK_INDEX.md` and related JSONs in `release-aggregator` have been synchronized with the actual state of `content-ko`.
- **Accomplishments**:
    - `KO-GEMINI-05` (TOPIK POS Audit) is marked **DONE**.
    - `KO-MAP-04` (Comprehensive POS Cleanup) is marked **DONE**.
    - `KO-GEMINI-03` is now split into level-specific phases (`KO-GEMINI-03-A1`, etc.).
    - New series `KO-MAP-05` (Golden Locking) added to ensure A1/A2/B1 segmentation doesn't regress.
- **Current Position**: A1 Lessons 01-10 already have verified Golden standards. L11-20 are next.

## 🛠️ Infrastructure & Tools
- **GSD Runner**: `scripts/ops/gsd_window_runner.py` is ready to be used for windowed audits.
- **Policy Config**: `data/review_history/window_policy.json` (needs to be updated with A1-11+ list).
- **Core Script**: `scripts/ops/run_mapping_pipeline.py` provides the token extraction layer.

## 🎯 Next Steps (Immediate)
1. **Window Audit**: Start **KO-GEMINI-03-A1** for lessons A1-11 to A1-20.
2. **Review & Build**: Run the `gsd_window_runner` to collect Gemini findings and generate `A1_segmentation_golden.json`.

## 📝 Next Session Prompt
```text
請接手 2026-02-18 的進度，目標是啟動 KO-GEMINI-03-A1 的 L11-L20 審閱。
1. 確認 content-ko/data/review_history/window_policy.json 的 lessons 包含 A1-11 到 A1-20。
2. 先執行 scripts/ops/run_mapping_pipeline.py 確保 staging 資料最新。
3. 執行 python scripts/ops/gsd_window_runner.py --window-index 1 --run-review 啟動審閱程序。
4. 報告 audit 發現的 WRONG/SUSPECT 數量。
```
