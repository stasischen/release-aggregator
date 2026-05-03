import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TASK_DIR = os.path.join(BASE_DIR, "docs", "tasks")
INDEX_FILE = os.path.join(TASK_DIR, "TASK_INDEX.md")

DONE_STATUSES = {"done", "completed", "complete", "DONE", "COMPLETED"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_task_json(task_id):
    candidates = [
        os.path.join(TASK_DIR, f"{task_id}_TASKS.json"),
        os.path.join(TASK_DIR, f"{task_id}.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path

    for name in os.listdir(TASK_DIR):
        if name.endswith("_TASKS.json") and name.upper().startswith(task_id.upper()):
            return os.path.join(TASK_DIR, name)
    return None


def is_done(task):
    return task.get("status") in DONE_STATUSES


def task_map(tasks):
    return {task.get("id"): task for task in tasks if task.get("id")}


def dependency_report(tasks):
    by_id = task_map(tasks)
    ready = []
    blocked = []
    done = []

    for task in tasks:
        task_id = task.get("id", "<missing-id>")
        if is_done(task):
            done.append(task_id)
            continue

        missing = []
        unfinished = []
        for dep in task.get("depends_on", []):
            dep_task = by_id.get(dep)
            if dep_task is None:
                missing.append(dep)
            elif not is_done(dep_task):
                unfinished.append(dep)

        if missing or unfinished:
            blocked.append((task_id, missing, unfinished))
        else:
            ready.append(task_id)

    return ready, blocked, done


def index_line_for(task_id):
    if not os.path.exists(INDEX_FILE):
        return None
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("|") and f"| {task_id} " in line:
                return line.strip()
    return None


def main(argv):
    if len(argv) != 2:
        print("Usage: python scripts/check_task_readiness.py <TASK_ID>")
        return 2

    task_id = argv[1]
    json_path = find_task_json(task_id)
    if not json_path:
        print(f"Task JSON not found for {task_id}")
        return 1

    data = load_json(json_path)
    tasks = data.get("tasks", [])
    ready, blocked, done = dependency_report(tasks)
    index_line = index_line_for(task_id)

    print(f"task_id: {task_id}")
    print(f"task_json: {os.path.relpath(json_path, BASE_DIR)}")
    if index_line:
        print(f"task_index: {index_line}")
    print(f"done: {len(done)}/{len(tasks)}")

    print("\nready:")
    for item in ready:
        print(f"- {item}")
    if not ready:
        print("- none")

    print("\nblocked:")
    for item, missing, unfinished in blocked:
        details = []
        if missing:
            details.append("missing deps: " + ", ".join(missing))
        if unfinished:
            details.append("unfinished deps: " + ", ".join(unfinished))
        print(f"- {item}: {'; '.join(details)}")
    if not blocked:
        print("- none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
