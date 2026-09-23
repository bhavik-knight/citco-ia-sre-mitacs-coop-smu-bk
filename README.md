# SMU MCDA Major Project Report — Bhavik Kantilal Bhagat

> LaTeX-based academic report for the Saint Mary's University MCDA 5585 / 5586 Major Internship Project, documenting a 900-hour co-op placement at Citco Technology Management (CTM), Halifax, NS.

---

## Project Context

| Field | Value |
|-------|-------|
| Student | Bhavik Kantilal Bhagat (`A00494758`) |
| Program | MSc Computing and Data Analytics (MCDA), Saint Mary's University |
| Academic Supervisor | Dr. Pawan Lingras |
| Industry Partner | Citco Technology Management (CTM), Halifax, NS |
| Industry Supervisor | Mr. Kishor Deotale |
| Project Title | *Intelligent Automation and Reliability Engineering for Financial Services* |
| Internship Period | March 15 – August 31, 2026 (900 hours) |
| Funding | Mitacs BSI IT49539 |

---

## Repository Structure

```
citco-ia-sre-mitacs-coop-smu-bk/
├── latex-report/               # LaTeX source files
│   ├── main.tex                # Master document entry point
│   ├── cover_letter.tex        # Cover letter + feedback appendix
│   ├── includes.tex            # Packages, colors, fonts, heading styles
│   ├── references.bib          # BibTeX bibliography
│   ├── pages/                  # Front matter (title, certificate, acknowledgements)
│   ├── chapters/               # 15 chapters (ch01–ch15)
│   ├── appendices/             # Appendix A (Work Logs) + Appendix B (Glossary)
│   └── figures/                # Images and diagrams
├── submission/
│   └── mentor2/                # Final 5-file submission bundle + FEEDBACK_RESPONSE.md
├── grammarly/                  # Grammarly corrections tracking
│   ├── correction.txt          # Raw corrections from peer review
│   └── corrections_table.md    # Structured corrections table with status
├── feedback/                   # Mentor feedback files
├── knowledge-base/             # Project context, hotfix notes, dashboards
├── work-logs/                  # Weekly work log markdown files
├── src/                        # Python report pipeline utilities
├── config/                     # Pipeline configuration
├── pyproject.toml              # Python project config (uv)
└── build_reports.py            # CLI build script
```

---

## Submission Bundle

The final 5-file submission bundle lives in `submission/mentor2/`:

| File | Description |
|------|-------------|
| `BhavikBhagat_A00494758_CoverLetter.pdf` | Cover letter with feedback appendix table |
| `BhavikBhagat_A00494758_MajorReport.pdf` | Main report (129 pages, LaTeX compiled) |
| `BhavikBhavat_A00494758_MajorReport.docx` | Word format (manually formatted) |
| `BhavikBhagat_A00494758_WorkLogs.xlsx` | 900-hour weekly work logs |
| `BhavikBhagat_A00494758_WorkLogs.pdf` | PDF export of work logs |

---

## Building the Report

### Prerequisites

- MiKTeX (Windows) or TeX Live (Linux/macOS) with XeLaTeX
- Calibri font installed (system font, required for XeLaTeX)
- `uv` for Python tooling

### Compile LaTeX PDF

```bash
export PATH="$PATH:/c/Users/bbhagat/scoop/apps/miktex/25.12/texmfs/install/miktex/bin/x64"
cd latex-report

# Run twice for TOC/references to resolve
xelatex -interaction=nonstopmode main.tex
biber main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### Compile Cover Letter

```bash
cd latex-report
xelatex -interaction=nonstopmode cover_letter.tex
```

---

## Report Structure

| Chapter | Title |
|---------|-------|
| 1 | About Citco |
| 2 | Executive Summary |
| 3 | Team Composition & Responsibilities |
| 4 | Tools & Technologies |
| 5 | Project Overview |
| 6 | Project Goals & Deliverables |
| 7 | Learning Goals |
| 8 | Requirements Elicitation |
| 9 | Methodologies |
| 10 | Implementation & Architecture |
| 11 | Weekly Implementation Breakdown |
| 12 | Conclusions |
| 13 | Achievements & Business Value |
| 14 | Challenges & Mitigations |
| 15 | Future Work |
| A | Appendix (Work Logs + Glossary) |

---

## Key Design Decisions

- **Font**: Calibri (via fontspec/XeLaTeX) — matches Word document formatting
- **Color**: SMU Maroon `#8A0027` for all headings, links, and labels
- **TOC depth**: Chapters and sections only (`tocdepth=1`)
- **Numbering depth**: Chapters, sections, subsections (`secnumdepth=2`); subsubsections unnumbered
- **Page numbers**: Grey `#7F7F7F` footer
- **URL color**: Standard blue hyperlinks in references

---

## License & Confidentiality

The SRE automation scripts and financial technology operational processes documented in this report are proprietary to Citco Technology Management Canada Limited. Academic submission is restricted to authorized Saint Mary's University faculty and evaluators.
