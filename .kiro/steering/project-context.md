---
inclusion: always
---

# SMU MCDA Internship — Project Context

## Student & Program
- **Student**: Bhavik Kantilal Bhagat | ID: A00494758
- **Program**: MSc Computing and Data Analytics (MCDA), Saint Mary's University, Halifax NS
- **Academic Supervisor**: Dr. Pawan Lingras
- **Internship**: March 15 – August 31, 2026 | 900 total hours
- **Schedule**: Part-time Mar 15–Apr 15 (~10–20 h/wk) → Full-time Apr 15–Aug 31 (~40+ h/wk)
- **Funding**: Mitacs BSI IT49539

## Citco Team
- **Partner Org**: Citco Technology Management (CTM) / Citco (Canada) Inc.
- **Industry Supervisor (Manager)**: Kishor Deotale
- **Senior Mentors**: Ho Hoi Leung (Horace), Kristia Marie Labos (Kri)
- **Team Members (co-interns)**: Sridhar Vadla, Soundarya Venkataraman
- **CitcoWorks / Event Store KT**: Bhanu Teja Murari (BMurari@citco.com, Innovation IT, HYD1)

## Official Project Title
*Intelligent Automation and Reliability Engineering for Financial Services*

## Project Streams (Mitacs BSI Scope)
1. **SRE & Operational Observability** — SLIs/SLOs, Prometheus/Grafana, golden signals, BOT ops reliability, DR validation, performance tuning
2. **Intelligent Automation & Predictive Operations** — AI incident prediction, log anomaly detection, self-healing systems, IaC, CI/CD, policy-as-code
3. **Advanced Monitoring & Capacity Analytics** — synthetic monitoring probes, SLA tracking, predictive capacity forecasting

## Key JIRAs
- **IISS-487**: Centralized Grafana SRE Dashboard (140h, main deliverable)
- **IISS-482**: IA Resources Monitoring
- **IISS-455 / IISS-469**: CloudWatch Dashboards
- **IISS-538 / IISS-706 / IISS-741 / IISS-876**: Support shifts & follow-on work

## Submission Bundle (5 files → `output/`)
| File | Description |
|---|---|
| `output/CoverLetter.pdf` | Cover letter + feedback appendix |
| `output/Project_Report.pdf` | LaTeX compiled report (20-page benchmark) |
| `output/Project_Report.docx` | Auto-converted DOCX via pdf2docx |
| `output/WorkLogs.xlsx` | 900h weekly timesheet |
| `output/WorkLogs.pdf` | PDF export of xlsx |

Build command: `uv run python build_reports.py`

## Key Paths
- LaTeX source: `latex-report/`
- Knowledge base: `knowledge-base/`
- Work logs: `smu/work-logs/` (branch: `feature/work-logs`)
- Output: `output/`
- Build script: `build_reports.py`
- AI context: `.ai-agent/CONTEXT.md`, `.ai-agent/PROJECT_STATE.md`, `.ai-agent/TASK_LIST.md`
