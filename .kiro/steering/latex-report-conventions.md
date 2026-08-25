---
inclusion: fileMatch
fileMatchPattern: "**/*.tex"
---

# LaTeX Report Conventions

Applies when editing `.tex` files in this project.

## File Structure

```
latex-report/
├── main.tex                    # Entry point
├── preamble.tex                # Package imports, macros, colors
├── pages/                      # Front matter
│   ├── title_page.tex
│   ├── certificate.tex
│   ├── acknowledgements.tex
│   └── abstract.tex
├── chapters/                   # Main content
│   ├── new_ch01_company.tex
│   ├── new_ch02_overview.tex
│   └── ... (through ch15)
├── appendices/
│   └── work_logs.tex
└── figures/                    # Images
```

## Naming Conventions

- Chapter files: `new_chNN_topic.tex` (e.g., `new_ch04_tools.tex`)
- Figures: `figures/ws{N}_{description}.png` (e.g., `figures/ws2_grafana_dashboard.png`)
- Labels: `\label{sec:topic}`, `\label{fig:description}`, `\label{tab:description}`

## Table Formatting

### Standard Column Widths

Use `p{}` columns with explicit widths for text-heavy tables:

```latex
\begin{tabular}{|p{0.25\textwidth}|p{0.50\textwidth}|p{0.25\textwidth}|}
```

Common ratios:
- 2-column: 30/70 or 40/60
- 3-column: 25/50/25 or 30/35/35
- Status tables: avoid `\cellcolor` for status columns (use text badges instead)

### Status Tables

Do NOT use colored cells. Use text-based status:

```latex
% Bad
\cellcolor{statusgreen} Completed

% Good
Completed
```

## Section Structure

Each chapter should follow:

```latex
\chapter{Chapter Title}
\label{ch:shortname}

Brief intro paragraph.

\section{First Major Section}
\label{sec:topic}

Content...

\subsection{Subsection}

Details...
```

## Cross-References

Use `\ref{}` for numbered references, `\nameref{}` for named:

```latex
As discussed in Chapter~\ref{ch:tools}...
See Section~\ref{sec:grafana} for details...
```

## Lists

Prefer `itemize` for unordered lists, `enumerate` for ordered:

```latex
\begin{itemize}
    \item First item
    \item Second item with \textbf{bold emphasis}
\end{itemize}
```

## Code/Technical Terms

- Inline code: `\texttt{function\_name}`
- Package names: `\texttt{aws-lambda-powertools}`
- File paths: `\texttt{src/handler.py}`

## Figures

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/ws2_dashboard.png}
    \caption{Dashboard overview showing key metrics}
    \label{fig:dashboard}
\end{figure}
```

## Work Stream References

When referring to Work Streams in text:
- Full: "Work Stream 2 (Grafana AMG Dashboards)"
- Short: "WS2" or "Work Stream~2" (use `~` for non-breaking space)

## Common Packages (defined in preamble.tex)

- `graphicx` — images
- `tabularx` — flexible tables
- `hyperref` — clickable links
- `listings` — code blocks
- `booktabs` — professional tables (`\toprule`, `\midrule`, `\bottomrule`)

## Build Command

```bash
export PATH="$PATH:/c/Users/bbhagat/scoop/apps/miktex/25.12/texmfs/install/miktex/bin/x64"
cd latex-report && pdflatex -interaction=nonstopmode main.tex
```

Run twice for TOC/references to resolve properly.
