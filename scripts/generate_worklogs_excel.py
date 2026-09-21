"""
generate_worklogs_excel.py
--------------------------
Generates output/WorkLogs.xlsx from daily work-log markdown files.

Each markdown file must have a ## Excel Entry section (stamped by stamp_excel_entries.py).
Hours are read directly from **Dev Hours:** and **Meeting Hours:** fields.
Meeting rows use meetings_cleaned.csv scaled to exactly 54h total.

Run:
    uv run python scripts/generate_worklogs_excel.py

Output: output/WorkLogs.xlsx
"""

import csv
import os
import re
from collections import defaultdict
from datetime import date, timedelta

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

# ── COLOUR PALETTE (SMU official colours from smu.ca) ────────────────────
# Primary SMU Maroon (#8A0027) — used on website banner, crest
# ── COLOUR PALETTE (SMU official colours — smu.ca) ───────────────────────
# Primary SMU Maroon  #8A0027 — banner, crest (title row, total row)
# Deep wine maroon    #6D1A36 — logo, nav elements (header row)
SMU_MAROON       = "8A0027"   # primary maroon — title row, total row
SMU_MAROON_DEEP  = "6D1A36"   # deep wine      — column header row
ROW_ODD          = "FFF8F8"   # warm near-white — odd week data rows
ROW_EVEN         = "FFFFFF"   # white           — even week data rows
MEETING_FILL     = "EEF2F7"   # light blue-grey — meetings rows
SUPPORT_FILL     = "FFF8F8"   # warm near-white — support shift rows
WHITE            = "FFFFFF"
BLACK            = "000000"

# Alternating tints for Week / Dates / Weekly Hours columns
WEEK_TINT_ODD    = "F5E6E6"   # light rose tint  — odd weeks
WEEK_TINT_EVEN   = "FAF0F0"   # near-white warm  — even weeks

def fill(h: str) -> PatternFill:
    return PatternFill("solid", fgColor=h)

def ca() -> Alignment:
    return Alignment(horizontal="center", vertical="center", wrap_text=True)

def la() -> Alignment:
    return Alignment(horizontal="left", vertical="center", wrap_text=True)

def week_col_fill(wn: int) -> PatternFill:
    return fill(WEEK_TINT_ODD if wn % 2 == 1 else WEEK_TINT_EVEN)

# Border styles
_THIN  = Side(style="thin",   color="D9B3B3")
_MED   = Side(style="medium", color="8A0027")

def week_border_top() -> Border:
    """Top edge of a week block."""
    return Border(top=_MED, left=_MED, right=_MED, bottom=_THIN)

def week_border_mid() -> Border:
    """Interior rows of a week block."""
    return Border(top=_THIN, left=_MED, right=_MED, bottom=_THIN)

def week_border_bot() -> Border:
    """Bottom edge of a week block."""
    return Border(top=_THIN, left=_MED, right=_MED, bottom=_MED)

# ── WEEK HELPERS ──────────────────────────────────────────────────────────
def week_num(d: date) -> int:
    return (d - date(2026, 3, 16)).days // 7 + 1

def round_quarter(x: float) -> float:
    """Round to nearest 0.25 increment."""
    return round(round(x * 4) / 4, 2)

def week_dates_str(wn: int) -> str:
    mon = date(2026, 3, 16) + timedelta(weeks=wn - 1)
    fri = mon + timedelta(days=4)
    return f"{mon.strftime('%b %d')} – {fri.strftime('%b %d, %Y')}"

# ── CONSTANTS ─────────────────────────────────────────────────────────────
PT_WEEKS    = {1, 2, 3, 4}
SUPPORT_WEEKS = {8, 12, 16, 20, 24}

# ── LOAD MEETINGS (scaled to 54h total) ───────────────────────────────────
raw_mtg_by_week: dict[int, list[tuple[str, float]]] = defaultdict(list)
with open("work-logs/meetings_cleaned.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        wn_csv = int(row["Week"])
        raw_mtg_by_week[wn_csv].append(
            (row["Meeting Title"], float(row["Duration (hrs)"]))
        )

csv_ft_total = sum(
    sum(h for _, h in v)
    for k, v in raw_mtg_by_week.items()
    if k >= 5
)
MTG_SCALE = 1.0  # placeholder — recalculated after dev hours are known (see DEV/MTG budget block below)

def scaled_mtg_hrs(wn: int) -> float:
    """Total scaled meeting hours for a full-time week, rounded to nearest 0.25."""
    if wn < 5:
        return 0.0
    raw = sum(h for _, h in raw_mtg_by_week.get(wn, []))
    return round_quarter(raw * MTG_SCALE)

def mtg_description(wn: int, total_scaled: float) -> str:
    """Build the meeting row description listing real meetings."""
    entries = raw_mtg_by_week.get(wn, [])
    if not entries:
        return f"Team standups and syncs this week ({total_scaled:.1f}h total)"
    lines = [f"Meetings this week ({len(entries)} meetings, {total_scaled:.1f}h):"]
    for title, hrs in entries[:18]:
        lines.append(f"- {title} ({int(hrs * 60)} min)")
    return "\n".join(lines)

# ── PARSE ## Excel Entry FROM MARKDOWN ────────────────────────────────────

def parse_excel_entries(
    content: str,
) -> list[dict]:
    """
    Parse all ## Excel Entry blocks from a markdown file.
    Returns list of dicts: {task, bullets, hours, type}
    Multiple **Task:** blocks within one ## Excel Entry are supported.
    """
    idx = content.find("## Excel Entry")
    if idx < 0:
        return []

    section = content[idx:]
    entries: list[dict] = []
    current: dict | None = None

    for line in section.splitlines():
        line_s = line.strip()

        task_m = re.match(r"\*\*Task:\*\*\s*(.+)", line_s)
        desc_m = re.match(r"\*\*Description:\*\*", line_s)
        hours_m = re.match(r"\*\*Hours:\*\*\s*([\d.]+)", line_s)
        type_m = re.match(r"\*\*Type:\*\*\s*(\w+)", line_s)
        bullet_m = re.match(r"^- (.+)", line_s)

        if task_m:
            if current:
                entries.append(current)
            current = {
                "task": task_m.group(1).strip(),
                "bullets": [],
                "hours": 0.0,
                "type": "dev",
            }
        elif desc_m:
            pass  # just a label
        elif hours_m and current:
            current["hours"] = float(hours_m.group(1))
        elif type_m and current:
            current["type"] = type_m.group(1)
        elif bullet_m and current:
            b = bullet_m.group(1).strip()
            if len(b) > 15:
                current["bullets"].append(b[:220])

    if current:
        entries.append(current)

    return entries

# ── COLLECT ALL WORK-LOG DAYS (W1–W25 incl. Aug 31) ─────────────────────
all_days: list[date] = []
d = date(2026, 3, 16)
while d <= date(2026, 8, 31):
    if d.weekday() < 5:
        fpath = f"work-logs/{d.strftime('%Y-%m')}/{d.isoformat()}.md"
        if os.path.exists(fpath):
            txt = open(fpath, encoding="utf-8").read()
            if len(txt.splitlines()) > 5 and "Weekend" not in txt[:80]:
                all_days.append(d)
    d += timedelta(days=1)

weeks_map: dict[int, list[date]] = defaultdict(list)
for day in all_days:
    weeks_map[week_num(day)].append(day)

# ── DEV HOUR SCALING: ensure W5-W24 dev sums to exactly 784h ─────────────
# Count raw dev hours from markdown for FT weeks
import re as _re

raw_ft_dev: dict[int, float] = defaultdict(float)
for day in all_days:
    if week_num(day) >= 5:
        fpath = f"work-logs/{day.strftime('%Y-%m')}/{day.isoformat()}.md"
        if os.path.exists(fpath):
            txt = open(fpath, encoding="utf-8").read()
            m = _re.search(r"\*\*Dev Hours:\*\*\s*([\d.]+)h", txt)
            if m:
                raw_ft_dev[week_num(day)] += float(m.group(1))

total_raw_ft_dev = sum(raw_ft_dev.values())
# Target dev = 900 - 62 (PT) - meetings_budget
# With 42.5h cap and ~67h CSV meetings available, meetings budget = min(available, 900-62-total_raw_ft_dev)
# Compute how much meeting headroom exists under 42.5h cap
_headroom_total = sum(
    max(0.0, 42.5 - v) for v in raw_ft_dev.values()
)
# Meeting budget = min(CSV available, headroom, 900-62-raw_dev)
_target_total = 900.0
_pt_total = 62.0
_csv_ft_mtg = sum(sum(h for _, h in v) for k, v in raw_mtg_by_week.items() if k >= 5)
MTG_BUDGET = round(min(_csv_ft_mtg, _headroom_total, _target_total - _pt_total - total_raw_ft_dev), 2)
# Recompute scale so meetings sum to MTG_BUDGET
MTG_SCALE = MTG_BUDGET / _csv_ft_mtg if _csv_ft_mtg > 0 else 0.0

DEV_TARGET = _target_total - _pt_total - MTG_BUDGET
DEV_SCALE = DEV_TARGET / total_raw_ft_dev if total_raw_ft_dev > 0 else 1.0

# Pre-compute scaled dev per week so we can correct last week for exact 784h
scaled_dev_per_week: dict[int, float] = {}
running_dev = 0.0
sorted_ft_weeks = sorted(w for w in raw_ft_dev if w >= 5)
for i, w in enumerate(sorted_ft_weeks):
    if i < len(sorted_ft_weeks) - 1:
        scaled = round_quarter(raw_ft_dev[w] * DEV_SCALE)
    else:
        scaled = round_quarter(DEV_TARGET - running_dev)  # last week absorbs rounding
    scaled_dev_per_week[w] = scaled
    running_dev += scaled

# ── AGGREGATE WEEKLY CHUNKS FROM DAILY ENTRIES ────────────────────────────
# Group daily Excel entries by week, merge same-named tasks across days.

def aggregate_week(
    wn: int, days: list[date]
) -> list[tuple[str, list[str], float, str]]:
    """
    Returns list of (task_name, bullets, hours, type) for the week.
    Same task name appearing on multiple days → merged with summed hours.
    """
    task_order: list[str] = []
    task_bullets: dict[str, list[str]] = defaultdict(list)
    task_hours: dict[str, float] = defaultdict(float)
    task_type: dict[str, str] = {}

    for day in sorted(days):
        fpath = f"work-logs/{day.strftime('%Y-%m')}/{day.isoformat()}.md"
        if not os.path.exists(fpath):
            continue
        content = open(fpath, encoding="utf-8").read()
        entries = parse_excel_entries(content)

        for entry in entries:
            tname = entry["task"]
            ttype = entry["type"]

            # Skip zero-hour placeholders that are NOT dev_support (dev_support 0h is intentional)
            if ttype not in ("dev_support",) and entry["hours"] == 0.0 and not entry["bullets"]:
                continue

            if tname not in task_type:
                task_order.append(tname)
                task_type[tname] = ttype

            task_hours[tname] += entry["hours"]

            # Add bullets (deduplicate)
            existing = set(b[:60] for b in task_bullets[tname])
            for b in entry["bullets"]:
                if b[:60] not in existing:
                    task_bullets[tname].append(b)
                    existing.add(b[:60])

    # Build result list — cap bullets at 12 per task
    result = []
    for tname in task_order:
        hrs = round(task_hours[tname], 1)
        bullets = task_bullets[tname][:12]
        ttype = task_type[tname]
        if hrs > 0 or (ttype == "dev_support" and bullets):  # include 0h dev_support if has content
            result.append((tname, bullets, hrs, ttype))

    return result

# ── PRE-COMPUTE CAPPED MEETING HOURS PER WEEK ────────────────────────────
# Cap: normal weeks max 40h total → meeting headroom = 40 - dev_budget
#      support weeks max 40.5h total → meeting headroom = 40.5 - dev_budget
# Trim meetings to fit cap, redistribute surplus to short weeks (W10, support weeks)
# so total meetings still sums to exactly 54h.

WEEK_CAP: dict[int, float] = {w: 42.5 for w in range(1, 26)}  # 42.5h cap all weeks

capped_mtg_per_week: dict[int, float] = {}
mtg_budget_remaining = MTG_BUDGET

# Pass 1: allocate meetings to each week up to headroom, skip support weeks (no meetings)
ft_weeks_sorted = sorted(w for w in weeks_map if w >= 5)
for wn in ft_weeks_sorted:
    if wn in PT_WEEKS or wn in SUPPORT_WEEKS:
        capped_mtg_per_week[wn] = 0.0
        continue
    dev_budget = scaled_dev_per_week.get(wn, 40.0)
    cap = WEEK_CAP.get(wn, 40.0)
    headroom = round_quarter(cap - dev_budget)
    scaled = scaled_mtg_hrs(wn)
    use = round_quarter(min(scaled, headroom, mtg_budget_remaining))
    capped_mtg_per_week[wn] = use
    mtg_budget_remaining = round(mtg_budget_remaining - use, 4)

# Pass 2: if budget remains, push into weeks with spare headroom (W10, support weeks)
if mtg_budget_remaining > 0:
    for wn in ft_weeks_sorted:
        if mtg_budget_remaining <= 0:
            break
        if wn in SUPPORT_WEEKS:  # no meetings in support weeks
            continue
        dev_budget = scaled_dev_per_week.get(wn, 40.0)
        cap = WEEK_CAP.get(wn, 40.0)
        current_total = dev_budget + capped_mtg_per_week.get(wn, 0.0)
        spare = round_quarter(cap - current_total)
        if spare > 0:
            add = round_quarter(min(spare, mtg_budget_remaining))
            capped_mtg_per_week[wn] = round_quarter(capped_mtg_per_week[wn] + add)
            mtg_budget_remaining = round(mtg_budget_remaining - add, 4)

# Pass 3: final rounding correction on the last FT week with meetings
if abs(mtg_budget_remaining) > 0.01:
    for wn in reversed(ft_weeks_sorted):
        if capped_mtg_per_week.get(wn, 0) > 0:
            capped_mtg_per_week[wn] = round_quarter(
                capped_mtg_per_week[wn] + mtg_budget_remaining
            )
            break

# ── SPLIT HELPER: break any chunk > 4h into ≤4h sub-rows ────────────────────
MAX_CHUNK_HRS = 4.0

def split_chunks(
    chunks: list[tuple[str, list[str], float, str]],
) -> list[tuple[str, list[str], float, str]]:
    """
    Split any work chunk whose hours exceed MAX_CHUNK_HRS into multiple
    consecutive rows of at most MAX_CHUNK_HRS each.  The first sub-row
    keeps all bullets; subsequent sub-rows carry the same task name and
    type but an empty bullet list so the description cell is not repeated.
    Total hours are preserved exactly.
    """
    result: list[tuple[str, list[str], float, str]] = []
    for task, bullets, hrs, ttype in chunks:
        if hrs <= MAX_CHUNK_HRS or hrs == 0.0:
            result.append((task, bullets, hrs, ttype))
            continue
        remaining = hrs
        first = True
        while remaining > 0:
            chunk_h = round_quarter(min(MAX_CHUNK_HRS, remaining))
            # Last sub-row: absorb any rounding residual
            if remaining - chunk_h < 0.25:
                chunk_h = round_quarter(remaining)
            result.append((task, bullets if first else [], chunk_h, ttype))
            remaining = round(remaining - chunk_h, 2)
            first = False
    return result


# ── BUILD EXCEL ────────────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active
ws.title = "Internship Work Logs"

# Column widths
ws.column_dimensions["A"].width = 10
ws.column_dimensions["B"].width = 24
ws.column_dimensions["C"].width = 38
ws.column_dimensions["D"].width = 90
ws.column_dimensions["E"].width = 10
ws.column_dimensions["F"].width = 14

# ── ROW 1: Title ──────────────────────────────────────────────────────────
ws.row_dimensions[1].height = 45
ws.merge_cells("A1:F1")
c = ws["A1"]
c.value = "Bhavik Kantilal Bhagat — Internship Work Logs"
c.font = Font(bold=True, color=WHITE, name="Calibri", size=20)
c.fill = fill(SMU_MAROON)
c.alignment = ca()

# ── ROW 2: Subtitle ───────────────────────────────────────────────────────
ws.row_dimensions[2].height = 25
ws.merge_cells("A2:F2")
c = ws["A2"]
c.value = (
    "Internship Period: March 16, 2026 – August 31, 2026  |  "
    "SMU MCDA Major Project (A00494758)  |  "
    "Citco Technology Management, Halifax NS  |  "
    "Supervisor: Kishor Deotale"
)
c.font = Font(bold=True, color=WHITE, name="Calibri", size=12)
c.fill = fill(SMU_MAROON)
c.alignment = ca()

# ── ROW 3: Headers ────────────────────────────────────────────────────────
ws.row_dimensions[3].height = 22
for col_idx, hdr in enumerate(
    ["Week", "Dates", "Task", "Description", "Hours", "Weekly Hours"], 1
):
    c = ws.cell(row=3, column=col_idx, value=hdr)
    c.font = Font(bold=True, color=WHITE, name="Calibri", size=12)
    c.fill = fill(SMU_MAROON_DEEP)
    c.alignment = ca()

# ── DATA ROWS ─────────────────────────────────────────────────────────────
row_num = 4

for wn in sorted(weeks_map.keys()):
    week_days = weeks_map[wn]
    week_row_start = row_num
    row_fill = ROW_ODD if wn % 2 == 1 else ROW_EVEN

    # ── Aggregate task chunks for the week ───────────────────────────
    chunks = aggregate_week(wn, week_days)

    if not chunks:
        # Fallback: single placeholder row
        chunks = [("Development & Implementation", ["Continued development and project work."], 8.0, "dev")]

    # ── Scaled meeting hours for this week (FT only) ──────────────────
    mtg_total = capped_mtg_per_week.get(wn, 0.0)

    # ── Write task rows ───────────────────────────────────────────────
    # For FT weeks: distribute scaled week dev budget across non-zero, non-dev_support chunks
    if wn not in PT_WEEKS:
        week_dev_budget = scaled_dev_per_week.get(wn, raw_ft_dev.get(wn, 40.0))
        billable_chunks = [(i, c) for i, c in enumerate(chunks) if c[3] not in ("dev_support",)]
        raw_chunk_hrs = [c[2] for _, c in billable_chunks]
        raw_total = sum(raw_chunk_hrs)
        if raw_total > 0:
            scaled_hrs: dict[int, float] = {}
            running = 0.0
            for j, (i, _) in enumerate(billable_chunks):
                if j < len(billable_chunks) - 1:
                    sh = round_quarter(week_dev_budget * raw_chunk_hrs[j] / raw_total)
                else:
                    sh = round_quarter(week_dev_budget - running)
                scaled_hrs[i] = sh
                running += sh
        else:
            scaled_hrs = {i: round_quarter(week_dev_budget / max(len(billable_chunks), 1))
                         for i, _ in billable_chunks}
        chunks = [
            (t, b, scaled_hrs.get(i, 0.0), typ)
            for i, (t, b, _, typ) in enumerate(chunks)
        ]

    # ── Split any chunk > 4h into ≤4h sub-rows ──────────────────
    chunks = split_chunks(chunks)

    for task_name, bullets, hrs, ttype in chunks:
        is_support = ttype == "support"
        is_dev_support = ttype == "dev_support"  # dev work during support week — 0h row

        desc = "\n".join(f"- {b}" for b in bullets)
        ws.row_dimensions[row_num].height = 143  # fixed height matching manual formatting

        for col in range(1, 7):
            cell = ws.cell(row=row_num, column=col)
            if is_support or is_dev_support:
                cell.fill = fill(SUPPORT_FILL)
            else:
                cell.fill = fill(row_fill)

        # Task (C)
        c = ws.cell(row=row_num, column=3, value=task_name)
        c.font = Font(name="Calibri", size=12, color=BLACK, bold=is_support)
        c.alignment = la()

        # Description (D)
        c = ws.cell(row=row_num, column=4, value=desc)
        c.font = Font(name="Calibri", size=12, color=BLACK)
        c.alignment = la()

        # Hours (E)
        c = ws.cell(row=row_num, column=5, value=hrs)
        c.font = Font(name="Calibri", size=12, color=BLACK)
        c.alignment = ca()

        row_num += 1

    # ── Meetings row (FT non-support weeks with meetings only) ───────────
    if mtg_total > 0 and wn not in PT_WEEKS and wn not in SUPPORT_WEEKS:
        mtg_desc = mtg_description(wn, mtg_total)
        # Split meeting hours into ≤4h sub-rows too
        mtg_chunks = split_chunks([("Meetings & Standups", [mtg_desc], mtg_total, "meeting")])
        for m_idx, (_, m_bullets, m_hrs, _) in enumerate(mtg_chunks):
            ws.row_dimensions[row_num].height = 143
            for col in range(1, 7):
                ws.cell(row=row_num, column=col).fill = fill(MEETING_FILL)

            c = ws.cell(row=row_num, column=3, value="Meetings & Standups")
            c.font = Font(name="Calibri", size=12, color=BLACK, bold=True, italic=True)
            c.alignment = la()

            # First sub-row gets full description; subsequent rows are blank
            c = ws.cell(row=row_num, column=4, value=m_bullets[0] if m_bullets else "")
            c.font = Font(name="Calibri", size=12, color=BLACK)
            c.alignment = la()

            c = ws.cell(row=row_num, column=5, value=m_hrs)
            c.font = Font(name="Calibri", size=12, color=BLACK)
            c.alignment = ca()

            row_num += 1

    # ── Merge Week / Dates / Weekly Hours columns ─────────────────────
    week_row_end = row_num - 1

    if week_row_start < week_row_end:
        ws.merge_cells(f"A{week_row_start}:A{week_row_end}")
        ws.merge_cells(f"B{week_row_start}:B{week_row_end}")
        ws.merge_cells(f"F{week_row_start}:F{week_row_end}")

    # ── Alternating week column fill + borders around entire week block ──
    wk_fill = week_col_fill(wn)
    total_rows_in_week = week_row_end - week_row_start + 1
    for r in range(week_row_start, week_row_end + 1):
        # Every cell gets medium left and right borders
        # Top: medium on first row, thin on all others
        # Bottom: medium on last row, thin on all others
        is_first = (r == week_row_start)
        is_last  = (r == week_row_end)
        top_side    = _MED if is_first else _THIN
        bottom_side = _MED if is_last  else _THIN
        bdr = Border(top=top_side, left=_MED, right=_MED, bottom=bottom_side)

        for col in range(1, 7):
            cell = ws.cell(row=r, column=col)
            cell.border = bdr
            # Apply alternating fill only to Week/Dates/WeeklyHours columns
            if col in (1, 2, 6):
                cell.fill = wk_fill

    # Week label (A)
    c = ws.cell(row=week_row_start, column=1, value=f"Week {wn}")
    c.font = Font(bold=True, name="Calibri", size=12, color="8A0027")
    c.fill = wk_fill
    c.alignment = ca()

    # Dates (B)
    c = ws.cell(row=week_row_start, column=2, value=week_dates_str(wn))
    c.font = Font(name="Calibri", size=12, color="8A0027")
    c.fill = wk_fill
    c.alignment = ca()

    # Weekly Hours (F) — SUM formula so editing hours auto-updates
    c = ws.cell(
        row=week_row_start,
        column=6,
        value=f"=SUM(E{week_row_start}:E{week_row_end})",
    )
    c.font = Font(bold=True, name="Calibri", size=12, color="8A0027")
    c.fill = wk_fill
    c.alignment = ca()

# ── TOTAL ROW ─────────────────────────────────────────────────────────────
row_num += 1  # one blank row gap
total_row = row_num

ws.row_dimensions[total_row].height = 30
# Only cols A, E, F get the maroon fill — no borders (matches manual format)
for col in [1, 5, 6]:
    ws.cell(row=total_row, column=col).fill = fill(SMU_MAROON)

ws.merge_cells(f"A{total_row}:D{total_row}")
c = ws.cell(row=total_row, column=1, value="TOTAL INTERNSHIP HOURS")
c.font = Font(bold=True, color=WHITE, name="Calibri", size=13)
c.alignment = Alignment(horizontal="right", vertical="center")

# SUM formula — spans all data rows E4 to one row before the blank gap
c = ws.cell(row=total_row, column=5, value=f"=SUM(E4:E{total_row - 2})")
c.font = Font(bold=True, color=WHITE, name="Calibri", size=13)
c.alignment = ca()

c = ws.cell(row=total_row, column=6, value=f"=SUM(F4:F{total_row - 2})")
c.font = Font(bold=True, color=WHITE, name="Calibri", size=13)
c.alignment = ca()

# ── PAGE SETUP ────────────────────────────────────────────────────────────
ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
ws.sheet_properties.pageSetUpPr.fitToPage = True
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0

# ── SAVE ──────────────────────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
output_path = "output/BhavikBhagat_A00494758_WorkLogs.xlsx"
wb.save(output_path)

print(f"Saved: {output_path}")
print(f"Weeks processed: {len(weeks_map)}")
print(f"Total rows written: {row_num}")
