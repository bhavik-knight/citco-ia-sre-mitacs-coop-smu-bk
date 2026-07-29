# 🎓 SMU MCDA Major Project Report & Submission Automation Pipeline

> **Automated PDF, DOCX, and WorkLog Generation Pipeline for Saint Mary's University MCDA 5585 / 5586 Major Internship Project Report.**

---

## 📌 Project Context & Overview

- **Student Name**: Bhavik Kantilal Bhagat (Student ID: `A00494758`)
- **Degree Program**: Master of Science in Computing and Data Analytics (MCDA)
- **University**: Department of Mathematics & Computing Science, Saint Mary's University, Halifax, NS
- **Academic Supervisor**: Dr. Pawan Lingras
- **Industry Partner**: **Citco Technology Management Canada Limited (CTM)**
- **Industry Lead / Manager**: Mr. Kishor Deotale
- **Office Location**: 5151 George St, Halifax, NS B3J 1M5
- **Funding & Award**: Mitacs Business Strategy Internship (BSI) Application `IT49539` ($150,000 Award)
- **Official Project Title**: *Intelligent Automation and Reliability Engineering for Financial Services*
- **Internship Duration & Scope**: March 15, 2026 – August 31, 2026 (Total 900 Hours)

---

## 🏛️ Report Architecture & Formatting

This report follows the formal **Neeyati Mehta benchmark structure** required by the MCDA program guidelines:

### Visual Design & Branding Tokens
- **Primary Accent Color**: Official Saint Mary's University Maroon (`#8A0027` / `RGB(138, 0, 39)`).
- **Typography**: Primary serif `Charter (bch)` paired with `Latin Modern Teletype (lmtt)` for code snippets.
- **Running Headers & Footers**: Crisp black running headers with total page numbering (`X of Y` via `LastPage`).
- **Logo Integration**: High-resolution SMU header logo configured on a single-page compact title page layout.
- **Dual-Signature Certificate**: Formatted signature blocks for Dr. Pawan Lingras and Mr. Kishor Deotale.

---

## 📁 Repository Directory Structure

```text
citco-report/
├── config/                     # Centralized Configuration Package
│   ├── __init__.py
│   └── settings.py             # Global pathlib.Path constants & build settings
├── src/                        # Python Source Package (PEP 8 Compliant)
│   └── report_pipeline/
│       ├── __init__.py
│       ├── builder.py          # Multi-pass LaTeXBuilder compilation service
│       ├── converter.py        # DocxConverter PDF-to-DOCX transformation service
│       ├── logger.py           # Structlog ISO-timestamped JSON logger
│       └── utils.py            # Subprocess & filesystem utilities
├── latex-report/               # Modular LaTeX Source Files
│   ├── includes.tex            # Centralized packages, color tokens & macro definitions
│   ├── main.tex                # Master LaTeX document
│   ├── cover_letter.tex        # SMU MCDA Formal Cover Letter & Feedback History Table
│   ├── figures/                # Visual graphics & branding assets (smu_logo.png)
│   ├── pages/                  # Front matter (title_page, certificate, abstract, acknowledgements)
│   ├── chapters/               # 10 Core Report Chapters (Introduction .. Conclusion)
│   └── appendices/             # Supplementary materials & work logs table
├── tests/                      # Automated Test Suite
│   ├── __init__.py
│   └── test_pipeline.py        # Pytest pipeline tests
├── work-logs/                  # Internship 900-Hour Activity Log Directory (.gitkeep preserved)
├── logs/                       # Application Runtime Script Execution Logs (structlog)
├── output/                     # Final 5-File Submission Bundle Target
├── pyproject.toml              # Modern Python dependency & test configuration
└── build_reports.py            # CLI Entry Point to compile and bundle reports
```

---

## 🚀 Automated Submission Pipeline

The build pipeline is automated via `build_reports.py` and produces the **strict 5-file MCDA graduation submission bundle** inside `output/`:

1. `CoverLetter.pdf`: Formal cover letter with student declaration & feedback history appendix.
2. `Project_Report.pdf`: Compiled 20-page LaTeX report with complete TOC and hyperref navigation.
3. `Project_Report.docx`: Converted, fully editable Word document version.
4. `WorkLogs.xlsx`: Detailed 900-hour weekly timesheets & task breakdown.
5. `WorkLogs.pdf`: Exported PDF copy of the timesheets.

---

## ⚡ Quickstart & Setup

### Prerequisites
- Python 3.12+
- `uv` package manager (`curl -sSf https://astral.sh/uv/install.sh | sh`)
- `pdflatex` (TeX Live / Flatpak TeX distribution)

### Installation
```bash
# Clone repository
git clone git@github.com:bhavik-knight/citco-ia-sre-mitacs-coop-smu-bk.git
cd citco-ia-sre-mitacs-coop-smu-bk

# Install dependencies using uv
uv sync
```

### Build Submission Bundle
```bash
# Execute automated build pipeline
uv run python build_reports.py
```

### Run Tests
```bash
# Run pytest test suite
uv run pytest
```

---

## 📄 License & Confidentiality

Notice: The underlying technical framework, SRE automation scripts, and financial technology operational processes documented in this report are proprietary to **Citco Technology Management Canada Limited**. Academic submission is restricted to authorized Saint Mary's University faculty and evaluators.
