#!/usr/bin/env python3
"""
Rewrite the learning goals longtable:
- Remove S.N. column
- Task (p{3.5cm}), Description (X, wide), Status (p{1.8cm}, checkmark)
- Top-aligned cells (m{} -> p{} which is top-aligned in longtable)
- Checkmark instead of 'Completed' text
"""
import re
from pathlib import Path

path = Path("latex-report/chapters/new_ch12_conclusions.tex")
content = path.read_text(encoding="utf-8")

# Find and replace the entire longtable block
pattern = re.compile(
    r'\\definecolor\{statusgreen\}.*?\\end\{longtable\}',
    re.DOTALL
)

NEW_TABLE = r"""\definecolor{statusgreen}{RGB}{168,208,141}

\begin{longtable}{p{3.5cm}Xp{1.6cm}}
\rowcolor{smubrand}
  \textcolor{white}{\textbf{Task}} &
  \textcolor{white}{\textbf{Description}} &
  \textcolor{white}{\centering\textbf{Status}} \\
\hline
\endfirsthead
\rowcolor{smubrand}
  \textcolor{white}{\textbf{Task}} &
  \textcolor{white}{\textbf{Description}} &
  \textcolor{white}{\centering\textbf{Status}} \\
\hline
\endhead
\multicolumn{3}{r}{\small\itshape continued on next page} \\
\endfoot
\caption{Learning Goals --- Self-Evaluation at Internship Completion}
\label{tab:learning_goals_eval}
\endlastfoot
\rowcolor{tablerowA}AWS Cloud Services \& Infrastructure &
  13 AWS service namespaces monitored across all six platforms; Lambda, ECS, EC2 inventoried; full DB spectrum (DocumentDB, Neptune, RDS, Redis, OpenSearch) &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}Site Reliability Engineering Principles &
  Four golden signals applied; SLOs defined for Lambda, ECS, MSK, SQS; MSK lag alarm reduces MTTD from 3.5h to $<$30s &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Infrastructure-as-Code &
  4 CloudFormation stacks deployed; Lambda-backed dynamic provisioner; S3-staged templates; multi-env reuse via \texttt{samconfig.toml} &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}Observability Platforms (AMG) &
  17-row / 152-panel Grafana workspace; survived 10.4$\to$12.4 upgrade; 38 alarms wired to SNS &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Proactive vs.\ Reactive Reliability &
  Alarm-backed detection replaces business escalation; Meridian Incident used as design proof point &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}Python Development &
  Flask REST API; 562 tests at 99\% coverage; boto3 concurrent discovery; Hypothesis PBT; structlog &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Software Engineering Practices &
  TDD with pytest; spec-driven development via Kiro IDE; PR-based merges on CodeCommit &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}AI-Augmented Engineering &
  Kiro IDE spec workflow; Amazon~Q inline; Claude Sonnet for architecture reasoning &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Agile and Kanban Methodology &
  25+ JIRA tickets across IISS board; story decomposition, work-log discipline, sprint rituals &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}Technical Communication &
  RCA reports (IISS-706, Apr~17); Confluence pages; JIRA acceptance criteria; this report &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Production Incident Response &
  4 support rotations; 5 notable incidents resolved; IISS-706 hotfix within 7h &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowB}Cross-Functional Collaboration &
  Halifax--Hyderabad time-zone coordination; Meridian team architecture sessions &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\rowcolor{tablerowA}Financial Domain Knowledge &
  VPL queue, Corp Actions, MESO, CAIS operational familiarity; fund admin SLA awareness &
  \cellcolor{statusgreen}\centering{\Large\checkmark} \\[2pt]
\end{longtable}"""

new_content, n = pattern.subn(lambda m: NEW_TABLE, content, count=1)
if n:
    path.write_text(new_content, encoding="utf-8")
    print(f"Done — replaced {n} longtable.")
else:
    print("ERROR: longtable not found.")
