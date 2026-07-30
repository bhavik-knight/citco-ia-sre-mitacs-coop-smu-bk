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
    """Return structured task log data for the 240-Hour Major Project (16 Weeks)."""
    data = []
    
    # Phase 1: Foundation & Requirements (Weeks 1-4)
    p1 = "Phase 1: Foundation & Requirements"
    p1_weeks = [
        ("Week 1", "March 15, 2026 to March 21, 2026", [
            ("Scoping & Workspace Configuration", "Set up the report repository, configured pyproject.toml, and established git branch policies.", 12.5),
            ("Initial Structure Setup", "Created package folders (src/report_pipeline) and drafted initial outline for 10 core chapters in LaTeX.", 1.25)
        ]),
        ("Week 2", "March 22, 2026 to March 28, 2026", [
            ("Requirements Gathering", "Documented SMU MCDA graduation process guidelines for cover letters, reports, and timesheets.", 12.5),
            ("Validation Scaffolding", "Wrote a test script to check that all mandatory LaTeX source files exist in the workspace.", 1.25)
        ]),
        ("Week 3", "March 29, 2026 to April 04, 2026", [
            ("LaTeXBuilder Development", "Developed the LaTeXBuilder class to run pdflatex from Python and capture stderr.", 12.5),
            ("Multi-pass Compilation Logic", "Programmed the builder to compile documents multiple times to resolve refs and TOC.", 1.25)
        ]),
        ("Week 4", "April 05, 2026 to April 11, 2026", [
            ("DocxConverter Development", "Integrated pdf2docx library and created converter class to convert report PDF to editable DOCX format.", 12.5),
            ("Output Synchronization", "Wrote file copying utilities in build_reports.py to sync built documents into output/.", 1.25)
        ])
    ]
    
    # Phase 2: Core Engineering & Modular Structure (Weeks 5-8)
    p2 = "Phase 2: Core Engineering & Modeling"
    p2_weeks = [
        ("Week 5", "April 12, 2026 to April 18, 2026", [
            ("Structlog Logging Service", "Integrated structlog to format all output in JSON format with ISO timestamps.", 12.5),
            ("Error Log Parsing", "Configured log capturing to parse and display compiler errors directly in pipeline output.", 1.25)
        ]),
        ("Week 6", "April 19, 2026 to April 25, 2026", [
            ("build_reports.py CLI", "Unified builder, converter, and logger under build_reports.py to allow single-command compilation.", 12.5),
            ("Log File Synchronization", "Configured pipeline to dump JSON logs to logs/build.log for tracing.", 1.25)
        ]),
        ("Week 7", "April 26, 2026 to May 02, 2026", [
            ("LaTeX Styling Configurations", "Created includes.tex containing fonts (Charter/lmtt), margin rules, and custom maroon headers.", 12.5),
            ("Cover Letter Document", "Drafted cover_letter.tex containing student declaration and feedback history table.", 1.25)
        ]),
        ("Week 8", "May 03, 2026 to May 09, 2026", [
            ("Narrative Draft Setup", "Drafted Chapter 1 (Introduction) describing project goals, and Chapter 2 (About Company) describing Citco.", 12.5),
            ("Aesthetics Compliance Review", "Verified visual styles and layout configurations against the Neeyati Mehta benchmark guidelines.", 1.25)
        ])
    ]
    
    # Phase 3: Integration & Validation (Weeks 9-12)
    p3 = "Phase 3: Integration & Validation"
    p3_weeks = [
        ("Week 9", "May 10, 2026 to May 16, 2026", [
            ("Pytest Suite Development", "Wrote unit tests in tests/test_pipeline.py to verify path existence and output directory creation.", 12.5),
            ("Conversion Testing", "Verified the pdf-to-docx converter performance on sample document formats under pytest.", 2.5)
        ]),
        ("Week 10", "May 17, 2026 to May 23, 2026", [
            ("Chapters 3-4 Drafting", "Completed Chapter 3 (Project Overview) detailing SRE scope, and Chapter 4 (Learning Goals).", 12.5),
            ("Branding Asset Integration", "Integrated high-resolution SMU logos and SRE system architecture diagrams into figures/.", 2.5)
        ]),
        ("Week 11", "May 24, 2026 to May 30, 2026", [
            ("Chapters 5-6 Drafting", "Completed Chapter 5 (Tools and Technologies) and Chapter 6 (Requirements Elicitation).", 12.5),
            ("Formatting Listings", "Styled code listings using the LaTeX listings package to display code snippets beautifully.", 2.5)
        ]),
        ("Week 12", "May 31, 2026 to June 06, 2026", [
            ("Chapters 7-8 Drafting", "Completed Chapter 7 (Methodologies) and Chapter 8 (System Architecture) with Mermaid flow diagrams.", 12.5),
            ("Table Layout Adjustments", "Formatted multi-page tables using tabularx and longtable for SRE tool reviews.", 2.5)
        ])
    ]
    
    # Phase 4: Final Evaluation & Deployment (Weeks 13-16)
    p4 = "Phase 4: Final Evaluation & Deployment"
    p4_weeks = [
        ("Week 13", "June 07, 2026 to June 13, 2026", [
            ("Chapters 9-10 Drafting", "Completed Chapter 9 (Implementation) detailing script writing, and Chapter 10 (Results Evaluation).", 12.5),
            ("Narrative Proofreading", "Corrected spelling, punctuation, and style details using language verification tools.", 5.0)
        ]),
        ("Week 14", "June 14, 2026 to June 20, 2026", [
            ("Compilation Fixes", "Fixed undefined control sequence errors in bibliography files and updated references.bib.", 12.5),
            ("DOCX Layout Verification", "Checked and adjusted paragraph margins in converted Word documents to ensure layout parity.", 5.0)
        ]),
        ("Week 15", "June 21, 2026 to June 27, 2026", [
            ("Review & Modifications", "Adjusted document text based on advisor feedback. Updated acknowledgements and certificate pages.", 12.5),
            ("Timesheet Integration", "Synchronized generated timesheet data in output/ with the LaTeX appendix summary table.", 5.0)
        ]),
        ("Week 16", "June 28, 2026 to July 04, 2026", [
            ("Final Pipeline Run", "Executed end-to-end build script to compile PDFs, convert to DOCX, and output all 5 final submission files.", 12.5),
            ("Submission Readiness Audit", "Verified output formatting, total page count (20+ pages), and metadata correctness.", 5.0)
        ])
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
                    "hours": hrs
                })
    return data


def get_internship_data() -> list[dict]:
    """Return structured task log data for the 900-Hour Full-Time Internship (24 Weeks)."""
    data = []
    
    # Phase 1: Foundation & SRE Monitoring (Weeks 1-6)
    p1 = "Phase 1: Foundation & SRE Monitoring"
    p1_weeks = [
        ("Week 1", "March 15, 2026 to March 21, 2026", [
            ("SRE Scope & Workspace Setup", "Onboarded at Citco, finalized workspace permissions, and set up local development and test environments.", 30.0),
            ("Team Coordination & Scoping", "Participated in initial sprint planning and outlined SRE scope with manager Mr. Kishor Deotale.", 7.5)
        ]),
        ("Week 2", "March 22, 2026 to March 28, 2026", [
            ("Prometheus Telemetry", "Configured Prometheus node exporters on CFS-BPM environments to collect basic system metrics (CPU, RAM).", 30.0),
            ("System Metrics Planning", "Documented telemetry endpoints and metric naming conventions for Platform SRE.", 7.5)
        ]),
        ("Week 3", "March 29, 2026 to April 04, 2026", [
            ("Queue Telemetry Setup", "Configured custom collectors for RPA work queues to monitor transaction backlogs and lock status.", 30.0),
            ("Telemetry Review Meetings", "Collaborated with RPA developers to align queue monitoring with business requirements.", 7.5)
        ]),
        ("Week 4", "April 05, 2026 to April 11, 2026", [
            ("Grafana Dashboard Design", "Designed and deployed baseline Grafana dashboards to visualize Citco Works platform health.", 30.0),
            ("Dashboard Walkthroughs", "Presented dashboard design to the operations team to collect feedback on usability.", 7.5)
        ]),
        ("Week 5", "April 12, 2026 to April 18, 2026", [
            ("Alert Tier Implementation", "Configured pager alerts, mapping critical events to SMS alerts and warnings to email notifications.", 30.0),
            ("Runbook Documentation", "Drafted standard incident response runbooks for common CFS-BPM database connection failures.", 7.5)
        ]),
        ("Week 6", "April 19, 2026 to April 25, 2026", [
            ("Resilience Testing Setup", "Wrote scripts to simulate high queue volumes and test auto-alerting mechanisms in CFS-BPM.", 30.0),
            ("Sprint 1 Retrospective", "Compiled sprint achievements, documented telemetry gaps, and prepared for Phase 2.", 7.5)
        ])
    ]
    
    # Phase 2: Queue Optimization & Intelligent BOT Management (Weeks 7-12)
    p2 = "Phase 2: Queue Optimization & BOT Management"
    p2_weeks = [
        ("Week 7", "April 26, 2026 to May 02, 2026", [
            ("Congestion Analysis", "Analyzed historical RPA logs to identify workflow congestion patterns and bottleneck locations.", 30.0),
            ("Bottleneck Review Meeting", "Reviewed workflow logs with industry supervisors to prioritize bot optimizations.", 7.5)
        ]),
        ("Week 8", "May 03, 2026 to May 09, 2026", [
            ("Backlog Detector Tool", "Wrote a Python backlog detector tool that alerts on exceeding queue depth thresholds.", 30.0),
            ("Backlog Alert Validation", "Tested backlog alerts under simulated heavy queue loads in non-production systems.", 7.5)
        ]),
        ("Week 9", "May 10, 2026 to May 16, 2026", [
            ("Throttling Mechanics", "Designed and tested throttling algorithms to slow transaction ingestion during peak database loads.", 30.0),
            ("Design Documentation", "Drafted system design document for throttling mechanisms and queue policies.", 7.5)
        ]),
        ("Week 10", "May 17, 2026 to May 23, 2026", [
            ("Auto-scaling Bot Policy", "Programmed logic to auto-scale Docker containers running bot processes based on queue backlogs.", 30.0),
            ("Infrastructure Review", "Ensured the container orchestration environment has resources to support auto-scaling.", 7.5)
        ]),
        ("Week 11", "May 24, 2026 to May 30, 2026", [
            ("Automated Bot Retries", "Implemented error classification rules to retry transient bot errors while logging permanent failures.", 30.0),
            ("Error Class Review", "Refined error categories with developers to ensure retry logic does not loop on bad data.", 7.5)
        ]),
        ("Week 12", "May 31, 2026 to June 06, 2026", [
            ("Self-healing Recovery Bot", "Built automated recovery scripts that restart crashed processes and unlock stuck transactions.", 30.0),
            ("Sprint 2 Retrospective", "Evaluated bot management and queue performance. Scheduled Phase 3 disaster recovery tasks.", 7.5)
        ])
    ]
    
    # Phase 3: Automated Service Reliability & DR (Weeks 13-18)
    p3 = "Phase 3: Automated Service Reliability & DR"
    p3_weeks = [
        ("Week 13", "June 07, 2026 to June 13, 2026", [
            ("Deployment Check Codification", "Wrote shell and Python scripts to automate deployment readiness and database health checks.", 30.0),
            ("Code Review Session", "Submitted automated deployment checking scripts for peer and supervisor code review.", 7.5)
        ]),
        ("Week 14", "June 14, 2026 to June 20, 2026", [
            ("DR Orchestration Scripts", "Developed Ansible playbooks to orchestrate automated database failovers for Citco Works.", 30.0),
            ("DR Workflow Design", "Mapped out failover sequences and dependency graphs for application components.", 7.5)
        ]),
        ("Week 15", "June 21, 2026 to June 27, 2026", [
            ("Post-Failover Health Checks", "Programmed automated endpoint validation scripts to verify application availability post-failover.", 30.0),
            ("Validation Testing", "Executed health checks under simulated partial and full platform failures.", 7.5)
        ]),
        ("Week 16", "June 28, 2026 to July 04, 2026", [
            ("CI/CD Deployment Pipelines", "Created GitHub Actions/GitLab CI pipelines to run SRE script tests and check style guidelines.", 30.0),
            ("Pipeline Integration Meeting", "Integrated SRE validation checks into core application repository workflows.", 7.5)
        ]),
        ("Week 17", "July 05, 2026 to July 11, 2026", [
            ("Policy-as-Code Compliance", "Implemented Open Policy Agent (OPA) policies to audit infrastructure configs for security compliance.", 30.0),
            ("Security Review Session", "Collaborated with the security team to align policy rules with company compliance regulations.", 7.5)
        ]),
        ("Week 18", "July 12, 2026 to July 18, 2026", [
            ("DR Failover Testing", "Conducted a successful end-to-end simulated disaster recovery drill using failover orchestration.", 30.0),
            ("Sprint 3 Retrospective", "Reviewed failover outcomes, addressed minor recovery lag bugs, and planned Phase 4 observability.", 7.5)
        ])
    ]
    
    # Phase 4: Advanced Monitoring, Observability & Analytics (Weeks 19-24)
    p4 = "Phase 4: Advanced Monitoring & Observability"
    p4_weeks = [
        ("Week 19", "July 19, 2026 to July 25, 2026", [
            ("Synthetic Probing Implementation", "Deployed synthetic HTTP/API probes to monitor endpoint response latencies globally.", 30.0),
            ("Global Probe Mapping", "Analyzed latency profiles from different network hubs to establish latency baselines.", 7.5)
        ]),
        ("Week 20", "July 26, 2026 to August 01, 2026", [
            ("SLA Tracker Development", "Developed real-time uptime calculators and integrated results into executive dashboards.", 30.0),
            ("SLA Presentation", "Walked supervisors through dashboard SLA panels to confirm calculation formulas.", 7.5)
        ]),
        ("Week 21", "August 02, 2026 to August 08, 2026", [
            ("OpenTelemetry Tracing", "Instrumented transaction-level tracing across microservices to detect database query delays.", 30.0),
            ("Trace Analysis & Debugging", "Fixed slow queries identified in distributed transactions to improve endpoint response.", 7.5)
        ]),
        ("Week 22", "August 09, 2026 to August 15, 2026", [
            ("ML Anomaly Detection", "Trained a machine learning model on CPU/memory usage profiles to flag abnormal utilization.", 30.0),
            ("Model Tuning & Testing", "Adjusted model confidence levels to minimize false alarms during normal processing peaks.", 7.5)
        ]),
        ("Week 23", "August 16, 2026 to August 22, 2026", [
            ("Capacity Forecasting Dashboard", "Built forecasting panels to model and project server storage and RAM needs for the next quarter.", 30.0),
            ("Supervisor Capacity Review", "Presented forecasting results to the SRE lead to support resource budgeting.", 7.5)
        ]),
        ("Week 24", "August 23, 2026 to August 29, 2026", [
            ("Internship Final Reporting", "Compiled all project metrics, achievements, SRE runbooks, and wrote the final report summary.", 30.0),
            ("Final Project Handover", "Completed final code handovers, presented work logs to supervisors, and closed out internship.", 7.5)
        ])
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
                    "hours": hrs
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
    """Use headless LibreOffice to convert generated Excel file into PDF."""
    if not xlsx_path.exists():
        logger.error("xlsx_file_not_found", path=str(xlsx_path))
        return False
        
    logger.info("converting_xlsx_to_pdf_via_libreoffice", src=str(xlsx_path), dest=str(output_pdf))
    try:
        # LibreOffice outputs PDF with the same basename in the output directory
        cmd = [
            "libreoffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", str(output_pdf.parent),
            str(xlsx_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            logger.error("libreoffice_conversion_failed", exit_code=res.returncode, stderr=res.stderr)
            return False
            
        # The output file name will be xlsx_path.stem + ".pdf"
        tmp_pdf = output_pdf.parent / (xlsx_path.stem + ".pdf")
        if tmp_pdf.exists() and tmp_pdf != output_pdf:
            shutil.move(tmp_pdf, output_pdf)
            
        logger.info("xlsx_pdf_conversion_success", pdf=output_pdf.name, size_bytes=output_pdf.stat().st_size)
        return True
    except Exception as e:
        logger.error("xlsx_pdf_conversion_exception", error=str(e))
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
    shutil.copy(active_pdf_src, final_pdf)
    logger.info("active_logs_synchronized", type=active_type, xlsx=final_xlsx.name, pdf=final_pdf.name)
