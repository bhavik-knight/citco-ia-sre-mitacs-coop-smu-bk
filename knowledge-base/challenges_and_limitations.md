# Challenges and Limitations — Comprehensive Knowledge Base

**Scope:** All technical challenges, platform limitations, and mitigations encountered during the Citco IA/SRE Mitacs internship (March–August 2026)

**Source Documents:**
- `ia-it-sre-infrastructure-monitoring-amg/docs/limitations/` (9 major limitations + 6 supplementary docs)
- `ia-resources-monitoring/docs/LIMITATIONS.md` (8 limitations + 6 architecture decisions)
- `knowledge-base/hotfixes/` (3 incident reports)
- Work logs (2026-06, 2026-07, 2026-08)

---

## Table of Contents

1. [AWS CloudWatch Limitations](#1-aws-cloudwatch-limitations)
2. [Grafana Platform Constraints](#2-grafana-platform-constraints)
3. [Infrastructure & Deployment Challenges](#3-infrastructure--deployment-challenges)
4. [Data Discovery & Filtering Limitations](#4-data-discovery--filtering-limitations)
5. [Production Incidents & Lessons Learned](#5-production-incidents--lessons-learned)
6. [Corporate Policy Constraints](#6-corporate-policy-constraints)
7. [Architecture Decisions & Trade-offs](#7-architecture-decisions--trade-offs)

---

## 1. AWS CloudWatch Limitations

### 1.1 Metrics Insights SQL — 10 TPS Hard Limit

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudWatch Metrics Insights SQL queries are limited to 10 transactions per second (TPS) per account per region. This limit is **not adjustable** via AWS Support. |
| **Impact** | Dashboard with 90+ SQL panels causes throttling on load. Panels show "Error" or timeout intermittently. Concurrent users multiply the problem (3 SRE team members = 3× pressure). |
| **Root Cause** | AWS imposes this limit to protect CloudWatch backend. Unlike `GetMetricData` (500 TPS, adjustable), Metrics Insights has a hard cap. |
| **Mitigation Applied** | (1) Collapsed rows by default — reduces initial queries from ~90 to ~40. (2) Dashboard refresh set to 5m. (3) Documented option to split into Overview + Deep Dive dashboards if throttling persists in production. |
| **Status** | Mitigated but not fully resolved — monitoring in UAT/PROD |

### 1.2 Log Insights — 50 Log Group Maximum

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudWatch Logs Insights supports maximum 50 log groups per query. IA environment has 54+ Lambda functions. |
| **Impact** | Error root cause widget excludes Lambdas ranked 51+. Some errors invisible in dashboard. |
| **Root Cause** | Hard limit imposed by AWS — cannot be increased. |
| **Mitigation Applied** | `get_validated_log_groups()` filters out Lambdas without active log groups first (prioritizes active functions). Saved Logs Insights queries cover the full set for manual investigation. |
| **Status** | Workaround in place |

### 1.3 CloudWatch Dashboard Body — 51KB CFN Limit

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudFormation has a 51,200-byte limit for inline dashboard body. With 54+ Lambdas × multiple widgets, JSON exceeds this limit. |
| **Impact** | Cannot deploy dashboards via pure IaC (CloudFormation). |
| **Root Cause** | CFN template size constraint — designed for static infrastructure, not dynamic metric configurations. |
| **Mitigation Applied** | Python `put_dashboard` API deployment (no size limit). Script is idempotent and version-controlled. Metric filters remain in CFN for alarm triggering. |
| **Status** | Resolved — Python deployment is production pattern |

### 1.4 SEARCH() Cannot Filter by Tags

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudWatch `SEARCH()` expression cannot filter resources by AWS tags. Only namespace, metric name, and dimension patterns are supported. |
| **Impact** | Cannot dynamically query "all Lambda functions tagged `BudgetCode=MERIDIAN`" — must enumerate each function explicitly. |
| **Root Cause** | CloudWatch API design limitation. Tags are metadata, not metric dimensions. |
| **Mitigation Applied** | Build explicit metric arrays per resource using YAML placeholders. Dashboard JSON grows linearly with resource count but is deterministic. |
| **Status** | Architectural decision — accepted trade-off |

### 1.5 Metrics Insights SQL — No Percentile Support

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudWatch Metrics Insights SQL does not support percentile aggregation functions (`PERCENTILE(Duration, 50)`). Percentiles only available via Metric Search API. |
| **Impact** | Percentile panels (p50, p95, p99 latency) use Metric Search mode, which defers execution on load → "No data" until manual query run. |
| **Root Cause** | Grafana CloudWatch plugin limitation — Metric Search with percentiles is computationally expensive, so Grafana defers execution. |
| **Mitigation Applied** | Users manually click "Run queries" or refresh page. Documented as known behavior. Monitoring for Grafana plugin updates. |
| **Status** | Workaround in place |

### 1.6 Log Widgets Require Explicit Log Group Names

| Aspect | Detail |
|--------|--------|
| **Challenge** | CloudWatch `type: log` widgets require a `logGroupNames` array. EC2, ECS, and EKS don't have predictable log group naming patterns. |
| **Impact** | Cannot embed live log queries for EC2/ECS/EKS in dashboard panels. |
| **Root Cause** | CloudWatch API requirement — queries fail with `MalformedQueryException` without explicit log group names. |
| **Mitigation Applied** | Text widgets linking to saved Logs Insights queries. Users click through to investigate — not inline but functional. |
| **Status** | Architectural decision — accepted trade-off |

### 1.7 ECS Fargate — No Free Cluster-Level Metrics

| Aspect | Detail |
|--------|--------|
| **Challenge** | Fargate clusters report no cluster-level CPU/Memory metrics in `AWS/ECS` namespace without Container Insights. Only service-level metrics are free. |
| **Impact** | ECS Infrastructure panels show no data for Fargate clusters without Container Insights enabled. |
| **Root Cause** | Architectural difference: EC2 clusters have fixed capacity (instances) to measure against. Fargate is serverless — no "cluster capacity" concept exists. AWS charges for visibility into managed infrastructure. |
| **Mitigation Applied** | Container Insights enabled per-cluster via AWS CLI (manual operational action). Cost: ~$0.30/custom metric/month. |
| **Status** | Partial — depends on cluster configuration |

### 1.8 Container Insights Accidental Enablement

| Aspect | Detail |
|--------|--------|
| **Challenge** | During initial rollout, Container Insights was enabled on 44 EKS clusters across DEV/UAT/PROD via CloudFormation — many belonged to other teams. |
| **Impact** | Potential cost impact ($0.30/metric × many metrics × 44 clusters). Required audit and selective reversion. |
| **Root Cause** | CloudFormation stack scope too broad — didn't filter by IA-owned clusters only. |
| **Mitigation Applied** | Developed `audit_container_insights.py` script to identify affected clusters. Removed CFN stack from release branch. Container Insights now enabled manually per-cluster. |
| **Status** | Resolved — audit script available |

---

## 2. Grafana Platform Constraints

### 2.1 Single SQL Query Per Panel

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana CloudWatch plugin enforces limit of **one** Metrics Insights SQL query per panel. Multiple dimension-based queries work, but SQL mode is restricted. |
| **Impact** | Cannot combine "Running Tasks" + "Desired Tasks" on single panel using SQL. |
| **Root Cause** | Grafana plugin architecture decision — SQL queries are more resource-intensive. |
| **Mitigation Applied** | Split multi-query panels into separate single-query panels. Dashboard has more panels but each loads reliably. |
| **Status** | Resolved |

### 2.2 Reduce Transformation Drops Rows (Single-Step)

| Aspect | Detail |
|--------|--------|
| **Challenge** | Using a single `reduce` transformation with `mode: "seriesToRows"` silently drops some series. Table panels show fewer rows than expected. |
| **Impact** | OpenSearch cluster status tables missing domains. No error displayed — data silently lost. |
| **Root Cause** | AMG bug when pivoting irregular time series data directly to table format. |
| **Mitigation Applied** | Two-step reduce pattern: (1) `reduceFields` to collapse time series to scalars, (2) `seriesToRows` to pivot. Reliable and now documented as standard. |
| **Status** | Resolved — pattern documented |

### 2.3 Bar Gauge Hides Name with Single Resource

| Aspect | Detail |
|--------|--------|
| **Challenge** | When bar gauge panel has only one bar, resource name is hidden regardless of `namePlacement` setting. Only numeric value appears. |
| **Impact** | Cosmetic issue in DEV (fewer resources). Less likely in UAT/PROD with more resources. |
| **Root Cause** | Grafana treats single-bar as "single stat" display — suppresses name to maximize value prominence. |
| **Mitigation Applied** | Accepted for DEV. Unlikely to affect production environments with more resources. |
| **Status** | Accepted limitation |

### 2.4 filterByValue — Integer vs Float Mismatch

| Aspect | Detail |
|--------|--------|
| **Challenge** | `filterByValue` with `"id": "equal"` and integer `"value": 1` does not match CloudWatch's `1.0` (float). |
| **Impact** | Table filters that check for exact status values (e.g., ClusterStatus = 1) fail silently. |
| **Root Cause** | Type coercion mismatch in Grafana transformation engine. |
| **Mitigation Applied** | Use `"id": "greater"` with `"value": 0.5` instead of equality check. Documented as standard pattern. |
| **Status** | Resolved |

### 2.5 Time Series Deep Link Limitations

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana time series panels cannot deep-link to CloudWatch console for specific metrics. Data links only work with table/stat panels. |
| **Impact** | Users cannot click graph points to investigate in CloudWatch console. |
| **Root Cause** | Grafana data link interpolation doesn't expose metric dimensions from time series hover context. |
| **Mitigation Applied** | Added text widgets with console links. Created saved queries for common investigations. |
| **Status** | Workaround in place |

### 2.6 No Cross-Panel or Dashboard-Level Filtering

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana does not support cross-panel filtering or dashboard-level filter propagation. Clicking a resource in one panel does not automatically filter other panels on the same row or dashboard. |
| **Impact** | Fragmented investigation experience. Selecting a Lambda function in error table doesn't filter duration, memory, cold start panels to that function. |
| **Root Cause** | Grafana architecture treats each panel as independent query unit. Cross-panel state synchronization not supported natively. Dashboard variables are the only coordination mechanism. |
| **Mitigation Applied** | Implemented dashboard-level template variables ($platform, $environment, $function) that filter all panels when changed. Added data links on table panels opening filtered views in new tabs. Documented two-step workflow. |
| **Status** | Architectural limitation — accepted trade-off |

### 2.7 AMG IAM Role Credential Rotation — Chicken-and-Egg Problem

| Aspect | Detail |
|--------|--------|
| **Challenge** | AMG authenticates to CloudWatch using IAM role with temporary credentials. Corporate policy requires monthly service account password rotation. Updating the IAM role trust policy requires workspace reconfiguration—but workspace can't authenticate to make this update when credentials are already invalid. |
| **Impact** | Each month when credentials rotate, AMG workspace loses CloudWatch access until IAM role trust relationship is manually updated. Dashboard shows "Error" on all panels. |
| **Root Cause** | AMG assumes IAM role via sts:AssumeRole. Trust policy specifies allowed principals. When service account credentials rotate, trust relationship must be updated to reflect new principal—but workspace cannot authenticate to make the update. |
| **Mitigation Applied** | Created runbook for monthly credential rotation procedure. Calendar reminder 3 days before rotation. Pre-staged updated trust policy document. Documented escalation path for off-hours rotation. |
| **Status** | Operational procedure in place |

### 2.8 Variable Dimension Discovery Limitations

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana CloudWatch variable queries (`dimension_values()`) return all values in account, not filtered by other variables. |
| **Impact** | Platform dropdown shows all platforms, not filtered by selected environment. Cross-filtering not supported. |
| **Root Cause** | CloudWatch `list-metrics` API doesn't support tag-based filtering in dimension value queries. |
| **Mitigation Applied** | Separate variable per environment. Users select correct combination. Documented in dashboard usage guide. |
| **Status** | Platform limitation — accepted |

### 2.7 VPC Data Source Requirements

| Aspect | Detail |
|--------|--------|
| **Challenge** | Amazon Managed Grafana requires VPC configuration to access CloudWatch in private subnets. Cross-account access requires additional IAM setup. |
| **Impact** | Initial AMG workspace couldn't query CloudWatch metrics. Setup required network configuration. |
| **Root Cause** | AMG security model — must be in VPC with route to CloudWatch endpoints. |
| **Mitigation Applied** | Configured VPC endpoints for CloudWatch. Set up cross-account IAM roles for multi-account queries. |
| **Status** | Resolved |

### 2.8 Infinity Plugin Connectivity

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana Infinity plugin (for REST API data sources) requires outbound internet access or VPC endpoints for internal APIs. |
| **Impact** | Could not fetch data from internal Meridian APIs initially. |
| **Root Cause** | AMG runs in isolated VPC. Infinity plugin makes HTTP calls that need network routing. |
| **Mitigation Applied** | Configured internal ALB endpoints accessible from AMG VPC. Alternative: use CloudWatch data source for metrics, Infinity for business data. |
| **Status** | Resolved |

---

## 3. Infrastructure & Deployment Challenges

### 3.1 Static Metrics at Deploy Time

| Aspect | Detail |
|--------|--------|
| **Challenge** | Dashboard metrics are baked into CloudWatch JSON at deploy time. If resources are added/removed, dashboard won't reflect changes until redeployed. |
| **Impact** | New Lambda functions invisible in dashboard until redeploy. Deleted functions show "No data". |
| **Root Cause** | CloudWatch doesn't support dynamic resource discovery in dashboard widgets. |
| **Mitigation Applied** | Redeploy script: `python main.py deploy -e DEV`. Documented as operational procedure. |
| **Status** | Architectural decision — accepted trade-off |

### 3.2 Lambda Insights Layer Stripped on Redeploy

| Aspect | Detail |
|--------|--------|
| **Challenge** | Lambda Insights layer must be manually attached. If another team redeploys a Lambda, the layer is stripped. |
| **Impact** | Cold start and memory utilization widgets show gaps for Lambdas missing the layer. |
| **Root Cause** | Lambda Insights is a layer, not a service-level setting. No CFN mechanism to enforce across teams. |
| **Mitigation Applied** | Periodic script: `add_lambda_insights.py --env DEV`. Supports dry-run and rollback. |
| **Status** | Operational procedure in place |

### 3.3 Registry API Local Only

| Aspect | Detail |
|--------|--------|
| **Challenge** | Flask resource discovery API runs on `localhost:5000` only. Not deployed to AWS. |
| **Impact** | During CI/CD, API is unavailable. Builder must fall back to S3 or local JSON. |
| **Root Cause** | Designed as developer tool. AWS deployment would require ECS/Lambda hosting + IAM. |
| **Mitigation Applied** | 3-tier fallback chain: API → S3 → local file. S3 updated on each API call. Local file is safety net. |
| **Status** | Architectural decision |

### 3.4 SSL Certificate Issues on Corporate VPN

| Aspect | Detail |
|--------|--------|
| **Challenge** | S3 cache operations fail with SSL errors when running on corporate VPN. Certificate chain verification fails due to proxy inspection. |
| **Impact** | Development workflow disrupted. Cache misses cause slower builds. |
| **Root Cause** | Corporate VPN performs TLS inspection, breaking certificate chain. |
| **Mitigation Applied** | S3Cache respects `AWS_CA_BUNDLE` environment variable. Catches `SSLError`/`ConnectionError` gracefully — returns cache miss instead of crashing. Added `certifi` as explicit dependency. |
| **Status** | Resolved (v1.1.1, v1.1.2) |

### 3.5 Dashboard JSON 65KB Secrets Manager Limit

| Aspect | Detail |
|--------|--------|
| **Challenge** | Dashboard JSON was stored in AWS Secrets Manager (65,536-byte limit). Growing dashboard exceeded limit. |
| **Impact** | Deployment failures when dashboard JSON > 65KB. |
| **Root Cause** | Secrets Manager designed for credentials, not large configuration objects. |
| **Mitigation Applied** | Migrated to S3 storage. No practical size limit. `ServerSideEncryption=AES256` for compliance. |
| **Status** | Resolved |

---

## 4. Data Discovery & Filtering Limitations

### 4.1 ALB Naming Inconsistency

| Aspect | Detail |
|--------|--------|
| **Challenge** | Platform filter (`$platform`) cannot be applied to ALB panels. Some ALBs use `meridian-*` prefix, others use abbreviated `mrdn-*`. |
| **Impact** | Row 6 ALB panels show all ALBs in account (unfiltered). SRE team must visually identify correct ones. |
| **Root Cause** | Historical naming inconsistency. ALB naming not standardized across teams. |
| **Mitigation Applied** | Documented. Recommended tag-based filtering (`AppName: MERIDIAN`) but blocked by Grafana plugin limitation (no `WHERE tag.*` support). DEV verified to use consistent `meridian-*` names. |
| **Status** | Workaround — awaiting plugin update |

### 4.2 Shared Budget Code Returns Cross-Team Resources

| Aspect | Detail |
|--------|--------|
| **Challenge** | When `budget_code=MERIDIAN` requested, resources from other teams (CTI, PREX, PE-SERVICES) also returned because they share `BudgetCode=Shared Cloud Artifacts`. |
| **Impact** | MERIDIAN filter returns more resources than expected. Dashboard shows non-MERIDIAN resources. |
| **Root Cause** | `Shared Cloud Artifacts` is used by multiple teams. MERIDIAN depends on these shared services. |
| **Mitigation Applied** | Strict filter utility available (`matches_budget_code_filter` in `api/utils/tag_filter.py`) but not active. Can be enabled to restrict to `AppName` match when `BudgetCode=Shared Cloud Artifacts`. |
| **Status** | Filter available but not enabled — intentional design decision |

### 4.3 EC2 Memory Monitoring Requires CloudWatch Agent

| Aspect | Detail |
|--------|--------|
| **Challenge** | EC2 instances don't report memory metrics to CloudWatch by default. Only CPU, network, and disk I/O are available. |
| **Impact** | Memory utilization panels show "No data" for EC2 instances without CloudWatch Agent. |
| **Root Cause** | Memory is internal to the instance — AWS cannot observe it without an agent inside the OS. |
| **Mitigation Applied** | Documented requirement for CloudWatch Agent installation. Added check in resource discovery to identify instances without memory metrics. |
| **Status** | Operational dependency |

### 4.4 Table Filter Transformation Limitations

| Aspect | Detail |
|--------|--------|
| **Challenge** | Grafana table panels with multiple filter transformations have performance issues. Complex filter chains cause timeout on large datasets. |
| **Impact** | Status tables with 50+ resources slow to load. Some filters don't apply correctly. |
| **Root Cause** | Transformation engine processes data in browser. Large datasets overwhelm client-side processing. |
| **Mitigation Applied** | Pre-filter data in CloudWatch query (SQL `WHERE` clause). Keep transformation chains short. Limit to top N results. |
| **Status** | Pattern documented |

---

## 5. Production Incidents & Lessons Learned

### 5.1 CAIS Deadline Pipeline Silent Failure (June 2026)

| Aspect | Detail |
|--------|--------|
| **Incident** | CAIS data load pipeline failed silently — no error notifications sent. Downstream systems received no data. |
| **Root Cause Chain** | (1) UCM credentials expired → SMB mount failed silently (no exception raised). (2) Empty `deadline_ids` list generated invalid SQL (`WHERE id IN ()`). (3) Zip file upload attempted before verifying file creation → `FileNotFoundError`. |
| **Impact** | Data delivery missed deadline. Cascading failures across downstream systems. No alerts triggered. |
| **Resolution** | (1) Added explicit credential validation with exception on failure. (2) Added empty list check before SQL generation. (3) Added file existence check before upload. (4) Enhanced error notification coverage. |
| **Lesson Learned** | Silent failures are worse than loud failures. Every integration point needs explicit health check with alerting. |

### 5.2 UCM Credential Validation Hotfix

| Aspect | Detail |
|--------|--------|
| **Incident** | SMB mount to UCM share succeeded but returned empty directory when credentials expired. No error raised. |
| **Root Cause** | SMB protocol allows "successful" connection with expired credentials but returns no data. Library didn't distinguish between empty share and auth failure. |
| **Resolution** | Added credential validation step before processing: attempt to list known directory, verify expected files exist. Fail fast with clear error if validation fails. |
| **Lesson Learned** | "No error" doesn't mean "success". Validate expected state, not just absence of exceptions. |

### 5.3 Meridian April 17 Incident

| Aspect | Detail |
|--------|--------|
| **Incident** | Meridian service degradation due to database connection pool exhaustion. |
| **Root Cause** | Connection leak in exception handling path. Connections not released on error. |
| **Impact** | Service latency increased 10x. Eventually led to complete unavailability. |
| **Resolution** | Fixed connection handling with proper `finally` blocks. Added connection pool monitoring. Set up alerts for pool utilization > 80%. |
| **Lesson Learned** | Resource cleanup must happen in `finally` blocks, not just happy path. Monitor resource pools, not just application metrics. |

### 5.4 SSL Crash in S3 Cache (July 2026)

| Aspect | Detail |
|--------|--------|
| **Incident** | Resource inventory Lambda crashing with SSL errors when S3 cache accessed. |
| **Root Cause** | Corporate VPN TLS inspection breaking certificate chain. Lambda running in VPC with proxy. |
| **Resolution** | (1) S3Cache respects `AWS_CA_BUNDLE` env var. (2) Graceful degradation — catch SSL/Connection errors, return cache miss, continue without cache. (3) Added `certifi` as explicit dependency. |
| **Lesson Learned** | Network-dependent code needs graceful degradation. Cache should accelerate, not block. |

---

## 6. Corporate Policy Constraints

### 6.1 CloudFormation ResourceExistenceCheck Hook

| Aspect | Detail |
|--------|--------|
| **Challenge** | Citco AWS accounts have custom CloudFormation hook (`AWS::EarlyValidation::ResourceExistenceCheck`) that validates resources before creation. |
| **Impact** | Blocked alarm stack deployment when attempting to rename alarms. All resources showed `CREATE_FAILED`. |
| **Root Cause** | Corporate guardrail checks for resource conflicts. Hook validation fails for reasons not visible in CloudFormation events. |
| **Resolution** | Superseded alarm deployment with dynamic Lambda provisioner. Alarms now managed programmatically, bypassing CFN hook. |
| **Lesson Learned** | Corporate guardrails can block standard AWS patterns. Have alternative deployment methods available. |

### 6.2 S3 Encryption Policy

| Aspect | Detail |
|--------|--------|
| **Challenge** | Corporate policy (`CITCO-S3ForceEncryptNoPublic`) requires `ServerSideEncryption=AES256` on all S3 uploads. |
| **Impact** | S3 uploads fail if encryption header missing. Not obvious from error message. |
| **Resolution** | Added `ServerSideEncryption='AES256'` to all `put_object` and `upload_file` calls. |
| **Lesson Learned** | Check corporate policies early. Standard AWS examples may not work in enterprise environments. |

### 6.3 Cross-Account IAM Constraints

| Aspect | Detail |
|--------|--------|
| **Challenge** | Multi-account CloudWatch queries require cross-account IAM roles. Enterprise IAM policies restrict role assumption patterns. |
| **Impact** | AMG workspace couldn't query metrics from all three accounts (DEV/UAT/PROD) initially. |
| **Resolution** | Worked with Cloud team to create appropriate cross-account roles. Documented the required trust relationships. |
| **Lesson Learned** | Plan for cross-account access early. IAM setup can take weeks in enterprise environments. |

---

## 7. Architecture Decisions & Trade-offs

### 7.1 Placeholder-Based Metrics over SQL/SEARCH

| Decision | Build explicit metric arrays per resource using YAML placeholders instead of `SEARCH()` or Metrics Insights SQL. |
|----------|--------|
| **Why** | `SEARCH()` cannot filter by tag. SQL `IN` clause causes quoting issues when embedded in JSON dashboard bodies. |
| **Trade-off** | Dashboard JSON grows linearly with resource count. Metrics are static at deploy time. |
| **Mitigated by** | Python `put_dashboard` API (no size limit). Modular YAML widget system. Redeploy to pick up changes. |

### 7.2 Python Deploy Script over CloudFormation

| Decision | Deploy dashboards via Python script using `put_dashboard` API, not CloudFormation. |
|----------|--------|
| **Why** | CFN 51,200 byte limit. Dashboard content is dynamic (depends on current resource list). |
| **Trade-off** | Not pure IaC. Dashboard state not tracked in CloudFormation stack. |
| **Mitigated by** | Script is idempotent, version-controlled, deterministic. Metric filters remain in CFN. |

### 7.3 Three-Tier Fallback Chain for Resource Discovery

| Decision | Try Registry API → S3 → local file. Never fail if one source unavailable. |
|----------|--------|
| **Why** | API is local-only. S3 updated on API call. Local file is safety net for offline development. |
| **Trade-off** | If API is down and S3 is stale, dashboard may not reflect latest resources. |
| **Acceptable because** | Resources rarely added/removed. Redeploy picks up changes. Stale data better than no data. |

### 7.4 Text Widgets for Error Investigation

| Decision | Use text widgets linking to saved Logs Insights queries instead of embedded `type: log` widgets for EC2/ECS/EKS. |
|----------|--------|
| **Why** | `type: log` widgets require `logGroupNames` which are not predictable for EC2/ECS/EKS. |
| **Trade-off** | Users must click through to Logs Insights instead of seeing results inline. |
| **Mitigated by** | Saved queries pre-configured with correct log groups and filters. One-click access. |

### 7.5 Separate Packages per Resource Type

| Decision | `src/lambda_dashboard`, `src/ec2_dashboard`, `src/ecs_dashboard`, `src/eks_dashboard` as separate packages. |
|----------|--------|
| **Why** | Different metric namespaces, dimensions, and widget configurations. Separate packages allow independent deployment and testing. |
| **Trade-off** | Some code duplication in deploy.py and dashboard_builder.py patterns. |
| **Mitigated by** | Shared `pyproject.toml` config, shared test patterns, shared pre-commit hooks, shared paths module. |

### 7.6 Dynamic Lambda Provisioner over Static CFN Alarms

| Decision | Manage CloudWatch alarms via Lambda provisioner instead of static CloudFormation stack. |
|----------|--------|
| **Why** | Corporate CFN hook blocked alarm creation. Dynamic provisioner can respond to resource changes. |
| **Trade-off** | More complex deployment. Alarms not visible in CFN stack. |
| **Mitigated by** | Provisioner is idempotent. Alarm state tracked in S3. Can recreate from scratch if needed. |

---

## Summary Statistics

| Category | Count | Resolved | Mitigated | Accepted | Open |
|----------|-------|----------|-----------|----------|------|
| AWS CloudWatch Limitations | 8 | 2 | 4 | 2 | 0 |
| Grafana Platform Constraints | 10 | 4 | 4 | 2 | 0 |
| Infrastructure & Deployment | 5 | 3 | 2 | 0 | 0 |
| Data Discovery & Filtering | 4 | 0 | 2 | 2 | 0 |
| Production Incidents | 4 | 4 | 0 | 0 | 0 |
| Corporate Policy Constraints | 3 | 2 | 0 | 0 | 1 |
| **Total** | **34** | **15** | **12** | **6** | **1** |

---

## Key Themes

1. **AWS Service Limits are Real Constraints** — The 10 TPS Metrics Insights limit, 50 log group cap, and 51KB CFN limit all required architectural workarounds. These aren't edge cases — they're encountered at modest scale (54 Lambdas, 113 panels).

2. **Silent Failures are Dangerous** — Multiple incidents (CAIS pipeline, UCM credentials) involved operations that "succeeded" but produced no useful output. Explicit validation of expected state is essential.

3. **Enterprise Environments Add Complexity** — Corporate policies (CFN hooks, S3 encryption, VPN TLS inspection) break standard AWS patterns. Budget time for enterprise-specific adaptations.

4. **Grafana CloudWatch Plugin Has Gaps** — Tag-based filtering, percentile support in SQL, and cross-variable filtering are missing. Many workarounds involve splitting panels or using alternative query modes.

5. **Dynamic > Static for Monitoring Infrastructure** — Static dashboards and alarms can't keep up with cloud resource churn. Python-based deployment scripts enable dynamic adaptation.

---

*Last updated: August 2026*
*Author: Bhavik Bhagat*
*Internship: Citco IA/SRE Mitacs BSI (March–August 2026)*
