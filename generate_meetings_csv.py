#!/usr/bin/env python3
"""
CLI script to parse ICS calendar export and generate work-logs/meetings.csv
with resolved meeting titles based on recurring day/time patterns.

Usage:
    uv run python generate_meetings_csv.py [path_to_ics]

If no path is provided, defaults to the Citco calendar ICS in the project root.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.calendar_parser import CalendarParser, MeetingMapper, MeetingsCSVExporter

DEFAULT_ICS = ROOT_DIR / "Bhagat Bhavik Kantilal    (Citco) Calendar.ics"
OUTPUT_CSV = ROOT_DIR / "work-logs" / "meetings.csv"


def main() -> None:
    ics_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ICS

    if not ics_path.exists():
        print(f"ERROR: ICS file not found: {ics_path}")
        sys.exit(1)

    # 1. Parse ICS
    parser = CalendarParser(ics_path)
    events = parser.parse()
    print(f"Parsed {len(events)} events from {ics_path.name}")

    # 2. Resolve meeting titles (all matching titles per event for collisions)
    mapper = MeetingMapper()
    titles_map: dict[str, list[str]] = {}
    for event in events:
        titles_map[event.uid] = mapper.resolve_all_titles(event)

    # 3. Determine last week with calendar data
    exporter = MeetingsCSVExporter(OUTPUT_CSV)
    last_week = 0
    for event in events:
        week = exporter.get_internship_week(event.start)
        if week is not None and week > last_week:
            last_week = week

    print(f"Calendar data covers up to Week {last_week}")

    # 4. Export CSV
    week_totals = exporter.export(events, titles_map, last_calendar_week=last_week)

    print(f"\nCSV written: {OUTPUT_CSV}")
    print(f"Total rows generated for {len(week_totals)} weeks\n")
    print(f"{'Week':<6} {'Hours':<8}")
    print("-" * 20)
    grand_total = 0.0
    for week in sorted(week_totals.keys()):
        hrs = week_totals[week]
        grand_total += hrs
        print(f"  {week:<4} {hrs:.1f}")
    print("-" * 20)
    print(f"Total: {grand_total:.1f} hrs")


if __name__ == "__main__":
    main()
