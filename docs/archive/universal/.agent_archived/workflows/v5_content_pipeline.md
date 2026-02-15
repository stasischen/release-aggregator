---
description: 核心技能：V5 模組化內容管線 (V5 Modular Pipeline)。用於同步 Yarn 腳本、處理翻譯、執行分詞、數據映射、詞典更新及 App 構建發布。當用戶要求更新課程內容或執行流程門禁時使用。
---
# V5 Content Pipeline: Authoritative SOP

這是本項目的核心內容生產管線。當需要同步故事變更、修復翻譯或準備 App 構建時，請調用此技能。
This is the core content production pipeline. Invoke this skill when syncing Story changes, fixing translations, or preparing App builds.

---

## 🔵 Phase 0: Writer (Source Management)
_Focus: Yarn Script Integrity & Syntax._
👉 **Reference**: [Phase 0 SOP](./v5_content_pipeline/0_writer/0_writer_sop.md)

```bash
# 1. Validate Yarn Syntax
python -m tools.v4 validate yarn {lang}

# 2. Check Line Counts (Prevention of data loss)
python3 tools/v4/qa/check_content_status.py {lang}
```

---

## 🟢 Phase 1: Translation (Content Localization)
_Focus: Sentence Translation & Big 5 Consistency._
👉 **Reference**: [Phase 1 SOP](./v5_content_pipeline/1_translation/1_translation_sop.md)

```bash
# 1. Update Database (Yarn -> CSV)
python -m tools.v5.core.update_db {lang}

# 2. Mandatory Linguistic Content Review ⚠️
# Must manually/systematically review ALL translations for semantic accuracy and tone.
```

---

## 🟡 Phase 2: Atoms (Structure & Segmentation)
_Focus: Word Segmentation & POS Tagging._
👉 **Reference**: [Phase 2 SOP](./v5_content_pipeline/2_atoms/2_atoms_sop.md)

```bash
# 1. Linguistic Segmentation & Validation
python -m tools.v5.2_atoms.validation {lang}

# 2. Data Integrity Guard (Universal)
python tools/v5/qa/integrity_guard_universal.py {lang}
```

---

## 🟠 Phase 3: Mapping (Chunk Management)
_Focus: Deduplication & Collision Detection._
👉 **Reference**: [Phase 3 SOP](./v5_content_pipeline/3_mapping/3_mapping_sop.md)

```bash
# 1. Extract Unique Chunks & Sync Mapping
python -m tools.v5.core.extract {lang} # Generates chunk_mapping.csv
python -m tools.v5.3_mapping.sync {lang} # Syncs mapping & handles homonyms

# 2. Generate Component List & Reports
python tools/v5/3_mapping/analyze_chunks.py {lang} # Generates component_list.csv & report
```

---

## 🟣 Phase 4: Dictionary (Vocabulary & Enrichment)
_Focus: Definition, Enrichment, and Repair._
👉 **Reference**: [Phase 4 SOP](./v5_content_pipeline/4_dictionary/4_dictionary_sop.md)

```bash
# 1. Sync to Dictionary & Enrich
python -m tools.v5.core.sync {lang}
python -m tools.v5.4_dictionary.enrich {lang}

# 2. Mandatory Expert Dictionary Audit ⚠️
# Confirm zero [TODO] entries in the core dictionary.
```

---

## 🏁 Phase 5 & 8: Build (Merge & Staging)
_Focus: Merger & Asset Staging._
👉 **Reference**: [Phase 8 Staging SOP](./v5_content_pipeline/8_staging/8_staging_sop.md)

```bash
# 1. Merger (Combine Phase 1 & 2)
python -m tools.v5.core.merger {lang}

# 2. Build Staging (V5 Structured Pack)
python -m tools.v5.8_staging.builder {lang}
```

---

## 🚀 Phase 9: Deploy (Production Release)
_Focus: Smart Routing & Manifest Discovery._
👉 **Reference**: [Phase 9 Deploy SOP](./v5_content_pipeline/9_deploy/9_deploy_sop.md)

```bash
# 1. Finalize & Deploy (Smart Router)
python -m tools.v5.9_deploy.deploy {lang}
```

---

## 📍 Resources (資源索引)
- **排除故障 (Troubleshooting)**: [Troubleshooting](./v5_content_pipeline/resources/troubleshooting.md)
- **模型與提示詞 (Prompts)**: [Prompts](./v5_content_pipeline/resources/prompts.md)
- **通用規則 (Mandatory)**: [Universal Project Rules](../universal_project_rules.md)
