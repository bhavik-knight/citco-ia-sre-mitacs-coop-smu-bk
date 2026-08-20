# Design: Neeyati Template Alignment

## Part 1 — Chapter Opener Replacements

For each chapter, remove the meta-intro and replace with a direct personal opener.

### CH04 — `new_ch04_project.tex`
**Remove:**
```latex
This chapter provides the production context that established the
monitoring gap and motivated the work, then describes the four project
streams and their engineering mandates.
```
**Replace with:** *(nothing — delete entirely; \section{Project Background} follows immediately and is self-explanatory)*

---

### CH05 — `new_ch05_project_goals.tex`
**Remove:**
```latex
This chapter defines the engineering objectives that guided the
internship, maps every deliverable to its JIRA scope and technical
stack, and specifies the acceptance criteria by which each deliverable
was evaluated.
```
**Replace with:**
```latex
I set the following engineering objectives at the outset of the internship,
guided by the two motivating incidents and the requirements sessions with
Kishor and Kri. Each objective maps directly to one of the four work streams
described in Chapter~\ref{chap:project}.
```

---

### CH07 — `new_ch07_methodologies.tex`
**Remove:**
```latex
This chapter documents the engineering methodology that underpinned my
internship. It begins with the Site Reliability Engineering principles
I adopted from the team's knowledge-transfer sessions and explains how
I operationalised those principles for the Citco Intelligent
Automation platform. It then characterises the observability gap that
existed at the start of my engagement, identifies the stakeholders who
shaped the requirements, describes how I elicited requirements, and
closes with the complete functional and non-functional requirements that
governed the build.
```
**Replace with:**
```latex
During my internship I adopted Site Reliability Engineering as the primary
methodology, applying the four golden signals framework and SLI/SLO discipline
to the observability gap exposed by the CAIS-Pricing Silent Outage and the
Meridian Incident. This chapter covers the SRE principles I operationalised,
the gap analysis that established the starting posture, and the Dynatrace
parity evaluation that framed the research question.
```
*(Note: after the split in Part 2, the sentence about requirements/stakeholders
is no longer needed here since those move to ch08)*

---

### CH09 — `new_ch09_weekly_breakdown.tex` (was ch08 before split; will be ch09 after)
**Remove:**
```latex
This chapter provides a phase-by-phase narrative of the internship delivery,
organised around the four major phases that structured the 24-week engagement.
The narrative complements the detailed technical account in
Chapter~\ref{chap:implementation} by focusing on the chronological flow ---
what was done each week, what blocked or accelerated progress, and how the
priorities shifted in response to production events.
```
**Replace with:**
```latex
My internship was structured across four delivery phases spanning 24~weeks.
The following narrative covers what I built each week, what blocked or
accelerated progress, and how priorities shifted in response to production
events and emerging technical constraints.
```

---

### CH10 (was ch09) — `new_ch10_conclusions.tex`
**Current:** Opens directly with `Chapter~\ref{chap:learning_goals} established eight technical...`
No meta-intro but the cross-ref opener is dry.

**Replace with:**
```latex
Throughout my internship I worked toward the technical and non-technical
goals established at the outset in consultation with Kishor Deotale and
Dr.\ Pawan Lingras. The following sections evaluate each goal against the
delivered outcomes and reflect on the broader impact of the engagement.
```
Then keep the existing `\section{Learning Goals Evaluation}` table.

---

### CH11 (was ch10) — `new_ch11_achievements.tex`
**Current:** Opens directly with `\section{}` (no chapter-level intro paragraph at all).

**Add before first section:**
```latex
Working on the IA-IT-SRE Infrastructure at Citco Technology Management,
I delivered three primary engineering work streams and contributed to
production operations across four RPA support rotations. The following
sections document the key deliverables, quantitative metrics, and
business value created during the internship.
```

---

### CH12 (was ch11) — `new_ch12_challenges.tex`
**Current:** "Six engineering challenges arose during my internship that were significant enough..."
✅ Already personal and direct. **No change.**

---

### CH13 (was ch12) — `new_ch13_challenges.tex` / Future Work
**Current:** "The work I delivered in this internship establishes a monitoring foundation --- not an endpoint."
✅ Already personal and direct. **No change.**

---

## Part 2 — Split Requirements out of ch07

### Step 2a: Read ch07 and find split point
The content to extract is everything from `\section{Stakeholder Identification}`
(line ~300) through the end of `\section{Functional and Non-Functional Requirements}`
(line ~551), inclusive. The `\section{Limitations and Mitigations}` stays in ch07.

### Step 2b: Create new_ch08_requirements_elicitation.tex
```latex
% ============================================================
% CHAPTER 8: REQUIREMENTS ELICITATION
% MCDA 5585 / 5586 Major Project Report
% Bhavik Kantilal Bhagat | A00494758 | Saint Mary's University
% ============================================================

\chapter{Requirements Elicitation}
\label{chap:requirements}

During my internship I worked with a small set of internal stakeholders
whose needs shaped the functional and non-functional requirements of the
IA-IT-SRE Infrastructure monitoring platform. This chapter identifies
those stakeholders, describes the elicitation techniques I used, and
documents the requirements that governed the build.

[EXTRACTED CONTENT: Stakeholder Identification + Requirements Elicitation
+ Functional/Non-Functional Requirements + Traceability]
```

### Step 2c: Trim ch07
Remove lines 300–551 from `new_ch07_methodologies.tex` (Stakeholder through
end of Requirements Traceability). The `\section{Limitations and Mitigations}`
remains at the end of ch07.

### Step 2d: Rename subsequent files (+1)
Use `git mv` to rename:
```
new_ch08_implementation.tex    → new_ch09_implementation.tex
new_ch09_weekly_breakdown.tex  → new_ch10_weekly_breakdown.tex
new_ch10_conclusions.tex       → new_ch11_conclusions.tex
new_ch11_achievements.tex      → new_ch12_achievements.tex
new_ch12_challenges.tex        → new_ch13_challenges.tex
new_ch13_future_work.tex       → new_ch14_future_work.tex
```

### Step 2e: Update chapter comment headers
Update `% CHAPTER N:` in each renamed file to the new number (9 through 14).

### Step 2f: Update main.tex
Insert the new `\input{chapters/new_ch08_requirements_elicitation}` line
and update all subsequent `\input` lines to use the new filenames.

## Final Chapter Map (14 chapters)

```
ch01  new_ch01_about_citco.tex            About Company & Organization
ch02  new_ch02_executive_summary.tex      Executive Summary
ch03  new_ch03_tools.tex                  Tools & Technologies
ch04  new_ch04_project.tex                Project Overview
ch05  new_ch05_project_goals.tex          Project Goals & Deliverables
ch06  new_ch06_learning_goals.tex         Learning Goals
ch07  new_ch07_methodologies.tex          Methodologies (SRE + Gap Analysis)
ch08  new_ch08_requirements_elicitation.tex  Requirements Elicitation  [NEW]
ch09  new_ch09_implementation.tex         Implementation & Architecture
ch10  new_ch10_weekly_breakdown.tex       Weekly Breakdown
ch11  new_ch11_conclusions.tex            Conclusions
ch12  new_ch12_achievements.tex           Achievements & Business Value
ch13  new_ch13_challenges.tex             Challenges & Mitigations
ch14  new_ch14_future_work.tex            Future Work
```

## Cross-Reference Safety
All `\label{chap:xxx}` are semantic names, not numbers. Renaming files does
not break any existing `\ref{chap:xxx}` calls. The only new label introduced
is `\label{chap:requirements}` in the new ch08 file.

Any prose reference to "Chapter~7" or "Chapter~8" as hard numbers (rare)
must be found and updated to `Chapter~\ref{chap:methodologies}` etc.
