import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
WORKLOG_DIR = os.path.join(DOCS_DIR, "worklogs")
INDEX_FILE = os.path.join(DOCS_DIR, "index.md")

START = "## 📋 Recent Worklogs"
END = "## 🎯 Task Registry"


def latest_worklogs(limit=10):
    names = [
        name
        for name in os.listdir(WORKLOG_DIR)
        if name.endswith(".md") and name[0].isdigit()
    ]
    return sorted(names, reverse=True)[:limit]


def render_section():
    lines = [
        START,
        "",
        "| Date | File |",
        "| :--- | :--- |",
    ]
    for name in latest_worklogs():
        date = name.removesuffix(".md")
        lines.append(f"| {date} | [{name}](worklogs/{name}) |")
    lines.extend([
        "",
        "> [!TIP]",
        "> Worklog 唯一存放處：`docs/worklogs/YYYY-MM-DD.md`。",
        "> 所有 Repo 的收工協議 (`/wrap`) 都會自動寫入此處。",
        "> 若 recent list 過期，執行 `python scripts/update_recent_worklogs.py`。",
        "",
    ])
    return "\n".join(lines)


def main():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(START)
    end_idx = content.find(END)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        raise SystemExit("Recent Worklogs section markers not found")

    updated = content[:start_idx] + render_section() + "\n" + content[end_idx:]
    if updated == content:
        print("No changes needed in docs/index.md")
        return

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(updated)
    print("Updated docs/index.md recent worklogs")


if __name__ == "__main__":
    main()
