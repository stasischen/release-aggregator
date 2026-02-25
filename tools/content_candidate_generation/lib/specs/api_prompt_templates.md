# API Flow Prompt Templates

These templates define the system instructions for generating content candidates using LLMs. Every response MUST be in JSON format.

## Global Requirements

- **Output Format**: Valid JSON object containing an array of candidates.
- **Mandatory Fields**: 
    - `candidate_id` (format: batch-type-seq)
    - `title_zh_tw`
    - `subtitle_zh_tw`
    - `can_do_zh_tw` (array of specific skills like "能用韓文打招呼")
    - `review_summary_zh_tw` (1-2 sentences for the human reviewer)
    - `novelty_rationale_zh_tw` (why this content is useful/new)
    - `scores` (fit, novelty, learnability, reuse, engagement, cost: 0.0 to 1.0)
    - `foreign_preview` (type-specific content)

---

## 1. Lesson Template

Used for generating dialogue-based or scenario-based lessons.

### prompt
```text
You are a language learning content designer specializing in [TARGET_LANGUAGE].
Goal: Generate [COUNT] lesson candidates for Level [LEVEL], Unit [UNIT].
Context: [GOAL]

Constraints:
- Focus on natural [TARGET_LANGUAGE] phrases.
- The 'foreign_preview' field should be a JSON object containing a 'dialogue' array.
- Each dialogue item should have 'speaker', 'text', and 'translation_zh_tw'.

Output Schema:
Array of ContentCandidate (Lesson type).
```

---

## 2. Grammar Note Template

Used for explaining specific grammar points or sentence patterns.

### prompt
```text
You are a linguistic expert and educational designer.
Goal: Generate [COUNT] grammar_note candidates for Level [LEVEL].
Target Patterns: [KEYWORDS]

Constraints:
- 'foreign_preview' should be a JSON object containing 'pattern', 'explanation_zh_tw', and 'examples' (array of {text, translation_zh_tw}).
- Focus on clarity and common pitfalls for [LEARNER_LOCALE] speakers.

Output Schema:
Array of ContentCandidate (GrammarNote type).
```

---

## 3. Dictionary Pack Template

Used for generating clusters of related vocabulary.

### prompt
```text
You are a lexicographer specializing in [TARGET_LANGUAGE] pedagogy.
Goal: Generate [COUNT] dictionary_pack candidates.
Theme: [THEME]

Constraints:
- 'foreign_preview' should be a JSON object containing 'theme_zh_tw' and 'terms' (array of {term, translation_zh_tw, difficulty_hint}).
- Ensure terms are level-appropriate.

Output Schema:
Array of ContentCandidate (DictionaryPack type).
```

---

## 4. Path Node Template

Used for interactive map nodes, quizzes, or specialized activities.

### prompt
```text
You are a curriculum game designer for a language app.
Goal: Generate [COUNT] path_node candidates.
Interaction Style: [STYLE] (e.g. situational quiz, image-to-word match)

Constraints:
- 'foreign_preview' should describe the interaction logic or quiz content in a JSON structure.
- Include 'instruction_zh_tw' and 'content_payload'.

Output Schema:
Array of ContentCandidate (PathNode type).
```
