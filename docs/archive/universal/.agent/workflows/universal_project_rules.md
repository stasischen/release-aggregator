---
description: 專案開發與內容生產通用規則 (Mandatory Rules)。包含工作流紀律、安全驗證、數據架構標準及操作約束。在開始任何開發任務、提交代碼或執行內容腳本前必須閱讀並遵守。
---
# 🛑 Universal Project Rules (MANDATORY V6)

## Pillar 1: 🛡️ Workflow Integrity (工作流紀律)

1. **SOP FIRST**: Before starting any Phase (0-9), you **MUST** read its specific SOP (e.g., `v5_content_pipeline/1_translation/1_translation_sop.md`). Do not guess or rely on memory.
2. **GIT STATE GUARD**: Before running ANY destructive or batch-update tool (`update_db`, `merger`, `sync`, `builder`), you **MUST** ensure a clean `git status`. Commit or stash changes first.
3. **PHYSICAL GATES**: Transitioning between Phases **REQUIRES** a verified status in the Audit Report (e.g., `audit_report_p2.md`). The report is the **Single Source of Truth**; if it says "PENDING", you are blocked.
4. **ZERO TOLERANCE**: Do not proceed until the current Phase has **0 Errors** and **0 Warnings**.

## Pillar 2: 🧪 Safety & Validation (安全與驗證)

1. **TEST-FIRST (RULE #16)**: You are **STRICTLY PROHIBITED** from running any script on multiple files without first testing it on a **SINGLE TARGET FILE**. Present the `git diff` to the USER for formatting and content approval before batching.
2. **VISUAL VERIFICATION**: Compare every translation and atom with the Source text line-by-line. Evidence must be quoted in "Named Evidence" format (e.g., `Verified Row 5: Source 'X' matches Atoms ['Y']`).
3. **STOP ON LOSS**: If a script deletes data or looks wrong (e.g., encoding shift), **STOP IMMEDIATELY**. Do not attempt recursive repairs on corrupted states.

## Pillar 3: 📐 Data Architecture (數據與架構標準)

1. **V6 TAXONOMY (LEXICAL vs LITERAL)**: Strictly split Lexical items (Verbs, Nouns) from Literal items (`XNUM`, `TAG`, `PUNCT`, `SPACE`). Literals MUST be routed to `others.csv` and excluded from AI enrichment.
2. **DUAL-LAYER POS**: Every atom must have a **Teaching Layer (pos)** for pedagogy and a **Universal Layer (upos)** following UD (Universal Dependencies) for alignment.
3. **ARCHITECTURAL FIDELITY**: For all languages, **(Concatenated Atoms == Source Text)** must be 100% true. Spaces MUST be represented as explicit `lang_SPACE` atoms.
4. **UNIFIED ENCODING**: All CSV files **MUST** use `utf-8-sig` (UTF-8 with BOM) and maintain consistent Quoting (as per Rule #5 validation).

## Pillar 4: 🏗️ Operational Constraints (操作約束)

1. **BAN LOCAL LLM**: The use of local LLMs (Ollama, Llama.cpp) is **STRICTLY PROHIBITED** to ensure hardware-independent reliability. Use authorized cloud APIs only.
2. **BILINGUAL COMM**: All conversations and artifacts must be **Chinese/English**.
3. **TOOL DISCOVERY & EXISTENCE**: Before building a new tool, you **MUST** verify existing tools (via `find_by_name` or `grep`) to avoid redundancy. If a required SOP tool is truly missing, you **MUST PAUSE AND BUILD IT**; do not skip safety checks.
4. **CROSS-PLATFORM VERIFICATION**: All universal utility scripts **MUST** have implementations for both Windows (`.ps1`) and Mac/Linux (`.sh`). Do not assume the user is on Windows.
