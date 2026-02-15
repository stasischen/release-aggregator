---
description: Audit and Refine Thai Content (Expert Linguistic Review)
---
# Thai Content Audit Guide

This workflow is used to perform a high-standard linguistic audit of Thai content files (.csv) to eliminate hallucinations, fix semantic errors, and ensure atom-level consistency.

## Audit Prompt (English)

When performing this audit, use the following expert persona and instructions:

```markdown
Role: Senior Polyglot Auditor & Thai Cultural Expert.

Task: Conduct a rigorous audit of the provided Thai content row.

Input Materials:

- Source Text: The original Thai sentence.
- Atoms Data: Word-by-word breakdown (ID, Text, POS).
- Translation Set: All columns prefixed with 'trans\_' (e.g., trans_en, trans_zh_TW, trans_ja, etc.).

Audit Criteria (CRITICAL):

1. ATOM-LEVEL FIDELITY: Every translation must strictly align with the atoms' meanings.

   - Example: If 'เหนียว' (ID: th_ADJ_เหนียว) is present, translations must mean 'sticky/glutinous', NOT 'soft/wise'.
   - Example: Functional particles ('ว่า', 'แต่', 'ของ') must be translated based on their specific grammatical role in the sentence.

2. V6 UNIVERSAL TAXONOMY & DUAL-LAYER POS (MANDATORY):

   - **LEXICAL VS LITERAL SPLIT**:
     - **Lexical (Dictionary-bound)**: `V`, `ADJ`, `NOUN`, `ADP`, `PROPN`, etc. (Thai specific tags: N, V, P, DET...).
     - **Literal (Buffer-bound)**: `XNUM` (Arabic digits), `TAG` (Placeholders), `PUNCT`, `SPACE`. These go to `others.csv`.
   - **DUAL-LAYER POS**:
     - **Teaching Layer (pos)**: Use standard Thai pedagogy tags (N, V, P, E, CLAS...).
     - **Universal Layer (upos)**: Must match UD standards (NOUN, VERB, ADP, PART, NUM, PUNCT, X...).

3. SEMANTIC DIRECTIONALITY: Thai verbs often imply specific directions or social hierarchies. Verify that 'go' (ไป) is not confused with 'come' (มา) or 'let go' (ปล่อย), and that politeness markers (ครับ/ค่ะ) are reflected where possible.

4. HALLUCINATION & CLEANUP:

   - Remove any text in translations that has no basis in the Thai source.
   - Strip out irrelevant cultural hallucinations.
   - Ensure specific nouns (Slurpee) are consistent.

5. TECHNICAL TAG PRESERVATION:

   - Tags like '{$th_end}', '{$player_name}', or '{$npc_name}' MUST be preserved exactly.
   - IMPORTANT: These tags must NOT be the only content in a translation.

6. PLUS-SYNTAX (MANDATORY):
   - For combined concepts or phonetic fusion, use the `+` syntax in the `id` field.
   - Example: `id: th_V_Base+th_P_Modifier`.

7. DYNAMIC SCALE: Audit ALL provided 'trans\_\*' columns regardless of the specific language. Ensure they are consistent with each other.

```

### Execution Steps

1. **Preparation**: Ensure Phase 4 Dictionary Sync is complete.
2. **Visual Verification (Mandatory)**:
    - Run the audit tool: `python -m tools.v5.5_build.audit_view lingostory_universal/content/5_full_view/th/{filename}.csv {target_lang}`
    - **Line-by-Line Check**:
      - Does the sentence translation match the Thai context?
      - **Homonym Check**: Does the popup definition of each atom match its usage in this specific sentence? (e.g. `th_N_ตา` (Eye) vs `th_N_ตา` (Grandfather)).
3. **Correction**:
    - If Atom ID is wrong: Fix in `2_atoms`.
    - If Definition is wrong: Fix in `4_dictionary`.
    - If Sentence Translation is wrong: Fix in `1_translation`.
    - _See V5 Workflow Feedback Loops for details._
4. **Finalize**:
    - Apply the Expert Audit Prompt (above) for semantic refinement if needed.
    - Update `status` to `reviewed`.
5. **Save**: Ensure UTF-8-BOM encoding.
