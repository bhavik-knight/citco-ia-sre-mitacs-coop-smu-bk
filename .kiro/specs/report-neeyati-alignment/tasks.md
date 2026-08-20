# Tasks: Neeyati Template Alignment

## TASK 1 — Fix ch04 opener
**File:** `latex-report/chapters/new_ch04_project.tex`
**Action:** Delete the opening paragraph (3 lines) that begins "This chapter provides
the production context...". Nothing replaces it — the `\section{Project Background}`
follows immediately and is self-explanatory.
**Verify:** File opens with `\chapter{Project Overview}` then immediately the
section/subsection structure with no intervening paragraph.

---

## TASK 2 — Fix ch05 opener
**File:** `latex-report/chapters/new_ch05_project_goals.tex`
**Action:** Replace the opening paragraph "This chapter defines the engineering
objectives..." with the personal version from design.md.
**New text:**
```
I set the following engineering objectives at the outset of the internship,
guided by the two motivating incidents and the requirements sessions with
Kishor and Kri. Each objective maps directly to one of the four work streams
described in Chapter~\ref{chap:project}.
```

---

## TASK 3 — Fix ch07 opener (pre-split)
**File:** `latex-report/chapters/new_ch07_methodologies.tex`
**Action:** Replace the long "This chapter documents..." multi-sentence opener
with the shorter personal version from design.md.
**New text:**
```
During my internship I adopted Site Reliability Engineering as the primary
methodology, applying the four golden signals framework and SLI/SLO discipline
to the observability gap exposed by the CAIS-Pricing Silent Outage and the
Meridian Incident. This chapter covers the SRE principles I operationalised,
the gap analysis that established the starting posture, and the Dynatrace
parity evaluation that framed the research question.
```

---

## TASK 4 — Fix ch09 opener (Weekly Breakdown — currently ch09, will be ch10 after split)
**File:** `latex-report/chapters/new_ch09_weekly_breakdown.tex`
**Action:** Replace the opening paragraph "This chapter provides a phase-by-phase
narrative..." with the personal version.
**New text:**
```
My internship was structured across four delivery phases spanning 24~weeks.
The following narrative covers what I built each week, what blocked or
accelerated progress, and how priorities shifted in response to production
events and emerging technical constraints.
```

---

## TASK 5 — Fix ch10 opener (Conclusions)
**File:** `latex-report/chapters/new_ch10_conclusions.tex`
**Action:** Add a personal opening paragraph before the first `\section{}`.
**New text (insert after `\label{chap:conclusions}` blank line):**
```
Throughout my internship I worked toward the technical and non-technical
goals established at the outset in consultation with Kishor Deotale and
Dr.\ Pawan Lingras. The following sections evaluate each goal against the
delivered outcomes and reflect on the broader impact of the engagement.
```

---

## TASK 6 — Fix ch11 opener (Achievements — currently ch10)
**File:** `latex-report/chapters/new_ch11_achievements.tex`
**Action:** Add a personal opening paragraph before the first `\section{}`.
**New text:**
```
Working on the IA-IT-SRE Infrastructure at Citco Technology Management,
I delivered three primary engineering work streams and contributed to
production operations across four RPA support rotations. The following
sections document the key deliverables, quantitative metrics, and
business value created during the internship.
```

---

## TASK 7 — Split ch07: Extract Requirements into new ch08

### 7a. Read ch07 methodologies
Read `new_ch07_methodologies.tex` line by line. Find:
- Start: first line of `\section{Stakeholder Identification}` (~line 300)
- End: last line before `\section{Limitations and Mitigations}` (~line 551)

### 7b. Create new_ch08_requirements_elicitation.tex
Write a new file with:
- Chapter header comment block (CHAPTER 8: REQUIREMENTS ELICITATION)
- `\chapter{Requirements Elicitation}` with `\label{chap:requirements}`
- Personal opener paragraph (see design.md)
- The extracted content (lines 300–551 from ch07)

### 7c. Trim ch07
Remove lines 300–551 from `new_ch07_methodologies.tex`.
The file should now end with `\section{Limitations and Mitigations}`.

---

## TASK 8 — Rename subsequent chapters with git mv

Run these git mv commands in `latex-report/chapters/`:
```
git mv new_ch08_implementation.tex    new_ch09_implementation.tex
git mv new_ch09_weekly_breakdown.tex  new_ch10_weekly_breakdown.tex
git mv new_ch10_conclusions.tex       new_ch11_conclusions.tex
git mv new_ch11_achievements.tex      new_ch12_achievements.tex
git mv new_ch12_challenges.tex        new_ch13_challenges.tex
git mv new_ch13_future_work.tex       new_ch14_future_work.tex
```

---

## TASK 9 — Update chapter comment headers in renamed files

For each renamed file, update the `% CHAPTER N:` comment at the top:
- new_ch09_implementation.tex   → `% CHAPTER 9: IMPLEMENTATION & ARCHITECTURE`
- new_ch10_weekly_breakdown.tex → `% CHAPTER 10: WEEKLY BREAKDOWN`
- new_ch11_conclusions.tex      → `% CHAPTER 11: CONCLUSIONS`
- new_ch12_achievements.tex     → `% CHAPTER 12: ACHIEVEMENTS & BUSINESS VALUE`
- new_ch13_challenges.tex       → `% CHAPTER 13: CHALLENGES & MITIGATIONS`
- new_ch14_future_work.tex      → `% CHAPTER 14: FUTURE WORK`

Also update main.tex comment labels for these chapters.

---

## TASK 10 — Update main.tex

Replace the chapter inputs block in `main.tex` so the order is:

```latex
% Chapter 4: Project Overview
\input{chapters/new_ch04_project}
\clearpage

% Chapter 5: Project Goals & Deliverables
\input{chapters/new_ch05_project_goals}
\clearpage

% Chapter 6: Learning Goals
\input{chapters/new_ch06_learning_goals}
\clearpage

% Chapter 7: Methodologies
\input{chapters/new_ch07_methodologies}
\clearpage

% Chapter 8: Requirements Elicitation
\input{chapters/new_ch08_requirements_elicitation}
\clearpage

% Chapter 9: Implementation & Architecture
\input{chapters/new_ch09_implementation}
\clearpage

% Chapter 10: Weekly Breakdown
\input{chapters/new_ch10_weekly_breakdown}
\clearpage

% Chapter 11: Conclusions
\input{chapters/new_ch11_conclusions}
\clearpage

% Chapter 12: Achievements & Business Value
\input{chapters/new_ch12_achievements}
\clearpage

% Chapter 13: Challenges & Mitigations
\input{chapters/new_ch13_challenges}
\clearpage

% Chapter 14: Future Work
\input{chapters/new_ch14_future_work}
\clearpage
```

---

## TASK 11 — Verify cross-references

Grep all chapter files for:
1. Any remaining "This chapter documents/provides/covers/presents..." opener
2. Any hard-coded chapter numbers in prose like "Chapter~7", "Chapter~8" etc.
3. Any `\ref{chap:requirements}` — only valid after Task 7b creates the label

Fix any issues found.

---

## TASK 12 — Commit and merge

**Stage all changes** (new file, trimmed ch07, renamed files, main.tex, headers).

**Commit message:**
```
report: Neeyati alignment — Requirements chapter split + personal openers

Part 1 - Chapter opener tone:
- ch04: remove 'This chapter provides...' meta-intro
- ch05: personal opener replacing 'This chapter defines...'
- ch07: shorter personal opener replacing long list opener
- ch09 (Weekly Breakdown): personal opener
- ch10 (Conclusions): add personal opening paragraph
- ch11 (Achievements): add personal opening paragraph

Part 2 - Requirements Elicitation as standalone chapter:
- Extract lines 300-551 from ch07 into new ch08
  new_ch08_requirements_elicitation.tex
- Trim ch07 to SRE Principles + Gap Analysis + Dynatrace only
- Rename ch08-ch13 to ch09-ch14 (git mv, history preserved)
- Update chapter comment headers
- Update main.tex input block (now 14 chapters)

Aligns with Neeyati's report structure:
ch7 Methodologies | ch8 Requirements | ch9 Implementation
```

**Then merge to release/v1.0.**
