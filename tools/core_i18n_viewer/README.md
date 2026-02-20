# Core + I18N Viewer

This viewer reads frontend intake artifacts in `core+i18n` shape.

## Expected files (`tools/core_i18n_viewer/data`)
- `course.package.json`
- `dictionary_core.json`
- `dict_ko_zh_tw.json`
- `mapping.json`

## Sync data from frontend intake

```bash
python3 /Users/ywchen/Dev/lingo/release-aggregator/scripts/viewer/sync_core_i18n_viewer_data.py \
  --run-id 20260220_demo \
  --lang ko
```

Use `--run-id latest` to auto-pick the latest run folder.

## Open viewer

Serve this directory with any static server and open `index.html`.

```bash
cd /Users/ywchen/Dev/lingo/release-aggregator/tools/core_i18n_viewer
python3 -m http.server 8080
```
