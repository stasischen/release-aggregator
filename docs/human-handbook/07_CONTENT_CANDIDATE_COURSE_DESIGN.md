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
- `docs/tasks/COURSE_PEDAGOGY_OPTIMIZATION_PLAN.md` (pedagogy quality optimization workstream)

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

## Why Pedagogy Optimization Matters (Reviewer Lens)
## 為什麼要做教學優化（審稿者視角）

The unit skeleton and taxonomy are necessary, but not sufficient.
單元骨架與 taxonomy 很重要，但還不夠。

Without explicit pedagogy quality rules, units can look structurally complete while remaining weak for learning transfer.
如果沒有教學品質規則，單元可能「看起來結構完整」，但實際學習遷移效果偏弱。

### 1) Comprehension check should not become translation-only
### 1) 理解檢查不能退化成翻譯題

- Risk:
  - Learners can pass by reading Chinese support only.
  - 風險：學習者可能只靠中文對照就過關。
- Improvement direction:
  - Mix at least two comprehension types (e.g. key info + intent/next response).
  - 改進方向：至少混合兩種題型（例如資訊提取 + 意圖/下一步回應）。
- Why it helps:
  - Confirms that immersion input is actually processed, not only "read with translation."
  - 價值：確認學習者真的處理了輸入，而不是只是看翻譯。

### 2) Transform practice should train transfer, not only word replacement
### 2) 變體練習要訓練遷移，不只換字

- Risk:
  - `pattern_transform` may degrade into simple noun swapping.
  - 風險：`pattern_transform` 容易變成單純換名詞。
- Improvement direction:
  - Include scenario/function/politeness/correction transforms, not only slot transforms.
  - 改進方向：加入情境/功能/禮貌度/修正型轉換，不只 slot 替換。
- Why it helps:
  - Builds the ability to reuse sentence patterns across contexts (cafe -> pharmacy -> hotel).
  - 價值：訓練跨情境使用句型的能力（咖啡廳 -> 藥局 -> 旅館）。

### 3) Repair practice is an interaction strategy, not just a phrase list
### 3) 修復練習是互動策略，不只是句庫

- Risk:
  - Learners memorize "please repeat" but do not know when to use it.
  - 風險：只背「請再說一次」，卻不知道何時該用。
- Improvement direction:
  - Train both trigger recognition and repair response selection.
  - 改進方向：同時練「何時需要修復」與「要用哪種修復回應」。
- Why it helps:
  - In survival contexts, communication recovery matters as much as ideal outputs.
  - 價值：生存場景中，修復能力和理想輸出同等重要。

### 4) Retrieval review should distinguish form vs function
### 4) 檢索複習要區分句型回想與情境反應

- Risk:
  - Review becomes only sentence translation/recall.
  - 風險：複習容易只剩句子翻譯/回想。
- Improvement direction:
  - Tag review targets as `form`, `function`, or `mixed`.
  - 改進方向：標註 `form` / `function` / `mixed` 檢索目標。
- Why it helps:
  - Survival learners need "what should I say next?" retrieval, not just phrase memory.
  - 價值：生存學習更需要「下一句怎麼回」而不只是記住句子。

### 5) Guided output needs a completion rubric (even without auto scoring)
### 5) 引導輸出要有完成標準（即使沒有自動評分）

- Risk:
  - "Learner wrote something" may be treated as complete regardless of task success.
  - 風險：只要有寫字就算完成，忽略任務是否達成。
- Improvement direction:
  - Define completion conditions, required elements, acceptable variants, and common mistakes.
  - 改進方向：定義完成條件、必含元素、可接受變體、常見錯誤。
- Why it helps:
  - Aligns authors, PM reviewers, and future UI feedback behavior.
  - 價值：讓作者、PM、未來前端回饋機制有一致標準。

### 6) Followups should carry review/transfer goals, not only timing
### 6) Followup 要有回收/遷移目標，不只是時間點

- Risk:
  - `+1` / `+3` followups become reminder-only.
  - 風險：`+1` / `+3` 變成提醒而非學習任務。
- Improvement direction:
  - Distinguish `review` vs `transfer` and include pattern references / task hints.
  - 改進方向：區分 `review` / `transfer` 並標註 pattern refs 與任務提示。
- Why it helps:
  - Spaced review becomes productive reuse, not passive repetition.
  - 價值：讓間隔複習變成「再用一次」，不是只重看。

## What Reviewers Should Look For (Pedagogy v2 Preview)
## 審稿者應特別看什麼（教學品質 v2 預告）

When reviewing a unit fixture or mockup, do not only check whether all node types exist.
審單元 fixture 或 mockup 時，不要只看節點種類是否齊全。

Also check:
同時請檢查：

- Does the comprehension check require real understanding (not only reading zh-TW)?
- 理解檢查是否真的要求理解（而非只看中文）？
- Does transform practice create transfer value across contexts/functions?
- 變體練習是否真的有遷移價值（跨情境/功能）？
- Is repair practice teaching recovery strategy, not only phrases?
- 修復練習是否在教互動策略，而不只是句子？
- Does review retrieval train both phrase recall and response selection?
- 複習是否同時訓練句型回想與情境反應？
- Does guided output have a clear completion standard?
- 引導輸出是否有清楚完成標準？
- Do followups clearly state review vs transfer goals?
- followup 是否明確區分回收與遷移？

For the formal optimization workstream, see:
正式優化工單請見：

- `docs/tasks/COURSE_PEDAGOGY_OPTIMIZATION_PLAN.md`
- `docs/tasks/COURSE_PEDAGOGY_OPTIMIZATION_TASKS.json`

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
