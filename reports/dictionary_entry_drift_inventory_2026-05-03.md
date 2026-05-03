# Dictionary Entry Drift Inventory

Source: `/Users/ywchen/Dev/lingo/content-ko`

## Count Summary

- total rows: 7317
- duplicate atom_id count: 0
- same surface + same POS multi-row count: 0
- same surface cross-POS candidate count: 421
- same row multi-entry_no count: 748
- same row multi-sense count: 1861
- multi-entry rows missing row-level origin/hanja/source: 345
- multi-entry rows with row-level origin/hanja/source: 403

## Interpretation

Current key model is `ko:{pos}:{lemma}`. Cross-POS same-surface rows should remain separate candidates. Same-POS homonyms are currently represented inside one atom row via `entry_no`, not as separate atom IDs.

## Top Suspicious Rows

| atom_id | pos | lemma | entries | senses | origin | sample glosses | source |
|---|---:|---|---:|---:|---|---|---|
| ko:n:영 | n | 영 | 1,3 | 6 | hanja=漢字: 零 / 靈 / 令 / 英 | 零 (0)<br>完全 (常用於否定)<br>命令<br>靈魂；神靈<br>英語；英國<br>零 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:2510 |
| ko:n:일어 | n | 일어 | 1,3 | 2 | - | 日語；日文<br>日語 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:2607 |
| ko:adv:꼭 | adv | 꼭 | 1,2 | 4 | - | 一定；務必<br>正好；恰好<br>一定、必須<br>緊、穩、恰好 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:46 |
| ko:adv:딱 | adv | 딱 | 1,2 | 7 | - | 正好；恰好<br>胖嘟嘟<br>緊緊<br>斷然<br>豁然<br>緊緊地；完全地 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:162 |
| ko:adv:막 | adv | 막 | 1,2 | 6 | - | 亂；隨便；胡亂<br>剛；剛才<br>正要<br>剛剛<br>隨便；亂<br>幕 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:106 |
| ko:adv:이리 | adv | 이리 | 1,2,4 | 4 | - | 到這裡；這方<br>狼<br>這兒；這裡；往這兒<br>這邊 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:259 |
| ko:count:만 | count | 만 | 1,2 | 4 | - | 滿；周（時間、年齡）<br>瓷器<br>磁力<br>自己；自我 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:44 |
| ko:count:채 | count | 채 | 1,2 | 5 | - | 棟；座（房屋單位）<br>著；保持（狀態）<br>棟（建築單位）<br>輛（車輛單位）<br>完全；都 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:20 |
| ko:count:틈 | count | 틈 | 1,3 | 4 | - | 縫隙；裂縫<br>空閒；時間<br>(感情間的) 隔閡<br>縫隙 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:109 |
| ko:intj:참 | intj | 참 | 1,4 | 4 | - | 真；真實；真正<br>（副詞）真；真是<br>（感嘆詞）啊；對了<br>真是 | content_v2/inventory/dictionary/2026-04-30-fix/intj.jsonl:13 |
| ko:n:김 | n | 김 | 1,3 | 4 | - | 紫菜；海苔<br>蒸汽；熱氣<br>順便；順手<br>熱氣 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:1955 |
| ko:n:눈 | n | 눈 | 1,2 | 4 | - | 眼睛<br>目光；視線<br>雪<br>芽；胚芽 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:23 |
| ko:n:레스토랑 | n | 레스토랑 | 2,3 | 4 | - | 首都<br>自來水；水道<br>修道<br>餐廳 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:2446 |
| ko:n:말 | n | 말 | 1,2 | 5 | - | 話；言語<br>話；語言<br>馬<br>末；底<br>斗(計量單位) | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:3 |
| ko:n:밤 | n | 밤 | 1,2 | 4 | - | 夜晚；晚上<br>例子；例句<br>禮貌；禮節<br>是 (答話) | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:102 |
| ko:n:배 | n | 배 | 1,2,3,4 | 9 | - | 肚子；腹部<br>船<br>梨子<br>船；船舶<br>倍；倍數<br>倍；加倍 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:192 |
| ko:n:비 | n | 비 | 1,4 | 4 | - | 雨<br>掃帚<br>比；比率<br>碑, 石碑 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:265 |
| ko:n:새 | n | 새 | 1,2 | 5 | - | 鳥<br>新；新的<br>鳥、鳥類<br>間、間隔（縮略語）<br>新、新鮮 (冠詞用法或名詞部分) | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:492 |
| ko:n:애 | n | 애 | 1,2 | 4 | - | 小孩；孩子<br>心思；心神<br>小孩；兒童<br>焦慮；焦急；操心 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:119 |
| ko:n:일 | n | 일 | 1,2,3,6 | 4 | - | 事情；工作<br>日；星期<br>天；日<br>日 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:4 |
| ko:n:절 | n | 절 | 1,2,3 | 6 | - | 拜；行禮<br>寺廟；寺院<br>節；段落<br>拜；磕頭；行禮<br>寺廟；佛寺<br>章節；段落 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:1182 |
| ko:n:팬 | n | 팬 | 1,2 | 4 | - | 迷；愛好者<br>風扇<br>平底鍋<br>粉絲；愛好者 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:1328 |
| ko:n:풀 | n | 풀 | 1,2 | 4 | - | 草<br>漿糊；膠水<br>氣勢；精神<br>自私的；利己的 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:1199 |
| ko:n:프로 | n | 프로 | 1,2 | 6 | - | 節目<br>專業；職業<br>百分比<br>節目 (program)<br>職業；專業 (pro)<br>百分比 (percent) | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:817 |
| ko:n:화 | n | 화 | 1,2,5 | 5 | - | 火；怒氣<br>禍；災禍<br>氣；怒氣<br>禍；災難<br>星期二 | content_v2/inventory/dictionary/2026-04-30-fix/n.jsonl:787 |
| ko:v:가리다 | v | 가리다 | 1,2 | 9 | - | 遮擋；遮掩<br>挑選；選擇<br>分辨；區分<br>認生<br>結帳；還債<br>遮擋；掩蓋 | content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl:492 |
| ko:v:갈다 | v | 갈다 | 1,4 | 4 | - | 更換；更替<br>磨；研磨<br>耕作；翻土<br>換 | content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl:506 |
| ko:v:감다 | v | 감다 | 1,2,5 | 7 | - | 閉 (眼)<br>洗 (頭)<br>纏繞；盤繞<br>閉（眼）<br>洗（頭）<br>纏繞 | content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl:453 |
| ko:v:걷다 | v | 걷다 | 1,2,5 | 6 | - | 走路；行走<br>捲起；收拾 (袖子、網)<br>捲起；撩起<br>收起；收拾<br>收取<br>收拾 | content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl:110 |
| ko:v:깨다 | v | 깨다 | 1,2 | 7 | - | 醒；弄醒<br>覺悟；清醒<br>打破；弄壞；突破<br>孵化<br>醒；覺醒<br>打碎；弄壞 | content_v2/inventory/dictionary/2026-04-30-fix/v.jsonl:486 |

## Multi-Entry Rows Missing Row-Level Origin

| atom_id | pos | lemma | entries | senses | origin | sample glosses | source |
|---|---:|---|---:|---:|---|---|---|
| ko:adj:고프다 | adj | 고프다 | 2,3 | 2 | - | 勢力；力量<br>餓 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:297 |
| ko:adj:곧다 | adj | 곧다 | 2,3 | 2 | - | 人份 (計算食物分量的單位)<br>直 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:312 |
| ko:adj:그만하다 | adj | 그만하다 | 2,3 | 2 | - | 和解<br>差不多 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:329 |
| ko:adj:떠들썩하다 | adj | 떠들썩하다 | 2,3 | 2 | - | 方法；手段；招數<br>吵鬧 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:298 |
| ko:adj:맵다 | adj | 맵다 | 2,3 | 2 | - | 池塘<br>辣 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:307 |
| ko:adj:번거롭다 | adj | 번거롭다 | 2,3 | 3 | - | 側面<br>方面<br>繁瑣 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:322 |
| ko:adj:부르다 | adj | 부르다 | 2,3 | 2 | - | 很久；古老<br>飽 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:308 |
| ko:adj:씩씩하다 | adj | 씩씩하다 | 2,3 | 2 | - | 絕對的<br>朝氣蓬勃 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:317 |
| ko:adj:장하다 | adj | 장하다 | 1,3 | 2 | - | 了不起；值得驕傲；優異<br>了不起 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:315 |
| ko:adj:졸리다 | adj | 졸리다 | 1,3 | 2 | - | 睏倦；想睡<br>想睡 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:318 |
| ko:adj:쾌적하다 | adj | 쾌적하다 | 1,3 | 2 | - | 舒適；清爽<br>舒適 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:323 |
| ko:adj:통통하다 | adj | 통통하다 | 1,3 | 2 | - | 胖乎乎；圓滾滾；豐滿<br>胖乎乎 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:324 |
| ko:adj:편찮다 | adj | 편찮다 | 1,3 | 2 | - | 不舒服；患病 (用於長輩)<br>欠安 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:325 |
| ko:adv:그때그때 | adv | 그때그때 | 2,3 | 2 | - | 一<br>隨時 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:360 |
| ko:adv:그리 | adv | 그리 | 1,3 | 3 | - | 那樣地<br>不怎麼；不太 (與否定連用)<br>那樣, 往那裡 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:125 |
| ko:adv:그제야 | adv | 그제야 | 2,3 | 2 | - | 釐米；公分<br>那時才 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:343 |
| ko:adv:꼭 | adv | 꼭 | 1,2 | 4 | - | 一定；務必<br>正好；恰好<br>一定、必須<br>緊、穩、恰好 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:46 |
| ko:adv:딱 | adv | 딱 | 1,2 | 7 | - | 正好；恰好<br>胖嘟嘟<br>緊緊<br>斷然<br>豁然<br>緊緊地；完全地 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:162 |
| ko:adv:뜻대로 | adv | 뜻대로 | 2,4 | 2 | - | 嘮叨；閒聊；喋喋不休<br>照意思 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:344 |
| ko:adv:뜻밖에 | adv | 뜻밖에 | 2,3 | 2 | - | 入學典禮；開學典禮<br>出乎意料 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:363 |
| ko:adv:막 | adv | 막 | 1,2 | 6 | - | 亂；隨便；胡亂<br>剛；剛才<br>正要<br>剛剛<br>隨便；亂<br>幕 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:106 |
| ko:adv:새로이 | adv | 새로이 | 2,3 | 2 | - | 衣櫃；衣櫥<br>重新 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:352 |
| ko:adv:억지로 | adv | 억지로 | 1,3 | 2 | - | 硬要；勉強地<br>勉強 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:349 |
| ko:adv:오래도록 | adv | 오래도록 | 2,3 | 2 | - | 右側；右邊<br>長久地 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:353 |
| ko:adv:오래오래 | adv | 오래오래 | 1,3 | 2 | - | 長長久久；很久很久<br>長長久久 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:351 |
| ko:adv:으악 | adv | 으악 | 1,3 | 2 | - | 哇(驚叫聲)<br>哇 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:355 |
| ko:adv:이른바 | adv | 이른바 | 1,3 | 2 | - | 所謂；所說的<br>所謂 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:357 |
| ko:adv:이리 | adv | 이리 | 1,2,4 | 4 | - | 到這裡；這方<br>狼<br>這兒；這裡；往這兒<br>這邊 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:259 |
| ko:adv:이만큼 | adv | 이만큼 | 1,3 | 2 | - | 這麼；到這種程度地<br>這麼些 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:358 |
| ko:adv:일쑤 | adv | 일쑤 | 1,3 | 2 | - | 總是；習慣於；動不動就...<br>總是 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:361 |

## Multi-Entry Rows With Row-Level Origin

These may need entry-level origin review if different `entry_no` values have different Hanja/source.

| atom_id | pos | lemma | entries | senses | origin | sample glosses | source |
|---|---:|---|---:|---:|---|---|---|
| ko:adj:독하다 | adj | 독하다 | 2,3 | 2 | hanja=毒- | 日出<br>刺鼻 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:313 |
| ko:adj:무의미하다 | adj | 무의미하다 | 2,4 | 3 | hanja=無意味- | 自然；天然<br>自然地；理所當然地<br>無意義 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:314 |
| ko:adj:불평등하다 | adj | 불평등하다 | 2,4 | 2 | hanja=不平等- | 右邊；右側<br>不平等 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:309 |
| ko:adj:신기하다 | adj | 신기하다 | 1,2 | 2 | hanja=神奇- | 神奇；新奇；奧妙<br>神奇；新奇 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:239 |
| ko:adj:엄숙하다 | adj | 엄숙하다 | 2,4 | 2 | hanja=嚴肅- | 用品<br>嚴肅 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:310 |
| ko:adj:여유롭다 | adj | 여유롭다 | 1,3 | 3 | hanja=漢字: 餘裕-- | 餘裕；從容<br>富足；寬裕<br>寬裕 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:306 |
| ko:adj:원만하다 | adj | 원만하다 | 1,3 | 3 | hanja=漢字: 圓滿-- | 圓滿；完美<br>圓滑；和藹<br>圓滿 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:311 |
| ko:adj:저렴하다 | adj | 저렴하다 | 1,3 | 2 | hanja=漢字: 低廉 | 低廉；便宜<br>便宜 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:316 |
| ko:adj:지혜롭다 | adj | 지혜롭다 | 1,3 | 2 | hanja=漢字: 知慧롭다 | 英明；聰慧的；有智慧的<br>聰慧 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:320 |
| ko:adj:진정하다 | adj | 진정하다 | 1,3 | 2 | hanja=漢字: 眞正하다 | 真正的；真心的<br>真正的 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:321 |
| ko:adj:창피하다 | adj | 창피하다 | 1,4 | 2 | hanja=猖披- | 畢業典禮<br>丟臉 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:319 |
| ko:adj:초조하다 | adj | 초조하다 | 2,4 | 2 | hanja=焦燥- | 寄宿<br>焦急 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:326 |
| ko:adj:험하다 | adj | 험하다 | 1,3 | 4 | hanja=漢字: 險-- | 險峻；陡峭<br>兇險<br>粗俗<br>險峻 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:327 |
| ko:adj:화창하다 | adj | 화창하다 | 1,3 | 2 | hanja=漢字: 和暢-- | 和煦；晴朗<br>晴朗 | content_v2/inventory/dictionary/2026-04-30-fix/adj.jsonl:328 |
| ko:adv:각각 | adv | 각각 | 1,2 | 2 | hanja=各各 | 各自；各個<br>各自；各別；各 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:80 |
| ko:adv:결코 | adv | 결코 | 1,2 | 2 | hanja=決- | 絕不<br>決不；絕對不；萬萬不 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:81 |
| ko:adv:공연히 | adv | 공연히 | 2,3 | 2 | hanja=空然- | 億<br>徒然 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:348 |
| ko:adv:당분간 | adv | 당분간 | 2,3 | 2 | hanja=當分間 | 第六<br>暫時 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:350 |
| ko:adv:매달 | adv | 매달 | 2,3 | 2 | hanja=每- | 數萬；好幾萬<br>每個月 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:345 |
| ko:adv:원래 | adv | 원래 | 1,3 | 2 | hanja=漢字: 原來 | 本來；原來；起初<br>原本 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:354 |
| ko:adv:이왕 | adv | 이왕 | 1,3 | 2 | hanja=漢字: 已往 | 以往；既然<br>既然 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:359 |
| ko:adv:제일 | adv | 제일 | 1,3 | 2 | hanja=漢字: 第一 | 最；第一地<br>最 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:366 |
| ko:adv:종일 | adv | 종일 | 1,3 | 2 | hanja=漢字: 終日 | 整天；終日<br>整天 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:368 |
| ko:adv:항상 | adv | 항상 | 1,2 | 2 | hanja=恒常 | 總是；經常<br>總是；經常；始終 | content_v2/inventory/dictionary/2026-04-30-fix/adv.jsonl:82 |
| ko:count:대 | count | 대 | 1,2,3,4,7 | 13 | hanja=代 | 代；世代<br>台；輛 (機器、車輛單位)<br>(量詞)台；輛；架；(表示一代或款項)<br>竹子；莖；桿<br>代；輩<br>款；款項 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:31 |
| ko:count:등 | count | 등 | 1,2 | 4 | hanja=等 | 等；等等<br>等；等等 (用於列舉後)<br>等級；等 (用於分類)<br>背；背脊 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:3 |
| ko:count:법 | count | 법 | 1,3 | 4 | hanja=法 | 法律；法規。國家規定的行為準則。<br>方法；辦法。做某事的方式。<br>道理；常理。事物發展的規律。<br>法律；法 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:63 |
| ko:count:세 | count | 세 | 1,2 | 4 | hanja=歲 | 歲<br>三（數字）<br>歲；年齡<br>租；租賃 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:55 |
| ko:count:인분 | count | 인분 | 1,3 | 2 | hanja=人分 | 人份（計量單位）<br>人份 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:97 |
| ko:count:장 | count | 장 | 1,2,5 | 3 | hanja=張 | 張 (紙、圖等的量詞)<br>張；頁（紙張、照片等計量單位）<br>張 | content_v2/inventory/dictionary/2026-04-30-fix/count.jsonl:51 |

## Same Surface + Same POS Multi-Row Check

No same-surface same-POS multi-row collisions found.

## Next Actions

1. Review the top suspicious rows manually before editing inventory.
2. Decide whether rows with row-level origin and multiple `entry_no` need entry-level origin metadata.
3. Keep `mapping_v2.entry_refs` aligned with the current key model until an explicit homonym-ID migration is approved.
4. Use tokenizer/handoff context for lesson-level disambiguation instead of changing global atom IDs prematurely.
