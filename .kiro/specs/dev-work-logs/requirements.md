# Requirements: Dev Work Logs

## Goal
Generate comprehensive daily work logs for all non-support dev work weeks
based on JIRA tickets, git commits, and documented activities.

## JIRA Tickets Captured (Dev Work)

### IISS-487 — Amazon Managed Grafana Meridian Dashboard (CRITICAL, 140h logged)
- Primary deliverable: single-pane Grafana dashboard for Meridian platform
- 14 service rows, 110+ panels, 17 alerting rules
- CloudFormation IaC, Lambda provisioner, S3 dashboard storage
- Full alarm notification pipeline (Re-Notifier Lambda, composite alarms, Grafana alerts)
- Per-panel folder structure migration
- 960+ tests (unit, e2e, property-based)
- Extensive documentation suite
- Active: May 14 – present

### IISS-455 — Lambda Monitoring Dashboard (DONE, 2h logged)
- CloudWatch dashboard via CFN for rpacfs1/IA-BPO lambdas
- Due: Apr 13, Completed: Apr 7
- Subtask IISS-461 (Confluence page, 51 Lambda inventory)

### IISS-469 — Improve Centralized Lambda Dashboard (TEST)
- Additional tag support, log errors widget, CSV/Excel export, Top N filter, Lambda inventory UI
- Deep research on OOM detection, subscription filters, budget code filtering
- Active: Apr 15–22

### IISS-482 — IA Resources/Infrastructure Monitoring Dashboard (IN PROGRESS, 11h logged)
- Parent story: Lambda + EC2 + ECS + EKS dashboards + S3 export
- SQS monitoring feature (Jun 12, 5.5h): registry, exporter, API, dashboard builder, 960 tests
- Architecture documentation (Apr 29)

### IISS-483 — EC2 Monitoring Dashboard (IN PROGRESS)
- Gap analysis: 83 instances, 1 relevant, tag mismatch root cause
- AppName fallback pattern, CWAgent via SSM, cost analysis ($1.29/month)
- 5-phase implementation plan

### IISS-484 — ECS Monitoring Dashboard (IN PROGRESS)
- Container Insights cost analysis (4 options compared)
- Recommended Standard CI at $10.44/month
- Enabled CI on 11 clusters

### IISS-485 — EKS Monitoring Dashboard (IN PROGRESS)
- Scope change: AUTOMATIONHUB budget code added
- Only 1 cluster (idle, logging disabled)
- On Hold then resumed

### IISS-486 — Export to S3 (IN PROGRESS)
- Centralized export: S3 bucket via CFN, CLI script, API endpoints, scheduled Lambda

### Pending JIRA Details (to be shared in next session)
- IISS-846 — Create LogGroupDiscoverer (To Do)
- IISS-838 — Lambda Instrumentation (Powertools Tracer) (To Do)
- IISS-837 — Instrument services to emit AWS X-Ray trace data by platform group for SRE Grafana dashboard (To Do)
- IISS-824 — Understand the Document Agent Implementation in ML-RPA-Status LLM Repos (To Do)
- IISS-510 — Extend Registry API to Support CITCOWORKS Budget Code (In Progress)
- IISS-509 — Frontend — IA Resources Monitoring Dashboard (To Do)
- IISS-508 — Backend — IA Resources Monitoring Dashboard (In Progress)
- IISS-506 — MERIDIAN - related issue - need monitoring infrastructure (To Do)
- IISS-505 — Extend Registry API to Support MERIDIAN Budget Code (In Progress)
- IISS-504 — Extend Registry API to Support AUTOMATIONHUB Budget Code Resource Discovery (In Progress)
- IISS-489 — Meridian — SRE Observability, Monitoring & Auto-Healing Roadmap (To Do)
- IISS-488 — Auto-Healing: Implement Alert-Driven Auto-Healing Pipeline with User-Friendly Email Notifications (To Do)

## Data Sources for Dev Work Logs
1. JIRA work logs (detailed session descriptions with line counts)
2. JIRA history (status changes, comments, dates)
3. Git commits (pending — repos to be shared)
4. Meetings/calls during dev weeks
5. Knowledge base documents (dashboard notes, TODOs)

## Output
- Daily work logs in work-logs/2026-{MM}/ folders
- Evidence-backed entries from JIRA timestamps
- Progressive narrative showing skill development
