"""
stamp_excel_entries.py
----------------------
Reads each daily work-log markdown file and appends an ## Excel Entry section
with pre-formatted Task / Description / Hours / Type fields ready for the
Excel generator to consume directly.

Run:
    uv run python scripts/stamp_excel_entries.py
"""
import os
import re
from datetime import date, timedelta
from collections import defaultdict
import csv

# ── HELPERS ───────────────────────────────────────────────────────────────

def wn(d: date) -> int:
    return (d - date(2026, 3, 16)).days // 7 + 1

SUPPORT_WEEKS = {8, 12, 16, 20, 24}
PT_WEEKS = {1, 2, 3, 4}

# ── LOAD SCALED MEETING HOURS PER WEEK ───────────────────────────────────
# Scale CSV total (67h) down to exactly 54h budget
mtg_by_week: dict[int, float] = defaultdict(float)
with open("work-logs/meetings_cleaned.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        mtg_by_week[int(row["Week"])] += float(row["Duration (hrs)"])

MTG_SCALE = 54.0 / sum(v for k, v in mtg_by_week.items() if k >= 5)

def scaled_mtg(week: int) -> float:
    raw = mtg_by_week.get(week, 0.0)
    return round(raw * MTG_SCALE, 2) if week >= 5 else 0.0

# ── LOAD MEETINGS LIST PER WEEK (for description) ─────────────────────────
mtg_list_by_week: dict[int, list[tuple[str, float]]] = defaultdict(list)
with open("work-logs/meetings_cleaned.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        mtg_list_by_week[int(row["Week"])].append(
            (row["Meeting Title"], float(row["Duration (hrs)"]))
        )

# ── COLLECT ALL WORK LOG FILES ────────────────────────────────────────────
all_files: list[tuple[date, str]] = []
d = date(2026, 3, 16)
while d <= date(2026, 8, 31):
    if d.weekday() < 5:
        fpath = f"work-logs/{d.strftime('%Y-%m')}/{d.isoformat()}.md"
        if os.path.exists(fpath):
            content = open(fpath, encoding="utf-8").read()
            if len(content.splitlines()) > 5:
                all_files.append((d, fpath))
    d += timedelta(days=1)

# Pre-compute days per week for meeting hour distribution
days_per_week: dict[int, int] = defaultdict(int)
for d, _ in all_files:
    days_per_week[wn(d)] += 1

# ── PARSE WORK LOG SECTIONS ───────────────────────────────────────────────

def extract_task_and_bullets(content: str) -> list[tuple[str, list[str], str]]:
    """
    Returns list of (task_name, bullets, section_type).
    section_type: 'dev' | 'support'
    """
    results = []

    # Split on --- separators, find Work Log / RPA Support sections
    sections = re.split(r'\n---+\n', content)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Work Log section: **Work Log — TASK — repo**
        wl_match = re.search(r'\*\*Work Log[^\*]*?—\s*([^—\n\*]+?)(?:\s*—[^\*\n]+)?\*\*', section)
        # RPA Support section
        sup_match = re.search(r'\*\*RPA Support Shift', section)

        if wl_match:
            task_name = wl_match.group(1).strip()
            # Extract bullet lines (skip commit table rows)
            bullets = []
            for line in section.splitlines():
                line = line.strip()
                if line.startswith("- ") and len(line) > 25:
                    # Skip lines that look like commit table rows (have | Time |)
                    if "|" not in line:
                        b = line[2:].strip()
                        # Clean markdown
                        b = re.sub(r'`([^`]+)`', r'\1', b)
                        b = re.sub(r'\*+', '', b)
                        b = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', b)
                        if len(b) > 20:
                            bullets.append(b)
            if task_name and bullets:
                results.append((task_name[:80], bullets[:10], "dev"))

        elif sup_match:
            task_name = "RPA Production Support Shift"
            bullets = []
            for line in section.splitlines():
                line = line.strip()
                if line.startswith("- ") and len(line) > 25 and "|" not in line:
                    b = line[2:].strip()
                    b = re.sub(r'`([^`]+)`', r'\1', b)
                    b = re.sub(r'\*+', '', b)
                    b = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', b)
                    if len(b) > 20:
                        bullets.append(b[:200])
            if bullets:
                results.append((task_name, bullets[:8], "support"))

    return results


def read_hours(content: str) -> tuple[float, float]:
    """Returns (dev_hours, meeting_hours) from the stamped fields."""
    dev = 0.0
    mtg = 0.0
    m = re.search(r'\*\*Dev Hours:\*\*\s*([\d.]+)h', content)
    if m:
        dev = float(m.group(1))
    m = re.search(r'\*\*Meeting Hours:\*\*\s*([\d.]+)h', content)
    if m:
        mtg = float(m.group(1))
    return dev, mtg


# ── BUILD AND STAMP EXCEL ENTRY SECTIONS ─────────────────────────────────

stamped = 0
skipped = 0

for d, fpath in all_files:
    week = wn(d)
    content = open(fpath, encoding="utf-8").read()

    # Remove existing ## Excel Entry section if present
    content = re.sub(r'\n## Excel Entry\n[\s\S]*$', '', content).rstrip()

    dev_hrs, _ = read_hours(content)
    task_sections = extract_task_and_bullets(content)

    if not task_sections and week not in PT_WEEKS:
        skipped += 1
        # Still stamp with a minimal entry so file is consistent
        entry_lines = ["", "## Excel Entry", ""]
        entry_lines += [f"**Task:** Development & Implementation"]
        entry_lines += ["**Description:**"]
        entry_lines += ["- Continued development work and implementation tasks."]
        entry_lines += [f"**Hours:** {dev_hrs:.1f}"]
        entry_lines += ["**Type:** dev"]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content + "\n" + "\n".join(entry_lines) + "\n")
        continue

    # ── PT WEEKS: single combined entry ───────────────────────────────
    if week in PT_WEEKS:
        entry_lines = ["", "## Excel Entry", ""]
        if task_sections:
            # Use first task name
            task_name = task_sections[0][0]
            all_bullets = []
            for _, bullets, _ in task_sections:
                all_bullets.extend(bullets)
            entry_lines += [f"**Task:** {task_name}"]
            entry_lines += ["**Description:**"]
            for b in all_bullets[:10]:
                entry_lines += [f"- {b}"]
        else:
            entry_lines += ["**Task:** Onboarding & Environment Setup"]
            entry_lines += ["**Description:**"]
            entry_lines += ["- Environment setup, access configuration, and learning."]
        entry_lines += [f"**Hours:** {dev_hrs:.1f}"]
        entry_lines += ["**Type:** dev"]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content + "\n" + "\n".join(entry_lines) + "\n")
        stamped += 1
        continue

    # ── SUPPORT WEEKS: dev tasks + support shift ───────────────────────
    if week in SUPPORT_WEEKS:
        entry_lines = ["", "## Excel Entry", ""]
        # Separate support vs dev sections
        dev_tasks = [(t, b) for t, b, typ in task_sections if typ == "dev"]
        sup_tasks = [(t, b) for t, b, typ in task_sections if typ == "support"]

        if sup_tasks:
            # Support shift entry
            entry_lines += ["**Task:** RPA Production Support Shift"]
            entry_lines += ["**Description:**"]
            for b in sup_tasks[0][1][:8]:
                entry_lines += [f"- {b}"]
            entry_lines += [f"**Hours:** {dev_hrs:.1f}"]
            entry_lines += ["**Type:** support"]

        if dev_tasks:
            # Additional dev work done during support week
            entry_lines += [""]
            entry_lines += [f"**Task:** {dev_tasks[0][0]}"]
            entry_lines += ["**Description:**"]
            for b in dev_tasks[0][1][:8]:
                entry_lines += [f"- {b}"]
            entry_lines += ["**Hours:** 0.0"]  # hours already counted in support row
            entry_lines += ["**Type:** dev_support"]

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content + "\n" + "\n".join(entry_lines) + "\n")
        stamped += 1
        continue

    # ── NORMAL FT WEEKS ───────────────────────────────────────────────
    # Distribute dev hours across task sections proportionally
    # All tasks in a day share the day's dev hours equally
    n_tasks = len([t for t in task_sections if t[2] == "dev"])
    hours_per_task = round(dev_hrs / n_tasks, 1) if n_tasks > 0 else dev_hrs

    entry_lines = ["", "## Excel Entry", ""]
    first = True
    for task_name, bullets, typ in task_sections:
        if not first:
            entry_lines += [""]
        first = False
        entry_lines += [f"**Task:** {task_name}"]
        entry_lines += ["**Description:**"]
        for b in bullets[:8]:
            entry_lines += [f"- {b}"]
        entry_lines += [f"**Hours:** {hours_per_task:.1f}"]
        entry_lines += [f"**Type:** {typ}"]

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content + "\n" + "\n".join(entry_lines) + "\n")
    stamped += 1

print(f"Stamped: {stamped}  Skipped (no tasks): {skipped}  Total: {stamped + skipped}")
print()

# ── VERIFICATION: show sample entries ─────────────────────────────────────
samples = [
    "work-logs/2026-03/2026-03-16.md",   # PT W1
    "work-logs/2026-05/2026-05-11.md",   # FT W9
    "work-logs/2026-06/2026-06-01.md",   # Support W12
    "work-logs/2026-07/2026-07-28.md",   # Support W20
]
for p in samples:
    if os.path.exists(p):
        content = open(p, encoding="utf-8").read()
        idx = content.find("## Excel Entry")
        if idx >= 0:
            print(f"=== {p} ===")
            print(content[idx:idx+400])
            print()
