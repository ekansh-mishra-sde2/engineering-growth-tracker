#!/usr/bin/env python3
"""
update_readme.py
Reads LeetCode progress + learning logs and updates the README stats block.
Runs automatically via GitHub Actions daily.
"""

import json
import os
import glob
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(ROOT, "README.md")
LEETCODE_PATH = os.path.join(ROOT, "logs", "leetcode", "progress.json")
LEARNING_DIR = os.path.join(ROOT, "logs", "learning")


def load_leetcode():
    try:
        with open(LEETCODE_PATH) as f:
            return json.load(f)
    except Exception:
        return {"easy": 0, "medium": 0, "hard": 0, "streak_days": 0,
                "total": 0, "last_solved": "", "last_updated": ""}


def count_learning_logs():
    files = glob.glob(os.path.join(LEARNING_DIR, "*.md"))
    return len(files)


def get_recent_topics(n=5):
    files = sorted(glob.glob(os.path.join(LEARNING_DIR, "*.md")), reverse=True)[:n]
    topics = []
    for f in files:
        date_str = os.path.basename(f).replace(".md", "")
        try:
            with open(f) as fh:
                first_line = fh.readline().strip().replace("## Topic: ", "")
            topics.append(f"- `{date_str}` — {first_line}")
        except Exception:
            topics.append(f"- `{date_str}` — (no title)")
    return "\n".join(topics) if topics else "- No entries yet"


def get_week_log_count():
    count = 0
    today = datetime.utcnow().date()
    for i in range(7):
        d = today - timedelta(days=i)
        path = os.path.join(LEARNING_DIR, f"{d}.md")
        if os.path.exists(path):
            count += 1
    return count


def build_stats_block(lc, log_count, recent_topics, week_count):
    total = lc.get("easy", 0) + lc.get("medium", 0) + lc.get("hard", 0)
    streak = lc.get("streak_days", 0)
    last_solved = lc.get("last_solved", "—") or "—"
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # simple ASCII progress bar (out of 200 target)
    target = 200
    filled = min(int((total / target) * 20), 20)
    bar = "█" * filled + "░" * (20 - filled)

    block = f"""### 🧩 LeetCode Progress
| Difficulty | Solved |
|---|---|
| 🟢 Easy | {lc.get('easy', 0)} |
| 🟡 Medium | {lc.get('medium', 0)} |
| 🔴 Hard | {lc.get('hard', 0)} |
| **Total** | **{total}** |

**Target:** {total} / {target} problems  
`{bar}` {round((total/target)*100, 1)}%

🔥 **Current streak:** {streak} day(s)  
✅ **Last solved:** {last_solved}

---

### ☁️ Learning Log
| Metric | Count |
|---|---|
| 📝 Total learning entries | {log_count} |
| 📅 Entries this week | {week_count} |

**Recent topics:**
{recent_topics}

---

*🤖 Auto-updated on {now}*"""
    return block


def update_readme(stats_block):
    with open(README_PATH, "r") as f:
        content = f.read()

    start_marker = "<!-- STATS:START -->"
    end_marker = "<!-- STATS:END -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: markers not found in README")
        return False

    new_content = (
        content[:start_idx + len(start_marker)]
        + "\n"
        + stats_block
        + "\n"
        + content[end_idx:]
    )

    with open(README_PATH, "w") as f:
        f.write(new_content)

    print("✅ README updated successfully")
    return True


if __name__ == "__main__":
    lc = load_leetcode()
    log_count = count_learning_logs()
    recent_topics = get_recent_topics(5)
    week_count = get_week_log_count()
    stats_block = build_stats_block(lc, log_count, recent_topics, week_count)
    update_readme(stats_block)
