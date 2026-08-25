---
inclusion: always
---

# Report Development Workflow — Phases

This steering defines the phased approach for developing the SMU MCDA Major Project Report.

## Phase Overview

```
Phase 1: Context & Setup        [COMPLETED]
    ↓
Phase 2: Report Structure       [COMPLETED]
    ↓
Phase 3: Drafting & Content     [IN PROGRESS]
    ↓
Phase 4: Compilation & Bundle   [PENDING]
```

## Phase 1: Context & Setup (Completed)

- Analyze program rules from `templates/reportWritingGraduationProcess.pdf`
- Analyze Neeyati Mehta's benchmark report for structure/formatting reference
- Establish AI context memory bank in `.ai-agent/`
- Verify toolchain: pdflatex, pandoc, pdf2docx

## Phase 2: Report Structure (Completed)

LaTeX modular structure created in `latex-report/`:

| Category | Files |
|----------|-------|
| Front matter | `pages/title_page.tex`, `certificate.tex`, `acknowledgements.tex`, `abstract.tex` |
| Chapters | `new_ch01_company.tex` through `new_ch15_future_work.tex` |
| Appendices | `appendices/work_logs.tex` |

## Phase 3: Drafting & Content (Current)

Content population tasks:
- Chapter metadata (company, supervisor, dates)
- Technical chapters (tools, methodologies, implementation)
- Weekly breakdown narrative (Weeks 1–24)
- Work logs (`WorkLogs.xlsx` with 900h + 120h = 1020h total)

### Chapter Mapping (Current Structure)

| Ch | Topic | Status |
|----|-------|--------|
| 1 | About Company & Team | Done |
| 2 | Project Overview | Done |
| 3 | Learning Goals | Done |
| 4 | Tools & Technologies | Done |
| 5 | Requirements Elicitation | Done |
| 6 | Methodologies | Done |
| 7–9 | Implementation (WS1–3) | Done |
| 10 | Implementation (WS4–6) + Design Decisions | Done |
| 11 | Weekly Breakdown | Done |
| 12 | Conclusion (per Work Stream) | Done |
| 13 | Achievements | Done |
| 14 | Challenges & Mitigation | Done |
| 15 | Future Work | Done |

## Phase 4: Compilation & Bundle (Final)

Build command: `uv run python build_reports.py`

### 5-File Submission Bundle

| # | File | Source |
|---|------|--------|
| 1 | `output/CoverLetter.pdf` | LaTeX cover letter |
| 2 | `output/Project_Report.pdf` | Main LaTeX report |
| 3 | `output/Project_Report.docx` | Auto-converted via pdf2docx |
| 4 | `output/WorkLogs.xlsx` | Excel timesheet (900h internship + 120h writing) |
| 5 | `output/WorkLogs.pdf` | PDF export of xlsx |

## LaTeX Build Path

```bash
export PATH="$PATH:/c/Users/bbhagat/scoop/apps/miktex/25.12/texmfs/install/miktex/bin/x64"
cd latex-report && pdflatex -interaction=nonstopmode main.tex
```

## Work Stream Reference

| WS# | Name | Primary Chapters |
|-----|------|------------------|
| WS1 | CloudWatch Dashboards | Ch 7 |
| WS2 | Grafana AMG Dashboards | Ch 8 |
| WS3 | Inventory API | Ch 9 |
| WS4 | RPA Support | Ch 10.1 |
| WS5 | RPA LLM Agent | Ch 10.2 |
| WS6 | UI Dashboards (Planning) | Ch 10.3 |

## Quality Checks Before Submission

- [ ] Report compiles without errors
- [ ] All chapters present in TOC
- [ ] Page count reasonable (~100 pages)
- [ ] Hours total correct (900 internship + 120 writing = 1020)
- [ ] All figures/tables referenced
- [ ] No TODO markers remaining
- [ ] Cover letter feedback appendix complete
