"""
Exports parsed and title-resolved calendar events to CSV format.
All times in the output CSV are in ADT (Atlantic Daylight Time, UTC-3).
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path

from src.calendar_parser.models import CalendarEvent


class MeetingsCSVExporter:
    """Generates meetings.csv with proper week numbering and titles in local time."""

    INTERNSHIP_START = datetime(2026, 3, 15)  # Week 1 Sunday
    INTERNSHIP_WEEKS = 24

    # Support shift weeks: 12 PM – 8 PM ADT (didn't attend morning meetings)
    SUPPORT_SHIFT_WEEKS = {8, 12, 16, 20}

    # Morning meetings to exclude during support shift weeks
    MORNING_RECURRING_TITLES = {
        "SRE Weekly Call",
        "Innovation IT - AWS Centralized Dashboard Planning",
        "Daily Standup - Innovation IT",
        "BPM Flight Control - Platform & Dev",
    }

    # Specific events not attended (date_str UTC, start_time UTC)
    SKIPPED_EVENTS: set[tuple[str, str]] = {
        ("2026-06-04", "01:30"),  # CTM Town Hall overflow (10:30 PM ADT Jun 3) - not attended
    }

    HEADER = [
        "Week",
        "Week Dates (Mon-Fri)",
        "Date",
        "Day",
        "Start (ADT)",
        "End (ADT)",
        "Duration (hrs)",
        "Meeting Title",
        "Source",
    ]

    # Estimated meetings for weeks 1-6 (part-time, no calendar data)
    ESTIMATED_MEETINGS: dict[int, list[tuple[str, float]]] = {
        1: [("Onboarding / Orientation", 1.0)],
        2: [("Team Introduction and Setup", 1.0), ("1:1 with Manager", 0.5)],
        3: [
            ("SRE Team Standup", 0.5),
            ("Project Kickoff", 1.0),
            ("1:1 with Manager", 0.5),
        ],
        4: [
            ("SRE Team Standup", 0.5),
            ("IA Team Sync", 1.0),
            ("1:1 with Manager", 0.5),
            ("Knowledge Transfer", 0.5),
        ],
        5: [
            ("SRE Team Standup", 0.5),
            ("IA Team Sync", 1.0),
            ("1:1 with Manager", 0.5),
            ("Knowledge Transfer", 0.5),
        ],
        6: [
            ("SRE Team Standup", 0.5),
            ("IA Team Sync", 1.0),
            ("1:1 with Manager", 0.5),
            ("Sprint Planning", 1.0),
        ],
    }

    # Projected meetings for future weeks (based on observed recurring patterns)
    # These are generated per-day in the export method instead of as weekly totals.
    PROJECTED_DAILY_MEETINGS: dict[str, list[tuple[str, str, str, float]]] = {
        # day: [(start_adt, end_adt, title, duration_hrs), ...]
        "Monday": [
            ("09:00", "09:30", "SRE Weekly Call", 0.5),
            ("09:00", "09:30", "Innovation IT - AWS Centralized Dashboard Planning", 0.5),
            ("09:30", "10:00", "Daily Standup - Innovation IT", 0.5),
        ],
        "Tuesday": [
            ("09:00", "09:30", "SRE Weekly Call", 0.5),
            ("09:30", "10:00", "Daily Standup - Innovation IT", 0.5),
            ("09:30", "10:00", "BPM Flight Control - Platform & Dev", 0.5),
        ],
        "Wednesday": [
            ("09:00", "09:30", "SRE Weekly Call", 0.5),
            ("09:00", "09:30", "Innovation IT - AWS Centralized Dashboard Planning", 0.5),
            ("09:30", "10:00", "Daily Standup - Innovation IT", 0.5),
        ],
        "Thursday": [
            ("09:00", "09:30", "SRE Weekly Call", 0.5),
            ("09:30", "10:00", "Daily Standup - Innovation IT", 0.5),
        ],
        "Friday": [
            ("09:00", "09:30", "SRE Weekly Call", 0.5),
            ("09:00", "09:30", "Innovation IT - AWS Centralized Dashboard Planning", 0.5),
            ("09:30", "10:00", "Daily Standup - Innovation IT", 0.5),
        ],
    }

    def __init__(self, output_path: Path | str) -> None:
        self.output_path = Path(output_path)

    def get_internship_week(self, dt: datetime) -> int | None:
        """Map a datetime to internship week number (1-based)."""
        delta = (dt - self.INTERNSHIP_START).days
        if delta < 0:
            return None
        week = (delta // 7) + 1
        return week if week <= self.INTERNSHIP_WEEKS else None

    def get_week_dates_mf(self, week_num: int) -> tuple[str, str]:
        """Get Mon-Fri date strings for a given internship week."""
        week_start = self.INTERNSHIP_START + timedelta(weeks=week_num - 1)
        monday = week_start + timedelta(days=1)
        friday = week_start + timedelta(days=5)
        return monday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d")

    def export(
        self,
        events: list[CalendarEvent],
        titles_map: dict[str, list[str]],
        last_calendar_week: int | None = None,
    ) -> dict[int, float]:
        """
        Write meetings.csv and return weekly hour totals.

        Args:
            events: Parsed calendar events.
            titles_map: Mapping of event UID to list of resolved meeting titles.
                Multiple titles = multiple rows emitted (overlapping meetings).
            last_calendar_week: Last week with actual calendar data.
                Weeks after this get projected entries.
        """
        rows: list[list] = []

        # Phase 1: Estimated weeks (no calendar data)
        for week_num, meetings in self.ESTIMATED_MEETINGS.items():
            mon, fri = self.get_week_dates_mf(week_num)
            week_dates = f"{mon} to {fri}"
            for title, hrs in meetings:
                rows.append(
                    [week_num, week_dates, "", "", "", "", hrs, title, "estimated"]
                )

        # Phase 2: Calendar-sourced events (output in ADT)
        for event in events:
            week = self.get_internship_week(event.start)
            if week is None or week <= 6:
                continue  # skip events in estimated range

            # Skip specific events not attended
            if (event.date_str, event.start_time) in self.SKIPPED_EVENTS:
                continue

            mon, fri = self.get_week_dates_mf(week)
            week_dates = f"{mon} to {fri}"
            event_titles = titles_map.get(event.uid, [event.summary])

            # During support shift weeks, skip morning recurring meetings
            if week in self.SUPPORT_SHIFT_WEEKS:
                event_titles = [
                    t for t in event_titles
                    if t not in self.MORNING_RECURRING_TITLES
                ]
                if not event_titles:
                    continue

            for title in event_titles:
                rows.append([
                    week,
                    week_dates,
                    event.date_str_local,
                    event.day_of_week_local,
                    event.start_time_local,
                    event.end_time_local,
                    event.duration_hours,
                    title,
                    "calendar",
                ])

        # Phase 3: Projected future weeks (day-by-day breakdown)
        if last_calendar_week is not None:
            for week_num in range(last_calendar_week + 1, self.INTERNSHIP_WEEKS + 1):
                mon, fri = self.get_week_dates_mf(week_num)
                week_dates = f"{mon} to {fri}"
                week_start = self.INTERNSHIP_START + timedelta(weeks=week_num - 1)
                for day_offset in range(1, 6):  # Mon=1 .. Fri=5
                    day_dt = week_start + timedelta(days=day_offset)
                    day_name = day_dt.strftime("%A")
                    date_str = day_dt.strftime("%Y-%m-%d")
                    daily_meetings = self.PROJECTED_DAILY_MEETINGS.get(day_name, [])
                    for start_t, end_t, title, hrs in daily_meetings:
                        rows.append([
                            week_num,
                            week_dates,
                            date_str,
                            day_name,
                            start_t,
                            end_t,
                            hrs,
                            title,
                            "projected",
                        ])

        # Sort by week, then date, then start time
        rows.sort(key=lambda r: (r[0], r[2], r[4]))

        # Write CSV
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            writer.writerows(rows)

        # Compute weekly totals
        week_totals: dict[int, float] = {}
        for row in rows:
            week_totals[row[0]] = week_totals.get(row[0], 0) + row[6]

        return week_totals
