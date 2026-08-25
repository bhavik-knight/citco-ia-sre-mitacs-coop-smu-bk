# Dev Work JIRA Summary

Complete inventory of all development JIRAs assigned to Bhavik Kantilal Bhagat
during the Citco CTM internship (March 15 – August 31, 2026).

## Fusion Project Reference

### IISS-403 — Intelligent Automation (Fusion Project 4098002-KY2050)
- **Fusion Project**: 4098002-KY2050 — Intelligent Automation
- **Space**: Innovation IT SRE and Support
- **Description**: Parent Fusion project that all IA monitoring and automation work
  is tracked against. All IISS-48x, IISS-50x, and IISS-82x tickets reference this
  Fusion project code for billing and time-tracking purposes.
- **Used in**: IISS-509 (Frontend Dashboard), IISS-487 (Grafana AMG), IISS-507
  (Inventory API), and all sub-tasks under IISS-482.

## Enterprise Custom UI (Citco)

### IISS-919 — Infrastructure Monitoring Dashboard — Citco Enterprise (To Do)
- **Space**: Innovation IT SRE and Support
- **Description**: Add a new infrastructure monitoring dashboard page to the existing
  `ia-config-portal` UI (built by Soundarya/Sridhar). This will be Citco's
  **Enterprise Custom UI** — eliminating the limitations of CloudWatch Dashboards
  and Grafana (no drag-and-drop, limited panel types, no config-driven customisation).

**Repositories:**
- IA Config Portal UI: Bitbucket repo (`ia_config_service_portal`)
- AWS CodeCommit repo (linked)

**Pipelines:**
- Infrastructure Pipeline
- ECR Pipeline

**Key requirements:**
1. Add a new dashboard page within the `ia-config-portal` UI
2. Data source: AWS CloudWatch for metrics
3. Use the existing **My Resources API** to fetch resources in real time
4. Dashboard must be **config-driven** — panels/widgets defined via configuration
5. **Drag-and-drop** panel rearrangement and layout customisation
6. Experiment with chart/panel types: line, bar, gauge, heatmap, etc.
7. Replace CloudWatch + Grafana limitations with a fully customisable enterprise UI

**Subtasks:** TBD (none defined at ticket creation)

**Context / Why this matters:**
- CloudWatch dashboards are siloed per service, no cross-service filtering
- Grafana AMG (IISS-487) achieves ~60% Dynatrace parity but has fixed panel types
  and no drag-and-drop layout customisation
- The `ia-config-portal` is an existing internal UI (React 19/TypeScript with Rsbuild
  bundler, Express.js BFF) already used for IA configuration management — adding a
  monitoring page here gives the SRE team a single Citco-owned interface without
  external tool dependency
- Depends on IISS-509 (inventory API frontend) and IISS-507 (My Resources API) being
  available as data sources

**Technology Stack:**
- Frontend: React 19, TypeScript, MUI, AG Grid Enterprise, Tailwind CSS, Framer Motion
- Backend: Express.js BFF (server.js), proxies to CloudWatch and Inventory API
- Auth: Ping Access SSO (SM_USER header) + AuthMaster API (role-based access)
- Deployment: ECS Fargate, internal ALB, 3 envs (DEV auto-deploy, UAT/PROD IT approval)

**Status:** In Progress (collaborative with Soundarya/Sridhar; Bhavik focuses on
CloudWatch integration and config-driven panel rendering)

## Primary Deliverable

### IISS-487 — Amazon Managed Grafana: Meridian Platform Monitoring Dashboard
- **Status**: In Progress | **Priority**: Critical | **Hours Logged**: 140h
- **Requested By**: Kishor Deotale
- **Started**: May 6, 2026 (created Apr 22 by Bhavik)
- **Description**: Single-pane Grafana dashboard for Meridian platform health
- **Scope**: 14 service rows, 110+ panels, 17 alerting rules, 960+ tests
- **Architecture**: CloudFormation IaC, Lambda provisioner, S3 dashboard storage
- **Key milestone dates**:
  - May 6: Kishor elevates to Critical, full spec
  - May 11-12: Infrastructure deployed (Grafana workspace, alarms, Container Insights)
  - May 13-15: Lambda/ECS panels, Grafana 12 upgrade, automation pipeline
  - May 19-22: MSK, DocumentDB, Neptune, RDS, OpenSearch rows, S3 migration
  - May 25-27: Redis row, datasource analysis, alarm notifications, documentation
  - May 29: Re-Notifier Lambda, composite alarms, Grafana alerting
  - Jun 9-11: EC2 row, per-panel folder structure migration, S3 template staging
  - Jun 15-18: Deep-links, resource tables, Redis/OpenSearch restructure, deployment v728

## CloudWatch Dashboard Platform (pre-Grafana)

### IISS-455 — Lambda Monitoring Dashboard (DONE, 2h logged)
- Due: Apr 13 | Completed: Apr 7
- CloudWatch dashboard via CFN for rpacfs1/IA-BPO lambdas (51 functions)
- Subtask IISS-461: Confluence page with 51 Lambda inventory + trigger mapping

### IISS-469 — Improve Centralized Lambda Dashboard (TEST)
- Active: Apr 15–22
- Additional tags (cfsbpm, citcoworks, meridian), log errors widget, CSV/Excel export
- Deep research: OOM detection (5 approaches), subscription filters, Top K limitations
- Documented architectural constraint: 106 metric filters needed (IAM blocks central approach)

## IA Resources Monitoring Platform

### IISS-482 — IA Resources/Infrastructure Monitoring Dashboard (In Progress, 11h logged)
- Parent story for the full monitoring platform
- SQS monitoring feature (Jun 12): registry, exporter, API, dashboard builder, 960 tests
- Architecture: 3-tier fallback (API → S3 → local file), placeholder resolution

### IISS-483 — EC2 Monitoring Dashboard (In Progress)
- Gap analysis: 83 instances, 1 relevant (tag mismatch BudgetCode="CFS/RPA")
- Solution: AppName fallback pattern in registry API
- CWAgent via SSM for memory/disk metrics ($1.29/month)
- 5-phase implementation plan with validation checklist

### IISS-484 — ECS Monitoring Dashboard (In Progress)
- Container Insights cost analysis: 4 options (Free/$0, Lambda/$10, Standard CI/$10.44, Enhanced/$18.60)
- Recommended Standard CI at $10.44/month for 100% dashboard coverage
- Enabled CI on 11 clusters (led to Container Insights audit/reversion work)

### IISS-485 — EKS Monitoring Dashboard (In Progress)
- Scope change: only 1 EKS cluster (uipath-eks-cluster-01, AUTOMATIONHUB, idle)
- Added AUTOMATIONHUB to budget codes, on hold pending cluster activation

### IISS-486 — Export to S3 (In Progress)
- S3 bucket via CFN, CLI script, API endpoints, scheduled Lambda (daily 6AM UTC)
- Excel export: one sheet per widget, auto-sized columns

## Registry API Extensions

### IISS-504 — Extend Registry API for AUTOMATIONHUB (In Progress)
- 4 EC2 (stopped), 22 Lambdas, 1 EKS cluster

### IISS-505 — Extend Registry API for MERIDIAN (In Progress)
- Largest scope: 6 ECS clusters (5 untagged), 32 Lambdas, 2 EC2
- Name-based discovery needed, "Shared Cloud Artifacts" alias

### IISS-510 — Extend Registry API for CITCOWORKS (In Progress)
- Critical finding: CITCOWORKS and MERIDIAN share "Shared Cloud Artifacts" BudgetCode
- AppName mandatory to distinguish, 1 EC2, 5 ECS clusters, 5 Lambdas

### IISS-506 — MERIDIAN Monitoring Infrastructure (To Do)
- Umbrella story: triggered by Apr 17 + May 1 incidents
- 6-component gap analysis (Event Service, SQS, Lambda, MSK, OpenSearch, ODL)
- Clones IISS-487, parent of IISS-505

### IISS-507 — Full-Stack Implementation (In Progress, 2.5h logged)
- New Flask async API project: `ia-sre-resources-inventory`
- Discoverer registry pattern, 3 concrete + 7 stub discoverers
- Parent of IISS-508 (Backend) and IISS-509 (Frontend)

### IISS-508 — Backend — IA Resources (In Progress)
- 6 tasks: core extension, AUTOMATIONHUB, MERIDIAN, aggregation, export API, tag strategy
- Full BUDGET_CODE_CONFIG with 4 budget codes + AppName fallback

### IISS-509 — Frontend — IA Infrastructure Inventory Dashboard (To Do)
- **Parent**: IISS-507 (full-stack), IISS-482 (IA Resources Monitoring)
- **Fusion Project**: 4098002-KY2050 — Intelligent Automation
- **Depends on**: IISS-508 (Backend API completion)
- **Description**: Implement all frontend components, widgets, and UI logic for the
  IA Resources Monitoring Dashboard. Displays EC2, ECS, EKS, and Lambda resources
  across all budget codes with export-to-Excel functionality.

**Scope (7 tasks):**

| # | Task | Details |
|---|------|---------|
| 1 | Dashboard Layout | Main layout with budget code navigation and filtering |
| 2 | EC2 Widget | EC2 instances per budget code — running and stopped states |
| 3 | ECS Widget | ECS clusters/services — name-based discovery for Meridian (6 clusters, 13+ services) |
| 4 | EKS Widget | EKS clusters — handle empty/zero node state (AUTOMATIONHUB) |
| 5 | Lambda Widget | Lambda functions per budget code with key metrics |
| 6 | Export to Excel | Export button per widget — formatted Excel sheet download |
| 7 | Resource State Indicators | Visual indicators: running, stopped, degraded, empty |

**Resource scope reference (4 budget codes at time of ticket):**

| Resource | rpacfs1 | IA-BPO | AUTOMATIONHUB | MERIDIAN | Total |
|----------|---------|--------|---------------|----------|-------|
| EC2 (running) | 1 | 0 | 0 | 1 | 2 |
| EC2 (stopped) | 0 | 0 | 4 | 1 | 5 |
| ECS Clusters | 5 | 6 | 0 | 6 | 17 |
| ECS Services | 5 | 6 | 0 | 13+ | 24+ |
| Lambda | ~30 | ~30 | 22 | 32 | ~114 |
| EKS | 0 | 0 | 1 | 0 | 1 |

**Acceptance criteria:**
- EC2, ECS, EKS, Lambda widgets displayed per budget code
- Stopped/empty resource states visually indicated
- Export to Excel functional on all widgets
- Budget code filter/navigation working
- Dashboard responsive and accessible; tested across supported browsers

## Auto-Healing & Roadmap

### IISS-488 — Auto-Healing Pipeline (To Do)
- Alerts → SNS → Lambda → User-Friendly Emails → Auto-Healing actions
- Driven by KRI, prioritized after Meridian dashboard completion

### IISS-489 — Meridian SRE Observability Roadmap (To Do)
- Triggered by Apr 17 incident (9M Kafka messages, 7.5h delay)
- 4 pillars: Baseline, CloudWatch Alarms, Auto-Healing, SRE Observability
- Linked to incident report on Confluence

## X-Ray Tracing (Future Work)

### IISS-837 — Instrument services for X-Ray (To Do)
- Grafana Row 17 panels exist but empty (services not instrumented)
- 7 sub-tasks: Lambda, ECS ADOT, EKS DaemonSet, API Gateway, SQS, MSK, EC2
- Child of IISS-487

### IISS-838 — Lambda Instrumentation / Powertools Tracer (To Do, assigned to Bhavik)
- aws-lambda-powertools[tracer], @tracer.capture_lambda_handler
- No legacy aws-xray-sdk

### IISS-839 — ECS ADOT Sidecar (To Do)
### IISS-840 — EKS ADOT DaemonSet (To Do)
### IISS-841 — API Gateway Tracing (To Do)
### IISS-842 — SQS Trace Propagation (To Do)
### IISS-843 — MSK/Kafka Trace Propagation (To Do)
### IISS-844 — EC2 Standalone Tracing (To Do)

## Log Group Discovery & Observability

### IISS-845 — CloudWatch Log Group Discovery & Observability Integration (To Do)
- Solves "2-3 min to find relevant log group" problem
- 3,423 log groups, mapped to 7 platforms (748 matched)
- 4-part solution: LogGroupDiscoverer, alarm email links, Grafana panel, saved queries
- 10 sub-tasks (IISS-846 through IISS-873)
- Child of IISS-487

### IISS-846 — Create LogGroupDiscoverer (To Do, assigned to Bhavik)
### IISS-847 — Register discoverer + mapping (To Do)
### IISS-848 — API endpoint GET /platforms/{platform}/log-groups (To Do)
### IISS-849 — IAM permission logs:DescribeLogGroups (To Do)
### IISS-850 — Deploy inventory + verify S3 cache (To Do)
### IISS-851 — Deploy saved queries script (To Do)
### IISS-852 — Integrate log_groups.py into alarm formatter (To Do)
### IISS-853 — S3 read permission + env vars for alarm_notifier (To Do)
### IISS-872 — Grafana CloudWatch Logs panel (To Do)
### IISS-873 — Deploy monitoring repo + verify end-to-end (To Do)

## ML/AI

### IISS-824 — RPA LLM Agent: Study, Fixes, KB Enrichment \& Improvements (Aug 2026)
- **Repos**: `ml-rpa-status-llm-agent` + `core-smart-rpa-llm-ecr-image` (CodeCommit, coredev, us-east-1)
- **Status**: Critical bugs in production, KB sync fixes deployed; dev best-practice approval pending

**System Overview — Ask Citco RPA Chatbot (RAG Architecture):**

```
LibreChat UI → ECS Fargate (FastAPI) → Bedrock Agent (Claude)
                                          ├── Action Groups (Lambda) → Event Service, SDM, LE
                                          └── Knowledge Base (OpenSearch) → IRCOEKB wiki pages
```

**11 Lambda Functions:**

| Lambda | Purpose | Schedule |
|--------|---------|----------|
| `RPABedrockAgent` | Action groups: process status, SDM tickets, LE lookup | On-demand |
| `IRCOEKBExtractLambda` | SharePoint wiki → S3 (49 libraries, ~5,000 pages) | Daily 12:00 UTC |
| `RPALLMKBIngestionFunction` | Trigger Bedrock KB sync S3 → OpenSearch | Daily 14:00 UTC |
| `RPALLMIndexCreatorFunction` | Create OpenSearch 1024-dim FAISS/HNSW vector index | On deploy |
| `EventStoreExtractLambda` | Databricks event store → S3 CSV for process lookups | Daily 12:00 UTC |
| `ClientFundMappingLambda` | BPM API client/fund master data → S3 JSON | Every 3 hours |
| `AthenaTableLambda` | Create usage tracking Athena table (Parquet/KMS) | On deploy |
| `AthenaRepairLambda` | `MSCK REPAIR TABLE` for new S3 partitions | Every 10 min |
| `RPALLMUsageReportLambda` | Weekly usage report via SES | Fridays 16:00 UTC |
| `UploadFileFunction` | Upload API schema to S3 | On deploy |
| `ALBTestFunction` | ALB connectivity diagnostic (DEV only) | Manual |

**Critical Production Bugs Fixed (IISS-824, Aug 2026):**

1. **IRCOEKB Lambda 52% timeout rate** (most critical): 77 of 148 PROD runs hit 300s timeout (May–Aug 2026, 93-day CloudWatch analysis). Root cause: unconditional re-upload of all ~980 wiki pages daily. Fix (v1.1.x + v1.1.18): Two-phase hybrid sync — Phase 1 checks each of 49 libraries with `filter=Modified gt last_synced_at` (25s total); Phase 2 processes only changed libraries. Per-page idempotency using SharePoint `Modified` timestamp in S3 metadata. Steady-state time reduced from 291s avg → **~25 seconds**.

2. **OpenSearch silent delete bug** (v1.1.1): On index creation failure, code silently deleted the index and reported CloudFormation SUCCESS. Fixed: raise exception properly, add `index_exists()` idempotency check before create.

3. **Athena SSE encryption inconsistency**: `athena_repair.py` used `SSE_S3`; fix unified to `SSE_KMS` across all Athena queries.

4. **SSL verification disabled**: `client_and_fund_report.py` used `verify=False` on BPM API. Fixed to `verify=True`.

5. **Lambda fire-and-forget pattern**: `EventStoreExtractLambda` and `ClientFundMappingLambda` always reported SUCCESS regardless of actual outcome (caught `BotoError` which doesn't exist; `ClientError` not imported). Fixed: proper exception imports and re-raise.

6. **Athena race condition**: `MSCK REPAIR TABLE` ran immediately after `CREATE TABLE` before table existed. Fixed: `wait_for_query()` polling loop.

**KB Content Added:**
- NAV Checklist PDFs uploaded to S3 (`RPA Processes/NAV Checklist/`) via idempotent upload script and triggered KB ingestion. Now in PROD KB.

**Additional Work:**
- Refactored 1,140-line `function.py` → 8 focused modules
- Structlog migration across all 11 Lambda functions
- Type hints, Google docstrings, Pydantic models added
- 194 unit tests at 99% code coverage (v1.1.x series)
- X-Ray tracing instrumented (Powertools Tracer, DEV only pending approval)
- Kill switch pattern via SSM Parameter Store (`/{Env}/rpa-llm/ircoekb/process-run-status`)
- Versions v1.1.1 through v1.1.32 released during Aug 3–20 2026

**Proposed (not yet implemented): Hybrid Graph-RAG Architecture**
- Observation: Citco RPA domain is highly relational — clients, funds, processes, platforms (BP/UiPath), process knowledge are interconnected entities
- Proposal: Add Graph-RAG layer (Amazon Neptune or similar) alongside existing vector RAG
- Rationale: Graph traversal over entity relationships (client → funds → processes → platform) would improve chatbot accuracy for complex multi-hop queries (e.g. "What processes run on Blue Prism for client X?")
- Status: Identified during IISS-824 engagement; to be formally proposed as IISS follow-on

## Support/Incident JIRAs

### IISS-538 — MESO High Memory/CPU didn't autoscale (~Jun 5)
### IISS-706 — CAIS Deadline SpnegoError hotfix (Jun 8, 7h logged)
### IISS-741 — MESO month-end stuck tasks (Jul 1, Critical)
### IISS-753 — VPL IPV UI element failure (Jul 8, 16h estimate)
### IISS-876 — VPL Pricing GTL incorrect booking (Jul 30)

## Resource Totals Across All 6 Budget Codes
| Resource | rpacfs1 | IA-BPO | BPM | AUTOMATIONHUB | MERIDIAN | CITCOWORKS | Total |
|----------|---------|--------|-----|---------------|----------|------------|-------|
| EC2 (running) | 1 | 0 | 0 | 0 | 1 | 1 | 3 |
| EC2 (stopped) | 0 | 0 | 4 | 1 | 0 | 5 |
| ECS Clusters | 5 | 6 | 0 | 6 | 5 | 22 |
| Lambda | ~30 | ~30 | 22 | 32 | 5 | ~119 |
| EKS | 0 | 0 | 1 | 0 | 0 | 1 |
