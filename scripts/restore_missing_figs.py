#!/usr/bin/env python3
"""
Temporarily revert figures that don't have PNGs yet back to ASCII
so the report still compiles. Run restore_png_figs.py once PNGs are saved.

Missing PNGs:
  - latex-report/figures/amg_system_arch.png
  - latex-report/figures/grafana_inventory_integration.png
"""
from pathlib import Path

figures_dir = Path("latex-report/figures")
missing = []
for name in ["amg_system_arch.png", "grafana_inventory_integration.png",
             "iam_role_model.png", "cicd_pipeline.png", "cicd_pipeline_envs.png"]:
    if not (figures_dir / name).exists():
        missing.append(name)

if not missing:
    print("All PNG files present — no revert needed.")
    raise SystemExit(0)

print("Missing PNGs:", missing)

path = Path("latex-report/chapters/new_ch10_implementation.tex")
content = path.read_text(encoding="utf-8")
original = content

# ── amg_system_arch ───────────────────────────────────────────────────────────
if "amg_system_arch.png" in missing:
    content = content.replace(
        r"""\begin{figure}[ht]
\centering
\includegraphics[width=0.80\textwidth]{figures/amg_system_arch.png}
\caption{AMG Observability Platform --- System Architecture}
\label{fig:amg_system_arch}
\end{figure}""",
        r"""\begin{figure}[ht]
\begin{center}
\begin{minipage}{0.92\textwidth}
\begin{lstlisting}[language={}, basicstyle=\ttfamily\scriptsize, frame=none, backgroundcolor=\color{white}, numbers=none]
+---------------------------------------------------------------+
| AWS Account (eu-west-1)                                       |
|  [SQS] [Lambda] [ECS] [MSK] [EC2] [ECR] [EKS]               |
|  [DocumentDB] [Neptune] [OpenSearch] [Redis] [RDS]            |
|          |                                                    |
|          v                                                    |
|  +----------------+     +-----------+     +-----------+       |
|  | Amazon         |     | SNS Topic |     | S3 Bucket |       |
|  | CloudWatch     |---->| (Alarms)  |     | Templates |       |
|  +-------+--------+     +-----+-----+     +-----+-----+       |
|          |                    v                 |             |
|          v               Email Alert            v             |
|  +----------------+                    Lambda Provisioner     |
|  | Amazon Managed |<-----------------------------------+      |
|  | Grafana (AMG)  |                                          |
|  | 17 rows/152    |                                          |
|  | panels         |                                          |
|  +----------------+                                          |
+---------------------------------------------------------------+
\end{lstlisting}
\end{minipage}
\end{center}
\caption{AMG Observability Platform --- System Architecture}
\label{fig:amg_system_arch}
\end{figure}"""
    )
    print("  Reverted: amg_system_arch")

# ── grafana_inventory_integration ────────────────────────────────────────────
if "grafana_inventory_integration.png" in missing:
    content = content.replace(
        r"""\begin{figure}[ht]
\centering
\includegraphics[width=\textwidth]{figures/grafana_inventory_integration.png}
\caption{Inventory API --- Grafana AMG Integration (cache refresh, CW metrics, template variables)}
\label{fig:grafana_inventory_integration}
\end{figure}""",
        r"""\begin{figure}[ht]
\begin{center}
\begin{minipage}{0.92\textwidth}
\begin{lstlisting}[language={}, basicstyle=\ttfamily\scriptsize, frame=none, backgroundcolor=\color{white}, numbers=none]
+------------------+   +------------------+   +------------------+
| Lambda:          |   | CloudWatch:      |   | Grafana AMG:     |
| cache_refresh    |-->| platform/Monitor |-->| Variables        |
| Discovers AWS    |   | LambdaActive     |   | dimensionValues  |
| Writes S3 cache  |   | SQSQueueActive   |   | Panels: Metric   |
+------------------+   | MSKClusterActive |   | Insights SQL     |
         |             +------------------+   | Deep-links       |
         v                                    +------------------+
+------------------+   +------------------+
| S3: latest.json  |-->| Lambda API:      |
| per service/plat |   | handler_resources|
+------------------+   | Returns JSON     |
                        +------------------+
\end{lstlisting}
\end{minipage}
\end{center}
\caption{Inventory API --- Grafana AMG Integration}
\label{fig:grafana_inventory_integration}
\end{figure}"""
    )
    print("  Reverted: grafana_inventory_integration")

if content != original:
    path.write_text(content, encoding="utf-8")
    print("File updated.")

print("\nTODO — save these PNGs to latex-report/figures/ when ready:")
for name in missing:
    print(f"  - {name}")
