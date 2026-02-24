# Content Candidate Course Design (Draft v1)
# 候選內容課程設計（草案 v1）

Purpose: preserve the agreed course-design taxonomy and unit skeleton for content candidate generation/review work.
目的：保存內容候選生成/審核所使用的課程設計分類法與單元骨架，避免後續遺忘或漂移。

Scope: `release-aggregator` generation/review framework only (schema / briefs / QA / review bundle / adapters).
範圍：僅限 `release-aggregator` 的生成/審核 framework（schema / brief / QA / review bundle / adapters）。

Related tasks:
- `AGG-GEN-016` multilingual curriculum architecture blueprint
- `AGG-GEN-017` curriculum learning-loop design
- `AGG-GEN-018` schema/brief extensions for multilingual pedagogy + review cadence

Formal task spec draft:
- `docs/tasks/AGG_GEN_017_CURRICULUM_LEARNING_LOOP_SPEC.md`

## Core Principle
## 核心原則

- Do not model content as only `dialogue` vs `article`.
- 不要只用 `對話` / `文章` 兩類來管理內容。
- Use a taxonomy so the framework can generate balanced batches, detect gaps, and QA course structure.
- 要用分類法（taxonomy），讓 framework 能補缺口、做平衡檢查、支援 QA。

## Unit Skeleton (A1/A2 Default)
## 推薦單元骨架（A1/A2 預設）

1. Situation onboarding (`Immersion input`)
1. 情境導入（沉浸式輸入）
2. Core pattern breakdown (`Structure: sentence frames`)
2. 核心句型拆解（結構化：常用句框）
3. Minimal grammar note (`Structure: grammar note`)
3. 文法最小必要說明（結構化：文法卡）
4. Controlled output (substitution / guided role-play)
4. 控制式輸出（替換練習 / 引導角色扮演）
5. Full task output in context (`Immersion output`)
5. 情境回到完整輸出（沉浸式輸出任務）
6. Same-day retrieval review node
6. 微型複習節點（當日 retrieval）
7. Cross-unit review node (`+1 unit`, `+3 units`)
7. 跨單元複習節點（`+1 unit` / `+3 units`）

## Four-Skill Integration with Output-Heavy Bias
## 聽說讀寫整合（偏重輸出）

Design rule: every input segment should lead to an output hook.
設計原則：每一段輸入最好都接一個輸出鉤子。

Recommended A1/A2 time split (starting point):
- `Input (listening + reading)`: `30-35%`
- `Structure (patterns + minimal grammar)`: `20-25%`
- `Output (speaking + writing)`: `40-50%`

Output ladder (use at least 3 levels per unit):
- `controlled` (safe template use)
- `guided` (partial freedom with prompts)
- `open_task` / `retell` / `transform` (real output)

## Content Form Taxonomy v1
## 素材形式分類法 v1 (`content_form`)

This is the main form taxonomy used by generation briefs, QA, and review.
這是供 generation brief、QA、審核台共同使用的主分類。

Allowed forms (`content_form` enum v1):
- `dialogue`
- `monologue`
- `message_thread`
- `notice`
- `form_profile`
- `schedule_timetable`
- `howto_steps`
- `comparison_card`
- `mini_story`
- `article_short`
- `faq_qa`
- `announcement_broadcast`
- `image_prompt`

### Quick guidance by form
### 各形式快速用途

- `dialogue`: turn-taking interaction; good for listening/speaking; risk = too template-like.
- `monologue`: single-speaker explanation/share; strong for retell; risk = too long for A1/A2.
- `message_thread`: practical async chat; strong for reading/writing; risk = context gaps.
- `notice`: signs/announcements; strong for short reading; must add output follow-up.
- `form_profile`: forms/profile cards; strong for functional reading-writing integration.
- `schedule_timetable`: schedule/plan tables; strong for planning + justification tasks.
- `howto_steps`: process instruction; strong for sequence language and procedural output.
- `comparison_card`: compare options; strong for decision + reasons (speaking/writing).
- `mini_story`: short narrative/diary; strong for retell and sequence output; watch vocab load.
- `article_short`: short expository text; useful but should not dominate A1/A2.
- `faq_qa`: common Q&A/customer support; strong for functional sentence patterns.
- `announcement_broadcast`: broadcast/PA notices; strong for key-info listening + retell.
- `image_prompt`: image-based description/inference; high output with low reading load.

## Supporting Axes (for brief/schema/QA)
## 補充分類軸（供 brief/schema/QA 使用）

### `learning_role` (course role)
- `immersion_input`
- `structure_pattern`
- `structure_grammar`
- `controlled_output`
- `immersion_output`
- `review_retrieval`
- `cross_unit_transfer`

### `skill_focus`
- `listening`
- `speaking`
- `reading`
- `writing`
- `integrated`

### `output_mode`
- `none`
- `controlled`
- `guided`
- `open_task`
- `retell`
- `transform`
- `review_retrieval`

## Candidate-Type Mapping (Framework)
## 與候選類型的對應（Framework）

- `lesson`
  - Can use many `content_form`s, not only `dialogue`.
  - 可使用多種 `content_form`，不應只限 `dialogue`。
- `grammar_note`
  - Minimal grammar + sentence-frame support for output.
  - 文法應服務輸出任務（最小必要）。
- `dictionary_pack`
  - Prefer functional phrases/collocations and usage by form/context.
  - 不只單字表，應包含功能詞組/搭配與使用情境。
- `path_node`
  - Best place for output/review nodes (`retrieval`, `output_challenge`, `transfer`).
  - 最適合承接輸出節點與複習節點。

## QA Balance Rules (v1 Draft)
## QA 平衡規則（v1 草案）

- At least 1 non-dialogue input per unit.
- 每單元至少 1 個非對話輸入。
- At least 1 writing output per unit.
- 每單元至少 1 個寫作輸出。
- At least 1 `open_task` / `retell` / `transform` output per unit.
- 每單元至少 1 個開放式或重述/轉換輸出。
- `dialogue` should not exceed ~60% of unit input content.
- `dialogue` 不宜超過單元輸入內容約 60%。
- Every `grammar_note` should connect to at least 1 output node.
- 每個 `grammar_note` 應連到至少 1 個輸出節點。
- Cross-unit review nodes must declare recycled units.
- 跨單元複習節點必須標註回收來源單元。

## Minimum Unit Package (A1/A2)
## 單元最低配置（A1/A2）

- 1x immersion `lesson` (`dialogue` or `monologue`)
- 1x non-dialogue input `lesson` (e.g. `notice`, `message_thread`, `schedule_timetable`)
- 1-2x `grammar_note` (minimal grammar)
- 1x `dictionary_pack` (functional phrases/collocations)
- 1x `path_node` controlled output
- 1x `path_node` open output
- 1x `path_node` same-unit retrieval review
- cross-unit review node(s) scheduled at `+1` / `+3` units (can be generated separately)

## Multilingual Curriculum Direction (Reminder)
## 多語系課程方向（提醒）

- Separate `target_language` from `learner_locale`.
- 分離 `target_language`（學習目標語言）與 `learner_locale`（教學語言）。
- Start with `zh-TW` as pedagogy overlay source-of-truth.
- 先以 `zh-TW` 作為教學 overlay 的 source-of-truth。
- Future locales (`en`, `ja`, etc.) should localize pedagogy overlays instead of duplicating the full course core.
- 未來其他 learner locale 應翻譯 pedagogy overlay，而不是複製整份課程 core。
