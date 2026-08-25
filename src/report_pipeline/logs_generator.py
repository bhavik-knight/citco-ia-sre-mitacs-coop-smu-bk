"""
Work Logs Generator Service module.
Generates styled Excel spreadsheets and compiles them to PDF for:
1. Major Project Report (240 Hours, 16 Weeks)
2. Internship Report (900 Hours, 24 Weeks)
"""
import shutil
import subprocess
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from src.report_pipeline.logger import get_logger

logger = get_logger("LogsGenerator")

# -------------------------------------------------------------------------
# CONSTANTS & STYLES
# -------------------------------------------------------------------------
SMU_MAROON = "8A0027"
LIGHT_GRAY = "F7F9FA"
BORDER_GRAY = "D3D3D3"

FONT_NAME = "Segoe UI"  # Clean, modern sans-serif font for Excel

TITLE_FONT = Font(name=FONT_NAME, size=15, bold=True, color=SMU_MAROON)
META_FONT = Font(name=FONT_NAME, size=10, italic=True)
HEADER_FONT = Font(name=FONT_NAME, size=11, bold=True, color="FFFFFF")
HEADER_FILL = PatternFill(fill_type="solid", start_color=SMU_MAROON, end_color=SMU_MAROON)

DATA_FONT = Font(name=FONT_NAME, size=10)
BOLD_DATA_FONT = Font(name=FONT_NAME, size=10, bold=True)
TOTAL_FONT = Font(name=FONT_NAME, size=11, bold=True, color=SMU_MAROON)

ALIGN_CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
ALIGN_LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

THIN_SIDE = Side(style="thin", color=BORDER_GRAY)
DATA_BORDER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)

# -------------------------------------------------------------------------
# LOGS DATA DEFINITION
# -------------------------------------------------------------------------

def get_major_project_data() -> list[dict]:
    """
    Real JIRA-mapped work log data for the 240-hour Major Project (16 Weeks).
    Covers: IISS-435, IISS-455/461/469, IISS-482-486, IISS-487, IISS-507/508,
    IISS-706, IISS-538, IISS-741, IISS-753, IISS-824, and X-Ray/log-group work.
    Repos: ia-it-sre-infrastructure-monitoring-amg, ia-resources-monitoring,
           ia-it-sre-infrastructure-inventory, rpacfs1-cais-pricing-extract-genai-infrastructure.
    """
    data = []

    # Phase 1: Part-Time Onboarding & CloudWatch Dashboards (Weeks 1-4)
    p1 = "Phase 1: Part-Time Onboarding & CloudWatch Dashboards"
    p1_weeks = [
        ("Week 1", "March 16, 2026 to March 20, 2026", [
            ("Environment Setup & Access Onboarding", "Day-1 orientation with manager Kishor Deotale; raised access tickets for Confluence (#14193911), JIRA (#14193674, #14193943), BitBucket (#14196961), AWS Core Dev; installed VSCode, Git, PyCharm, Amazon Q plugin.", 5.0),
            ("Environment Configuration & Architecture Study", "Configured AWS CLI with SSO authentication; explored Lambda fleet (51 functions), Meridian, CitcoWorks platform documentation; studied five budget code environments.", 5.0),
            ("Security & Compliance Training", "Attended BPM Control Questionnaire meeting; learned Active Directory integration, Ping authentication, penetration testing process, Dynatrace monitoring, ELK/Kibana logging infrastructure.", 5.0),
        ]),
        ("Week 2", "March 23, 2026 to March 27, 2026", [
            ("AWS Database Services Deep Dive", "Studied RDS (Single/Multi-AZ), Aurora, Redshift, DynamoDB, DocumentDB, Neptune Graph DB (Gremlin vs SPARQL), ElastiCache (Redis vs Memcached), TimeStream, QLDB.", 6.0),
            ("CloudWatch & CloudFormation Study", "Learned CloudWatch CMAA cycle, metrics, logs, alarms, EventBridge; completed CloudFormation IaC fundamentals: templates, stacks, change sets.", 6.0),
            ("AWS Lambda & Serverless Architecture", "Deep dive into Lambda execution model, memory/CPU allocation, cold starts, triggers, layers, concurrency, VPC configuration, CloudWatch logging.", 6.0),
        ]),
        ("Week 3", "March 30, 2026 to April 03, 2026", [
            ("IISS-435: CTI CloudWatch Metrics & Dashboard", "Added CloudWatch metrics instrumentation for CTI pipeline; created Pipeline Health Dashboard; refactored metrics into dedicated module; added unit tests; repository hygiene (.gitignore, pycache cleanup).", 7.0),
            ("IISS-435: Technical Dashboard with Log Insights", "Added CloudWatch Logs Insights widget for error pattern extraction; configured time ranges and query syntax; documented query setup with screenshots.", 7.0),
            ("IISS-435: Testing & Code Quality", "Added unit tests for Logs Insights queries and CFN templates; refactored imports; added type hints; ran full test suite (262 tests passing); prepared PR documentation.", 6.0),
        ]),
        ("Week 4", "April 06, 2026 to April 10, 2026", [
            ("IISS-435: Merge & IISS-455: Lambda Dashboard", "Merged IISS-435 to release/SRE; created IA-Lambda-Monitoring-Dashboard with modular YAML widgets: invocations, errors, throttles, duration (Avg/Max/P99), cold starts, concurrency, memory.", 7.0),
            ("IISS-455: Dashboard Testing & Refinement", "Added 21 unit tests; fixed text widget markdown validation; resolved circular dependencies; implemented filter propagation across widgets.", 7.0),
            ("IISS-461: Confluence Lambda Inventory", "Published Lambda inventory page covering 51 functions with trigger mappings, memory configs, timeout settings, budget code allocations; updated team runbook.", 6.0),
        ]),
    ]

    # Phase 2: IA Monitoring Platform & Grafana Foundation (Weeks 5-8)
    p2 = "Phase 2: IA Monitoring Platform & Grafana Foundation"
    p2_weeks = [
        ("Week 5", "April 12, 2026 to April 18, 2026", [
            ("Training Week KT", "Full-week knowledge transfer: RPA support (Horace), CitcoWorks/Event Store (Bhanu), Meridian architecture, Aexeo Treasury platform; observed Apr 17 Meridian incident firsthand.", 20.0),
            ("IISS-469: Dashboard Improvements Implementation", "Added cfsbpm/citcoworks/meridian tag dimensions, log errors widget, CSV/Excel export, subscription filter architecture documentation.", 10.0),
        ]),
        ("Week 6", "April 19, 2026 to April 25, 2026", [
            ("IISS-469: Completed & IISS-487 Created", "Finalized IISS-469; created IISS-487 Grafana story; wrote full spec for 14-row dashboard; created IISS-482/483/484/485/486 board.", 15.0),
            ("IISS-482: EC2/ECS/EKS API Endpoints", "Added EC2, ECS, EKS resource discovery endpoints to resources_monitoring_api; consolidated under /api/v1/resources/.", 10.0),
        ]),
        ("Week 7", "April 26, 2026 to May 02, 2026", [
            ("IISS-484: ECS Monitoring Dashboard", "Built ia_ecs_monitoring_dashboard package — dashboards, widgets, tests, CFN, export; Standard Container Insights recommended at $10.44/month.", 15.0),
            ("IISS-485: EKS Monitoring Dashboard", "Completed EKS monitoring dashboard with control plane metrics; scope change to AUTOMATIONHUB (1 idle cluster).", 10.0),
            ("IISS-483: EC2 Gap Analysis", "Scanned 83 EC2 instances; discovered BudgetCode=CFS/RPA tag mismatch on rpacfs1; implemented AppName fallback pattern.", 5.0),
        ]),
        ("Week 8", "May 03, 2026 to May 09, 2026", [
            ("RPA Support Rotation #1", "Week 8 on-call support shift: monitored VPL queue, Corporate Actions, BPM/UiPath Orchestrator health; handled service desk escalations.", 15.0),
            ("IISS-504/505/507/508/510 Setup", "Created JIRA links for AUTOMATIONHUB/MERIDIAN/CITCOWORKS registry extensions; added dynamic tag discovery with budget_code filtering; scaffolded ia-it-sre-infrastructure-monitoring-amg repo.", 15.0),
        ]),
    ]

    # Phase 3: Grafana AMG Dashboard Intensive Build (Weeks 9-12)
    p3 = "Phase 3: Grafana AMG Dashboard Intensive Build (IISS-487)"
    p3_weeks = [
        ("Week 9", "May 10, 2026 to May 16, 2026", [
            ("IISS-487: Infrastructure Deployment (May 11)", "Deployed 4 CloudFormation stacks; provisioned Grafana AMG workspace; 16-role IAM agent system; enabled Container Insights on 5/6 Meridian clusters; 30+ hours this week.", 30.0),
            ("IISS-487: Grafana Upgrade & Core Panels", "Grafana 10.4→12.4 upgrade mid-development; Lambda/ECS panels with Metrics Insights SQL migration; $platform variable; SQS 49 tests; automation pipeline.", 14.5),
        ]),
        ("Week 10", "May 17, 2026 to May 23, 2026", [
            ("IISS-487: MSK, DocumentDB, Neptune, OpenSearch, RDS Rows", "Implemented MSK consumer lag panels, DocumentDB/Neptune/OpenSearch SQL migration, RDS row; noData standardization; 28.5h this week.", 20.0),
            ("IISS-487: Secrets Manager 64KB Limit → S3 Migration", "Hit Secrets Manager 64KB limit at 14,720 lines of YAML; agentic refactor to per-row YAML files; Lambda provisioner assembly via S3; S3 migration complete.", 14.5),
        ]),
        ("Week 11", "May 24, 2026 to May 30, 2026", [
            ("IISS-487: Redis Row, Health Panels, SNS Alarms", "Redis row (11 panels); DocumentDB/Neptune/OpenSearch/RDS health stats; Performance row; SNS setup (3 topics); 17 alarms documented; 8 composite alarms; Grafana alerting.", 35.0),
        ]),
        ("Week 12", "May 31, 2026 to June 06, 2026", [
            ("RPA Support Rotation #2", "Week 12 on-call support: FX Closeout queue, MESO retriggering, Two Sigma wire, SD ticket management; minimal IISS-487 work.", 20.0),
            ("IISS-538: MESO Autoscale Hotfix", "Investigated ia_meso_process ECS CPU/memory autoscale failure; missing step-scaling policy; corrected ECS autoscaling configuration.", 10.0),
        ]),
    ]

    # Phase 4: Dashboard Completion, Inventory API & Refinements (Weeks 13-16)
    p4 = "Phase 4: Dashboard Completion, Inventory API & Refinements"
    p4_weeks = [
        ("Week 13", "June 07, 2026 to June 13, 2026", [
            ("IISS-706: CAIS Deadline Hotfix (7h)", "Production incident: CAIS Deadline SpnegoError from empty UCM credentials post-Secrets Manager rotation; root cause analysis; fail-fast validation in constants.py and pysmb_helper.py; 14 unit tests added.", 10.0),
            ("IISS-487: EC2 Row & Per-Panel Folder Migration", "EC2 instance mapper Lambda; EC2 monitoring row; per-panel folder extraction (357 tests passing); S3 template staging fix; 19h total this week.", 20.0),
            ("IISS-507: ia-sre-resources-inventory Scaffolded (2.5h)", "Scaffolded Flask async REST API for IA resource discovery; discoverer registry pattern; 3 concrete + 7 stub discoverers; parent of IISS-508/509.", 5.0),
            ("IISS-482: SQS Feature (5.5h)", "Registry-based SQS monitoring with 3-tier fallback (API→S3→local file); 960 automated tests.", 5.0),
        ]),
        ("Week 14", "June 14, 2026 to June 20, 2026", [
            ("IISS-487: Dashboard Polish & Final Deployment (v728)", "Deep-links for 9 service rows; resource tables with AWS Console links; ECS legend fixes; DocumentDB/RDS/Redis/OpenSearch restructure; final deployment v728; 140h total reached.", 25.0),
            ("IISS-482: Final — EC2/ECS/EKS/Lambda dashboards live", "IISS-482 closed at 11h total; SQS monitoring, EC2/ECS/EKS/Lambda dashboards all live in ia-resources-monitoring repo.", 5.0),
        ]),
        ("Week 15", "June 21, 2026 to June 27, 2026", [
            ("IISS-487: Post-Delivery Refinements", "MSK deep-links, consumer lag by topic/group panels; EC2 restructure with 3 sub-rows; 6 new resource mapper Lambdas; MSK cluster ARN variable; dashboard variable reorder.", 15.0),
            ("IISS-507/508: Inventory API Development", "Lambda discoverers for all 5 budget codes (119 functions confirmed); ECS discoverers (22 clusters, CITCOWORKS/MERIDIAN two-stage AppName filter); EC2 discoverers (83 instances).", 15.0),
        ]),
        ("Week 16", "June 28, 2026 to July 04, 2026", [
            ("IISS-741: MESO Month-End Stuck Tasks (Critical)", "INNOCAP/SAMLMOS tasks stuck; manual retrigger after admin access granted; resolved without data loss.", 5.0),
            ("IISS-507/508: Test Suite Milestone", "562 automated tests achieving 99% code coverage; Hypothesis property-based tests for tag-parsing; integration tests for all REST endpoints.", 20.0),
            ("IISS-487: Log Group Observability Research", "Mapped 3,423 CloudWatch log groups to 7 platforms (748 matched); drafted 4-part solution (IISS-845); created IISS-837-844 X-Ray sub-tasks.", 10.0),
        ]),
    ]

    for phase_name, weeks in [(p1, p1_weeks), (p2, p2_weeks), (p3, p3_weeks), (p4, p4_weeks)]:
        for wk, dates, tasks in weeks:
            for task_name, desc, hrs in tasks:
                data.append({
                    "phase": phase_name,
                    "week": wk,
                    "dates": dates,
                    "task": task_name,
                    "description": desc,
                    "hours": hrs,
                })
    return data


def get_internship_data() -> list[dict]:
    """
    Real JIRA-mapped work log data for the 900-hour Full-Time Internship (24 Weeks).
    Covers all phases from onboarding through Dynatrace-equivalent observability
    platform delivery, inventory API, ML/LLM work (IISS-824), and X-Ray tracing specs.
    """
    data = []

    # Phase 1: Foundation & SRE Platform Discovery (Weeks 1-6)
    p1 = "Phase 1: Foundation & SRE Platform Discovery"
    p1_weeks = [
        ("Week 1", "March 15, 2026 to March 21, 2026", [
            ("Environment Setup & Onboarding", "Day-1 orientation; access tickets for AWS/JIRA/Confluence/CodeCommit; AWS CLI and SSO setup; Amazon Q and VSCode setup.", 37.5),
        ]),
        ("Week 2", "March 22, 2026 to March 28, 2026", [
            ("IISS-435: RPACFS1 CloudWatch Health Dashboard", "Designed and deployed CloudWatch pipeline health dashboard with CTI metrics, Logs Insights widget, Lambda error investigation, unit tests (RPACFS1 automation repo).", 37.5),
        ]),
        ("Week 3", "March 29, 2026 to April 04, 2026", [
            ("IISS-435 Completion & IISS-455/461 Start", "Completed RPACFS1 dashboard (262 tests); created IISS-461 Lambda inventory subtask; designed CFN dashboard structure for rpacfs1/IA-BPO (51 functions).", 37.5),
        ]),
        ("Week 4", "April 05, 2026 to April 11, 2026", [
            ("IISS-455/461: Lambda Dashboard & Inventory", "Completed Lambda monitoring CloudWatch dashboard (2h JIRA); published Confluence Lambda inventory page (IISS-461); researched IISS-469 Top-K limitations.", 37.5),
        ]),
        ("Week 5", "April 12, 2026 to April 18, 2026", [
            ("Training Week & IISS-469", "Full-week KT sessions (Horace: RPA/BPM/UiPath; Bhanu: CitcoWorks/Event Store; Meridian; Aexeo); observed Apr 17 Meridian incident; implemented IISS-469 dashboard improvements.", 37.5),
        ]),
        ("Week 6", "April 19, 2026 to April 25, 2026", [
            ("IISS-469 Done; IISS-487 Created; IISS-482 Board Setup", "Closed IISS-469; created IISS-487 Grafana story with full 14-row spec; created IISS-482/483/484/485/486; added EC2/ECS/EKS API endpoints; migrated packages to ia-resources-monitoring repo.", 37.5),
        ]),
    ]

    # Phase 2: IA Monitoring Platform & Grafana Infrastructure (Weeks 7-12)
    p2 = "Phase 2: IA Monitoring Platform & Grafana Infrastructure"
    p2_weeks = [
        ("Week 7", "April 26, 2026 to May 02, 2026", [
            ("IISS-484/485/483: ECS/EKS/EC2 Dashboards", "Built ECS monitoring dashboard (Container Insights cost analysis: Standard CI recommended at $10.44/mo); EKS dashboard (AUTOMATIONHUB scope); EC2 gap analysis (83 instances, AppName fallback pattern); CWAgent cost analysis.", 37.5),
        ]),
        ("Week 8", "May 03, 2026 to May 09, 2026", [
            ("RPA Support Rotation #1 & IISS-487 Scaffolding", "Week 8 on-call: VPL queue, Corporate Actions, BPM/UiPath Orchestrator; IISS-504/505/507/508/510 created; AUTOMATIONHUB/CITCOWORKS registry extensions; ia-it-sre-infrastructure-monitoring-amg scaffolded; IISS-487 elevated to Critical.", 37.5),
        ]),
        ("Week 9", "May 10, 2026 to May 16, 2026", [
            ("IISS-487: Infrastructure Deployment & Core Dashboard Build", "May 11: 4 CFN stacks deployed; Grafana AMG workspace live; 16-role IAM system; Container Insights on 5/6 Meridian clusters. May 13: Grafana 10.4→12.4 upgrade. Lambda/ECS/SQS panels with Metrics Insights SQL; automation pipeline.", 37.5),
        ]),
        ("Week 10", "May 17, 2026 to May 23, 2026", [
            ("IISS-487: MSK, DocumentDB, Neptune, OpenSearch, RDS + S3 Migration", "MSK consumer lag/broker panels; DocumentDB/Neptune/OpenSearch/RDS SQL migration; Secrets Manager 64KB limit hit at 14,720 YAML lines → migrated to S3 assembly; Health Overview breakthrough.", 37.5),
        ]),
        ("Week 11", "May 24, 2026 to May 30, 2026", [
            ("IISS-487: Redis, Alarms, SNS, Composite Alarms", "Redis row (11 panels); health stat panels for all database services; Performance row; SNS 3-topic setup; 17 CloudWatch alarms documented; Re-Notifier Lambda; 8 composite alarms; Grafana alerting configured.", 37.5),
        ]),
        ("Week 12", "May 31, 2026 to June 06, 2026", [
            ("RPA Support Rotation #2 & IISS-538 Hotfix", "Week 12 support: FX Closeout, MESO, Two Sigma wire, SD tickets. IISS-538: investigated and fixed MESO ECS autoscale policy gap. Continued alarm tuning on IISS-487.", 37.5),
        ]),
    ]

    # Phase 3: Dashboard Completion, Hotfixes & Inventory API (Weeks 13-18)
    p3 = "Phase 3: Dashboard Completion, Hotfixes & Inventory API"
    p3_weeks = [
        ("Week 13", "June 07, 2026 to June 13, 2026", [
            ("IISS-706: CAIS Hotfix (7h) + IISS-487 EC2 Row + IISS-507 Scaffold", "CAIS Deadline SpnegoError root cause analysis; fail-fast credential validation (14 unit tests); EC2 instance mapper Lambda; per-panel folder migration (357 tests); IISS-507 ia-sre-resources-inventory scaffolded (2.5h); IISS-482 SQS registry (960 tests).", 37.5),
        ]),
        ("Week 14", "June 14, 2026 to June 20, 2026", [
            ("IISS-487: Final Deployment v728 (140h total) + IISS-482 Closed", "Deep-links for 9 service rows; resource tables; ECS legend fixes; DocumentDB/RDS/Redis/OpenSearch restructure; final deployment v728; all 14 rows / 110+ panels / 38 alarms live. IISS-482 final at 11h.", 37.5),
        ]),
        ("Week 15", "June 21, 2026 to June 27, 2026", [
            ("IISS-487: MSK/EC2 Refinements + IISS-507/508 Lambda Discoverers", "MSK consumer lag by topic/group; EC2 3-sub-row restructure; 6 resource mapper Lambdas. IISS-507: Lambda discoverers for all 5 budget codes (119 functions confirmed); Pydantic response models.", 37.5),
        ]),
        ("Week 16", "June 28, 2026 to July 04, 2026", [
            ("IISS-741: MESO Critical + IISS-507/508 ECS Discoverers + Log Group Research", "IISS-741: MESO month-end stuck tasks (Critical) — retriggered INNOCAP/SAMLMOS. ECS discoverers (22 clusters, CITCOWORKS/MERIDIAN two-stage AppName filter). Log group observability research (3,423 groups mapped); IISS-845/837-844 created.", 37.5),
        ]),
        ("Week 17", "July 05, 2026 to July 11, 2026", [
            ("IISS-753: VPL Selector Failure + IISS-507 EC2 Discoverers + X-Ray Specs", "IISS-753: VPL IPV UI selector investigation (16h estimate). EC2 discoverers for 83 instances. X-Ray tracing specs written for Lambda/ECS/EKS/API Gateway/SQS/MSK/EC2 (IISS-837-844). 562-test / 99% coverage milestone.", 37.5),
        ]),
        ("Week 18", "July 12, 2026 to July 18, 2026", [
            ("IISS-487: Log Group Utilities + Structured Logging Guide", "Implemented create_saved_queries.py (30 queries × 7 platforms); log_groups.py URL utility; Grafana CloudWatch Logs panel (Row 17); structured logging comparison guide; dry-run validation.", 37.5),
        ]),
    ]

    # Phase 4: ML/LLM Work, X-Ray Specs, RPA Support & Report (Weeks 19-24)
    p4 = "Phase 4: ML/LLM Work, Support Operations & Report Writing"
    p4_weeks = [
        ("Week 19", "July 19, 2026 to July 25, 2026", [
            ("IISS-487: Saved Queries + Log Group Observability PR", "Implemented 30 CloudWatch Logs Insights saved queries; log group URL encoding utility; feature PR merged (feature/IISS-487-alarms-notifications into release); SRE Observability Platform v2.19.9 released.", 37.5),
        ]),
        ("Week 20", "July 26, 2026 to August 01, 2026", [
            ("RPA Support Rotation #4 + IISS-838-844: X-Ray Specs", "Week 20 support: FX Closeout (PICTET_RPA), TUDOR3/MESO SD tickets, Auto Rec Download update. IISS-838-844: wrote 7 X-Ray tracing feature specs in ia_meso_process repo (Lambda Powertools, ECS ADOT, EKS DaemonSet, API Gateway, SQS, MSK, EC2).", 37.5),
        ]),
        ("Week 21", "August 02, 2026 to August 08, 2026", [
            ("IISS-824: ML-RPA-Status LLM Agent Improvements", "Reviewed ml-rpa-status-llm-agent and core-smart-rpa-llm-ecr-image repos; fixed 11 critical bugs (OOM Lambda, Athena SSE, Databricks validation, SSL, idempotent KB sync); 194 unit tests (99% coverage); split 1140-line function.py into 8 modules; structlog migration; CI quality gates.", 37.5),
        ]),
        ("Week 22", "August 09, 2026 to August 15, 2026", [
            ("IISS-487: AMG Repo Cleanup + Report Writing", "Renamed repo to ia-it-sre-infrastructure-monitoring-amg; deleted mapper stack; cleaned .env structure; updated README alerting section (38 alarms, 3 lambdas). LaTeX report: methods, IaC, SRE methodology sections drafted.", 37.5),
        ]),
        ("Week 23", "August 16, 2026 to August 22, 2026", [
            ("IISS-876: VPL GTL Pricing + Report Completion", "IISS-876: VPL Pricing GTL incorrect booking root cause analysis and fix; business team NAV reconciliation. LaTeX report: results chapter, all chapter completion, build pipeline validation.", 37.5),
        ]),
        ("Week 24", "August 23, 2026 to August 29, 2026", [
            ("Final Report, KT & Project Handover", "Finalized LaTeX report PDF; converted to DOCX; generated 900-hour work logs; completed KT documentation with Horace and Kri; Mitacs BSI renewal (Sept–Dec 2026) confirmed; project handover.", 37.5),
        ]),
    ]

    for phase_name, weeks in [(p1, p1_weeks), (p2, p2_weeks), (p3, p3_weeks), (p4, p4_weeks)]:
        for wk, dates, tasks in weeks:
            for task_name, desc, hrs in tasks:
                data.append({
                    "phase": phase_name,
                    "week": wk,
                    "dates": dates,
                    "task": task_name,
                    "description": desc,
                    "hours": hrs,
                })
    return data


# -------------------------------------------------------------------------
# EXCEL GENERATOR
# -------------------------------------------------------------------------

def write_data_to_excel(data: list[dict], title: str, subtitle: str, out_path: Path) -> None:
    """Generate and format a beautiful work log sheet with merged cells and professional styling."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Activity Logs"
    
    # Enable grid lines explicitly
    ws.views.sheetView[0].showGridLines = True
    
    # 1. Write Header Info
    ws.cell(row=1, column=1, value=title).font = TITLE_FONT
    ws.cell(row=2, column=1, value=subtitle).font = META_FONT
    ws.row_dimensions[1].height = 25
    ws.row_dimensions[2].height = 20
    
    # Empty Row
    ws.row_dimensions[3].height = 10
    
    # 2. Write Table Headers
    headers = ["Phases", "Week", "Dates", "Task", "Description", "Hours", "Weekly Hours"]
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=4, column=col_idx, value=header)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = ALIGN_CENTER
        cell.border = DATA_BORDER
    ws.row_dimensions[4].height = 28
    
    # 3. Write Data Rows
    current_row = 5
    week_groups = {}  # week_num -> list of rows
    
    for item in data:
        ws.cell(row=current_row, column=1, value=item["phase"]).alignment = ALIGN_CENTER
        ws.cell(row=current_row, column=2, value=item["week"]).alignment = ALIGN_CENTER
        ws.cell(row=current_row, column=3, value=item["dates"]).alignment = ALIGN_CENTER
        ws.cell(row=current_row, column=4, value=item["task"]).alignment = ALIGN_LEFT
        ws.cell(row=current_row, column=5, value=item["description"]).alignment = ALIGN_LEFT
        ws.cell(row=current_row, column=6, value=item["hours"]).alignment = ALIGN_CENTER
        
        # Apply fonts and borders to data cells
        for c in range(1, 8):
            cell = ws.cell(row=current_row, column=c)
            cell.font = DATA_FONT
            cell.border = DATA_BORDER
            
        wk = item["week"]
        if wk not in week_groups:
            week_groups[wk] = []
        week_groups[wk].append(current_row)
        current_row += 1
        
    # 4. Process Weekly Hours and Merging
    total_hours_sum = 0
    is_alt_week = False
    
    for wk, rows in week_groups.items():
        start_row = rows[0]
        end_row = rows[-1]
        
        # Calculate sum for this week
        weekly_sum = sum(ws.cell(row=r, column=6).value for r in rows)
        total_hours_sum += weekly_sum
        
        # Write weekly sum in the top-left cell of the merged column
        sum_cell = ws.cell(row=start_row, column=7, value=weekly_sum)
        sum_cell.font = BOLD_DATA_FONT
        sum_cell.alignment = ALIGN_CENTER
        
        # Apply alternating background color for this week's rows
        week_fill = PatternFill(fill_type="solid", start_color=LIGHT_GRAY, end_color=LIGHT_GRAY) if is_alt_week else None
        
        for r in rows:
            ws.row_dimensions[r].height = 42 # generous row height for long descriptions
            if week_fill:
                for c in range(1, 8):
                    ws.cell(row=r, column=c).fill = week_fill
                    
        is_alt_week = not is_alt_week
        
        # Perform merges if more than 1 row in the week
        if len(rows) > 1:
            ws.merge_cells(start_row=start_row, start_column=1, end_row=end_row, end_column=1)
            ws.merge_cells(start_row=start_row, start_column=2, end_row=end_row, end_column=2)
            ws.merge_cells(start_row=start_row, start_column=3, end_row=end_row, end_column=3)
            ws.merge_cells(start_row=start_row, start_column=7, end_row=end_row, end_column=7)
            
    # 5. Write Total Row
    total_row = current_row
    ws.row_dimensions[total_row].height = 25
    
    # Merge and style total row
    ws.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=5)
    total_label_cell = ws.cell(row=total_row, column=1, value="TOTAL LOGGED HOURS")
    total_label_cell.font = TOTAL_FONT
    total_label_cell.alignment = Alignment(horizontal="right", vertical="center")
    
    total_val_cell = ws.cell(row=total_row, column=6, value=total_hours_sum)
    total_val_cell.font = TOTAL_FONT
    total_val_cell.alignment = ALIGN_CENTER
    
    # Format total cell in weekly hours column
    total_week_cell = ws.cell(row=total_row, column=7, value=total_hours_sum)
    total_week_cell.font = TOTAL_FONT
    total_week_cell.alignment = ALIGN_CENTER
    
    # Apply borders to total row
    double_bottom_border = Border(
        left=THIN_SIDE, right=THIN_SIDE,
        top=THIN_SIDE,
        bottom=Side(style="double", color=SMU_MAROON)
    )
    for c in range(1, 8):
        cell = ws.cell(row=total_row, column=c)
        cell.border = double_bottom_border
        
    # 6. Column Widths
    # Define widths for columns
    widths = {
        1: 28,  # Phase
        2: 12,  # Week
        3: 26,  # Dates
        4: 30,  # Task
        5: 55,  # Description
        6: 10,  # Hours
        7: 15   # Weekly Hours
    }
    for col_idx, w in widths.items():
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = w
        
    # 7. Print page setups for clean PDF output
    ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    
    # Save Workbook
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    logger.info("excel_saved", path=str(out_path), rows=current_row, total_hours=total_hours_sum)


# -------------------------------------------------------------------------
# PDF CONVERSION SERVICE
# -------------------------------------------------------------------------

def convert_xlsx_to_pdf(xlsx_path: Path, output_pdf: Path) -> bool:
    """Use headless LibreOffice/soffice to convert generated Excel file into PDF.

    Tries 'libreoffice' first (Linux/Mac), then 'soffice' (Windows) as fallback.
    Returns False gracefully if neither is available — the xlsx artifact is still usable.
    """
    if not xlsx_path.exists():
        logger.error("xlsx_file_not_found", path=str(xlsx_path))
        return False

    logger.info("converting_xlsx_to_pdf_via_libreoffice", src=str(xlsx_path), dest=str(output_pdf))

    # Try both common executable names
    for exe in ("libreoffice", "soffice"):
        cmd = [
            exe,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_pdf.parent),
            str(xlsx_path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                # LibreOffice outputs PDF with the same basename in the output directory
                tmp_pdf = output_pdf.parent / (xlsx_path.stem + ".pdf")
                if tmp_pdf.exists() and tmp_pdf != output_pdf:
                    shutil.move(tmp_pdf, output_pdf)
                if output_pdf.exists():
                    logger.info("xlsx_pdf_conversion_success", pdf=output_pdf.name, size_bytes=output_pdf.stat().st_size)
                    return True
            else:
                logger.warning("libreoffice_conversion_failed", exe=exe, exit_code=res.returncode, stderr=res.stderr[:200])
        except FileNotFoundError:
            logger.warning("libreoffice_not_found", exe=exe)
        except Exception as e:
            logger.error("xlsx_pdf_conversion_exception", exe=exe, error=str(e))

    logger.warning(
        "xlsx_pdf_skipped",
        reason="LibreOffice/soffice not available — xlsx saved but PDF not generated. "
               "Open the xlsx in Excel and print/export to PDF manually.",
        xlsx=str(xlsx_path),
    )
    return False


# -------------------------------------------------------------------------
# CORE PIPELINE RUNNER
# -------------------------------------------------------------------------

def generate_all_logs(output_dir: Path, active_type: str = "major_project") -> None:
    """
    Generate both Major Project and Internship logs (xlsx + pdf).
    Syncs the active type to final WorkLogs.xlsx and WorkLogs.pdf in output_dir.
    """
    # 1. Output file definitions
    mp_xlsx = output_dir / "WorkLogs_MajorProject.xlsx"
    mp_pdf = output_dir / "WorkLogs_MajorProject.pdf"
    
    int_xlsx = output_dir / "WorkLogs_Internship.xlsx"
    int_pdf = output_dir / "WorkLogs_Internship.pdf"
    
    final_xlsx = output_dir / "WorkLogs.xlsx"
    final_pdf = output_dir / "WorkLogs.pdf"
    
    # 2. Generate Major Project logs
    logger.info("generating_major_project_logs")
    mp_data = get_major_project_data()
    write_data_to_excel(
        data=mp_data,
        title="SMU MCDA Major Project Activity Logs",
        subtitle="Student: Bhavik Kantilal Bhagat (ID: A00494758) | Course: MCDA 5585 & 5586 | Duration: 16 Weeks",
        out_path=mp_xlsx
    )
    convert_xlsx_to_pdf(mp_xlsx, mp_pdf)
    
    # 3. Generate Internship logs
    logger.info("generating_internship_logs")
    int_data = get_internship_data()
    write_data_to_excel(
        data=int_data,
        title="Citco Business Strategy Internship Work Logs",
        subtitle="Student: Bhavik Kantilal Bhagat (ID: A00494758) | Course: MCDA 5587 & 5588 | Duration: 24 Weeks",
        out_path=int_xlsx
    )
    convert_xlsx_to_pdf(int_xlsx, int_pdf)
    
    # 4. Copy active to final
    if active_type == "major_project":
        active_xlsx_src = mp_xlsx
        active_pdf_src = mp_pdf
    elif active_type == "internship":
        active_xlsx_src = int_xlsx
        active_pdf_src = int_pdf
    else:
        raise ValueError(f"Unknown active_type: {active_type}")
        
    shutil.copy(active_xlsx_src, final_xlsx)
    logger.info("active_xlsx_synchronized", type=active_type, xlsx=final_xlsx.name)

    if active_pdf_src.exists():
        shutil.copy(active_pdf_src, final_pdf)
        logger.info("active_pdf_synchronized", type=active_type, pdf=final_pdf.name)
    else:
        logger.warning(
            "active_pdf_not_available",
            reason="LibreOffice conversion was skipped — WorkLogs.pdf not generated. "
                   "Export WorkLogs.xlsx to PDF manually.",
            xlsx=str(active_xlsx_src),
        )
