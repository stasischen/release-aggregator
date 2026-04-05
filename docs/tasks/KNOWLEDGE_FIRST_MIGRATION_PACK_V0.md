# Knowledge First Migration Pack v0

## Goal

定義第一批最適合從 `reports` 遷移到 `content-ko` 正式 knowledge library 的內容。

這一批的原則是：

- 穩定
- 高價值
- 低歧義
- 易於正規化
- 易於接進現有 app 與 pipeline

---

## Inclusion Gate

只有符合以下條件的內容才應進 first pack：

- 單一概念清楚
- canonical surface 易於抽取
- 中文解說可在不依附影片脈絡下重寫
- 例句數量足夠且品質穩定
- 不需要新增複雜 schema 才能表示

---

## Recommended First Pack

### A. Beginner Copula / Basic Statement Family

建議納入：

- `~입니다`
- `~이에요/예요`
- `~야/이야`

理由：

- 核心 A1 高頻
- canonical concept 明確
- 與自我介紹、名詞句、基本禮貌層級直接相關
- 容易連到現有 dialogue / source

建議 taxonomy：

- `grammar > copula`

### B. Greetings / Social Formula

建議納入：

- `안녕하세요`
- 基礎自我介紹相關問候與回應

理由：

- learner value 極高
- 適合知識卡與 source link
- 不需複雜活用邏輯

建議 taxonomy：

- `expression > greeting`

### C. Honorific Suffix / Address Forms

建議納入：

- `~씨`
- 常見稱呼形式的基礎說明

理由：

- 社會語用價值高
- 可獨立成穩定知識點
- 與稱呼與禮貌層級教學直接相關

建議 taxonomy：

- `grammar > honorific`

### D. Core Beginner Particles

建議納入：

- `~이/가`

可視實際 source 再評估：

- `~은/는`
- `~을/를`

理由：

- A1 基礎骨架
- 規則清楚
- learner 重複接觸率高

建議 taxonomy：

- `grammar > particle`

### E. Core Connective Endings

建議納入：

- `-아서/어서/해서`
- `-(으)면`
- `-지만`
- `-거나`

理由：

- 都是高頻基礎接續
- 各自主要語用相對清楚
- 可直接提升 source/sentence 對 knowledge 的連結密度

建議 taxonomy：

- `grammar > ending`

### F. Core Connectors

建議納入的核心方向：

- sequence
- contrast
- cause / result

具體項目建議優先挑真正核心且高頻者，例如：

- `그리고`
- `그래서`
- `하지만`

若目前報表已整理完整，也可補少量語感型 connector：

- `하필`
- `공교롭게도`
- `의외로`

理由：

- 與 grammar endings 形成清楚對照
- learner 在閱讀與聽力中辨識價值高
- 不需要活用規則

建議 taxonomy：

- `connector > sequence`
- `connector > contrast`
- `connector > cause`
- `connector > stance`

---

## Suggested Initial Pack Size

建議第一輪 manual migration 控制在 8-15 個 knowledge items。

建議優先順序：

1. `~이에요/예요`
2. `~입니다`
3. `~야/이야`
4. `안녕하세요`
5. `~씨`
6. `~이/가`
7. `-아서/어서/해서`
8. `-(으)면`
9. `-지만`
10. `-거나`
11. `그리고`
12. `그래서`
13. `하지만`

如果要更保守，可先只做前 8-10 個。

---

## High-Risk Content: Do Not Migrate Yet

以下內容暫時不建議進正式 knowledge library：

### 高度多義的 connective endings

例如：

- 同時涵蓋原因、結果、背景鋪陳、語氣轉折的語尾
- 同形但受 register / discourse function 強影響的形式

原因：

- 需要更細的 usage block 與 constraints schema
- 容易在 v0 被錯誤壓平成單一說明

### 書面語或修辭感強的 endings

例如：

- 書面正式、感性、文語色彩很強的接續語尾

原因：

- learner value 對第一批不夠高
- 說明成本高，例句也較不通用

### 報表高度依附影片脈絡的內容

例如：

- 主體是情緒包裝或情境鋪陳
- 缺乏穩定規則與可抽象的 canonical concept

原因：

- 不適合成為正式 knowledge item

### 高語用依賴的敬語細分

例如：

- 需精細區分社會地位、親疏、場合的進階表現

原因：

- 需要更完整的 register / politeness schema

---

## Migration Rules for First Pack

### Canonicalization

- 每個 item 都先建立 canonical ID
- 不以 report 檔名當最終 ID
- 保留 source report path 與 video id 作為 migration note

### Explanation Rewrite

- 允許保留 source 的中文內容
- 但必須移除 emoji、系列包裝、影片導向語氣
- 改寫為正式且可長期維護的知識點說明

### Example Selection

- 每個 item 先保留 3-5 個代表性例句
- 避免把所有 report 例句一次全搬
- 若例句高度重複，優先保留語意最清楚者

### Level Policy

- first pack 以 `A1` 為主
- 若內容介於 `A1/A2`，先由人工判定，避免批次 AI 自動標錯

---

## Recommended Next Step

最適合的下一輪工作：

1. 在 `content-ko` 建立 8-15 個 canonical knowledge items
2. 同步建立對應 i18n explanation
3. 驗證 links 與 artifact schema 是否足夠承載
4. 再決定是否進入 normalizer script 階段

原因：

- 先用小批量驗證 taxonomy 與 schema
- 比直接批次搬遷更容易控制風險
- 能更快看出哪些欄位真的需要 schema extension
