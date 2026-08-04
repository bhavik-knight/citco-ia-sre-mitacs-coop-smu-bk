"""
Calendar Parser Package.

Parses ICS calendar exports and maps anonymized events to actual meeting titles
based on recurring day/time patterns identified from the internship period.
"""

from src.calendar_parser.parser import CalendarParser
from src.calendar_parser.meeting_mapper import MeetingMapper
from src.calendar_parser.exporter import MeetingsCSVExporter

__all__ = ["CalendarParser", "MeetingMapper", "MeetingsCSVExporter"]
