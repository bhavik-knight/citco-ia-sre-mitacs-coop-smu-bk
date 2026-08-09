# Dev Work Timeline (Chronological)

## Week 4 (Apr 6–11) — Part-Time, Infrastructure Discovery
- Apr 6: IISS-461 created (Lambda inventory), IISS-455 started
- Apr 7: IISS-455 completed (Lambda dashboard, 2h), IISS-461 done (51 functions mapped)

## Week 5 (Apr 13–18) — Training Week + Dashboard Research
- Apr 15: IISS-469 created (dashboard improvements)
- Apr 16: IISS-469 In Progress, description written
- Apr 17: Deep OOM detection research (5 approaches), subscription filter architecture
- Apr 20: Budget code filtering, Top K limitations, export format spec
- Apr 21: IISS-469 moved to Test

## Week 6 (Apr 19–25) — Architecture & Planning
- Apr 22: Created IISS-482, 483, 484, 485, 486, 487 (full board setup)
- Apr 23: Self-assigned all tasks
- Apr 24: IISS-483/484/485/486 In Progress, EKS discovered empty → On Hold
- Apr 28: IISS-485 scope change (AUTOMATIONHUB), CloudWatch widget prototype (IISS-487)

## Week 7 (Apr 26 – May 2) — EC2/ECS Investigation
- Apr 29: EC2 gap analysis (83 instances, tag mismatch), ECS investigation (11 clusters)
  - Container Insights cost analysis (4 options)
  - Architecture flow diagram documented
- Apr 30: CWAgent cost ($1.29/month), free ECS metrics approach

## Week 8 (May 4–8) — SUPPORT SHIFT #1
- May 4: IISS-504/505/507/510 links created
- May 6: IISS-487 elevated to Critical by Kishor, moved to In Progress

## Week 9 (May 11–16) — Grafana Dashboard Intensive
- May 11: IISS-487 infrastructure deployed (4 CFN stacks, IAM battles)
  - 30h estimated, gap analysis
- May 12: All 3 DEV stacks deployed, Grafana live, 16-role agent system
  - Cost analysis ($45-90/month recommendation)
- May 13: 7h logged (early dashboard work)
- May 14-15: 29h over 3 sessions
  - Lambda panels, ECS SQL migration, $platform variable
  - Grafana 10.4→12.4 upgrade, SQS 49 tests
  - Automation pipeline (--deploy, auto-sync .env)

## Week 10 (May 17–23) — Dashboard Expansion
- May 19: MSK-Kafka migration, DocumentDB row, Neptune row (8h)
- May 20: OpenSearch SQL, RDS row added, noData messages (7h)
- May 21: Secrets Manager 64KB limit hit, agentic refactor (14,720 lines), RDS temp fix (7h)
- May 22: E2e tests, SSL cert fix, Health Overview breakthrough, S3 migration (6.5h)

## Week 11 (May 24–30) — Dashboard Maturation
- May 25: DocumentDB/Neptune/RDS/OpenSearch health panels, S3 migration, Performance row (13h)
- May 26: Redis row (11 panels), AMG compliance, row renumbering, LCD gauges (8h)
- May 27: Alerts & Notifications branch, SNS setup, alarms documentation (7.5h)
- May 28: Additional work (7.5h)
- May 29: Re-Notifier Lambda, 8 composite alarms, Grafana alerting (6h)

## Week 12 (Jun 1–5) — SUPPORT SHIFT #2
- Jun 1: 6h logged on IISS-487 (support shift week, minimal dashboard work)

## Week 13 (Jun 8–12) — Restructure & New Features
- Jun 8: CAIS Deadline hotfix (IISS-706, 7h)
- Jun 9: Alarm panels, EC2 monitoring row, instance mapper Lambda (8h)
- Jun 10: Per-panel folder extraction, S3 template staging fix (7h)
- Jun 11: Rows 02-14 folder migration, 357 tests passing (4h)
  - IISS-507: ia-sre-resources-inventory scaffolded (2.5h)
- Jun 12: IISS-482 SQS monitoring feature (5.5h): registry, API, dashboard, 960 tests

## Week 14 (Jun 15–18) — Dashboard Polish & Completion
- Jun 15: Documentation, deep-links, resource tables for 9 services (7h)
- Jun 16: ECS legend fixes, bargauge deep-links, DocumentDB/RDS restructure (7h)
- Jun 17: Redis/OpenSearch restructure, Grafana transformation pitfalls (6.5h)
- Jun 18: Final polish, deployment v698→v728, release merge (19h over multiple sessions)
  - Total IISS-487 reaches 140h logged

## Week 16 (Jun 29 – Jul 3) — SUPPORT SHIFT #3
- Jul 1: IISS-741 created (MESO month-end stuck tasks)

## Week 17 (Jul 5–11) — Continued Development
- Jul 8: IISS-753 created (VPL IPV failure)

## Week 20 (Jul 27–31) — SUPPORT SHIFT #4
- Jul 30: IISS-876 created (VPL GTL pricing incident)
- Jul 30-31: X-Ray tracing work on ia_meso_process repo (7 feature branches with specs)

## Hours Summary
| JIRA | Hours Logged | Period |
|------|-------------|--------|
| IISS-487 | 140h | May 6 – Jun 18 |
| IISS-482 | 11h | Apr 29, Jun 12, Jun 18 |
| IISS-507 | 2.5h | Jun 11 |
| IISS-706 | 7h | Jun 8 |
| IISS-455 | 2h | Apr 7 |
| **Total logged** | **162.5h** | |

Note: Many more hours worked but not logged (IISS-469 research, 483/484/485 investigations,
support weeks, meetings, etc.). Git commits will fill remaining gaps.
