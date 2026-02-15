---
description: Audit and Refine German Content (Expert Linguistic Review)
---

This workflow is used to perform a high-standard linguistic audit of German content files (.csv) to eliminate hallucinations, fix semantic errors (gender, case, capitalization), and ensure atom-level consistency.

### Audit Prompt (English)

When performing this audit, use the following expert persona and instructions:

```markdown
Role: Senior Polyglot Auditor & German Linguistic Expert.

Task: Conduct a rigorous audit of the provided German content row.

Input Materials:

- Source Text: The original German sentence.
- Atoms Data: Word-by-word breakdown (ID, Text, POS).
- Translation Set: All columns prefixed with 'trans\_' (e.g., trans_en, trans_zh_TW, trans_ja, trans_es, etc.).

Audit Criteria (CRITICAL):

1. ATOM-LEVEL FIDELITY: Every translation must strictly align with the atoms' meanings and POS.

   - Example: Ensure compound nouns (e.g., 'Kühlschrank') are translated as a single conceptual unit if atomized as such, or component-wise if atomized separately.
   - Example: Verify separable verbs (e.g., 'einkaufen' -> 'kauft' ... 'ein') are correctly identified and translated as the full verb meaning.

2. V6 UNIVERSAL TAXONOMY & DUAL-LAYER POS (MANDATORY):

   - **LEXICAL VS LITERAL SPLIT**:
     - **Lexical (Teach/Translate)**: `V`, `ADJ`, `NOUN`, `ADP`, `PROPN`, `DET`, `PRON`, `ADV`, `NUM` (Textual).
     - **Literal (System/Buffer)**: `XNUM` (Arabic digits), `TAG`, `PUNCT`, `SPACE`. These go to `others.csv`.
   - **DUAL-LAYER POS**:
     - **Teaching Layer (pos)**: Use standard German tags (N, V, ADJ, ADV, P, DET, PRON...).
     - **Universal Layer (upos)**: Must match UD standards (NOUN, VERB, ADJ, ADV, ADP, DET, PRON, NUM, PUNCT...).

3. GRAMMATICAL ACCURACY (Gender, Case, Capitalization):

   - Strict adherence to German capitalization rules (Nouns always capitalized).
   - Ensure articles and adjective endings match the correct Gender (Masculine, Feminine, Neuter) and Case (Nominative, Accusative, Dative, Genitive).
   - Verify subject-verb agreement.

4. FORMAL VS. INFORMAL:

   - Identify if the context implies Formal ('Sie') or Informal ('Du') address.
   - Ensure consistency of address throughout the scenario/article.

5. SEPARABLE VERBS & PLUS-SYNTAX:
   - For separable verbs (e.g., 'einkaufen'), even if split in the sentence ('kaufe ... ein'), they should be atomized carefully.
   - **Lexical Policy**: Use `+` if the atom represents a combined concept or contraction (e.g. `zum` -> `id: de_P_zu+de_DET_dem`).

6. HALLUCINATION & CLEANUP:

   - Remove any text in translations that has no basis in the German source.
   - Strip out irrelevant cultural hallucinations or placeholders.

7. TECHNICAL TAG PRESERVATION:

   - Tags like '{$player_name}', '{$npc_name}', or other engine-specific tags MUST be preserved exactly.

8. DYNAMIC SCALE: Audit ALL provided 'trans\_\*' columns regardless of the specific language.


Output Requirement:
Return ONLY a JSON object containing the corrected values for all translation columns. Do not provide commentary.
```

### Execution Steps

1. **Preparation**: Ensure Phase 4 Dictionary Sync is complete.
2. **Visual Verification (Mandatory)**:
    - Run the audit tool: `python -m tools.v5.5_build.audit_view lingostory_universal/content/5_full_view/de/{filename}.csv {target_lang}`
    - **Line-by-Line Check**:
      - Does the sentence translation match the German context (Gender/Case/Formal address)?
      - **Homonym Check**: Does the popup definition of each atom match its usage? (e.g. Separable verbs `ein` + `kaufen` -> `einkaufen`).
3. **Correction**:
    - If Atom ID is wrong: Fix in `2_atoms`.
    - If Definition is wrong: Fix in `4_dictionary`.
    - _See V5 Workflow Feedback Loops for details._
4. **Finalize**:
    - Apply the Expert Audit Prompt (above).
    - Update `status` to `reviewed`.
5. **Save**: Ensure UTF-8-BOM encoding.
