"""
Centralized Configuration for SMU MCDA Major Project Pipeline.
Uses pathlib.Path for all project directory references.
"""
from pathlib import Path

# Base Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
LATEX_DIR = ROOT_DIR / "latex-report"
OUTPUT_DIR = ROOT_DIR / "output"
PAPERWORK_DIR = ROOT_DIR / "citco-internship-paperwork"
TEMPLATES_DIR = ROOT_DIR / "templates"

# LaTeX Source Files
COVER_LETTER_TEX = LATEX_DIR / "cover_letter.tex"
MAIN_REPORT_TEX = LATEX_DIR / "main.tex"

# Compiled Intermediate Artifacts
COVER_LETTER_PDF = LATEX_DIR / "cover_letter.pdf"
MAIN_REPORT_PDF = LATEX_DIR / "main.pdf"

# Submission Bundle Target Artifacts
SUBMISSION_COVER_LETTER_PDF = OUTPUT_DIR / "CoverLetter.pdf"
SUBMISSION_REPORT_PDF = OUTPUT_DIR / "Project_Report.pdf"
SUBMISSION_REPORT_DOCX = OUTPUT_DIR / "Project_Report.docx"
SUBMISSION_WORKLOGS_XLSX = OUTPUT_DIR / "WorkLogs.xlsx"
SUBMISSION_WORKLOGS_PDF = OUTPUT_DIR / "WorkLogs.pdf"
