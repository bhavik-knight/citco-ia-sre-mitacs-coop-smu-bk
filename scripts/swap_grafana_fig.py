#!/usr/bin/env python3
from pathlib import Path

path = Path("latex-report/chapters/new_ch10_implementation.tex")
content = path.read_text(encoding="utf-8")

old = r"""\begin{figure}[ht]
\begin{center}
\begin{minipage}{0.92\textwidth}
\begin{lstlisting}[language={}, basicstyle=\ttfamily\scriptsize, frame=none, backgroundcolor=\color{white}, numbers=none]
+---------------------------+     +---------------------------+
| Lambda: cache_refresh     |     | Lambda API: handler_      |
|                           |     | resources                 |
| 1. Discover AWS resources |     |                           |
|    (all 13 service types) |     | 1. Read S3 cache          |
| 2. Write S3 cache         |---->| 2. Return JSON            |
|    (latest.json per row)  |     |                           |
| 3. Publish CW metrics     |     +---------------------------+
|    (platform/Monitoring)  |              |
+---------------------------+              v
           |                   +---------------------------+
           v                   | Grafana AMG               |
+---------------------------+  |                           |
| CloudWatch                |  | Variables (dimensionValues|
| platform/Monitoring       |->|   -> lambda_function etc) |
| LambdaFunctionActive      |  |                           |
| SQSQueueActive            |  | Panels (Metric Insights   |
| MSKClusterActive ...      |  |   SQL per resource)       |
+---------------------------+  |                           |
                               | Deep-links (AWS Console   |
                               |   URLs per resource)      |
                               +---------------------------+
\end{lstlisting}
\end{minipage}
\end{center}"""

new = r"""\begin{figure}[ht]
\centering
\includegraphics[width=\textwidth]{figures/grafana_inventory_integration.png}"""

if old in content:
    content = content.replace(old, new, 1)
    path.write_text(content, encoding="utf-8")
    print("Done.")
else:
    print("ERROR: string not found")
