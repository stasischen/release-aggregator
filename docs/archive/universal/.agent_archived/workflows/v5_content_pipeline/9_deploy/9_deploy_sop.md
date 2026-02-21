---
description: Phase 9 SOP: Deployment (Production Release)
---
# Phase 9 SOP: Deployment

**Objective**: Validate, package, and promote staged contents to the live application directory (`production`).

## Validations
- **Phase 8 Complete**: JSON artifacts exist in `8_output`.
- **Manual Approval**: Release to production requires approval.

## Workflow

### 1. Run Deploy
```bash
python -m tools.v5.9_deploy.deploy {lang}
```
**Logic**:
- **Smart Router**: Routes files to `yarn/`, `article/`, `video/` based on filename.
- **i18n**: Consolidates `Strings_*.json` and `dict_*.json` into `i18n/`.
- **Manifest**: Generates `manifest.json`.
- **Sync**: Copies to `lingourmet_universal/assets/content/production`.

### 2. Validation
Check structure in `assets/content/production/packages/{lang}/`:

| Folder | Content |
|:---|:---|
| `yarn/` | Dialogue lessons (`*_social_*`) |
| `article/` | Reading articles (`art_*`) |
| `video/` | Video content (`*_video_*`) |
| `core/` | Metadata (`dictionary_core.json`) |
| `mapping/` | `chunk_mapping.json` |
| `i18n/` | ALL translations (`Strings_*.json`, `dict_*.json`) |

**Checklist**:
- [ ] `manifest.json` exists and lists modules.
- [ ] `i18n/` contains both Strings and Dict translations.
- [ ] No misplaced files in root.

## 7. Critical Rules
- **UNIFIED I18N**: All translations MUST go to `i18n/`.
- **CORE = METADATA**: `dictionary_core.json` contains NO translations.
- **LEGACY**: `dialogue/` and `support/` are deprecated.

## Handover
- **Final**: Workflow complete. Notify user of deployment success.
