# Design: Report Chapters — Feature Branch Structure

## Branch Strategy
- Branch: `feature/report-chapters` (create from `main`)
- All chapter files written on this branch
- Merge to `main` when all chapters complete

## File Mapping

```
latex-report/
├── main.tex                     ← UPDATE: add new chapter includes
├── pages/
│   └── abstract.tex             ← UPDATE: SRE-focused abstract
└── chapters/
    ├── about_company.tex        ← KEEP (already complete)
    ├── ch1_introduction.tex     ← NEW
    ├── ch2_org_context.tex      ← NEW
    ├── ch3_tools.tex            ← NEW
    ├── ch4_project_overview.tex ← NEW
    ├── ch5_sre_methodology.tex  ← NEW
    ├── ch6_architecture.tex     ← NEW
    ├── ch7_implementation.tex   ← NEW
    └── ch8_results_conclusion.tex ← NEW
```

## main.tex Chapter Order
```latex
\input{chapters/about_company}      % Ch 1: Company (existing)
\input{chapters/ch1_introduction}   % Ch 2: Introduction & Learning Goals
\input{chapters/ch2_org_context}    % Ch 3: Org & Team Context
\input{chapters/ch3_tools}          % Ch 4: Tools & Technologies
\input{chapters/ch4_project_overview} % Ch 5: Project Overview
\input{chapters/ch5_sre_methodology}  % Ch 6: SRE Methodology
\input{chapters/ch6_architecture}     % Ch 7: Architecture & Design
\input{chapters/ch7_implementation}   % Ch 8: Implementation
\input{chapters/ch8_results_conclusion} % Ch 9: Results & Conclusion
```

## LaTeX Style Conventions
- Chapter heading: `\chapter{Title}` with `\label{chap:filename}`
- Sections: `\section{}`, Subsections: `\subsection{}`
- Tables: use `tabular` with `\toprule`, `\midrule`, `\bottomrule` (booktabs)
- Code: use `lstlisting` environment
- Lists: `itemize` or `enumerate`
- Cross-references: `\ref{}` for labels
- SMU maroon color available as `\textcolor{smumaroon}{}`
- Registered trademark: `\textsuperscript{\textregistered}`
- Æxeo: `\AE xeo`
- Em-dash: `---`
- Quotes: use LaTeX quotes `` `text' `` or `` ``text'' ``
