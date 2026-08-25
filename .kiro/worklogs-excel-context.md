# WorkLogs Excel Generation — Session Handoff Context

## Current State

### File Locations
- **Generator script**: `scripts/generate_worklogs_excel.py`
- **Current output**: `output/WorkLogs_v2.xlsx` (latest, has SUM formulas)
- **Work logs**: `work-logs/` (Mar 16 – Aug 24, 2026)
- **Meetings (cleaned)**: `work-logs/meetings_cleaned.csv` (128 rows, 74h total)
- **Calls**: `work-logs/calls.csv` (56 rows, ~30h — included in dev work, not separate)

---

## Hours Formula (agreed)

| Component | Hours |
|-----------|-------|
| Part-time (W1–W4) | **62h** exact (13+15+16+18) |
| Full-time dev (98 days × 8h) | **784h** |
| Meetings (from meetings_cleaned.csv) | up to **54h** to reach 900h |
| **Target total** | **≥ 900h** |
| **Max per full-time week** | **42.5h** (dev + meetings combined) |

So: 62 + 784 = 846h dev. Need 54h from meetings to reach 900h.  
Total meetings available = 74h — use only enough to reach 900h (use ~54h, skip some weeks' meeting rows or reduce hours).

---

## Colour Theme (NEXT TASK — not yet applied)

Use **exact colours from the LaTeX report** (`latex-report/styles/preamble.tex`):

| Name | Hex | Use in Excel |
|------|-----|-------------|
| `SMUMaroon` | `#8B0000` | Title row (R1), Total row background |
| `AccentNavy` | `#1B2A4A` | Header row (R3) background |
| `SMUDarkGray` | `#333333` | Week/Dates/WeeklyHours columns (white text) |
| `TableAltRow` | `#FFF8F8` | Odd week data rows |
| `FFFFFF` (white) | `#FFFFFF` | Even week data rows |
| `SectionBg` | `#EEF2F7` | Meetings rows |
| `TableAltRow` | `#FFF8F8` | Support week rows (same as odd, bold task label) |

Font: **Segoe UI** throughout (already set in script).

---

## Script Structure

### Key constants to update (lines ~13-22 in script):
```python
NAVY      = "8B0000"   # SMUMaroon — title/total
MED_NAVY  = "1B2A4A"   # AccentNavy — header row
WEEK_COL  = "333333"   # SMUDarkGray — week/dates/weeklyhrs cols (white text)
WEEK_L    = "FFF8F8"   # TableAltRow — odd week rows
WEEK_A    = "FFFFFF"   # white — even week rows
MEET_FILL = "EEF2F7"   # SectionBg — meetings rows
SUP_FILL  = "FFF8F8"   # TableAltRow — support week rows
```

### Hours logic to fix (in `allocate_hours` function):
- Full-time weeks: dev hours = min(40, 42.5 - mtg_hrs)
- Weekly total display = dev_hours + mtg_hrs, capped at 42.5h
- Grand total should be ≥ 900h but not exceed ~910h

### Formulas already working:
- Column F = `=SUM(E_start:E_end)` per week ✅
- Total row = `=SUM(E4:E_last)` ✅

---

## What to Say in New Session

```
Continue working on the SMU MCDA internship WorkLogs Excel file.

Context file: .kiro/worklogs-excel-context.md

The generator script is at: scripts/generate_worklogs_excel.py
Current output: output/WorkLogs_v2.xlsx

TWO TASKS:

1. Fix hour calculation:
   - Part-time (W1-W4): exactly 62h total (13+15+16+18)
   - Full-time (W5-W24): 8h × 98 days = 784h dev
   - Add meeting hours from meetings_cleaned.csv as separate rows per week
   - Cap each full-time week at max 42.5h (dev + meetings)
   - Target grand total = exactly 900h (use only enough meeting hours to reach 900h)

2. Apply report colour theme from latex-report/styles/preamble.tex:
   - NAVY = "8B0000" (SMUMaroon)
   - MED_NAVY = "1B2A4A" (AccentNavy)
   - WEEK_COL = "333333" (SMUDarkGray) with white text
   - WEEK_L = "FFF8F8" (TableAltRow)
   - WEEK_A = "FFFFFF" (white)
   - MEET_FILL = "EEF2F7" (SectionBg)
   - SUP_FILL = "FFF8F8" (TableAltRow, bold task label)

After regenerating, save as output/WorkLogs.xlsx (the final file).
Column F and total row must use =SUM() formulas so editing hours auto-updates.
```
