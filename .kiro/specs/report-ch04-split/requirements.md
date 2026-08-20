# Requirements: Split ch04 into Neeyati-aligned chapters

## Context

Neeyati's report (the MCDA reference report) separates project content into
distinct chapters:
- Ch5: Project Overview (~2pp)
- Ch6: Project Goals (~2pp)

Your current `new_ch04_project.tex` (~477 lines, ~8.7pp) contains both of these
plus Deliverables/Technical Scope and Acceptance Criteria — all in one chapter.
This spec defines the split.

## Current State

`new_ch04_project.tex` contains these `\section` blocks in order:

1. `\section{Project Background and the Motivating Incident}` (~lines 18–77)
   - Pre-Internship Monitoring Posture
   - CAIS-Pricing Silent Outage (Jan--Feb 2026)
   - The Meridian Incident (Apr~2026)
   - From Incident to Programme

2. `\section{Project Overview}` (~lines 78–226)
   - Work Stream 1: CloudWatch Dashboards
   - Work Stream 2: Grafana AMG
   - Work Stream 3: Inventory API
   - Work Stream 4: RPA Production Support

3. `\section{Project Goals}` (~lines 227–273)

4. `\section{Deliverables and Technical Scope}` (~lines 274–392)
   - Centralized Grafana SRE Dashboard (IISS-487)
   - IA Infrastructure Monitoring Platform (IISS-435/455/461/469/482--486)
   - IA Infrastructure Inventory API (IISS-507--510)

5. `\section{Acceptance Criteria}` (~lines 393–480)
   - SRE Observability Platform
   - IA Infrastructure Monitoring Platform
   - IA Infrastructure Inventory API
   - RPA Production Support

`main.tex` currently inputs chapters in this order:
```
new_ch01_about_citco
new_ch02_executive_summary
new_ch03_tools
new_ch04_project        ← split target
new_ch05_learning_goals
new_ch06_methodologies
new_ch07_implementation
new_ch08_weekly_breakdown
new_ch09_conclusions
new_ch10_achievements
new_ch11_challenges
new_ch12_future_work
```

## Target State (Neeyati-aligned)

Split `new_ch04_project.tex` into **two** files, then renumber all subsequent
chapters by +1:

### new_ch04_project.tex (keep, trimmed)
**Title:** `Project Overview`
**Contents:** Sections 1 + 2 only (Background + Overview work streams)
- §4.1 Project Background and the Motivating Incident (4 subsections)
- §4.2 Project Overview (4 work stream subsections)
**Target ~3pp**

### new_ch05_project_goals.tex (new)
**Title:** `Project Goals \& Deliverables`
**Contents:** Sections 3 + 4 + 5 (Goals + Technical Scope + Acceptance Criteria)
- §5.1 Project Goals (bullet list of objectives)
- §5.2 Deliverables and Technical Scope (3 subsections)
- §5.3 Acceptance Criteria (4 subsections)
**Target ~5pp**

### Renumber all subsequent files (+1)
| Old filename | New filename | Old title | New title |
|---|---|---|---|
| new_ch05_learning_goals.tex | new_ch06_learning_goals.tex | Learning Goals | Learning Goals |
| new_ch06_methodologies.tex | new_ch07_methodologies.tex | Methodologies & Requirements | Methodologies & Requirements |
| new_ch07_implementation.tex | new_ch08_implementation.tex | Implementation & Architecture | Implementation & Architecture |
| new_ch08_weekly_breakdown.tex | new_ch09_weekly_breakdown.tex | Weekly Breakdown | Weekly Breakdown |
| new_ch09_conclusions.tex | new_ch10_conclusions.tex | Conclusions | Conclusions |
| new_ch10_achievements.tex | new_ch11_achievements.tex | Achievements & Business Value | Achievements & Business Value |
| new_ch11_challenges.tex | new_ch12_challenges.tex | Challenges & Mitigations | Challenges & Mitigations |
| new_ch12_future_work.tex | new_ch13_future_work.tex | Future Work | Future Work |

### Update main.tex
Replace chapter inputs in order:
```latex
\input{chapters/new_ch04_project}
\input{chapters/new_ch05_project_goals}
\input{chapters/new_ch06_learning_goals}
\input{chapters/new_ch07_methodologies}
\input{chapters/new_ch08_implementation}
\input{chapters/new_ch09_weekly_breakdown}
\input{chapters/new_ch10_conclusions}
\input{chapters/new_ch11_achievements}
\input{chapters/new_ch12_challenges}
\input{chapters/new_ch13_future_work}
```

### Update all \label and \ref cross-references
All chapters use `\label{chap:xxx}` and `\ref{chap:xxx}` — these labels do NOT
need changing because they are semantic (e.g., `chap:learning_goals`), not
number-based. Only the filenames and `\input` lines in `main.tex` change.

However, check and update any `Chapter~\ref{chap:X}` prose references that say
"Chapter 5" or "Chapter 6" explicitly as numbers (rare, but verify).

## Acceptance Criteria

- [ ] `new_ch04_project.tex` compiles with no `\section` for Goals/Scope/Criteria
- [ ] `new_ch05_project_goals.tex` exists and contains Goals + Technical Scope + Acceptance Criteria
- [ ] All 8 subsequent chapters are renamed with new numbers
- [ ] `main.tex` inputs all 13 chapters in correct order
- [ ] No orphaned `\label` or broken `\ref` cross-references
- [ ] No `\input{chapters/new_ch05_learning_goals}` remains in main.tex (old name)
- [ ] Branch: `feature/report-chapters`; merge to `release/v1.0` when complete
