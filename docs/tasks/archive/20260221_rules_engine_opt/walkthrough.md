# A1 Overrides Rationality Audit Report

> [!NOTE]
> Review Context: `content/overrides/A1-11.jsonl` to `A1-25.jsonl`
> Standard: `docs/SOPs/KO_DATA_STANDARDIZATION_PROTOCOL.md` (V5)
> Analyst: Senior Korean Linguist AI Node

## 1. Executive Summary

The V5 standard implementation for A1-11 to A1-25 shows **exceptional quality in atomic decomposition**.

- **0 Lemma Errors**: All verbs and adjectives correctly end in `-다`.
- **0 Copula Abuses**: `ko:cop:이다` is perfectly isolated.
- **0 Zombie Composites**: Complex endings (e.g., `셨어요`, `안녕하세요`) were robustly decomposed into their atomic sequences.

The structure is highly conformant, but the scale of the overrides file suggests **rule-engine redundancy**. Over 50% of the overrides appear to be predictable combinations that could be handled dynamically or mapped globally.

## 2. Surgical Fixes Required (Linguistic Errors)

There is a minor edge-case collision regarding the classification of `요`.

### 🚨 `ko:p:요` vs `ko:e:요` Mismatches

According to the protocol, when `요` attaches to a noun/pronoun/particle, it is a polite particle (`ko:p:요`). When it attaches to a verbal/connective ending, it is part of the ending (`ko:e:요`).

**Targeted Surgery Required:**
- **A1-21 (`L21-D2-06`)**: `['ko:v:하다', 'ko:e:아서', 'ko:p:요']`
  - **Issue**: `요` follows the connective ending `-아서` (e.g., "해서요"). This must be `ko:e:요` (cf. Standard `비싸서요` -> `비싸다+어서+요`).
- **A1-19 (`L19-D4-04`)**: `['ko:n:것', 'ko:p:이', 'ko:e:ㄹ', 'ko:p:요']`
  - **Issue**: `요` follows the prospective ending `-ㄹ` (e.g., "것일요"?). This requires manual check in the GS but `ko:p:요` following `ko:e` is an invalid state.

## 3. De-Overridization Candidates (Global Redundancy)

The following combinations appear at a very high frequency. They are mathematically predictable or heavily reused. Leaving them in `overrides` clutters the lesson-level configuration.

**Recommended Action**: Move to Rules Engine or Global `mapping_phrase.json` / `mapping_verbs.json`, then delete from `content/overrides/*.jsonl`.

| Surface (Predicted) | Atomic Sequence | Freq | Resolution Strategy |
| :--- | :--- | :--- | :--- |
| 있어요 | `ko:adj:있다+ko:e:어요` | 50x | Rules Engine (Standard Conjugation) |
| 저는 | `ko:pron:저+ko:p:는` | 23x | Rules Engine (Noun + Particle) |
| 해요 | `ko:v:하다+ko:e:어요` | 14x | Rules Engine (Standard Conjugation) |
| 있었어요 | `ko:adj:있다+ko:e:었+ko:e:어요` | 11x | Rules Engine (Tense + Conjugation) |
| 씨는요 | `ko:n:씨+ko:p:는+ko:p:요` | 8x | Dictionary (Global Mapping) |
| 했어요 | `ko:v:하다+ko:e:었+ko:e:어요` | 8x | Rules Engine (Tense + Conjugation) |
| 좋네요 | `ko:adj:좋다+ko:e:네+ko:e:요` | 7x | Rules Engine (Standard Conjugation) |
| 언제예요 | `ko:pron:언제+ko:cop:이다+ko:e:에요`| 7x | Rules Engine (Copula + Ending) |

## 4. Automation Script Optimization

For the next iteration of `generate_overrides_from_gold.py`, implement the following heuristic updates to make standard generation "smarter":

1. **Auto-Resolution Filter (The "Try-Engine-First" Pattern)**:
   Before writing a mapping to the override JSONL, have the script simulate a Rules Engine parse of the surface Eojeol. If the engine outputs the *exact same atomic sequence* using its global dictionary and standard inflection rules, **skip writing the override**. Only write overrides for algorithmic exceptions.
2. **Context-Aware `요` Switch**:
   Add a quick lookbehind when encountering `요`:

   ```python
   if current_lemma == "요":
       if previous_pos in ["e"]:
           current_pos = "e"
       elif previous_pos in ["n", "pron", "adv", "p", "prop"]:
           current_pos = "p"
   ```

3. **Blacklist for Pure Particles**:
   Sequences like `저+는` or `이+가` should organically pass the morphological segmentation and never require hardcoding. Strip basic Subject/Topic/Object particle resolutions from overrides entirely.
