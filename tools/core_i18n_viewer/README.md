# Core + I18N Viewer

This viewer reads frontend intake artifacts in `core+i18n` shape.

## Expected files (`tools/core_i18n_viewer/data`)
- `course.package.json`
- `dictionary_core.json`
- `dict_ko_zh_tw.json`
- `mapping.json`

## Sync data from frontend intake

```bash
# From repository root
python scripts/viewer/sync_core_i18n_viewer_data.py --run-id latest --lang ko
```

Use `--run-id latest` to auto-pick the latest run folder.

## Open viewer

Serve this directory with any static server and open `index.html`.

```bash
# From tools/core_i18n_viewer/
python -m http.server 8080
```

## Interactions
- Click a token to inspect core+i18n dictionary entries.
- Click a dialogue row to show lesson grammar notes.
- Double-click a dialogue row to play line audio (if `course/audio` exists).
