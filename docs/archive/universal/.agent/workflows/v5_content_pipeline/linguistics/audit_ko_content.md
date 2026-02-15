---
description: Audit and Refine Korean Content (Expert Linguistic Review)
---

# Korean Content Audit Guide

This workflow is used to perform a high-standard linguistic audit of Korean content files (.csv) to eliminate hallucinations, fix semantic errors (especially honorifics and speech levels), and ensure atom-level consistency.

## Audit Prompt (English)

When performing this audit, use the following expert persona and instructions:

```markdown
Role: Senior Polyglot Auditor & Korean Linguistic Expert.

Task: Conduct a rigorous audit of the provided Korean content row.

Input Materials:

- Source Text: The original Korean sentence.
- Atoms Data: Word-by-word breakdown (ID, Text, POS).
- Translation Set: All columns prefixed with 'trans\_' (e.g., trans_en, trans_zh_TW, trans_ja, trans_es, etc.).

Audit Criteria (CRITICAL):

1. ATOM-LEVEL FIDELITY: Every translation must strictly align with the atoms' meanings and POS.

   - Example: Ensure fused adjectives/verbs (e.g., '있어요' containing '있다') are translated correctly according to the dictionary.
   - Example: Check for common confusion between similar-sounding words or incorrect dictionary lookups.

2. HONORIFICS & SPEECH LEVELS: Korean relies heavily on speech levels (Formal, Polite, Casual).

   - Ensure the 'tone' of the translation matches the Korean source (e.g., a sentence ending in '-읍니다' should be more formal than '-어').
   - Verify that honorific particles (like '-시-') are reflected in the dignity of the target language translation where appropriate.

3. SEMANTIC ACCURACY: Verify the subject-object relationship. Since Korean often omits subjects, use the 'Atoms' and context to ensure the translation correctly identifies who is doing what to whom.

4. HALLUCINATION & CLEANUP:

   - Remove any text in translations that has no basis in the Korean source.
   - Strip out irrelevant cultural hallucinations or placeholders.
   - Ensure specific nouns (brand names, locations) are translated consistently.

5. TECHNICAL TAG PRESERVATION:

   - Tags like '{$player_name}', '{$npc_name}', or other engine-specific tags MUST be preserved exactly.
   - IMPORTANT: These tags must NOT be the only content in a translation.

6. V6 UNIVERSAL TAXONOMY & DUAL-LAYER POS (MANDATORY):

   - **LEXICAL VS LITERAL SPLIT**:
     - **Lexical (Teacher's Domain)**: `V`, `ADJ`, `N`, `P`, `E`, `PRON`, `NUM`. These enter the dictionary.
     - **Literal (System Domain)**: `XNUM` (Arabic digits), `TAG` (Placeholders), `PUNCT`, `SPACE`. These go to `others.csv`.
   - **EOJEOL-LEVEL (WORD-BLOCK) RULE**: Collapse stems, particles, and endings into single clickable atoms unless separated by a physical space.
   - **PLUS-SYNTAX (MULTI-MAPPING)**: Use `+` in the `id` field to link to multiple dictionary entries for combined blocks.
   - **MANDATORY INTEGRATION (NO SPLITS)**:
     - Noun + Particle: `그림보다` (N+P) -> `ko_N_그림+ko_P_보다`.
     - Verb + Ending: `먹어요` (V+E) -> `ko_V_먹다+ko_E_어요`.
   - **PERFECT RECONSTRUCTION**:
     - Spaces must be `{"id": "ko_SPACE_SPACE", "text": " ", "pos": "SPACE", "upos": "PUNCT"}`.
     - Arabic numerals must be `{"id": "ko_XNUM_10", "text": "10", "pos": "XNUM", "upos": "NUM"}`.
     - Reconstruction (Atoms + Spaces) MUST exactly match `text_source`.
   - **DUAL-LAYER POS**:
     - **Teaching Layer (pos)**: Korean specific (N, V, P, E, VCP, XNUM, TAG...).
     - **Universal Layer (upos)**: Universal Dependencies (NOUN, VERB, ADP, PART, NUM, X...).

7. DYNAMIC SCALE: Audit ALL provided 'trans\_\*' columns regardless of the specific language. Ensure they are consistent with each other.


Output Requirement:
Return ONLY a JSON object containing the corrected values for all translation columns. Do not provide commentary.
```

### Phase 2: Manual Segmentation Process (Atoms)

When manual repair or audit is required for Korean Atoms, follow this literal step-by-step protocol. Do **NOT** rely on automated scripts for final verification.

#### 1. Literal Word-by-Word Inspection

Compare the `atoms_json` against the `text_source` character by character.

- **Goal**: 100% Perfect Reconstruction.
- **Rule**: `text_source == "".join(atoms.text)`.

#### 2. Manual Boundary Detection (Suffix Splitting)

Do NOT guess boundaries. Apply the following linguistic logic:

1. **Eojeol-Level Integration (語塊化)**:
    - **Boundary Rule**: Do NOT split particles or endings from the base stem. Merge them into a single atom (clickable block).
    - **Plus-Syntax (複合 ID)**: For fused forms like `그림보다`, `날`, or `채운`, use the `+` syntax in the `id` field.
    - **Examples**:
        - `그림보다` -> `id: ko_N_그림+ko_P_보다`
        - `날` -> `id: ko_N_나+ko_P_를`
        - `채운` -> `id: ko_V_채우다+ko_E_ㄴ`
        - `빼곡히` -> `id: ko_ADV_빼곡하다+ko_E_히`
    - **Syllable Integrity**: Never split a single Korean character into Jamo (e.g., `날` is one atom).

#### 3. POS Correctness (N vs V/ADJ)

- **Check for "Noun-Leakage"**: Often scripts tag nouns as verbs (e.g., `한옥` tagged as `V`).
- **Check for "Helper Verbs"**: `해드릴게요` -> `해`(V) + `드리`(V) + `ㄹ게요`(E).
- **Check for Particles (P)**: `한옥은` -> `한옥`(N) + `은`(P). Note: Sentence endings like `다` are `E`, but case markers like `은/는/이/가` are `P`.

#### 4. Reconstruction Verification & Regression Test

Before saving, MUST perform a literal reconstruction verification.

- **Check**: `text_source == "".join(atoms.text)`.
- **Space Integrity**: Every space in `text_source` must have a corresponding `ko_SPACE` atom.
- **Punctuation Integrity**: Every mark in `text_source` must have a `ko_PUNCT` atom.
- **Regression Requirement**: After any bulk splitting (e.g., Number-Units or Conjugation hardening), run the `audit_reconstruction_p2.py` tool to ensure zero character loss across all files.

#### 5. Save & Audit Sign-off

- Ensure the CSV is saved with **UTF-8-BOM** (Encoding: `utf-8-sig`).
- Update the [audit_report_ko_p2.md](file:///e:/Githubs/Lingourmet_universal/lingostory_universal/content/2_atoms/ko/audit_report_ko_p2.md) status to `🟢 Pass` for the specific file.

### Execution Steps

1. **Preparation**: Ensure Phase 4 Dictionary Sync is complete.
2. **Visual Verification (Mandatory)**:
    - Run the audit tool: `python -m tools.v5.5_build.audit_view lingostory_universal/content/5_full_view/ko/{filename}.csv {target_lang}`
    - **Line-by-Line Check**:
      - Does the sentence translation match the Korean context (Honorifics/Speech Level)?
      - **Homonym Check**: Does the popup definition of each atom match its usage? (e.g. `ko_N_눈` (Eye) vs `ko_N_눈` (Snow)).
3. **Correction**:
    - If Atom ID is wrong: Fix in `2_atoms`.
    - If Definition is wrong: Fix in `4_dictionary`.
    - _See V5 Workflow Feedback Loops for details._
4. **Finalize**:
    - Apply the Expert Audit Prompt (above).
    - Update `status` to `reviewed`.
5. **Save**: Ensure UTF-8-BOM encoding.
