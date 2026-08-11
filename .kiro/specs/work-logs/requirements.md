# Requirements: Work Logs Generation

## Goal
Generate accurate daily work log markdown files from git commit history across all dev repos, then convert to Excel/PDF for SMU submission.

## Output Files
- `smu/work-logs/YYYY-MM/YYYY-MM-DD.md` — one per workday
- `output/WorkLogs.xlsx` — submission Excel (Francis format)
- `output/WorkLogs.pdf` — PDF export

## Branch
All work log files committed to `feature/work-logs` only. Never to `main` or other feature branches.

## Work Log Folder (absolute path for multi-root workspace)
`c:\Users\bbhagat\dev_work\citco-ia-sre-mitacs-coop-smu-bk\smu\work-logs\`

## Source Repositories (scan all for commits by bbhagat / Bhavik)
| Repo | Path |
|---|---|
| citco-ia-sre-mitacs-coop-smu-bk | `c:\Users\bbhagat\dev_work\citco-ia-sre-mitacs-coop-smu-bk` |
| core-ia-bpo-cais-dl | `c:\Users\bbhagat\dev_work\AWS_Projects\core-ia-bpo-cais-dl` |
| core-ia-bpo-cais-pp | `c:\Users\bbhagat\dev_work\AWS_Projects\core-ia-bpo-cais-pp` |
| core-ia-bpo-ebinder-service-repo | `c:\Users\bbhagat\dev_work\AWS_Projects\core-ia-bpo-ebinder-service-repo` |
| core-ia-bpo-eventsrvc-investran | `c:\Users\bbhagat\dev_work\AWS_Projects\core-ia-bpo-eventsrvc-investran` |
| core-rpacfs1-web-ui | `c:\Users\bbhagat\dev_work\AWS_Projects\core-rpacfs1-web-ui` |
| core-smart-rpa-llm-ecr-image | `c:\Users\bbhagat\dev_work\AWS_Projects\core-smart-rpa-llm-ecr-image` |
| ia-it-sre-agent-orchestration | `c:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-agent-orchestration` |
| ia-it-sre-infrastructure-inventory | `c:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-inventory` |
| ia-it-sre-infrastructure-monitoring-amg | `c:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-infrastructure-monitoring-amg` |
| ia-it-sre-resources-inventory | `c:\Users\bbhagat\dev_work\AWS_Projects\ia-it-sre-resources-inventory` |
| ia-resources-monitoring | `c:\Users\bbhagat\dev_work\AWS_Projects\ia-resources-monitoring` |
| ml-rpa-status-llm-agent | `c:\Users\bbhagat\dev_work\AWS_Projects\ml-rpa-status-llm-agent` |
| rpacfs1-aexeo-reporter-service | `c:\Users\bbhagat\dev_work\AWS_Projects\rpacfs1-aexeo-reporter-service` |
| rpacfs1-cais-pricing-extract-genai-infrastructure | `c:\Users\bbhagat\dev_work\AWS_Projects\rpacfs1-cais-pricing-extract-genai-infrastructure` |
| ia_common_utility | `c:\Users\bbhagat\dev_work\BitBucket_Projects\ia_common_utility` |
| ia_config_service_portal | `c:\Users\bbhagat\dev_work\BitBucket_Projects\ia_config_service_portal` |
| ia_ebinder_services | `c:\Users\bbhagat\dev_work\BitBucket_Projects\ia_ebinder_services` |
| ia_meso_process | `c:\Users\bbhagat\dev_work\BitBucket_Projects\ia_meso_process` |
| ia-uipath-vpl-pricingandchecks | `c:\Users\bbhagat\dev_work\ia-uipath-vpl-pricingandchecks` |

## Daily Markdown Format
```
# Work Log — YYYY-MM-DD (Weekday)
**Week:** W[N] | **Total Hours:** X hrs Y min

| # | Duration | JIRA | Repository | Task Description |
|---|----------|------|------------|-----------------|
| 1 | 0:30 | IA-XXXX | repo-name | Detailed description |
...
**Daily Total: X hrs Y min**
```

## Entry Rules
- JIRA extracted from branch name or commit message (IA-XXXX, IISS-XXXX, COMAPI-XXXXXX)
- Duration: 0:30 default per item
- **Minimum 15 entries/day** (= 7.5 hrs). Pad thin days by decomposing commits into sub-tasks: implement → test → review → document → standup
- **No maximum** on high-commit days — use every commit
- Always include: Daily standup (0:15), end-of-day ticket update (0:15)
- Descriptions must reference actual file names / modules / functions from that day's commits

## Excel Format (output/WorkLogs.xlsx)
Match `templates/samples/Francis_Kuzhippallil_A00463084_Minor_Project_Logs.xlsx`:
- Columns: Week | Date | Day | Task Description | Hrs Spent | Cumulative Total Hrs
- Color-code by weekday (Mon=blue, Tue=green, Wed=yellow, Thu=orange, Fri=purple)
- Sheet: Legend, Summary (Week# | Date Range | Weekly Hours | Cumulative)

## Integration with LaTeX
After generating xlsx, update `latex-report/appendices/work_logs.tex` with actual weekly totals grouped by phase.

## Reference Files
- Sample Excel: `templates/samples/Francis_Kuzhippallil_A00463084_Minor_Project_Logs.xlsx`
- Existing partial log: `smu/work-logs/2026-03/w1d1_20260316.md` (incorporate, don't overwrite)
