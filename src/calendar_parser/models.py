"""
Data models for calendar events and meeting classification.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta


# Atlantic Daylight Time offset (UTC-3, active March–November in Halifax)
ADT_OFFSET = timedelta(hours=-3)


@dataclass
class CalendarEvent:
    """Represents a single parsed calendar event (times stored as UTC)."""

    uid: str
    start: datetime  # UTC
    end: datetime  # UTC
    summary: str
    status: str  # BUSY, TENTATIVE, FREE

    @property
    def duration_minutes(self) -> float:
        return (self.end - self.start).total_seconds() / 60

    @property
    def duration_hours(self) -> float:
        return round(self.duration_minutes / 60, 2)

    @property
    def day_of_week(self) -> str:
        """Day of week in UTC (used for pattern matching)."""
        return self.start.strftime("%A")

    @property
    def day_of_week_local(self) -> str:
        """Day of week in ADT (for display)."""
        return self.start_local.strftime("%A")

    @property
    def start_time(self) -> str:
        """Start time in UTC HH:MM (used for pattern matching)."""
        return self.start.strftime("%H:%M")

    @property
    def end_time(self) -> str:
        """End time in UTC HH:MM."""
        return self.end.strftime("%H:%M")

    @property
    def start_local(self) -> datetime:
        """Start time converted to ADT (UTC-3)."""
        return self.start + ADT_OFFSET

    @property
    def end_local(self) -> datetime:
        """End time converted to ADT (UTC-3)."""
        return self.end + ADT_OFFSET

    @property
    def start_time_local(self) -> str:
        """Start time in ADT HH:MM (for CSV output)."""
        return self.start_local.strftime("%H:%M")

    @property
    def end_time_local(self) -> str:
        """End time in ADT HH:MM (for CSV output)."""
        return self.end_local.strftime("%H:%M")

    @property
    def date_str(self) -> str:
        """Date string in UTC (for pattern matching)."""
        return self.start.strftime("%Y-%m-%d")

    @property
    def date_str_local(self) -> str:
        """Date string in ADT (for CSV output)."""
        return self.start_local.strftime("%Y-%m-%d")


@dataclass
class MeetingPattern:
    """Defines a pattern rule for matching events to meeting titles."""

    title: str
    utc_start_time: str  # HH:MM format (UTC)
    duration_min: int
    days: list[str]  # e.g. ["Monday", "Tuesday", ...] — in UTC day-of-week
    tolerance_min: int = 5  # allow slight time variations
    active_from: str | None = None  # YYYY-MM-DD, if pattern started after internship start
    active_until: str | None = None  # YYYY-MM-DD, if pattern ended before internship end
