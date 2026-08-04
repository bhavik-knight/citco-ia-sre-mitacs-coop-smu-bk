# Requirements: RPA Support Work Logs

## Goal
Generate comprehensive daily work logs for the 4 RPA support shift weeks (160 hours total)
to be included in the SMU MCDA Major Project Report submission.

## Support Shift Weeks
- **Week 8**: May 4–8, 2026 (11 AM – 7 PM EST = 12 PM – 8 PM ADT)
- **Week 12**: Jun 1–5, 2026 (same shift)
- **Week 16**: Jun 29 – Jul 3, 2026 (same shift, includes Canada Day Jul 1 — worked)
- **Week 20**: Jul 27–31, 2026 (same shift, Jul 31 is Friday — last day)

## Data Sources Available
1. **SD Ticket Logs** — 35 tickets assigned YTD (16 open, 19 resolved)
   - Detailed logs for: 14682157, 14915074, 15128694, 15138340, 15286963, 15294806
   - Acknowledged-only: 14488802, 14655334, 14655369, 14664186, 14686798, 14692963, 14824719, 14874489, 14929595, 14949664
2. **JIRAs Created** — IISS-538, IISS-706, IISS-741, IISS-753, IISS-876
3. **Ad-hoc Calls** (work-logs/calls.csv) — filtered for support weeks
4. **Knowledge Base Notes** — rpa_support_log_comments.txt, support-week4-July26-31.txt
5. **OneNote RPA Support Notes** — absorbed into context (MESO, FX, VPL, OTC, etc.)
6. **W30 Ticket Load Report** — 35 tickets, 3.45% of team load
7. **Updated 35-ticket list + report** (pending from user, expected tomorrow)

## Requirements

### R1: Daily Breakdown
Each support week must have a day-by-day log (Mon–Fri) showing:
- Date, day of week
- Shift hours (12 PM – 8 PM ADT)
- Tasks performed with approximate time allocations
- Tickets worked (SD#) with brief description
- Meetings/calls attended (from meetings.csv + calls.csv)
- Tools used (Blue Prism, UiPath, DBeaver, CloudWatch, SharePoint, etc.)

### R2: Activity Categories
Each day's work should be categorized into:
- **Monitoring & Queue Management** — queue checks, bot management, status responses
- **Ticket Investigation & Resolution** — SD ticket work, RCA, troubleshooting
- **Escalation & Communication** — Teams/email, user updates, handover docs
- **JIRA Creation & Documentation** — bug reports, incident write-ups
- **KT Sessions** — Horace calls, process learning
- **Self-learning** — Confluence pages, documentation review

### R3: Output Format
- One markdown file per week in `work-logs/2026-{MM}/` folder
- Naming: `support_week{N}_{dates}.md`
- Total hours per day must sum to 8 (shift length)
- Total per week: 40 hours (except holidays)

### R4: Holidays
- **May 18** (Victoria Day) — NOT a support week, no impact
- **Jul 1** (Canada Day) — Week 16, WORKED full shift

### R5: Evidence Linking
Each log entry should reference source evidence where available:
- SD ticket numbers
- JIRA ticket numbers
- Call records (from calls.csv)
- Meeting entries (from meetings.csv)
- Knowledge base file references

### R6: Accuracy
- Do NOT fabricate ticket numbers or specific details not provided
- Use general task descriptions for undocumented work (queue monitoring, chat responses, config checks)
- Mark estimated entries clearly vs evidence-backed entries
