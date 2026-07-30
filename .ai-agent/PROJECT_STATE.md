# ACTIVE PROJECT STATE

- **Current Stage**: Automated Output Directory, Build System, & Multi-Option Timesheet Generator Configured
- **Root Output Directory**: `output/`
- **Build Script**: `build_reports.py` (`uv run python build_reports.py`)
- **LaTeX Root**: `latex-report/`

## Generated Output Files (`output/`):
1. `output/CoverLetter.pdf`: Compiled Cover Letter + Feedback Appendix table
2. `output/Project_Report.pdf`: Compiled LaTeX Major Project Report (20-page benchmark)
3. `output/Project_Report.docx`: Automatically generated DOCX version from PDF
4. `output/WorkLogs.xlsx`: Dynamically generated Excel timesheet (copies active `REPORT_TYPE` logs)
5. `output/WorkLogs.pdf`: Dynamically compiled PDF timesheet via LibreOffice (copies active `REPORT_TYPE` logs)
6. `output/WorkLogs_MajorProject.xlsx` & `.pdf`: Separated 240-Hour Major Project logs (16 weeks)
7. `output/WorkLogs_Internship.xlsx` & `.pdf`: Separated 900-Hour Full-Time Internship logs (24 weeks)

## Build Automation:
- Run `uv run python build_reports.py` at any time to re-compile LaTeX files, convert PDF to DOCX, generate both Major Project & Internship logs, and sync all target submission files directly into the root `output/` directory.
