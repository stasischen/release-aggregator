# Artifact Map
# 產物路徑地圖

## Main Paths
## 主要路徑

| Phase | Path Pattern | Owner | 中文說明 |
|---|---|---|---|
| Build output | `../content-pipeline/dist/**` | `content-pipeline` | 建置輸出 |
| Staging output | `staging/<version>/**` | `release-aggregator` | 發版暫存輸出 |
| Manifest | `staging/<version>/global_manifest.json` | `release-aggregator` | 全域發版索引 |
| Frontend intake | frontend asset paths | `lingo-frontend-web` | 前端接收路徑 |

## Manifest Fields
## Manifest 欄位

`global_manifest.json` package entry fields:
`global_manifest.json` 每個 package 主要欄位：
- `id`
- `version`
- `path`
- `hash` (`sha256:*`)
- `provenance` (`source_repo`, `source_commit`, `pipeline_version`, `schema_version`, `built_at`)
