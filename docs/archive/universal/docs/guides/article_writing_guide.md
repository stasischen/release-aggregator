# Article Writing Guide / 文章寫作指南

This guide is for Agents writing reading articles in Markdown.
**Focus**: Formatting constraints for clean CSV conversion.

## 📂 Location

`lingostory_universal/content/0_article/{lang}/*.md`
 
## 🌟 Golden Samples
- **[Korean](samples/ko_article_sample.md)**
- **[Thai](samples/th_article_sample.md)**
- **[German](samples/de_article_sample.md)**
- **[Japanese](samples/ja_article_sample.md)**
- **[Chinese (TW)](samples/zh_tw_article_sample.md)**
- **[Spanish](samples/es_article_sample.md)**
- **[Indonesian](samples/id_article_sample.md)**

## 🚫 The 3 Deadly Sins (Don'ts) / 三大禁忌

### 1. ❌ NO Rich Text Formatting

**Wrong**: `**Bold**`, `*Italic*`, `[Link](url)`
**Why**: These symbols (`**`, `[]`) will be treated as part of the word by the atomization AI, causing "Junk Atoms" (e.g., `word_N_**bold**`).
**Right**: Plain text only.

### 2. ❌ NO Complex Layouts

**Wrong**: Tables, Blockquotes (`>`), Code Blocks.
**Why**: The converter only understands Paragraphs and Sentences.

### 3. ❌ NO Inline Translations or Tags

**Wrong**:
```text
Hello world. (你好世界)
Hello world. #grammar:be_verb
```

**Why**: Mixed text breaks grammar analysis and confuses LLM translation tools.
**Right**: Just write the target language. Put metadata tags on their own line.

### 4. 🔀 English Reference Translation

If you need to include an English reference translation, place it at the VERY END of the file after a `---` separator.

**Example**:
```markdown
Target language paragraph.

---
// English reference below is ignored by the pipeline
English translation.
```

## ✅ The Golden Standard (Do's)

### 1. Paragraphs

Use **Double Newlines** to separate paragraphs.
Each paragraph corresponds to one "Speaker Bubble" in the App.

```markdown
Paragraph 1 text here.

Paragraph 2 text here.
```

> **Note on Rendering**: Single newlines within a paragraph are **ignored**. The App will merge them into a single flowing block of text (Reflow). feel free to break lines in Markdown for readability.

### 2. Sentences

Use standard punctuation (`.`, `?`, `!`).
Keep sentences concise (avoid 5-line sentences).

### 3. Manual Word Segmentation (Thai/CJK)

**Rule**: Use **SPACES** to separate words, even for Thai/Japanese/Chinese.
**Why**: The App natively renders Thai/CJK without spaces. Adding spaces here helps the pipeline identify words but WON'T appear in the final UI.
**Right**: `ภาษา ไทย`, `日本 の 桜`, `你是 谁`

### 4. Writing Style Standards

**Strictly adhere to these style guides for each language:**

#### **Korean (KO)**: Plain Form (해라체 / Haera-che)
- **Citations/Narrative**: MUST use **Plain Form** (`-다`, `-는다`).
- **Forbidden**: Do NOT use polite endings (`-요`, `-합니다`) in the article body unless it is a direct quote.

#### **German (DE)**: Formal Written Style
- **Narrative Tense**: Use **Präteritum** (Simple Past) for storytelling, not Perfekt.
- **Tone**: Formal and objective. Avoid colloquialisms.

#### **Thai (TH)**: Standard Written Style
- **Particles**: Remove spoken polite particles (`ครับ/ค่ะ`) from the narrative text.
- **Pronouns**: Use formal/written pronouns or drop them if context is clear.
