# Tasks: Split ch04 into Two Chapters

## Task 1 — Split new_ch04_project.tex

**Action:** Read `new_ch04_project.tex`. Find the exact line where
`\section{Project Goals}` begins. Write everything from that line to EOF
into a new file `new_ch05_project_goals.tex` with the correct chapter header.
Truncate `new_ch04_project.tex` at that line and update its chapter title.

**Files modified:**
- `latex-report/chapters/new_ch04_project.tex` (truncated, title updated)
- `latex-report/chapters/new_ch05_project_goals.tex` (created)

**Verification:** `new_ch04_project.tex` ends after `\section{Project Overview}`
subsections. `new_ch05_project_goals.tex` starts with `\chapter{Project Goals \& Deliverables}`.

---

## Task 2 — Rename subsequent chapter files with git mv

**Action:** Rename 8 files using `git mv` to preserve history.

```
new_ch05_learning_goals.tex   → new_ch06_learning_goals.tex
new_ch06_methodologies.tex    → new_ch07_methodologies.tex
new_ch07_implementation.tex   → new_ch08_implementation.tex
new_ch08_weekly_breakdown.tex → new_ch09_weekly_breakdown.tex
new_ch09_conclusions.tex      → new_ch10_conclusions.tex
new_ch10_achievements.tex     → new_ch11_achievements.tex
new_ch11_challenges.tex       → new_ch12_challenges.tex
new_ch12_future_work.tex      → new_ch13_future_work.tex
```

**Verification:** `git status` shows 8 renames, no deletions.

---

## Task 3 — Update chapter number comments inside each renamed file

**Action:** In each renamed file, update the comment block at the top:
```
% CHAPTER N: TITLE
```
Change N to the new chapter number (6 through 13).

**Files modified:** All 8 renamed files.

---

## Task 4 — Update main.tex \input block

**Action:** Replace the chapter inputs block in `main.tex` to use the new
filenames in the correct order (ch04 through ch13). Update the comment labels.

**File modified:** `latex-report/main.tex`

**Verification:** `main.tex` has exactly 13 chapter `\input` lines, no old
filenames remain.

---

## Task 5 — Verify cross-references

**Action:** Grep all chapters for `\ref{chap:` and `\label{chap:`.
Verify every referenced label exists. Check for any hard-coded chapter
number references in prose (e.g., "Chapter~5", "Chapter~6") and update
to the new numbers or convert to `\ref{}`.

**Files modified:** Any chapter with hard-coded chapter number references.

---

## Task 6 — Commit and merge to release

**Action:** Stage all changes and commit on `feature/report-chapters`.
Then merge to `release/v1.0`.

**Commit message:**
```
report: split ch04 into ch04 Project Overview + ch05 Project Goals

- Extract \section{Project Goals} + Deliverables + Acceptance Criteria
  from new_ch04_project.tex into new new_ch05_project_goals.tex
- new_ch04_project.tex now contains only Background + Overview (~3pp)
- new_ch05_project_goals.tex contains Goals + Technical Scope + AC (~5pp)
- Rename ch05-ch12 to ch06-ch13 (+1 each) using git mv
- Update chapter comment headers in renamed files
- Update main.tex \input block with new filenames
- Verify no broken \label/\ref cross-references
Aligns chapter structure with Neeyati's report (ch5 Project Overview,
ch6 Project Goals as separate chapters)
```
