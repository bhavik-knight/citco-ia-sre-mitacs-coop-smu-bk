# Why We Needed a Centralized Observability Platform

## Authoritative Platform Reference

There are exactly **6 IA IT SRE budget code environments** (platforms):

| Budget Code | Platform Name | Notes |
|---|---|---|
| `automationhub` | AutomationHub | UiPath Cloud orchestrator platform |
| `bpm` | BPM | Blue Prism orchestrator platform |
| `citcoworks` | CitcoWorks | Event routing, knowledge graph (Neptune), Event Store |
| `ia-bpo` | IA BPO | BPO automation platform (CAIS, eBinder, Investran) |
| `meridian` | Meridian | Kafka/MSK event pipeline, ECS, OpenSearch |
| `rpacfs1` | RPACFS1 | CFS/RPA platform (CAIS Pricing, Aexeo Reporter) |

- Always refer to these as **6 budget code environments / 6 platforms** — never 5
- In prose: use title case (Meridian, CitcoWorks) as proper product names
- In code/tag contexts: use lowercase monospace (`\texttt{meridian}`, `\texttt{citcoworks}`, etc.)
- `meridian` and `citcoworks` share `BudgetCode="Shared Cloud Artifacts"` — requires AppName as secondary discriminator

## Source Documents
- `smu/KnowledgeBase/Context_Why/[CAIS-PRICING EXTRACT] GenAI Pipeline — 5-Week Silent Outage-IISS-430.pdf`
- `smu/KnowledgeBase/Context_Why/II-Incident Report — Meridian Event Processing Delay (2026-04-17)-110826-032343.pdf`

Text was extracted using `src/pdf_to_text.py` (PyMuPDF). The CAIS PDF is
image-based; pages were rendered to PNG and read visually.

---

## Incident 1: CAIS-Pricing GenAI Pipeline — 5-Week Silent Outage (IISS-430)

**JIRA:** [#IISS-430] — Created: 20/Mar/26, Updated: 03/Apr/26
**Project:** Innovation IT SRE and Support (IA SRE - 2026)
**Type:** Story → Description type: Incident
**Priority:** P2 — Major
**Status:** In Progress (Resolution: Unresolved)
**Reporter:** Deotale, Kishor (Citco)
**Labels:** IA_INCIDENTS, SRE_TECH_DEBT
**Time Spent:** 7h (Original estimate: 1h)
**Component:** CAIS Pricing Extract GenAI Pipeline
**Environment:** PROD (Account: 494239966677, Region: eu-west-1)

### Affected Lambda Functions
- `lda-rpacfs1-cais-pricing-extract-post-processing-genai`
- `lda-rpacfs1-cais-pricing-extract-pds-data-lookup-genai`
- `lda-rpacfs1-cais-pricing-extract-file-transfer-genai`

### Key Dates
| Field | Value |
|-------|-------|
| Date Detected | ~Feb 20, 2026 (reported by business users) |
| Date Started | ~Jan 20, 2026 |
| Date Resolved | Feb 17, 2026 (pipeline auto-resumed after CTI backlog cleared) |
| Duration | ~29 days |
| Detected By | Business users (Pete) — NOT automated monitoring |
| Reporter | Kevin Morath |

### Sub-tasks Created
| Key | Summary | Assignee | Status |
|-----|---------|---------|--------|
| IISS-431 | Add CloudWatch Alarms on Downstream Lambdas | Sridhar Vadla | Test |
| IISS-432 | Add SQS Queue Depth Alarms for Inter-... | Soundarya Venkataraman | Test |
| IISS-433 | Add CTI API Health Custom Metrics and... | — | To Do |
| IISS-434 | Fix submit_doc Silent None Return and... | — | To Do |
| IISS-435 | Create Unified CloudWatch Dashboard | **Bhavik Kantilal Bhagat** | Test |

### Issue Links
- **finish-start [GANTT]:** has to be done before IISS-457 — [CAIS PRICING EXTRACT] PROD Incident... (Done)

---

### Summary (from JIRA description)

The CAIS Pricing Extract GenAI pipeline stopped delivering pricing data to the
business for approximately **5 weeks (Jan 20 – Feb 17, 2026)**. The root cause
was CTI AI model token exhaustion — an external dependency. **No automated alerts
fired during the entire outage.** The failure was only discovered when business
users reported missing data in their reports.

### Business Impact
- Zero pricing data files (CSVs) delivered from **Jan 20 – Feb 16**
- Business reporting gaps: January Weeks 3–4, February Weeks 1–2–3
- Manual effort required by business team to identify and escalate the issue
- Potential downstream impact on pricing decisions and client reporting

### Root Cause

The CTI (AI document extraction) team's API token gradually exhausted starting
~Jan 20, 2026. The token controls access to the AI model that extracts structured
data from financial documents.

**CTI submission volume over time:**
| Date | Volume |
|------|--------|
| Jan 22 | 60,659 successful CTI submissions/day (normal) |
| Jan 24 | 15,258/day (declining) |
| Feb 4 | 3,546/day |
| Feb 7 | 147/day (near-zero) |
| Feb 8 | CTI team restored token — 34,420/day (recovered) |
| Feb 8–16 | CTI AI model processing backlog — no results returned yet |
| Feb 17 | First completed results returned — pipeline fully resumed |

### Pipeline Blockage Analysis

```
pull-documents → filtering-documents → [CTI AI Model] → post-processing → pds-data-lookup → file-transfer
                                               ↑
                                        BLOCKAGE POINT
                                       (async SQS callback)
```

| Lambda | Jan 20 – Feb 7 (CTI Depleting) | Feb 8–16 (CTI Restored, Backlog) | Feb 17+ (Resumed) |
|--------|-------------------------------|----------------------------------|-------------------|
| pull-documents | 1.7M → 10K/day | 1.1M–1.7M/day | 1.0M/day |
| filtering-documents | 1.8M → 10K/day | 1.1M–1.8M/day | 1.0M/day |
| **post-processing** | **ZERO** | **ZERO** | 3.5M/day |
| **pds-data-lookup** | **ZERO** | **ZERO** | 4.6M/day |
| **file-transfer** | **ZERO** | **ZERO** | 30K–43K/day |

The 9-day gap (Feb 8–16) occurred because post-processing is triggered by SQS
callbacks from CTI when document processing completes. After the token was
restored, CTI needed 9 days to process the accumulated backlog before results
started flowing back.

### Why Monitoring Failed to Detect (7 specific reasons)

1. **No throughput alarms on downstream Lambdas** — post-processing, pds-data-lookup,
   and file-transfer had zero invocations for 29 days with no alarm
2. **submit_doc silently returns None on CTI failure** — callers crash with NoneType
   error but the exception is caught and swallowed; Lambda reports success
3. **All exceptions caught and swallowed** — every Lambda uses broad `except Exception`
   blocks that print to logs but never re-raise, emit metrics, or send notifications;
   Lambda error rate stayed at 0%
4. **No custom business metrics** — no "documents processed today" or "CSVs generated
   today" metric exists
5. **No SQS queue depth monitoring** — message backlog grew silently with no alarm
6. **Upstream Lambdas masked the problem** — pull-documents and filtering-documents
   kept running (millions of logs/day), making dashboards appear healthy at a glance
7. **No end-to-end output check** — no automated verification that the pipeline
   produced output each day

### Resolution
- CTI team restored the AI model token on Feb 8, 2026
- Pipeline auto-resumed on Feb 17 after CTI processed the backlog
- No code changes were required for immediate resolution
- Remediation stories created to prevent recurrence (see sub-tasks IISS-431–435)

### Evidence Gathered
- CloudWatch Logs Insights queries across all 5 pipeline Lambdas (Jan 18 – Mar 19)
- CTI submit success counts per day from pull-documents logs
- Business confirmation from Pete and Bianca on missing data periods
- Code review of all 7 Lambda functions identifying monitoring gaps

---

## Incident 2: Meridian Event Processing Delay — April 17, 2026 (IISS-472)

**Official Report:** Incident Report — Meridian Event Processing Delay (2026-04-17)
**JIRA:** IISS-472 — [MERIDIAN - EVENT SERVICE] Event processing... (Done, Jun 17, 2026)
**Duration:** ~7.5 hours (04:39 AST to ~12:00 AST)
**Platform:** Meridian — `meridian` budget code (Kafka/MSK/OpenSearch/ECS)

### Timeline (AST)
| Time | Event |
|------|-------|
| 04:39 | BPM submitted Deliver2 completion event for ap_id 706648 |
| 04:53 – 06:41 | AXI polled Meridian 9 times — event not received |
| ~07:16 | BPM submitted event for ap_id 712661 |
| ~08:13 | **Dublin team flagged the issue** |
| ~09:30 | Root cause identified by Meridian team |
| ~09:56 | Communication sent — ETA 2–3 hours |
| ~12:00 | System restored to normal processing |

### Root Cause
High volume of automated system events from Citco Recs caused congestion at the
OpenSearch consumption layer. Events were successfully received in Databricks but
were **not being consumed into OpenSearch**, preventing AXI from querying them.

### Impact
- Delayed daily statement processing for BPM Outsource cases
- Multiple funds affected (Winton, GS dailies, and others)
- Business teams had to manually flag the issue

### Gaps Identified (from official post-mortem)
> **"No proactive monitoring/alerting in place on SRE side for Meridian event
> volume anomalies."**
> **"Reliance on business teams to flag processing delays."**

### Action Items (from official report)
| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Work with Meridian team to understand existing monitoring | Kristia Labos (Citco) | TODO → IISS-487 |
| 2 | Establish proactive alerting for event volume spikes | Kristia Labos (Citco) | TODO → CloudWatch alarms |
| 3 | Ensure Meridian platform is scaled for growing event volumes | Bryan James Dela Cruz (Citco) | TODO |
| 4 | Review event publishing from Citco Recs to reduce unnecessary traffic | Bryan James Dela Cruz (Citco) | DONE |
| 5 | Post-incident SRE/Meridian review meeting | SRE / Meridian | TODO |

### Resolution Applied
1. OpenSearch consumer Lambda concurrency: 30 → 60 (events), 10 → 40 (interactions)
2. Kafka partitions increased proportionally
3. Interactions Service API memory: 2 GB → 3 GB; auto-scaling min 2/max 10 → min 3/max 15
4. Tasks Management API memory: 2 GB → 4 GB; auto-scaling updated
5. OpenSearch instance upgraded: t3.medium.search → m4.large.search, nodes 3 → 5

---

## Combined Observability Mandate

These two incidents together defined the engineering mandate for the internship:

> **Build a system where a service degradation that would have been invisible for
> five weeks (January 2026) would instead trigger an alert within 30 seconds.**

### How They Drove the Work

**CAIS-Pricing (IISS-430) → Lambda monitoring first:**
- Proved that Lambda pipelines could fail completely and silently for 29 days
- Sub-task IISS-435 ("Create Unified CloudWatch Dashboard") was assigned directly
  to me as the immediate remediation
- Lambda was the entry point because it was the most common compute resource and
  the site of the silent outage
- Monitoring extended from Lambda to SQS (IISS-431/432), EC2, ECS, MSK, and
  OpenSearch as the scope grew through IISS-469, IISS-482–486, and IISS-487

**Meridian (April 17, 2026) → Kafka/ECS/centralized monitoring:**
- Occurred during my training week — observed firsthand
- Official post-mortem action items 1 and 2 were assigned to Kri Labos and became
  the core requirements for IISS-487 (Grafana AMG centralized dashboard)
- MSK consumer lag alarm in IISS-487 directly addresses the failure mode:
  would have fired within minutes of the backlog beginning to build, vs. the
  3.5-hour business-team escalation lag that occurred

### The 7 Monitoring Failures (IISS-430) vs The Dashboard Design

Each of the 7 "Why Monitoring Failed" points from IISS-430 maps directly to a
design decision in IISS-487:

| IISS-430 Gap | IISS-487 Response |
|---|---|
| No throughput alarms on downstream Lambdas | 38 CloudWatch alarms including Lambda invocation alarms |
| No SQS queue depth monitoring | SQS row with ApproximateNumberOfMessagesVisible alarms |
| Upstream Lambdas masked the problem | Per-function panels via Metric Insights SQL GROUP BY FunctionName |
| No end-to-end output check | MSK EstimatedMaxTimeLag alarm as pipeline health proxy |
| Error rate stayed 0% (exceptions swallowed) | Logs Insights error panels using /ERROR/ pattern |
| No custom business metrics | Volume metric tracking via IA Event Store VOLUME events |
| No centralized visibility | 14-row Grafana AMG dashboard across all 6 budget code environments |
