# Design: RPA Support Work Logs

## Overview
Generate 4 weekly work log files (one per support shift week) with daily breakdowns
of all RPA support activities, totaling 160 hours.

## File Structure
```
work-logs/
├── 2026-05/
│   └── support_week1_may04-08.md    (Week 8)
├── 2026-06/
│   ├── support_week2_jun01-05.md    (Week 12)
│   └── support_week3_jun29-jul03.md (Week 16)
└── 2026-07/
    └── support_week4_jul27-31.md    (Week 20)
```

## Daily Log Template
```markdown
## {Day}, {Date} — {Shift Hours}

### Summary
{1-2 sentence overview of the day}

### Tasks

| Time Block | Duration | Activity | Category | Reference |
|-----------|----------|----------|----------|-----------|
| 12:00 PM  | 0.5 hr   | Shift handover, queue status check | Monitoring | — |
| ...       | ...      | ...      | ...      | SD# / JIRA / call |

### Total: 8.0 hrs
```

## Data Mapping Strategy

### Week 8 (May 4–8): First Support Shift — Learning Phase
- **Evidence**: calls.csv (Horace KT sessions: 11m+7m+50m+21m), Kishor syncs (4m+3m)
- **Evidence**: SD# 14682157 (Unsettled Trade Recon, May 7, 1hr+)
- **Evidence**: OneNote notes (Bot restart, MESO, FX Settled, FX Closeout, EBinder KTs)
- **Character**: Heavy learning, Horace-guided, documenting procedures
- **Tickets**: ~9 assigned this week (from 35 total / 4 weeks average)

### Week 12 (Jun 1–5): Second Support Shift — Growing Independence
- **Evidence**: calls.csv (Horace: 35m+2m+27m+88m, Zhang: 13m+4m, Joseph group: 8m)
- **Evidence**: SD# 14915074 (OTC Deltroit, Jun 1, 1h20m)
- **Evidence**: rpa_support_log_comments.txt (Jun 3 entries: MESO, VCA/GTL, VPL tickets)
- **Evidence**: IISS-538 created (~Jun 5, MESO autoscaling)
- **Character**: Handling tickets independently, complex investigations, JIRA creation

### Week 16 (Jun 29–Jul 3): Third Support Shift — Full Capability
- **Evidence**: calls.csv (Horace: 80m+96m, Kishor: 13m+6m)
- **Evidence**: SD# 15128694 (MESO config, Jul 2, 1hr)
- **Evidence**: SD# 15138340 (Inaccurate RPA files, Jul 3, ~7min)
- **Evidence**: rpa_support_log_comments.txt (Jun 29–Jul 1: Corporate Actions, OTC, FX)
- **Evidence**: IISS-741 created (Jul 1 10:03 PM, MESO month-end stuck)
- **Character**: Confident resolution, admin access obtained, MESO month-end incident

### Week 20 (Jul 27–31): Fourth Support Shift — Expert Level
- **Evidence**: calls.csv (Kishor+Edmund+Horace+Jiannan: multiple calls)
- **Evidence**: SD# 15286963 (Long running rec, Jul 27, 1min)
- **Evidence**: SD# 15294806 (MESO Cash Reports, Jul 28, 45min)
- **Evidence**: support-week4-July26-31.txt (detailed daily logs)
- **Evidence**: IISS-876 created (Jul 30, VPL GTL pricing, live incident)
- **Character**: Leading incident response, drafting advisories, training-level comfort

## Time Allocation Pattern (per 8-hr shift day)

| Category | Typical Hours | Notes |
|----------|--------------|-------|
| Monitoring & Queue Management | 1.5–2.0 | Queue checks, bot status, dashboards |
| Ticket Investigation & Resolution | 2.5–3.5 | SD tickets, RCA, config fixes |
| Escalation & Communication | 1.0–1.5 | Teams chat, emails, user updates |
| KT Sessions & Calls | 0.5–1.5 | Horace/Kishor calls, process learning |
| JIRA & Documentation | 0.5–1.0 | Bug reports, handover docs |
| Self-learning | 0.5–1.0 | Confluence, process investigation |

## Dependencies
- **Pending**: Updated 35-ticket list with resolution dates (from user, expected tomorrow)
- **Pending**: Any additional SD ticket logs for Week 8 (May 4–8)
