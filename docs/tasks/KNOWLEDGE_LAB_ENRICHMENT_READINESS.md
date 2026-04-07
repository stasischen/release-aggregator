# Knowledge Lab Enrichment: V1 Extraction Readiness

This document tracks the extraction readiness of existing V1 knowledge enrichment content, evaluating which packages are ready to be integrated via `kg-mig-010` and subsequent sample bank extractions, and which remain "staged" or require item-local treatment.

## 1. Extraction-Ready (Proceed to `kg-mig-010`)

The following packages contain clean strings, clear canonical mappings, and cleanly separated translations that make them suitable for global sentence bank extraction:

- **Core Particles (`kg.grammar.particle.*`)**:
  - `subject`, `object`, `topic_eunneun`, `at_time_place`, `at_place_action`
  - Examples provided are canonical, structurally sound, and standalone.
- **Connectors (`kg.connector.*`)**:
  - Contains well-formed examples for causal/sequential connectors (`geuraeseo`, `geureomeuro`, `geurigo`, `geureonde`).
  - Extractable to sentence bank without conflict.
- **Pattern: Social Greetings (`kp.daily.greeting.*`)**:
  - `annyeong`, `bangawoyo`
  - Ready for extraction as discrete, fully-formed polite phrases.

## 2. Incomplete / Ambiguous (Requires Formatting Review)

These items should **NOT** be extracted until formatting ambiguities or mixed scripts are cleaned up in the `core/i18n` source.

- **Grammar: Verb Endings & Tense (`kg.grammar.ending.*`, `kg.grammar.tense.*`)**:
  - Examples currently heavily rely on instructional focus (often mixing `-아요` highlighting within the string itself).
  - *Alignment Required*: Must split the unadulterated Korean sentence into the `sentence` field, and move inline highlights or brackets entirely to the `explanation_md_i18n` or an independent presentation layer.
- **Pattern: Social Basic / Nationality (`kp.pattern.social_basic.*`)**:
  - Some snippets serve merely as substitution frames (e.g., `[Name] 입니다`). These are structural templates, not complete sentences.
  - *Alignment Required*: Differentiate full example sentences from purely pedagogical structural frames.

## 3. Disallowed (Item-Local Commentary Only)

These must never be extracted to the global example bank. They exist purely as in-item instructional material.

- **Contrastive Grammar Fragments**:
  - Items that contrast `은/는` vs `이/가` using broken or partial strings.
  - Any text explicitly showing the "wrong" way to say something (e.g., using intentional strike-through to teach common learner mistakes).
- **Suffix Isolation (`kg.grammar.honorific.suffix_ssi`)**:
  - Explanations isolating the suffix `~씨` without a full carrier sentence.

## 4. Next Steps for Extraction Pass

For downstream `kg-mig-010` scripts, apply this logic:
1. Process items mapped in **Section 1**.
2. Automatically skip items that have `is_local_commentary: true` or lack a structured, full `target_sentence` field.
3. Treat incomplete instructional frames as metadata (Commentary), failing them out of the global sentence bank injection if they arise during parsing.
