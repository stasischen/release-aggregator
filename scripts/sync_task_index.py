import os
import json
import re
import sys

# 設定路徑 (以 release-aggregator 根目錄為基準)
# 腳本預期在 release-aggregator/scripts 下執行，或從根目錄執行
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASK_DIR = os.path.join(BASE_DIR, "docs", "tasks")
INDEX_FILE = os.path.join(TASK_DIR, "TASK_INDEX.md")

def get_task_status(json_path):
    """讀取 JSON 檔案並計算任務進度 (DONE/TOTAL)"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
        return None
    
    tasks = data.get("tasks", [])
    if not tasks:
        return None
    
    done_count = sum(1 for t in tasks if t.get("status") == "DONE")
    total_count = len(tasks)
    
    return f"{done_count}/{total_count} tasks"

def update_index():
    """更新 TASK_INDEX.md 中的進度欄位"""
    if not os.path.exists(INDEX_FILE):
        print(f"Index file not found: {INDEX_FILE}")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    updated_lines = []
    
    # 正規表達式說明：
    # 1. | ID | Description | Phase | Progress | [JSON](FILE.json) |
    # 2. 擷取 ID, 當前 Progress, 以及 JSON 檔名
    # 範例：| MAPPING_DICTIONARY | ... | A2 | 8/14 tasks | [JSON](MAPPING_DICTIONARY_TASKS.json) |
    pattern = re.compile(r'\|\s*([A-Z0-9_-]+)\s*\|[^|]*\|[^|]*\|\s*([^|]*tasks[^|]*|Backlog|Pending)\s*\|\s*\[JSON\]\(([^)]+\.json)\)', re.IGNORECASE)

    change_count = 0
    for line in lines:
        new_line = line
        match = pattern.search(line)
        if match:
            task_id = match.group(1)
            current_progress = match.group(2).strip()
            json_filename = match.group(3)
            
            json_path = os.path.join(TASK_DIR, json_filename)
            if os.path.exists(json_path):
                new_progress = get_task_status(json_path)
                if new_progress and new_progress != current_progress:
                    print(f"Updating {task_id}: {current_progress} -> {new_progress}")
                    # 使用 replace 且確保只替換 Progress 部分
                    # 重新組合該列或使用更精確的 replace
                    new_line = line.replace(f" {current_progress} ", f" {new_progress} ")
                    # 如果 replace 失敗 (可能是空格不對)，改用分割替換
                    if new_line == line:
                         parts = line.split('|')
                         if len(parts) >= 5:
                             parts[4] = f" {new_progress} "
                             new_line = "|".join(parts)
                    change_count += 1
        
        updated_lines.append(new_line)

    if change_count > 0:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(updated_lines) + "\n")
        print(f"Successfully updated {change_count} task(s) in {INDEX_FILE}")
    else:
        print("No changes needed in TASK_INDEX.md")

if __name__ == "__main__":
    update_index()
