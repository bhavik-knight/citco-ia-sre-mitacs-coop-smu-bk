"""
Meeting pattern definitions based on observed calendar data.

Patterns are identified by correlating UTC timestamps in the ICS export
with visible meeting titles from the Outlook calendar UI (ADT timezone).

ADT (Atlantic Daylight Time) = UTC-3 (active March–November):
  09:00 AM ADT = 12:00 UTC
  09:30 AM ADT = 12:30 UTC
  08:00 AM ADT = 11:00 UTC
  08:30 AM ADT = 11:30 UTC
  10:00 AM ADT = 13:00 UTC
  10:30 AM ADT = 13:30 UTC
  01:00 PM ADT = 16:00 UTC
  07:30 PM ADT = 22:30 UTC
  05:00 AM ADT = 08:00 UTC
  07:30 AM ADT = 10:30 UTC
  04:00 AM ADT = 07:00 UTC

Source: Outlook calendar screenshots showing recurring weekly items and
one-off meetings from the internship period (March–August 2026).
"""

from datetime import datetime

from src.calendar_parser.models import MeetingPattern

ALL_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

# ============================================================================
# RECURRING WEEKLY MEETINGS (from screenshot "Weekly: 8 items")
# ============================================================================

WEEKLY_RECURRING: list[MeetingPattern] = [
    # "SRE Weekly Call" — every Mon, Tue, Wed, Thu from 9:00-9:30 AM ADT
    # Recurrence description: "every Monday, Tuesday, Wednesday, Thurs..."
    # 9:00 AM ADT = 12:00 UTC, 30 min
    MeetingPattern(
        title="SRE Weekly Call",
        utc_start_time="12:00",
        duration_min=30,
        days=["Monday", "Tuesday", "Wednesday", "Thursday"],
    ),
    # "SRE Weekly Call" — also on Fridays per earlier data (same time)
    MeetingPattern(
        title="SRE Weekly Call",
        utc_start_time="12:00",
        duration_min=30,
        days=["Friday"],
        active_from="2026-05-19",
    ),
    # "Daily Standup - Innovation IT" — every weekday 9:30-10:00 AM ADT
    # 9:30 AM ADT = 12:30 UTC, 30 min
    # Active from Jun 1 based on screenshot start date
    MeetingPattern(
        title="Daily Standup - Innovation IT",
        utc_start_time="12:30",
        duration_min=30,
        days=ALL_DAYS,
        active_from="2026-06-01",
    ),
    # "BPM Flight Control - Platform & Dev" — every Tuesday 9:30-10:00 AM ADT
    # 9:30 AM ADT = 12:30 UTC, 30 min
    # Active from Jun 17 based on screenshot start date
    MeetingPattern(
        title="BPM Flight Control - Platform & Dev",
        utc_start_time="12:30",
        duration_min=30,
        days=["Tuesday"],
        active_from="2026-06-17",
    ),
    # "Daily Standup" — every weekday 1:00-1:30 PM ADT
    # 1:00 PM ADT = 16:00 UTC, 30 min
    # Active from May 1, ended around May 31 (replaced by Innovation IT standup)
    MeetingPattern(
        title="Daily Standup",
        utc_start_time="16:00",
        duration_min=30,
        days=ALL_DAYS,
        active_from="2026-05-01",
        active_until="2026-05-31",
    ),
    # "Status Review - IA Developer Best Practice" — every Monday 7:30-8:00 PM ADT
    # 7:30 PM ADT = 23:30 UTC... but ICS shows 23:00 UTC 60 min on some days
    # Let's match the actual ICS timestamps: 23:00 UTC, 60 min
    MeetingPattern(
        title="Status Review - IA Developer Best Practice",
        utc_start_time="23:00",
        duration_min=60,
        days=["Monday", "Tuesday"],
        tolerance_min=30,
    ),
    # "Innovation IT – AWS Centralized Dashboard Planning"
    # Mon/Wed/Fri 9:00-9:30 AM ADT = 12:00 UTC, 30 min
    # Same slot as SRE Weekly Call — both meetings happen simultaneously.
    # Active from May 22 onwards. Cancelled during 4 support-shift weeks (TBD).
    MeetingPattern(
        title="Innovation IT - AWS Centralized Dashboard Planning",
        utc_start_time="12:00",
        duration_min=30,
        days=["Monday", "Wednesday", "Friday"],
        active_from="2026-05-22",
    ),
]

# ============================================================================
# ONE-OFF / OCCASIONAL MEETINGS (from screenshots 2 & 3)
# Mapped by exact date + time to override pattern matching
# ============================================================================

# These are keyed by (date_str, utc_start_time) for exact matching
ONE_OFF_MEETINGS: dict[tuple[str, str], str] = {
    # --- July 2026 ---
    ("2026-07-31", "13:00"): "Demo - IA Developer Best Practice Verification",
    ("2026-07-31", "10:30"): "KT for VPL Pricing Checks",
    ("2026-07-30", "10:30"): "KT for VPL Pricing Checks",
    ("2026-07-29", "12:30"): "3.25 Retrospective",
    ("2026-07-16", "08:00"): "NAV Checklist/Ebinder Support Walkthrough",
    ("2026-07-16", "09:00"): "CITCOWORKS 2026 Penetration Testing Req...",
    ("2026-07-14", "12:30"): "RPA Deployment Pause - Next Steps",
    ("2026-07-13", "11:00"): "CORA Support Handoff <> Final Connect",
    ("2026-07-10", "11:00"): "BPM Flight Control - close out actions for 3.25",
    ("2026-07-09", "12:00"): "Blue Prism Troubleshooting",
    ("2026-07-09", "11:00"): "IA CONFIG PORTAL - DEMO",
    ("2026-07-09", "11:30"): "Support Handoff <> CORA",
    ("2026-07-06", "13:00"): "IA Config Portal - DEMO",
    ("2026-07-06", "12:00"): "BPM 3.25 Handover (6 JIRAs)",
    ("2026-07-01", "07:45"): "TWOSIGMA Support Handover",
    ("2026-07-01", "11:30"): "Support Handoff <> CORA",
    # --- June 2026 ---
    ("2026-06-27", "07:00"): "Performance Testing - IA_EBINDER Stress Test",
    ("2026-06-24", "23:00"): "Support KT - FX Settled Process Exception Handling",
    ("2026-06-23", "11:00"): "Support KT - FX Closeouts Process Exception",
    ("2026-06-23", "23:00"): "Support KT - FX Closeouts Process Exception",
    ("2026-06-23", "12:30"): "Tech Talk || AURA (part of the Solution Snapshots)",
    ("2026-06-19", "12:30"): "Instrument Expiry - Support Exception Handling",
    ("2026-06-17", "11:30"): "BPM Flight Control - Platform & Dev",
    ("2026-06-11", "12:00"): "Citco Works Monitoring Requirements",
    ("2026-06-09", "12:30"): "Tech Talk || Idea Box Agent (part of the Solution...)",
    ("2026-06-03", "12:30"): "CTM Town Hall",
    ("2026-06-03", "13:30"): "CTM Town Hall",
    ("2026-06-03", "15:00"): "Citco Canada webinar - Your Group Retirement",
    # --- May 2026 ---
    ("2026-05-27", "12:30"): "Tech Talk || Agentic Agents",
    ("2026-05-21", "18:30"): "HFX Town Hall",
    ("2026-05-20", "12:30"): "Tech Talk || AI Use Case Framework overview",
    ("2026-05-19", "12:00"): "UiPATH - VPL PRICING",
    ("2026-05-15", "12:00"): "[Demo] RPA Support Agent",
    ("2026-05-14", "17:30"): "CONFIG SERVICE DEMO - NA",
    ("2026-05-12", "12:00"): "UiPath Sharepoint API Library - Overview",
    ("2026-05-12", "12:30"): "Tech Talk || Jira Automation",
    ("2026-05-11", "13:30"): "MAS - Infrastructure Monitoring Review",
    ("2026-05-08", "18:00"): "Support Handover - Sentry Loan Accrual",
    # --- April 2026 ---
    ("2026-04-30", "11:30"): "Container Insights Cost Discussion for Dashboard",
    ("2026-04-29", "14:00"): "Configuration Service DEMO",
    ("2026-04-28", "12:30"): "Tech Talk || AI Strategy",
}

# ============================================================================
# FALLBACK PATTERNS (less specific, used when no exact match or weekly match)
# ============================================================================

FALLBACK_PATTERNS: list[MeetingPattern] = [
    # Generic SRE VCE catch-all before the "SRE Weekly Call" naming was used
    MeetingPattern(
        title="SRE Weekly Call",
        utc_start_time="12:00",
        duration_min=30,
        days=ALL_DAYS,
        active_until="2026-05-18",
    ),
    # Generic daily standup sync (12:30 slot before Innovation IT started)
    MeetingPattern(
        title="Daily Standup - Team Sync",
        utc_start_time="12:30",
        duration_min=30,
        days=ALL_DAYS,
        active_from="2026-04-28",
        active_until="2026-05-31",
    ),
    # 1:1 with Manager at 14:00 UTC (11:00 AM ADT)
    MeetingPattern(
        title="1:1 with Manager (Deotale)",
        utc_start_time="14:00",
        duration_min=30,
        days=ALL_DAYS,
    ),
    # Extended meetings at 12:00 UTC lasting 60 min
    MeetingPattern(
        title="SRE Extended Review",
        utc_start_time="12:00",
        duration_min=60,
        days=ALL_DAYS,
    ),
    # Catch-all for 12:30 60min meetings
    MeetingPattern(
        title="Team Sync / Knowledge Transfer",
        utc_start_time="12:30",
        duration_min=60,
        days=ALL_DAYS,
    ),
    # Catch-all for 13:00 30min
    MeetingPattern(
        title="Team Standup",
        utc_start_time="13:00",
        duration_min=30,
        days=ALL_DAYS,
    ),
]

# Combined ordered list: one-offs checked first, then weekly, then fallbacks
MEETING_PATTERNS: list[MeetingPattern] = WEEKLY_RECURRING + FALLBACK_PATTERNS
