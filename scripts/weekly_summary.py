#!/usr/bin/env python3
"""
weekly_summary.py
Every Sunday, auto-generates a weekly summary from the learning logs.
Committed automatically by GitHub Actions.
"""

import os
import glob
import json
from datetime import datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNING_DIR = os.path.join(ROOT, "logs", "learning")
LEETCODE_PATH = os.path.join(ROOT, "logs", "leetcode", "progress.json")
SUMMARIES_DIR = os.path.join(ROOT, "summaries")


def get_week_entries():
    """Get all learning log entries from the past 7 days."""
    entries = []
    today = datetime.utcnow().date()
    for i in range(7):
        d = today - timedelta(days=i)
        path = os.path.join(LEARNING_DIR, f"{d}.md")
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            entries.append({"date": str(d), "content": content})
    return entries


def load_leetcode():
    try:
        with open(LEETCODE_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def build_summary(entries, lc):
    today = datetime.utcnow().date()
    week_start = today - timedelta(days=6)
    week_label = f"{week_start} to {today}"
    total_lc = lc.get("easy", 0) + lc.get("medium", 0) + lc.get("hard", 0)

    lines = [
        f"# 📋 Weekly Summary — {week_label}",
        "",
        "## 📊 Week at a Glance",
        f"- **Learning entries this week:** {len(entries)}",
        f"- **LeetCode total so far:** {total_lc} problems",
        f"  - 🟢 Easy: {lc.get('easy', 0)}  |  🟡 Medium: {lc.get('medium', 0)}  |  🔴 Hard: {lc.get('hard', 0)}",
        f"- **Streak:** {lc.get('streak_days', 0)} day(s)",
        "",
        "---",
        "",
        "## 📝 Learning Entries This Week",
        "",
    ]

    if not entries:
        lines.append("_No entries logged this week. Get back on track! 💪_")
    else:
        for entry in sorted(entries, key=lambda x: x["date"]):
            lines.append(f"### {entry['date']}")
            lines.append(entry["content"].strip())
            lines.append("")
            lines.append("---")
            lines.append("")

    lines += [
        "## 🎯 Reflection",
        "",
        "> _Auto-generated summary. Add your own reflection by editing this file._",
        "",
        "- What went well this week?",
        "- What was challenging?",
        "- Focus for next week:",
        "",
        f"_Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} by GitHub Actions_",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    os.makedirs(SUMMARIES_DIR, exist_ok=True)
    entries = get_week_entries()
    lc = load_leetcode()
    summary = build_summary(entries, lc)

    today = datetime.utcnow().date()
    week_start = today - timedelta(days=6)
    filename = f"week-{week_start}.md"
    out_path = os.path.join(SUMMARIES_DIR, filename)

    with open(out_path, "w") as f:
        f.write(summary)

    print(f"✅ Weekly summary written to summaries/{filename}")
