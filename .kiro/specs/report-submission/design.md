# Design: Report Submission — August 1, 2026

## Architecture

```
knowledge-base/          ← source material for all chapters
smu/work-logs/           ← raw daily commit-based logs → Excel
latex-report/            ← LaTeX source (10 chapters + front matter)
    └── main.tex         ← root, includes all chapters
build_reports.py         ← orchestrates: LaTeX compile → docx convert → xlsx generate
output/                  ← final 5-file submission bundle
```

## Chapter Content Mapping

| Chapter | Source Files |
|---|---|
| Ch 1: About Company | `.ai-agent/CONTEXT.md` → Citco CTM profile, team structure |
| Ch 2: Project Overview | `knowledge-base/project-context/dev_jira_summary.md`, `dev_work_timeline.md`, Mitacs BSI renewal |
| Ch 3: Learning Goals | CONTEXT.md streams, tools list, Agile/JIRA experience |
| Ch 4: Tools & Tech | `knowledge-base/infra/`, `knowledge-base/dashboard/` files, pyproject.toml |
| Ch 5: Requirements | `knowledge-base/project-context/dev_jira_summary.md`, IISS-487 scope |
| Ch 6: Methodologies | Agile/Kanban, IaC, TDD (960+ tests), design-first (.kiro specs) |
| Ch 7: Implementation | `knowledge-base/dashboard/`, `knowledge-base/hotfixes/`, IISS-487 architecture |
| Ch 8: Weekly Breakdown | `smu/work-logs/` monthly folders, git commit history |
| Ch 9: Challenges | `knowledge-base/hotfixes/`, incident reports, IISS-487 blockers |
| Ch 10: Conclusion | Deliverables summary, future scope (X-Ray, auto-healing) |

## Work Logs Pipeline

```
git log (all repos) → smu/work-logs/YYYY-MM/YYYY-MM-DD.md
                                ↓
                    build_reports.py
                                ↓
              output/WorkLogs.xlsx  +  output/WorkLogs.pdf
```

Format: Francis_Kuzhippallil sample (Week | Date | Day | Task | Hrs | Cumulative)
Branch: `feature/work-logs` — never commit to main directly

## Build Pipeline

```
uv run python build_reports.py
  1. pdflatex latex-report/main.tex → output/Project_Report.pdf
  2. pdflatex latex-report/cover_letter.tex → output/CoverLetter.pdf
  3. pdf2docx output/Project_Report.pdf → output/Project_Report.docx
  4. logs_generator.py → output/WorkLogs.xlsx
  5. LibreOffice/fallback → output/WorkLogs.pdf
```

## Hour Distribution (900h total)
| Period | Hours | Type |
|---|---|---|
| Mar 15 – Apr 14 (5 weeks, part-time) | ~75h | Onboarding, access setup, AWS learning |
| Apr 15 – Apr 20 (training week) | 40h | KT sessions (Horace, Kishor, Bhanu Teja) |
| Apr 21 – Aug 31 (19 weeks, full-time) | ~785h | Core dev, SRE, dashboards, support shifts |
