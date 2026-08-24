#!/usr/bin/env python3
"""
Rewrite the learning goals table to match Neeyati's format:
  S.N. | Task | Description | Status (green "Completed")
Also add a timesheet table: Internship work: 900h | Report writing: 120h
"""
import re
from pathlib import Path

path = Path("latex-report/chapters/new_ch12_conclusions.tex")
content = path.read_text(encoding="utf-8")

# ── New learning goals table (longtable, full text width) ─────────────────────
NEW_LG_TABLE = r"""\definecolor{statusgreen}{RGB}{168,208,141}

\begin{longtable}{p{0.7cm}p{4.0cm}Xp{2.2cm}}
\rowcolor{smubrand}
  \textcolor{white}{\textbf{S.N.}} &
  \textcolor{white}{\textbf{Task}} &
  \textcolor{white}{\textbf{Description}} &
  \textcolor{white}{\textbf{Status}} \\
\hline
\endfirsthead
\rowcolor{smubrand}
  \textcolor{white}{\textbf{S.N.}} &
  \textcolor{white}{\textbf{Task}} &
  \textcolor{white}{\textbf{Description}} &
  \textcolor{white}{\textbf{Status}} \\
\hline
\endhead
\multicolumn{4}{r}{\small\itshape continued on next page} \\
\endfoot
\caption{Learning Goals --- Self-Evaluation at Internship Completion}
\label{tab:learning_goals_eval}
\endlastfoot
1 & AWS Cloud Services \& Infrastructure &
  13 AWS service namespaces monitored across all six platforms; Lambda, ECS, EC2 inventoried; full DB spectrum (DocumentDB, Neptune, RDS, Redis, OpenSearch) &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
2 & Site Reliability Engineering Principles &
  Four golden signals applied; SLOs defined for Lambda, ECS, MSK, SQS; MSK lag alarm reduces MTTD from 3.5h to $<$30s &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
3 & Infrastructure-as-Code &
  4 CloudFormation stacks deployed; Lambda-backed dynamic provisioner; S3-staged templates; multi-env reuse via \texttt{samconfig.toml} &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
4 & Observability Platforms (AMG) &
  14-row / 110+ panel Grafana workspace; survived 10.4$\to$12.4 upgrade; 38 alarms wired to SNS &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
5 & Proactive vs.\ Reactive Reliability &
  Alarm-backed detection replaces business escalation; Meridian Incident used as design proof point &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
6 & Python Development &
  Flask REST API; 562 tests at 99\% coverage; boto3 concurrent discovery; Hypothesis PBT; structlog &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
7 & Software Engineering Practices &
  TDD with pytest; spec-driven development via Kiro IDE; PR-based merges on CodeCommit &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
8 & AI-Augmented Engineering &
  Kiro IDE spec workflow; Amazon~Q inline; Claude Sonnet for architecture reasoning &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
9 & Agile and Kanban Methodology &
  25+ JIRA tickets across IISS board; story decomposition, work-log discipline, sprint rituals &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
10 & Technical Communication &
  RCA reports (IISS-706, Apr~17); Confluence pages; JIRA acceptance criteria; this report &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
11 & Production Incident Response &
  4 support rotations; 5 notable incidents resolved; IISS-706 hotfix within 7h &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
12 & Cross-Functional Collaboration &
  Halifax--Hyderabad time-zone coordination; Meridian team architecture sessions &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
13 & Financial Domain Knowledge &
  VPL queue, Corp Actions, MESO, CAIS operational familiarity; fund admin SLA awareness &
  \cellcolor{statusgreen}\centering\textbf{Completed} \\
\end{longtable}"""

# ── Timesheet table ────────────────────────────────────────────────────────────
TIMESHEET_TABLE = r"""
% ────────────────────────────────────────────────────────────
\section{Internship Hours Summary}
\label{sec:hours_summary}
% ────────────────────────────────────────────────────────────

\begin{table}[H]
\centering
\caption{Internship Hours Summary}
\label{tab:hours_summary}
\begin{tabularx}{\textwidth}{Xr}
\hline
\rowcolor{smubrand}\textcolor{white}{\textbf{Work}} & \textcolor{white}{\textbf{Duration (hours)}} \\
\hline
Citco CTM Internship (IISS-487, IISS-507, IISS-824, support rotations) & 900 \\
Report Writing (MCDA 5585 / 5586 Major Project Report) & 120 \\
\hline
\rowcolor{tablerowA}\textbf{Total} & \textbf{1020} \\
\hline
\end{tabularx}
\end{table}"""

# ── Replace the existing longtable block ──────────────────────────────────────
pattern = re.compile(
    r'\\renewcommand\{\\arraystretch\}.*?\\end\{longtable\}',
    re.DOTALL
)
new_content, n = pattern.subn(lambda m: NEW_LG_TABLE, content, count=1)

if n == 0:
    # fallback: try matching just the longtable
    pattern2 = re.compile(r'\\begin\{longtable\}.*?\\end\{longtable\}', re.DOTALL)
    new_content, n = pattern2.subn(lambda m: NEW_LG_TABLE, content, count=1)

if n == 0:
    print("ERROR: could not find existing longtable — appending after LG text")
    new_content = content

# ── Insert timesheet table after "All my learning goals were met..." paragraph
insert_after = "into a single, concrete engineering outcome."
if insert_after in new_content and TIMESHEET_TABLE not in new_content:
    new_content = new_content.replace(
        insert_after,
        insert_after + "\n" + TIMESHEET_TABLE
    )
    print("Timesheet table inserted.")

path.write_text(new_content, encoding="utf-8")
print(f"Done — replaced {n} longtable block(s).")
