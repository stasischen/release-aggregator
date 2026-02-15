# Yarn Writing Guide / Yarn 寫作指南

This guide is for Agents writing interactive dialogues in Yarn.
**Focus**: Formatting constraints for a clean "Target Language First" workflow.

## 📂 Location
`lingostory_universal/content/0_article/{lang}/dialogue/*.yarn`

## 🌟 Golden Samples
- **[Korean](samples/ko_yarn_sample.yarn)**
- **[Thai](samples/th_yarn_sample.yarn)**
- **[German](samples/de_yarn_sample.yarn)**
- **[Japanese](samples/ja_yarn_sample.yarn)**
- **[Chinese (TW)](samples/zh_tw_yarn_sample.yarn)**
- **[Spanish](samples/es_yarn_sample.yarn)**
- **[Indonesian](samples/id_yarn_sample.yarn)**

## 🚫 The 3 Deadly Sins (Don'ts) / 三大禁忌

### 1. ❌ NO Inline Translations/Tags in Dialogue Block
**Wrong**: `Dad: Hello! (Bonjour!) #mood:happy`
**Why**: Mixed language and metadata tags within the dialogue line confuse LLM translation and atomization tools.

### 2. ❌ NO Mixed Language in Choice Text
**Wrong**: `-> Hello (你好)`
**Right**: `-> 你好` (English reference goes in the mirror block at the bottom)

## ✅ The Golden Standard (Do's)

### 1. Dialogue Block (Target Language Only)
Write strictly in the target language. Keep the original formatting but omit metadata (#tags) except for the required `#line:ID`.

```yarn
title: MyNode
---
Speaker: Target language text. #line:id_001
===
```

### 2. Reference Block (Perfect Mirror)
Place all English translations and metadata tags (#mood, #grammar) in the Reference Block at the bottom of the file. 

**Rule**: The Reference Block must be a **PERFECT MIRROR** of the Dialogue Block structure. This makes it easy for humans to verify line-by-line.

**Format**: `Speaker: English Translation #tags #line:ID`

```yarn
---
// English Mirror (For Review & Metadata)
Speaker: Hello! #mood:happy #grammar:intro #line:id_001
```

## 🚀 Rationale: Why Mirror?
1. **Focus**: Drafting is faster when you don't switch between Target and Source languages constantly.
2. **Reviewability**: Humans can scroll between the top and bottom to check if the translation or mood matches the original intent perfectly.
3. **Pipeline Safety**: The CSV tools extract the content from the top block, while the metadata sync tools can source IDs from the bottom block.
