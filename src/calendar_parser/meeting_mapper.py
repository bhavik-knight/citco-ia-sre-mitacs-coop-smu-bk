"""
Maps anonymized calendar events (Busy/Tentative) to actual meeting titles
using pattern-based matching on day-of-week, start time, and duration.

Resolution order:
1. Exact date+time match from ONE_OFF_MEETINGS dict
2. ALL matching weekly recurring patterns (supports multiple meetings per slot)
3. Fallback generic label with duration

When multiple patterns match the same timeslot (e.g., SRE Weekly Call and
Innovation IT - AWS Centralized Dashboard Planning both at 9:00 AM Mon/Wed/Fri),
all matching titles are returned so the exporter can emit multiple rows.
"""

from datetime import datetime

from src.calendar_parser.models import CalendarEvent, MeetingPattern
from src.calendar_parser.patterns import MEETING_PATTERNS, ONE_OFF_MEETINGS


class MeetingMapper:
    """Resolves meeting titles for events with masked summaries."""

    # Summaries that indicate the title was stripped by org policy
    MASKED_SUMMARIES = {"Busy", "Tentative", "Unknown", "Free"}

    def __init__(
        self,
        patterns: list[MeetingPattern] | None = None,
        one_offs: dict[tuple[str, str], str] | None = None,
    ) -> None:
        self.patterns = patterns or MEETING_PATTERNS
        self.one_offs = one_offs or ONE_OFF_MEETINGS

    def resolve_title(self, event: CalendarEvent) -> str:
        """
        Return the best matching meeting title for an event (single title).
        If the event already has a real title, return it as-is.
        """
        titles = self.resolve_all_titles(event)
        return titles[0] if titles else f"Meeting ({int(event.duration_minutes)} min)"

    def resolve_all_titles(self, event: CalendarEvent) -> list[str]:
        """
        Return ALL matching meeting titles for an event.
        Used to detect collisions and emit multiple rows per timeslot.
        """
        if event.summary not in self.MASKED_SUMMARIES:
            return [event.summary]

        # 1. Check exact date+time one-off match (takes priority, single result)
        key = (event.date_str, event.start_time)
        if key in self.one_offs:
            return [self.one_offs[key]]

        # 2. Collect ALL matching recurring patterns
        matches = []
        seen_titles = set()
        for pattern in self.patterns:
            if self._matches(event, pattern) and pattern.title not in seen_titles:
                matches.append(pattern.title)
                seen_titles.add(pattern.title)

        if matches:
            return matches

        # 3. Fallback
        return [f"Meeting ({int(event.duration_minutes)} min)"]

    def _matches(self, event: CalendarEvent, pattern: MeetingPattern) -> bool:
        """Check if an event matches a pattern rule."""
        # Day-of-week check
        if event.day_of_week not in pattern.days:
            return False

        # Time check with tolerance
        event_minutes = self._time_to_minutes(event.start_time)
        pattern_minutes = self._time_to_minutes(pattern.utc_start_time)
        if abs(event_minutes - pattern_minutes) > pattern.tolerance_min:
            return False

        # Duration check (allow 15 min tolerance)
        if abs(event.duration_minutes - pattern.duration_min) > 15:
            return False

        # Active date range check
        if pattern.active_from:
            from_date = datetime.strptime(pattern.active_from, "%Y-%m-%d")
            if event.start < from_date:
                return False

        if pattern.active_until:
            until_date = datetime.strptime(pattern.active_until, "%Y-%m-%d")
            if event.start > until_date:
                return False

        return True

    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert HH:MM string to minutes since midnight."""
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
