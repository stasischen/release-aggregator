import os
import json

# 設定路徑 (以 release-aggregator 根目錄為基準)
# 腳本預期在 release-aggregator/scripts 下執行，或從根目錄執行
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASK_DIR = os.path.join(BASE_DIR, "docs", "tasks")
INDEX_FILE = os.path.join(TASK_DIR, "TASK_INDEX.md")
DONE_STATUSES = {"done", "completed", "complete", "DONE", "COMPLETED", "COMPLETE"}

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
    
    done_count = sum(1 for t in tasks if t.get("status") in DONE_STATUSES)
    total_count = len(tasks)
    
    return f"{done_count}/{total_count} tasks"

def extract_json_filename(cell):
    marker = "[JSON]("
    start = cell.find(marker)
    if start == -1:
        return None
    start += len(marker)
    end = cell.find(")", start)
    if end == -1:
        return None
    filename = cell[start:end]
    return filename if filename.endswith(".json") else None

def update_index():
    """更新 TASK_INDEX.md 中的進度欄位"""
    if not os.path.exists(INDEX_FILE):
        print(f"Index file not found: {INDEX_FILE}")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.splitlines()
    updated_lines = []
    
    change_count = 0
    current_headers = None
    for line in lines:
        new_line = line

        if line.startswith("|") and "Task" in line and "檔案" in line:
            current_headers = [cell.strip() for cell in line.strip("|").split("|")]
        elif line.startswith("|") and current_headers and not set(line.replace("|", "").strip()) <= {":", "-", " "}:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) == len(current_headers):
                header_index = {name: idx for idx, name in enumerate(current_headers)}
                progress_idx = header_index.get("進度")
                files_idx = header_index.get("檔案")
                task_idx = header_index.get("TASK_ID", header_index.get("Task ID"))
                if progress_idx is not None and files_idx is not None and task_idx is not None:
                    json_filename = extract_json_filename(cells[files_idx])
                    if json_filename:
                        json_path = os.path.join(TASK_DIR, json_filename)
                        if os.path.exists(json_path):
                            current_progress = cells[progress_idx]
                            new_progress = get_task_status(json_path)
                            if new_progress and new_progress != current_progress:
                                print(f"Updating {cells[task_idx]}: {current_progress} -> {new_progress}")
                                cells[progress_idx] = new_progress
                                new_line = "| " + " | ".join(cells) + " |"
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
