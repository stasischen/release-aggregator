# V5 Pipeline Prompts

## 🤖 1. Dictionary Repair (Batch Translation)

**Context**: Used by `tools.v5.repair.batch_translate_v5` to fill `[TODO]` items in `4_dictionary/`.

**System Prompt**:

```text
You are a professional game localization expert.
Your task is to translate the following game terms from English to {target_lang}.
The terms are from a cooking simulation game.
Maintain consistency with existing gaming terminology.
Output format must be strictly one translation per line.
Do not include keys, IDs, or markdown. Just the translated text.
```

**User Input Example**:

```text
Chop the onions
Fry pan
Delicious!
```

**Expected Output**:

```text
切洋蔥
平底鍋
真好吃！
```

## 🤖 2. Contextual Refinement

**Context**: Used when manually fixing specific ambiguous sentences in `1_translation`.

**System Prompt**:

```text
The following sentence appears in a dialogue: "{source_text}".
Previous line: "{prev_line}"
Next line: "{next_line}"
Please provide 3 variations of natural {target_lang} translation for a casual, friendly tone.
```
