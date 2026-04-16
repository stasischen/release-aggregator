# Target Language Pattern Library

## Library
| field | value |
| :--- | :--- |
| library_id | ko_survival_pattern_library_v1 |
| version | target_lang_pattern_library_v1 |
| target_lang | ko |
| domain | survival |
| levels | ["A1", "A2"] |
| entry_count | 40 |

## Entry: ko-A1-survival-001

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能用禮貌體打招呼並開啟對話。 |
| frame | 안녕하세요. |
| required_elements | ["안녕하세요"] |
| acceptable_variants | ["안녕하십니까", "안녕"] |
| constraints | ["對陌生人與服務場景預設使用禮貌體。", "平語變體僅限朋友情境。"] |
| transform_types | ["speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-HON-001", "R-KO-PRAG-001"] |
| transfer_contexts | ["classroom", "office", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 先固定禮貌打招呼作為高頻開場，再練平語/正式語切換，避免一開始就混用語體。 |
| teaching_notes.en | Use this fixed greeting in polite first-contact situations. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-002

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能用韓語做基本自我介紹（姓名）。 |
| frame | 저는 {name}이에요. |
| required_elements | ["저는", "{name}", "이에요/예요"] |
| acceptable_variants | ["제 이름은 {name}이에요", "저는 {name}예요"] |
| constraints | ["名詞尾音有收尾子音時優先用 이에요。", "正式場景可提升為 입니다。"] |
| transform_types | ["slot_substitution", "speech_level_shift"] |
| repair_links | ["R-KO-FORM-001", "R-KO-HON-001"] |
| transfer_contexts | ["classroom", "office", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 自介先鎖定主語標記與句尾 copula；用名字詞尾收音規則帶入 이에요/예요 對比。 |
| teaching_notes.en | Use this frame to introduce your name politely. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| name | 說話者姓名 | true | word | ["유나", "민준"] |

## Entry: ko-A1-survival-003

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能禮貌詢問對方姓名。 |
| frame | 이름이 뭐예요? |
| required_elements | ["이름", "뭐예요"] |
| acceptable_variants | ["성함이 어떻게 되세요", "이름이 뭐야"] |
| constraints | ["對長輩或客戶建議使用 성함 + 되세요。", "朋友間可使用平語 뭐야。"] |
| transform_types | ["speech_level_shift", "question_statement"] |
| repair_links | ["R-KO-HON-002", "R-KO-PRAG-001"] |
| transfer_contexts | ["classroom", "hotel_checkin", "office"] |
| variant_of |  |
| teaching_notes.zh_tw | 名字詢問是敬語敏感句，需明確區分 이름/성함 與句尾禮貌層級。 |
| teaching_notes.en | Use this question to ask someone’s name in polite Korean. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-004

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能說明自己的國籍或出身國家。 |
| frame | 저는 {country} 사람이에요. |
| required_elements | ["저는", "{country}", "사람이에요"] |
| acceptable_variants | ["{country}에서 왔어요", "저는 {country} 출신이에요"] |
| constraints | ["國家名與 사람이에요 要保持自然搭配。", "正式場景可改為 출신입니다。"] |
| transform_types | ["slot_substitution", "context_retarget"] |
| repair_links | ["R-KO-FORM-001", "R-KO-PRAG-002"] |
| transfer_contexts | ["classroom", "airport", "friend_chat"] |
| variant_of |  |
| teaching_notes.zh_tw | 把國籍句型和出身句型並列，讓學習者能依場景切換 사람이에요 / 에서 왔어요。 |
| teaching_notes.en | Use this sentence to state your nationality politely. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| country | 國家名稱 | true | word | ["대만", "일본"] |

## Entry: ko-A1-survival-005

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能說明自己的職業。 |
| frame | 저는 {job}이에요. |
| required_elements | ["저는", "{job}", "이에요/예요"] |
| acceptable_variants | ["직업은 {job}이에요", "{job}로 일해요"] |
| constraints | ["職業名詞後接 이에요/예요。", "說工作內容時可改用 -로 일해요。"] |
| transform_types | ["slot_substitution", "question_statement"] |
| repair_links | ["R-KO-FORM-001", "R-KO-ORDER-001"] |
| transfer_contexts | ["office", "classroom", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 先練名詞判斷句，再擴展到 -로 일해요，避免把職稱直接硬接動詞。 |
| teaching_notes.en | Use this sentence to state your job or occupation politely. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| job | 職業名詞 | true | word | ["학생", "개발자"] |

## Entry: ko-A1-survival-006

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問與回答地點。 |
| frame | {place}이/가 어디예요? |
| required_elements | ["{place}", "어디예요"] |
| acceptable_variants | ["{place} 어디에 있어요", "{place}이/가 어디야"] |
| constraints | ["主題名詞需搭配 이/가 助詞。", "詢問公共場所位置時優先禮貌體。"] |
| transform_types | ["slot_substitution", "speech_level_shift"] |
| repair_links | ["R-KO-PART-001", "R-KO-HON-001"] |
| transfer_contexts | ["subway_navigation", "airport", "hotel_checkin"] |
| variant_of |  |
| teaching_notes.zh_tw | 地點問句要一起練助詞選擇與禮貌句尾，避免只背 어디예요 而忽略前綴名詞。 |
| teaching_notes.en | Use this location question to find a place politely. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| place | 地點名詞 | true | place_expr | ["화장실", "지하철역"] |

## Entry: ko-A1-survival-007

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問是否有某項物品或服務。 |
| frame | {item} 있어요? |
| required_elements | ["{item}", "있어요"] |
| acceptable_variants | ["{item} 있나요", "{item} 없어요"] |
| constraints | ["肯定/否定需成對練習 있어요/없어요。", "服務場景可使用更正式 있나요。"] |
| transform_types | ["negation", "speech_level_shift"] |
| repair_links | ["R-KO-FORM-002", "R-KO-HON-002"] |
| transfer_contexts | ["convenience_store", "hotel_checkin", "restaurant_order"] |
| variant_of |  |
| teaching_notes.zh_tw | 有無問句是生存核心，務必以成對輸入訓練 긍정/부정，提升回應速度。 |
| teaching_notes.en | Use this pattern to ask if an item is available. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item | 物品或服務名詞 | true | word | ["와이파이", "채식 메뉴"] |

## Entry: ko-A1-survival-008

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能在店家用禮貌體點單。 |
| frame | {item} 주세요. |
| required_elements | ["{item}", "주세요"] |
| acceptable_variants | ["{item} 하나 주세요", "{item} 부탁해요"] |
| constraints | ["服務場景避免平語命令式。", "可加數量詞提升完整度。"] |
| transform_types | ["slot_substitution", "context_retarget"] |
| repair_links | ["R-KO-HON-001", "R-KO-PRAG-003"] |
| transfer_contexts | ["cafe_order", "restaurant_order", "convenience_store"] |
| variant_of |  |
| teaching_notes.zh_tw | 把 주세요 當作禮貌請求核心，先固定句尾，再逐步加入數量/溫度等附加資訊。 |
| teaching_notes.en | Use this frame to place an order politely with 주세요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item | 欲購買項目 | true | word | ["아메리카노", "김밥"] |

## Entry: ko-A1-survival-009

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能指定數量點餐或購物。 |
| frame | {item} {quantity} {counter} 주세요. |
| required_elements | ["{item}", "{quantity}", "{counter}", "주세요"] |
| acceptable_variants | ["{item} {counter} {quantity} 주세요", "{item} {quantity}개 주세요"] |
| constraints | ["數詞與量詞要配對自然。", "初級可先接受 -개 泛用量詞，但需提示更自然量詞。"] |
| transform_types | ["slot_substitution", "context_retarget"] |
| repair_links | ["R-KO-FORM-003", "R-KO-ORDER-002"] |
| transfer_contexts | ["cafe_order", "restaurant_order", "convenience_store"] |
| variant_of |  |
| teaching_notes.zh_tw | 數量點單要把數詞-量詞視為一組 chunk，避免只替換單字造成不自然搭配。 |
| teaching_notes.en | Use this frame to ask for quantity with a counter. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item | 商品或餐點 | true | word | ["물", "티켓"] |
| quantity | 數量 | true | quantity_expr | ["한", "두"] |
| counter | 量詞 | true | word | ["잔", "장"] |

## Entry: ko-A1-survival-010

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問價格。 |
| frame | 이거 얼마예요? |
| required_elements | ["얼마예요"] |
| acceptable_variants | ["{item} 얼마예요", "가격이 얼마예요"] |
| constraints | ["指示詞 이거 要有明確指涉物。", "正式場景可補上 죄송하지만。"] |
| transform_types | ["slot_substitution", "politeness_shift"] |
| repair_links | ["R-KO-PRAG-002", "R-KO-HON-001"] |
| transfer_contexts | ["convenience_store", "airport", "market"] |
| variant_of |  |
| teaching_notes.zh_tw | 價格問句高頻且可立即遷移；訓練重點在指示詞與禮貌前綴搭配。 |
| teaching_notes.en | Use this expression to ask the price of an item. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-011

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問是否可刷卡或支付方式。 |
| frame | 카드 돼요? |
| required_elements | ["카드", "돼요"] |
| acceptable_variants | ["카드로 결제돼요", "현금만 돼요"] |
| constraints | ["口語 돼요 需與正式 가능해요 對應教學。", "支付方式詞彙需可替換。"] |
| transform_types | ["slot_substitution", "question_statement"] |
| repair_links | ["R-KO-FORM-004", "R-KO-PRAG-003"] |
| transfer_contexts | ["convenience_store", "restaurant_order", "taxi_ride"] |
| variant_of |  |
| teaching_notes.zh_tw | 把支付方式做 slot 代換，確保學習者不只會問 카드，也能切換到現金/行動支付。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 카드 돼요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-012

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問洗手間或設施位置。 |
| frame | 화장실이 어디예요? |
| required_elements | ["화장실", "어디예요"] |
| acceptable_variants | ["화장실 어디에 있어요", "화장실이 어디죠"] |
| constraints | ["公共場所詢問建議保留禮貌句尾。", "可擴展到 다른 시설 名詞。"] |
| transform_types | ["slot_substitution", "speech_level_shift"] |
| repair_links | ["R-KO-PART-001", "R-KO-HON-001"] |
| transfer_contexts | ["airport", "subway_navigation", "hotel_checkin"] |
| variant_of | ko-A1-survival-006 |
| teaching_notes.zh_tw | 固定設施問路框架後再替換地點名詞，能快速覆蓋旅遊生存需求。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 화장실이 어디예요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-013

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能在交通場景詢問目的地移動。 |
| frame | {destination}에 가요? |
| required_elements | ["{destination}에", "가요"] |
| acceptable_variants | ["{destination}까지 가요", "{destination}에 가 주세요"] |
| constraints | ["方向助詞 에/까지 需按語意選擇。", "計程車請求時建議使用 가 주세요。"] |
| transform_types | ["slot_substitution", "politeness_shift"] |
| repair_links | ["R-KO-PART-002", "R-KO-PRAG-003"] |
| transfer_contexts | ["taxi_ride", "subway_navigation", "airport"] |
| variant_of |  |
| teaching_notes.zh_tw | 交通句型重點在方向助詞與請求形式切換，避免只會直譯『去嗎』。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {destination}에 가요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| destination | 目的地 | true | place_expr | ["서울역", "공항"] |

## Entry: ko-A1-survival-014

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問現在時間。 |
| frame | 지금 몇 시예요? |
| required_elements | ["지금", "몇 시예요"] |
| acceptable_variants | ["몇 시예요", "현재 시간이 어떻게 돼요"] |
| constraints | ["口語場景可省略 지금。", "回答時建議用 시/분 完整格式。"] |
| transform_types | ["question_statement", "speech_level_shift"] |
| repair_links | ["R-KO-FORM-005", "R-KO-HON-001"] |
| transfer_contexts | ["subway_navigation", "office", "friend_chat"] |
| variant_of |  |
| teaching_notes.zh_tw | 時間問句可直接串接班次/約會場景，建議搭配韓語固有數詞報時練習。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 지금 몇 시예요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-015

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能詢問今天日期。 |
| frame | 오늘이 몇 월 며칠이에요? |
| required_elements | ["오늘", "몇 월", "며칠"] |
| acceptable_variants | ["오늘 날짜가 어떻게 돼요", "오늘 며칠이에요"] |
| constraints | ["月份與日期讀法需明確分開。", "可省略 이 但保留不影響理解。"] |
| transform_types | ["question_statement", "time_expression_shift"] |
| repair_links | ["R-KO-FORM-005", "R-KO-ORDER-001"] |
| transfer_contexts | ["office", "classroom", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 日期句型要和時間句型分離教學，避免學習者把 월/시 量詞混淆。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 오늘이 몇 월 며칠이에요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-016

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能描述基本天氣感受。 |
| frame | 오늘 날씨가 {weather_adj}. |
| required_elements | ["오늘 날씨가", "{weather_adj}"] |
| acceptable_variants | ["날씨가 좋아요", "오늘은 추워요"] |
| constraints | ["主題可用 은/는 強調對比。", "形容詞終結需保持同一語體層級。"] |
| transform_types | ["slot_substitution", "speech_level_shift"] |
| repair_links | ["R-KO-PART-003", "R-KO-HON-001"] |
| transfer_contexts | ["friend_chat", "online_message", "office"] |
| variant_of |  |
| teaching_notes.zh_tw | 用天氣形容詞做第一批描述句，方便帶入主題助詞與句尾語體一致性。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 오늘 날씨가 {weather_adj}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| weather_adj | 天氣形容詞禮貌終結 | true | phrase | ["추워요", "더워요"] |

## Entry: ko-A1-survival-017

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能表達喜好。 |
| frame | 저는 {item}을/를 좋아해요. |
| required_elements | ["저는", "{item}을/를", "좋아해요"] |
| acceptable_variants | ["{item} 좋아해요", "저는 {item}를 좋아합니다"] |
| constraints | ["受詞助詞 을/를 需依收音選擇。", "正式語可切換為 좋아합니다。"] |
| transform_types | ["slot_substitution", "negation"] |
| repair_links | ["R-KO-PART-004", "R-KO-HON-001"] |
| transfer_contexts | ["friend_chat", "classroom", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 喜好句型可與否定對照練習（좋아해요/안 좋아해요），同時鞏固受詞助詞。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 저는 {item}을/를 좋아해요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item | 喜好對象 | true | word | ["커피", "한국 영화"] |

## Entry: ko-A1-survival-018

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能表達不會做或不能做某事。 |
| frame | 저는 {action} 못 해요. |
| required_elements | ["저는", "{action}", "못 해요"] |
| acceptable_variants | ["저는 {action} 안 해요", "{action}를 잘 못 해요"] |
| constraints | ["能力不足與意願否定需區分 못/안。", "含受詞時要檢查助詞搭配。"] |
| transform_types | ["negation", "slot_substitution"] |
| repair_links | ["R-KO-FORM-006", "R-KO-PART-004"] |
| transfer_contexts | ["restaurant_order", "friend_chat", "classroom"] |
| variant_of |  |
| teaching_notes.zh_tw | 用 못/안 對比建立語意邊界，避免把所有否定都簡化成 안 해요。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 저는 {action} 못 해요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| action | 動作名詞或動詞詞幹 | true | phrase | ["매운 음식", "수영"] |

## Entry: ko-A1-survival-019

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能表達想做某事。 |
| frame | {action} 하고 싶어요. |
| required_elements | ["{action}", "하고 싶어요"] |
| acceptable_variants | ["{action}하고 싶습니다", "{action}를 하고 싶어요"] |
| constraints | ["動作名詞化後接 하고 싶어요 較穩定。", "正式情境可用 싶습니다。"] |
| transform_types | ["speech_level_shift", "slot_substitution"] |
| repair_links | ["R-KO-FORM-007", "R-KO-HON-001"] |
| transfer_contexts | ["friend_chat", "online_message", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 想要句型適合接續行程規劃任務，先固定 하고 싶어요 再換 action slot。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {action} 하고 싶어요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| action | 想做的行為 | true | phrase | ["한국어 공부", "여행"] |

## Entry: ko-A1-survival-020

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能說明自己的行程或約定。 |
| frame | {time}에 {plan}이/가 있어요. |
| required_elements | ["{time}에", "{plan}이/가", "있어요"] |
| acceptable_variants | ["{time}에 {plan} 있어요", "{time}에는 {plan}이 있어요"] |
| constraints | ["時間副詞後通常接 에。", "主詞助詞 이/가 需與名詞收音匹配。"] |
| transform_types | ["time_expression_shift", "slot_substitution"] |
| repair_links | ["R-KO-PART-002", "R-KO-PART-001"] |
| transfer_contexts | ["office", "friend_chat", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 行程句可同時練時間助詞與存在句結構，是 A1 進入任務型對話的重要橋接。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {time}에 {plan}이/가 있어요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| time | 時間表達 | true | time_expr | ["오후 세 시", "내일"] |
| plan | 行程或約定 | true | phrase | ["회의", "약속"] |

## Entry: ko-A1-survival-021

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能請對方說慢一點。 |
| frame | 천천히 말해 주세요. |
| required_elements | ["천천히", "말해 주세요"] |
| acceptable_variants | ["조금 천천히 말해 주세요", "천천히 말씀해 주세요"] |
| constraints | ["服務場景優先使用 주세요 請求型。", "可升級為 말씀해 주세요 提高敬意。"] |
| transform_types | ["politeness_shift", "context_retarget"] |
| repair_links | ["R-KO-HON-003", "R-KO-PRAG-004"] |
| transfer_contexts | ["service_call", "office", "classroom"] |
| variant_of |  |
| teaching_notes.zh_tw | 把溝通修復句型列為 survival 必備，降低聽不懂時的中斷成本。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 천천히 말해 주세요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-022

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能請對方重複一次。 |
| frame | 다시 말씀해 주세요. |
| required_elements | ["다시", "말씀해 주세요"] |
| acceptable_variants | ["다시 말해 주세요", "한 번 더 말씀해 주세요"] |
| constraints | ["對陌生人建議使用 말씀해 주세요。", "同儕可降為 말해 줘요。"] |
| transform_types | ["speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-HON-003", "R-KO-PRAG-004"] |
| transfer_contexts | ["service_call", "subway_navigation", "classroom"] |
| variant_of |  |
| teaching_notes.zh_tw | 與『說慢一點』成對訓練，讓學習者有完整聽力修復工具組。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 다시 말씀해 주세요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-023

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能做簡單確認與回應。 |
| frame | 네, 맞아요. |
| required_elements | ["네", "맞아요"] |
| acceptable_variants | ["맞습니다", "네, 맞아요."] |
| constraints | ["確認句需搭配肯定詞（네/맞아요）。", "反向確認可轉為 맞죠?"] |
| transform_types | ["question_statement", "speech_level_shift"] |
| repair_links | ["R-KO-HON-001", "R-KO-PRAG-001"] |
| transfer_contexts | ["hotel_checkin", "office", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 確認語是互動節奏關鍵，應搭配上升語調問句與陳述句雙向轉換。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 네, 맞아요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A1-survival-024

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能在服務情境中禮貌道歉。 |
| frame | 죄송합니다. {reason}. |
| required_elements | ["죄송합니다", "{reason}"] |
| acceptable_variants | ["죄송해요", "미안해요"] |
| constraints | ["服務與正式場景優先 죄송합니다。", "미안해요 多用於熟人。"] |
| transform_types | ["speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-HON-004", "R-KO-PRAG-005"] |
| transfer_contexts | ["service_call", "office", "friend_chat"] |
| variant_of |  |
| teaching_notes.zh_tw | 道歉語要明確分層：正式場合用 죄송합니다，熟人情境才用 미안해요。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 죄송합니다. {reason}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| reason | 道歉原因或補充說明 | true | clause | ["늦었어요", "잘 못 들었어요"] |

## Entry: ko-A1-survival-025

| field | value |
| :--- | :--- |
| level | A1 |
| can_do | 能表達感謝並完成基本互動收尾。 |
| frame | 감사합니다. |
| required_elements | ["감사합니다"] |
| acceptable_variants | ["고맙습니다", "고마워요"] |
| constraints | ["陌生人與服務場景優先 감사합니다/고맙습니다。", "平語變體僅限親近關係。"] |
| transform_types | ["speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-HON-001", "R-KO-PRAG-001"] |
| transfer_contexts | ["restaurant_order", "hotel_checkin", "office"] |
| variant_of |  |
| teaching_notes.zh_tw | 感謝語是收尾錨點，建議與道歉語一起教，形成禮貌互動閉環。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 감사합니다. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| (none) |  | false |  | [] |

## Entry: ko-A2-survival-001

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能用原因連接句說明行為理由。 |
| frame | {reason}아서/어서 {result}. |
| required_elements | ["{reason}", "아서/어서", "{result}"] |
| acceptable_variants | ["{reason}니까 {result}", "{reason}라서 {result}"] |
| constraints | ["原因連接語尾需與前詞幹型態匹配。", "A2 需避免只靠單字拼接，必須有完整子句。"] |
| transform_types | ["connective_extension", "negation", "time_expression_shift"] |
| repair_links | ["R-KO-FORM-008", "R-KO-ORDER-003"] |
| transfer_contexts | ["service_call", "office", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | A2 開始要把原因-結果當成雙子句單位，重點是連接語尾選擇而非單字替換。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {reason}아서/어서 {result}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| reason | 原因子句 | true | clause | ["비가 와서", "늦어서"] |
| result | 結果子句 | true | clause | ["택시를 탔어요", "못 갔어요"] |

## Entry: ko-A2-survival-002

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能提出一起做某事的建議。 |
| frame | {action}할까요? |
| required_elements | ["{action}", "할까요"] |
| acceptable_variants | ["{action}해 볼까요", "{action}할래요"] |
| constraints | ["建議語氣需維持邀請而非命令。", "同儕平語變體可用 할래。"] |
| transform_types | ["modality_shift", "speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-PRAG-006", "R-KO-HON-001"] |
| transfer_contexts | ["friend_chat", "office", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 建議句要練語氣強度，讓學習者能在『提議』與『要求』間做語用區分。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {action}할까요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| action | 建議行動 | true | phrase | ["같이 점심을 먹", "지금 출발"] |

## Entry: ko-A2-survival-003

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能詢問是否被允許做某事。 |
| frame | {action}아/어도 돼요? |
| required_elements | ["{action}", "아/어도 돼요"] |
| acceptable_variants | ["{action}아/어도 될까요", "{action}해도 괜찮아요"] |
| constraints | ["服務場景優先使用 될까요 強化禮貌。", "動詞語幹與 아/어 結合需正確。"] |
| transform_types | ["modality_shift", "speech_level_shift", "question_statement"] |
| repair_links | ["R-KO-FORM-009", "R-KO-HON-005"] |
| transfer_contexts | ["classroom", "office", "restaurant_order"] |
| variant_of |  |
| teaching_notes.zh_tw | 許可問句是高頻社交策略，A2 要求能在 돼요/될까요 間做情境升降。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {action}아/어도 돼요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| action | 欲執行行為 | true | phrase | ["여기 앉", "사진 찍"] |

## Entry: ko-A2-survival-004

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能表達禁止或不允許。 |
| frame | {action}으면 안 돼요. |
| required_elements | ["{action}", "으면 안 돼요"] |
| acceptable_variants | ["{action}면 안 돼요", "{action}시면 안 됩니다"] |
| constraints | ["禁令句需注意語氣，不宜過度直白對客戶使用。", "語尾正式化時建議用 안 됩니다。"] |
| transform_types | ["modality_shift", "speech_level_shift", "context_retarget"] |
| repair_links | ["R-KO-PRAG-006", "R-KO-FORM-010"] |
| transfer_contexts | ["classroom", "airport", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 禁止句要同步教語氣緩和策略，避免學習者在服務場景直接使用生硬口吻。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {action}으면 안 돼요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| action | 被禁止行為 | true | phrase | ["여기서 담배를 피우", "사진을 찍"] |

## Entry: ko-A2-survival-005

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能描述是否有過某種經驗。 |
| frame | {experience}아/어 본 적이 있어요. |
| required_elements | ["{experience}", "본 적이 있어요"] |
| acceptable_variants | ["{experience}아/어 본 적이 없어요", "{experience}해 봤어요"] |
| constraints | ["經驗句應與過去時間參照搭配更自然。", "있어요/없어요 否定轉換需可控。"] |
| transform_types | ["tense_shift", "negation", "slot_substitution"] |
| repair_links | ["R-KO-FORM-011", "R-KO-ORDER-003"] |
| transfer_contexts | ["friend_chat", "classroom", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 經驗句型是 A2 核心，需強化『本 적이』固定搭配與肯否定對照。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {experience}아/어 본 적이 있어요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| experience | 經驗行為 | true | phrase | ["한복을 입", "김치를 만들"] |

## Entry: ko-A2-survival-006

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能表達近期計畫或意圖。 |
| frame | {plan}려고 해요. |
| required_elements | ["{plan}", "려고 해요"] |
| acceptable_variants | ["{plan}려고 합니다", "{plan}할 계획이에요"] |
| constraints | ["意圖句要與時間詞共現時序更清楚。", "正式語切換時句尾一致。"] |
| transform_types | ["time_expression_shift", "speech_level_shift", "connective_extension"] |
| repair_links | ["R-KO-FORM-012", "R-KO-HON-001"] |
| transfer_contexts | ["office", "friend_chat", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 計畫句要從單句延伸到『時間 + 意圖』，為後續複句輸出打底。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {plan}려고 해요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| plan | 計畫行為 | true | phrase | ["내일 일찍 출발하", "한국에서 일하"] |

## Entry: ko-A2-survival-007

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能做基本比較並說出偏好。 |
| frame | {item_a}보다 {item_b}가 더 {adj}. |
| required_elements | ["{item_a}보다", "{item_b}가", "더", "{adj}"] |
| acceptable_variants | ["{item_a}보다 {item_b}가 덜 {adj}", "{item_b}가 {item_a}보다 더 {adj}"] |
| constraints | ["比較標記 보다 與主詞助詞 가 要保留。", "可加入 덜 做反向比較。"] |
| transform_types | ["slot_substitution", "modality_shift", "context_retarget"] |
| repair_links | ["R-KO-PART-005", "R-KO-ORDER-004"] |
| transfer_contexts | ["restaurant_order", "subway_navigation", "friend_chat"] |
| variant_of |  |
| teaching_notes.zh_tw | 比較句要把 보다 當結構核心，並訓練語序互換，避免中文直譯序。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {item_a}보다 {item_b}가 더 {adj}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item_a | 比較基準 | true | word | ["버스", "아침"] |
| item_b | 比較對象 | true | word | ["지하철", "저녁"] |
| adj | 形容詞敘述 | true | phrase | ["편해요", "좋아요"] |

## Entry: ko-A2-survival-008

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能表達條件與可能結果。 |
| frame | {condition}으면 {result}. |
| required_elements | ["{condition}", "으면/면", "{result}"] |
| acceptable_variants | ["{condition}면 {result}", "{condition}으면 {result}겠어요"] |
| constraints | ["條件語尾選擇要依前詞是否有收音。", "結果句語氣需與場景一致。"] |
| transform_types | ["connective_extension", "modality_shift", "negation"] |
| repair_links | ["R-KO-FORM-010", "R-KO-ORDER-003"] |
| transfer_contexts | ["friend_chat", "office", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 條件句是 A2 複句入口，需同時操練語尾形態與結果句語氣控制。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {condition}으면 {result}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| condition | 條件子句 | true | clause | ["시간이 있", "비가 오"] |
| result | 結果子句 | true | clause | ["같이 가요", "택시를 타요"] |

## Entry: ko-A2-survival-009

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能禮貌請求他人幫忙。 |
| frame | {request}아/어 주실 수 있어요? |
| required_elements | ["{request}", "주실 수 있어요"] |
| acceptable_variants | ["{request}아/어 주세요", "{request}아/어 주시겠어요"] |
| constraints | ["對陌生人請求建議使用 주실 수 있어요?", "命令式請求需降為建議或委婉問句。"] |
| transform_types | ["politeness_shift", "speech_level_shift", "question_statement"] |
| repair_links | ["R-KO-HON-005", "R-KO-PRAG-007"] |
| transfer_contexts | ["service_call", "office", "airport"] |
| variant_of |  |
| teaching_notes.zh_tw | A2 請求句要練『委婉度階梯』，從 주세요 到 주실 수 있어요? 的語用差異。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {request}아/어 주실 수 있어요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| request | 請求內容 | true | phrase | ["문 좀 열", "사진을 찍어 주"] |

## Entry: ko-A2-survival-010

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能表達義務或必要性。 |
| frame | {task}아/어야 해요. |
| required_elements | ["{task}", "아/어야 해요"] |
| acceptable_variants | ["{task}아/어야 돼요", "{task}아/어야 합니다"] |
| constraints | ["義務語氣需避免過度強硬，可搭配 이유 說明。", "正式場景可升級為 합니다。"] |
| transform_types | ["modality_shift", "speech_level_shift", "negation"] |
| repair_links | ["R-KO-FORM-013", "R-KO-PRAG-006"] |
| transfer_contexts | ["office", "service_call", "classroom"] |
| variant_of |  |
| teaching_notes.zh_tw | 必要句型常見於實務任務，教學要附帶語氣緩和策略以符合人際禮貌。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {task}아/어야 해요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| task | 必須執行任務 | true | phrase | ["약을 먹", "일찍 출발하"] |

## Entry: ko-A2-survival-011

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能描述個人習慣傾向。 |
| frame | 저는 보통 {habit}는 편이에요. |
| required_elements | ["저는", "{habit}", "는 편이에요"] |
| acceptable_variants | ["저는 {habit}는 편입니다", "저는 대체로 {habit}는 편이에요"] |
| constraints | ["-는 편이다 用於傾向，不等於絕對事實。", "前項動詞應保留習慣性語意。"] |
| transform_types | ["time_expression_shift", "speech_level_shift", "slot_substitution"] |
| repair_links | ["R-KO-FORM-014", "R-KO-PRAG-008"] |
| transfer_contexts | ["friend_chat", "office", "classroom"] |
| variant_of |  |
| teaching_notes.zh_tw | 『-는 편이에요』可提升描述精度，讓學習者避免過度絕對化表達。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 저는 보통 {habit}는 편이에요. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| habit | 習慣行為 | true | phrase | ["일찍 자", "커피를 많이 마시"] |

## Entry: ko-A2-survival-012

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能描述事件先後順序。 |
| frame | 먼저 {step1}고, 그다음에 {step2}. |
| required_elements | ["먼저", "{step1}", "그다음에", "{step2}"] |
| acceptable_variants | ["우선 {step1}고, 다음에 {step2}", "{step1}고 나서 {step2}"] |
| constraints | ["連接語與步驟順序需一致，不可顛倒。", "每步驟動詞語尾需在同一語體。"] |
| transform_types | ["connective_extension", "time_expression_shift", "context_retarget"] |
| repair_links | ["R-KO-ORDER-005", "R-KO-FORM-015"] |
| transfer_contexts | ["airport", "subway_navigation", "office"] |
| variant_of |  |
| teaching_notes.zh_tw | 流程描述是任務導向溝通核心，A2 要求能用連接詞清楚表達先後關係。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: 먼저 {step1}고, 그다음에 {step2}. |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| step1 | 第一步驟 | true | clause | ["표를 사고", "짐을 맡기"] |
| step2 | 第二步驟 | true | clause | ["플랫폼으로 가요", "체크인해요"] |

## Entry: ko-A2-survival-013

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能在服務場景描述問題並請求協助。 |
| frame | {issue} 문제가 생겼어요. 도와주실 수 있어요? |
| required_elements | ["{issue}", "문제가 생겼어요", "도와주실 수 있어요"] |
| acceptable_variants | ["{issue} 문제가 있어요. 도와주세요", "{issue}에 문제가 생겨서요"] |
| constraints | ["問題陳述後需接具體請求，避免只停在抱怨。", "服務場景優先使用敬語請求。"] |
| transform_types | ["connective_extension", "politeness_shift", "context_retarget"] |
| repair_links | ["R-KO-PRAG-009", "R-KO-HON-005"] |
| transfer_contexts | ["service_call", "hotel_checkin", "airport"] |
| variant_of |  |
| teaching_notes.zh_tw | 問題回報句要包含『問題 + 協助請求』雙段，才能在真實服務場景有效解決。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {issue} 문제가 생겼어요. 도와주실 수 있어요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| issue | 問題類型 | true | phrase | ["결제", "예약"] |

## Entry: ko-A2-survival-014

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能在購物場景禮貌詢問折扣或調整。 |
| frame | {item} 조금 깎아 주실 수 있어요? |
| required_elements | ["{item}", "조금", "깎아 주실 수 있어요"] |
| acceptable_variants | ["{item} 할인 가능해요", "조금만 할인해 주실 수 있을까요"] |
| constraints | ["談判語氣需委婉，建議保留 조금/만。", "非議價場景不建議強制使用。"] |
| transform_types | ["politeness_shift", "modality_shift", "context_retarget"] |
| repair_links | ["R-KO-PRAG-010", "R-KO-HON-005"] |
| transfer_contexts | ["market", "convenience_store", "service_call"] |
| variant_of |  |
| teaching_notes.zh_tw | 議價句型重點在語氣緩衝，不是語法難度；A2 要求能維持禮貌並提出明確請求。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {item} 조금 깎아 주실 수 있어요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| item | 商品或服務項目 | true | word | ["이 가방", "총금액"] |

## Entry: ko-A2-survival-015

| field | value |
| :--- | :--- |
| level | A2 |
| can_do | 能詢問詞語或句子的意思並做澄清。 |
| frame | {expression} 무슨 뜻이에요? |
| required_elements | ["{expression}", "무슨 뜻이에요"] |
| acceptable_variants | ["{expression} 뜻이 뭐예요", "{expression}가 무슨 의미예요"] |
| constraints | ["需明確引用不懂的表達，避免空泛提問。", "專業場景可提升為 무슨 의미인지 설명해 주세요。"] |
| transform_types | ["slot_substitution", "politeness_shift", "question_statement"] |
| repair_links | ["R-KO-PRAG-004", "R-KO-HON-003"] |
| transfer_contexts | ["classroom", "service_call", "online_message"] |
| variant_of |  |
| teaching_notes.zh_tw | 澄清句型能直接支援學習自救，建議與『請再說一次』搭配做 repair 任務鏈。 |
| teaching_notes.en | Use this survival pattern in polite Korean. Core frame: {expression} 무슨 뜻이에요? |

### Slots
| name | description | required | value_type | examples |
| :--- | :--- | :--- | :--- | :--- |
| expression | 欲澄清的詞語或句子 | true | phrase | ["환불 불가", "익일 배송"] |
