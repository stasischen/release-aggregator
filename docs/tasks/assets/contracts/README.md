# Content Contract Registry

This registry defines the runtime artifact shapes that frontend code is allowed
to read directly. The schemas are documentation-first; the executable gate is
`scripts/validate_content_contracts.py`.

## Contracts

| Contract | Scope | Validator |
| :--- | :--- | :--- |
| `learning_library.package.v1` | `assets/artifacts/learning_library/{lang}/library_manifest.json` plus referenced core/i18n files | `--learning-library-manifest` |
| `manifest.package.v1` | `assets/content/production/packages/{lang}/manifest.json` package bridge | `--package-manifest` |

## Current Gate

```bash
python3 scripts/validate_content_contracts.py \
  --learning-library-manifest /Users/ywchen/Dev/lingo/lingo-frontend-web/assets/artifacts/learning_library/ko/library_manifest.json \
  --require-locale zh_tw \
  --min-sentence-translations 3345
```

The Learning Library gate intentionally fails on deprecated `*_index.json`
aliases except `sources_index.json`, missing referenced files, missing locale
packs, and sentence i18n coverage dropping below the accepted baseline.
