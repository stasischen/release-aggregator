---
description: Phase 0 SOP: Content Writing & Narrative Design. Guidance for Yarn and Markdown content creation.
---
# Phase 0 Writer: Standard Operating Procedure

本手冊用於指導 Agent 生成或修改 `.yarn` 與 `.md` 原始內容。
**核心原則**: **Target Language First** (目標語言優先)。

## 📝 Part A: Yarn Dialogue Writing
**Path**: `lingostory_universal/content/0_article/{lang}/dialogue/*.yarn`

### 1. 結構要求 (The Mirror Structure)
Yarn 檔案必須分為兩個區塊：**Dialogue Block** (上) 與 **Reference Block** (下)。

#### ✅ Dialogue Block (Top)
- **僅包含目標語言**。
- 禁止任何行內標籤 (Inline Tags) 如 `#mood:happy`。
- 必須包含 `#line:ID`。

```yarn
title: NodeName
---
SpeakerName: 目標語言對話內容。 #line:node_001
===
```

#### ✅ Reference Block (Bottom)
- **僅包含英語翻譯** 與 **Metadata Tags**。
- 必須是 Dialogue Block 的 **完美鏡像 (Perfect Mirror)**。
- 放置在檔案底部，便於人工查閱。

```yarn
---
// Mirror Block
SpeakerName: English Translation. #mood:current_mood #line:node_001
```

### 2. 嚴禁事項 (Deadly Sins)
- ❌ **禁止行內混用**: `Speaker: Hello (你好)` -> **BANNED**.
- ❌ **禁止複雜標籤**: 上方 Block 除了 `#line:ID` 外不應有其他 Tag。

### 3. 特殊變數與佔位符 (Variables)
- **格式**: `{$variable_name}`。
- **角色變數**: `{$npc_clerk}` (須在開頭 `declare`)。
- **文本佔位符**: `你好 {$player_name}！`, `Sawadee {$th_end}`。
- **規則**: 翻譯時必須保留 `{$...}`，**不可翻譯或移除變數**。

---

## 📝 Part B: Article Writing
**Path**: `lingostory_universal/content/0_article/{lang}/*.md`

### 1. 格式要求
- **純文字 (Plain Text)**: 不使用 `**bold**` 或 `[link](url)`。
- **段落分明**: 使用 **雙換行 (Double Newlines)** 分隔段落。
- **單純換行**: 忽略單行換行 (App 自動 Reflow)。

### 2. 多語言分詞規則 (Segmentation)
- **TH/JP/ZH**: 必須使用 **空格** 手動分詞 (協助 Pipeline 識別原子)。
  - _範例_: `這 是 一個 測試`

### 3. 英語參考 (English Reference)
- 放置於檔案 **最末尾**，使用 `---` 分隔。

---

## 📝 Part C: Video Subtitles
**Path**: `lingostory_universal/assets/subtitles/{video_id}.json`

### 1. Workflow: Timestamp Mapping
我們**不**通過「聽寫」製作字幕。必須基於 **現有數據源**。
- **Source A (Time)**: Trusted Subtitles (YouTube Official/Community).
- **Source B (Text)**: Target Language Lyrics (Official).
- **Action**: 將 Source A 的時間軸 **1:1 映射** 到 Source B 的文本。

### 2. Guardrails (安全護欄) 🛡️
- ❌ **嚴禁聽寫 (No Dictation)**: 禁止 AI 嘗試「聽影片」生成時間軸。
- ❌ **嚴禁發明 (No Hallucination)**: 找不到 Source A 則放棄該影片。
- ❌ **行數對齊 (Line Match)**: 文本行數必須與時間軸行數完全一致。

---

## 📚 語言風格指南 (Style Guide)
- **Korean (KO)**: 必須使用 **Plain Form (해라체/-다)**。
- **German (DE)**: 敘述使用 **Präteritum (Simple Past)**。

---

## 🏁 Handover
- **Next Step**: 完成後，請閱讀 [Phase 1 Translation SOP](../1_translation/1_translation_sop.md)。
