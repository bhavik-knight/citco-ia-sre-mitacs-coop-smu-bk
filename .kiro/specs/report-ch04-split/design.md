# Design: Split ch04 into Two Chapters

## Approach

Use Python to perform the file operations (rename, extract, create) rather than
manual str_replace chains, since multiple files need atomic coordinated changes.

## Step-by-Step Plan

### Step 1: Extract new_ch05_project_goals.tex from ch04

Read `new_ch04_project.tex`. Find the line where `\section{Project Goals}` starts.
Everything from that line to end-of-file becomes the body of `new_ch05_project_goals.tex`.
Write the new file with the correct chapter header:

```latex
% ============================================================
% CHAPTER 5: PROJECT GOALS & DELIVERABLES
% MCDA 5585 / 5586 Major Project Report
% Bhavik Kantilal Bhagat | A00494758 | Saint Mary's University
% ============================================================

\chapter{Project Goals \& Deliverables}
\label{chap:project_goals}

<extracted sections: Project Goals + Deliverables + Acceptance Criteria>
```

Truncate `new_ch04_project.tex` at that same line, replacing the chapter title with:

```latex
\chapter{Project Overview}
\label{chap:project}
```

### Step 2: Rename subsequent chapter files

Using `git mv` (preserves history):

```
git mv new_ch05_learning_goals.tex  new_ch06_learning_goals.tex
git mv new_ch06_methodologies.tex   new_ch07_methodologies.tex
git mv new_ch07_implementation.tex  new_ch08_implementation.tex
git mv new_ch08_weekly_breakdown.tex new_ch09_weekly_breakdown.tex
git mv new_ch09_conclusions.tex     new_ch10_conclusions.tex
git mv new_ch10_achievements.tex    new_ch11_achievements.tex
git mv new_ch11_challenges.tex      new_ch12_challenges.tex
git mv new_ch12_future_work.tex     new_ch13_future_work.tex
```

### Step 3: Update chapter comment headers

Each renamed file has a comment block at the top:
```
% CHAPTER N: TITLE
```
Update N to the new chapter number in each file.

### Step 4: Update main.tex \input lines

Replace the chapter inputs block in `main.tex` with the new filenames in order.
The comment labels (e.g., `% Chapter 5: Learning Goals`) also update.

### Step 5: Verify \label and \ref consistency

Run a grep across all chapters for `\ref{chap:` to list all cross-references.
Check that every referenced label (`chap:project`, `chap:project_goals`,
`chap:tools`, `chap:learning_goals`, `chap:methodologies`, `chap:implementation`,
`chap:weekly_breakdown`, `chap:conclusions`, `chap:achievements`,
`chap:challenges`, `chap:future_work`) exists in the corresponding file.

The label names themselves do NOT change — only filenames. So no content edits
are needed for cross-references, only verification.

### Step 6: Verify chapter titles in text references

Search all chapters for prose like "Chapter~4", "Chapter~5" (number-based refs).
If any exist, update to the new number or convert to `\ref{}`.

## File Map After Changes

```
latex-report/chapters/
  new_ch01_about_citco.tex         (unchanged)
  new_ch02_executive_summary.tex   (unchanged)
  new_ch03_tools.tex               (unchanged)
  new_ch04_project.tex             (trimmed: Background + Overview only)
  new_ch05_project_goals.tex       (NEW: Goals + Deliverables + Acceptance)
  new_ch06_learning_goals.tex      (renamed from new_ch05_)
  new_ch07_methodologies.tex       (renamed from new_ch06_)
  new_ch08_implementation.tex      (renamed from new_ch07_)
  new_ch09_weekly_breakdown.tex    (renamed from new_ch08_)
  new_ch10_conclusions.tex         (renamed from new_ch09_)
  new_ch11_achievements.tex        (renamed from new_ch10_)
  new_ch12_challenges.tex          (renamed from new_ch11_)
  new_ch13_future_work.tex         (renamed from new_ch12_)
```

## main.tex Chapter Block (after)

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

% Chapter 7: Methodologies & Requirements
\input{chapters/new_ch07_methodologies}
\clearpage

% Chapter 8: Implementation & Architecture
\input{chapters/new_ch08_implementation}
\clearpage

% Chapter 9: Weekly Breakdown
\input{chapters/new_ch09_weekly_breakdown}
\clearpage

% Chapter 10: Conclusions
\input{chapters/new_ch10_conclusions}
\clearpage

% Chapter 11: Achievements & Business Value
\input{chapters/new_ch11_achievements}
\clearpage

% Chapter 12: Challenges & Mitigations
\input{chapters/new_ch12_challenges}
\clearpage

% Chapter 13: Future Work
\input{chapters/new_ch13_future_work}
\clearpage
```

## Risk Notes

- `\label{chap:project}` in `new_ch04_project.tex` is already set — keep it.
- `\label{chap:project_goals}` is a new label in `new_ch05_project_goals.tex`.
  Any existing `\ref{chap:project}` in ch02, ch04 intro text etc. will still
  resolve correctly to ch04.
- The split point (at `\section{Project Goals}`) is clean — no subsection
  straddles the boundary.
- ch06 Methodologies already has a `\section{Limitations and Mitigations}` added
  at the end — this is fine, it stays in the renamed new_ch07_methodologies.tex.
