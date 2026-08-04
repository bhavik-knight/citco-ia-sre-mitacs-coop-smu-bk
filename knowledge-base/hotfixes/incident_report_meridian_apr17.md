# Incident Report — Meridian Event Processing Delay (2026-04-17)

Source: Confluence (by Kishor Deotale), linked from IISS-489

## Summary
On April 17, 2026, event processing on the Meridian platform experienced significant
delays, preventing AXI from receiving BPM completion events. This impacted daily
statement processing for BPM Outsource Cases.

## Timeline (AST)
| Time | Event |
|------|-------|
| 04:39 | BPM submitted Deliver2 completion event for ap_id 706648 |
| 04:53–06:41 | AXI polled Meridian 9 times — event not received |
| ~07:16 | BPM submitted event for ap_id 712661 |
| ~08:13 | Dublin team flagged the issue |
| ~09:30 | Root cause identified by Meridian team |
| ~09:56 | Communication sent — ETA 2-3 hours |
| ~12:00 | System restored to normal processing |

## Root Cause
High volume of automated system events from Citco Recs caused congestion at the
OpenSearch consumption layer. Events were successfully received in Databricks but
were not being consumed into OpenSearch, preventing AXI from querying them.

## Resolution
- Unnecessary automated system events reduced (code changes)
- Resource upgrades applied to OpenSearch consumption layer

## Impact
- Delayed daily statement processing for BPM Outsources cases
- Multiple funds affected (Winton, GS dailies, and others)
- Business teams had to manually flag the issue

## Gaps Identified
- No proactive monitoring/alerting in place on SRE side for Meridian event volume anomalies
- Reliance on business teams to flag processing delays

## Detailed Resolution
1. **Concurrency & Kafka Partitions**:
   - events-opensearch-consumer: 30→60 concurrency, 30→60 partitions
   - interactions-opensearch-consumer: 10→40 concurrency, 10→40 partitions
2. **Interactions Service API**: Memory 2GB→3GB, autoscaling min 2/max 10 → min 3/max 15
3. **Tasks Management API**: Memory 2GB→4GB, autoscaling min 2/max 10 → min 3/max 15
4. **OpenSearch**: t3.medium.search → m4.large.search, 3→5 nodes

## Significance to Internship
This incident directly motivated:
- IISS-487 (Grafana dashboard) — single-pane monitoring to detect issues proactively
- IISS-489 (SRE Observability Roadmap) — formal monitoring framework
- IISS-488 (Auto-Healing Pipeline) — reduce manual intervention
- IISS-506 (Meridian monitoring infrastructure) — full gap analysis
