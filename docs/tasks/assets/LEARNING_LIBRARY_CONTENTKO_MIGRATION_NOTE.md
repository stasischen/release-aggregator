# Migration Note: LLCM-003b

## Overview
本次任務已將第一批經驗證的 Learning Library overlay 檔案正式建立於 `content-ko` 儲存庫。

## 建立檔案清單

### 1. Knowledge Items (知識點)
| 類別 | 路徑 (Core / i18n zh_tw) |
| --- | --- |
| Grammar | `content/core/learning_library/knowledge/grammar/copula/kg.beginner.present.copula.json` |
| Grammar | `content/core/learning_library/knowledge/grammar/honorific/kg.beginner.honorific.ssi.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/greetings/kp.daily.greeting.annyeong.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/greetings/kp.daily.greeting.bangawoyo.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/question/kp.daily.polite_question.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/time/kp.daily.today_is_noun.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/time/kp.time.today_is_weekday.json` |
| Pattern | `content/core/learning_library/knowledge/pattern/time/kp.time.on_weekday_do.json` |
| Grammar | `content/core/learning_library/knowledge/grammar/particles/kg.time.topic_particle_eunneun.json` |

### 2. Topics (學習主題)
| 主題家族 | 路徑 (Core / i18n zh_tw) |
| --- | --- |
| Time | `content/core/learning_library/topics/time/topic.time.weekday.json` |
| Time | `content/core/learning_library/topics/time/topic.time.relative_day.json` |
| Time | `content/core/learning_library/topics/time/topic.time.clock_time.json` |

### 3. Vocab Sets (教學詞彙集合)
| 類型 | 來源/主題 | 路徑 (Core / i18n zh_tw) |
| --- | --- | --- |
| Topic | Weekday | `content/core/learning_library/vocab_sets/topics/time/topic.time.weekday.vocab.json` |
| Source | Dialogue A1-01 | `content/core/learning_library/vocab_sets/sources/src.ko.dialogue.a1_01.vocab.json` |
| Source | Article A1-01 Intro | `content/core/learning_library/vocab_sets/sources/src.ko.article.a1_01_intro.vocab.json` |

### 4. Links (關聯索引)
*註：僅存在於 core 層*
- `content/core/learning_library/links/sources/src.ko.video.79Pwq7MTUPE.links.json`
- `content/core/learning_library/links/sources/src.ko.dialogue.a1_01.links.json`
- `content/core/learning_library/links/sources/src.ko.article.a1_01_intro.links.json`

## 資料來源標註

### 來自現有 `content-ko` Source Truth
- `src.ko.video.79Pwq7MTUPE` 的原文與時間軸
- `src.ko.dialogue.a1_01` 的原文與角色資訊

### 來自 App Prototype Seed (Prototype-derived)
以下內容目前僅存在於 `lingo-frontend-web` 的 `learning_library_seed_json.dart`，本次已將其正式化入 `content-ko`：
- **Article Source**: `src.ko.article.a1_01_intro` 本體 (註：本任務僅建立 vocab/links，其 core 原文待後續正式化)
- **Knowledge Items**: 所有的 `kg.*` 與 `kp.*` 解說、標題與例句。
- **Topics**: Time family 的主題摘要與結構。
- **Vocab Sets**: 教學挑選出的詞彙集合與翻譯。

## 任務狀態
- `LLCM-003b` 已標記為 **Done**。
- 下一階段將由 `content-pipeline` 處理自動化整合與 artifact 產出。
