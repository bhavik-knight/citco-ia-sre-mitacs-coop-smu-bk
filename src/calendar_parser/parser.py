"""
ICS file parser. Extracts VEVENT entries into CalendarEvent objects.
"""

import re
from datetime import datetime
from pathlib import Path

from src.calendar_parser.models import CalendarEvent


class CalendarParser:
    """Parses .ics files exported from Microsoft Outlook."""

    _EVENT_DELIMITER = "BEGIN:VEVENT"
    _DTSTART_RE = re.compile(r"DTSTART:(\d{8}T\d{6})")
    _DTEND_RE = re.compile(r"DTEND:(\d{8}T\d{6})")
    _SUMMARY_RE = re.compile(r"SUMMARY.*?:(.*)")
    _UID_RE = re.compile(r"UID:(.*)")
    _STATUS_RE = re.compile(r"X-MICROSOFT-CDO-BUSYSTATUS:(.*)")
    _DT_FORMAT = "%Y%m%dT%H%M%S"

    def __init__(self, ics_path: Path | str) -> None:
        self.ics_path = Path(ics_path)
        if not self.ics_path.exists():
            raise FileNotFoundError(f"ICS file not found: {self.ics_path}")

    def parse(self) -> list[CalendarEvent]:
        """Parse all VEVENT blocks from the ICS file."""
        content = self.ics_path.read_text(encoding="utf-8")
        raw_events = content.split(self._EVENT_DELIMITER)[1:]  # skip preamble
        events = []

        for raw in raw_events:
            event = self._parse_event(raw)
            if event is not None:
                events.append(event)

        return sorted(events, key=lambda e: e.start)

    def _parse_event(self, raw: str) -> CalendarEvent | None:
        """Parse a single VEVENT block into a CalendarEvent."""
        start_match = self._DTSTART_RE.search(raw)
        end_match = self._DTEND_RE.search(raw)

        if not start_match or not end_match:
            return None

        start = datetime.strptime(start_match.group(1), self._DT_FORMAT)
        end = datetime.strptime(end_match.group(1), self._DT_FORMAT)

        summary_match = self._SUMMARY_RE.search(raw)
        summary = summary_match.group(1).strip() if summary_match else "Unknown"

        uid_match = self._UID_RE.search(raw)
        uid = uid_match.group(1).strip() if uid_match else ""

        status_match = self._STATUS_RE.search(raw)
        status = status_match.group(1).strip() if status_match else "BUSY"

        return CalendarEvent(
            uid=uid,
            start=start,
            end=end,
            summary=summary,
            status=status,
        )
