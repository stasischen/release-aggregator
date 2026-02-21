# 下個 Session 的啟動 Prompt (Handoff Prompt)

請在開啟新的對話 (Session) 後，直接複製貼上以下這段指令給 AI，我們就能無縫接軌這份任務：

---

**[請複製以下內容至新的 Session]**

> **角色定位：** 你現在是一位 高級韓語語言學家 (Senior Korean Linguist) 與 Lingourmet 資深架構師。
>
> **任務背景：** 我們在先前的 Session 中審核了 A1 Overrides 的合理性，確認 V5 標準化推行順利。現在我們需要針對 `engine/rules_engine.py` 進行深度優化，以解決 `요` 助詞的上下文碰撞問題，清理 A1 Overrides 中的冗餘贅肉，並為未來的 A2/B1 課程建立「平語 (Banmal)」的支援架構。
>
> **啟動步驟 (Startup Instructions)：**
>
> 1. 請讀取剛才建立的任務清單：`e:\Githubs\lingo\release-aggregator\docs\tasks\20260221_rules_engine_opt\task.md`。
> 2. 請先執行 Phase 1：建立 `test_rules_engine.py` 迴歸測試框架，並用它來跑幾次現有的引擎確保基準線穩固。
> 3. 請依序執行 Phase 2 到 Phase 5。在每次重構 `rules_engine.py` 或加入新的 `31_verb_endings_banmal.json` 規則後，都必須先跑過測試腳本，確認不會發生「平語切壞敬語」的邊界碰撞（例如 `단어` 不會被切壞）。
>
> 目標是讓 Lingo 的 Rules Engine 成為一個既能處理 V5 敬語，又能完美處理 Banmal 的強大核心。

---
