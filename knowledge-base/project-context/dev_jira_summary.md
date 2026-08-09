# Dev Work JIRA Summary

Complete inventory of all development JIRAs assigned to Bhavik Kantilal Bhagat
during the Citco CTM internship (March 15 – August 31, 2026).

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

### IISS-509 — Frontend — IA Resources (To Do)
- 7 tasks: layout, EC2/ECS/EKS/Lambda widgets, export, state indicators
- Depends on backend completion

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

### IISS-824 — Understand Document Agent in ML-RPA-Status LLM Repos (To Do)
- Two CodeCommit repos: ml-rpa-status-llm-agent + core-smart-rpa-llm-ecr-image
- Research/documentation task

## Support/Incident JIRAs

### IISS-538 — MESO High Memory/CPU didn't autoscale (~Jun 5)
### IISS-706 — CAIS Deadline SpnegoError hotfix (Jun 8, 7h logged)
### IISS-741 — MESO month-end stuck tasks (Jul 1, Critical)
### IISS-753 — VPL IPV UI element failure (Jul 8, 16h estimate)
### IISS-876 — VPL Pricing GTL incorrect booking (Jul 30)

## Resource Totals Across All 5 Budget Codes
| Resource | rpacfs1 | IA-BPO | AUTOMATIONHUB | MERIDIAN | CITCOWORKS | Total |
|----------|---------|--------|---------------|----------|------------|-------|
| EC2 (running) | 1 | 0 | 0 | 1 | 1 | 3 |
| EC2 (stopped) | 0 | 0 | 4 | 1 | 0 | 5 |
| ECS Clusters | 5 | 6 | 0 | 6 | 5 | 22 |
| Lambda | ~30 | ~30 | 22 | 32 | 5 | ~119 |
| EKS | 0 | 0 | 1 | 0 | 0 | 1 |
