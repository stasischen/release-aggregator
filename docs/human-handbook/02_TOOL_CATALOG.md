# Tool Catalog (Current)
# 工具目錄（現行）

Only actively used tools are listed.
僅列出目前實際使用中的工具。

## Aggregator Tools
## Aggregator 工具

| Tool | Location | Function | 中文說明 |
|---|---|---|---|
| Release CLI wrapper | `scripts/release.sh` | Parses args and invokes Python aggregator | 解析參數並呼叫 Python 聚合器 |
| Release aggregator | `scripts/release.py` | Copies artifacts, hashes files, generates and validates manifest | 複製產物、計算雜湊、產生並驗證 manifest |
| Viewer sync | `scripts/viewer/sync_core_i18n_viewer_data.py` | Syncs package data into local viewer | 同步資料到本地 viewer |
| Control tower launcher | `scripts/ops/start_lingo_control_tower.sh` | Starts zellij control-tower layout | 啟動 zellij 控制塔布局 |

## Supporting Tools
## 支援工具

| Tool | Repo | Function | 中文說明 |
|---|---|---|---|
| Schema validator | `core-schema/validators/validate.py` | Contract and manifest validation | 契約與 manifest 驗證 |
| Build entrypoint | `content-pipeline/pipelines/build_ko_zh_tw.py` | Build release artifacts into `dist/` | 產生 `dist/` 發版產物 |

## Tool Detail Pages
## 工具細節頁

- `docs/human-handbook/tools/release_sh.md`
- `docs/human-handbook/tools/release_py.md`
- `docs/human-handbook/tools/viewer_sync.md`
- `docs/human-handbook/tools/control_tower_start.md`
