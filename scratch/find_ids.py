
import json
import glob
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

bank_path = r'e:\Githubs\lingo\content-ko\content\core\learning_library\example_sentence'
targets = ['빵하고 우유를 샀어요.', '여기 앉아도 돼요?', '화장실이 어디예요?']

results = []
for filepath in glob.glob(os.path.join(bank_path, "**/*.json"), recursive=True):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data.get('surface_ko') in targets:
                results.append({"ID": data.get('id'), "Surface": data.get('surface_ko')})
    except Exception:
        continue

print(json.dumps(results, ensure_ascii=False, indent=2))
