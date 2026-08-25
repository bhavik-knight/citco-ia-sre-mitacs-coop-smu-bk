# Requirements: Report Chapters — SMU MCDA Major Project

## Goal
Write 8 LaTeX chapter files for the major project report on the `feature/report-chapters`
branch. Target 40–50 pages total. SRE-focused structure (not data science). All work on
a dedicated git branch: `feature/report-chapters`.

## Chapter Structure (agreed)

| File | Chapter | Target Pages |
|------|---------|--------------|
| `ch1_introduction.tex` | Introduction & Learning Goals | 2 |
| `ch2_org_context.tex` | Organizational & Team Context | 3–4 |
| `ch3_tools.tex` | Tools & Technologies | 3–4 |
| `ch4_project_overview.tex` | Project Overview & Objectives | 3–4 |
| `ch5_sre_methodology.tex` | SRE Methodology & Requirements | 4–5 |
| `ch6_architecture.tex` | Technical Architecture & Design | 8–10 |
| `ch7_implementation.tex` | Implementation (+ RPA Support section) | 10–12 |
| `ch8_results_conclusion.tex` | Results, Evaluation & Conclusion | 4–5 |

## Key Constraints

- ALL chapter files go in `latex-report/chapters/`
- All work must be on git branch `feature/report-chapters` (create from `main` if not exists)
- `main.tex` must be updated to include the new chapter files
- Abstract (`pages/abstract.tex`) must be updated to reflect SRE content
- `about_company.tex` already exists and is complete — do NOT modify it
- Chapter 2 (org context): only about the IA team, not Citco business model (we don't have public info)
- Chapter 3 (tools): mention Kiro IDE and other AI tools that helped build the project — brief but substantive
- Chapter 7 (implementation): fold RPA support into this chapter as a dedicated section
- No `\tableofcontents` or `\listoffigures` changes needed — `main.tex` already handles these

## Content Sources (key facts to use)

### Project Numbers
- IISS-487: 140h logged, 14 dashboard rows, 110+ panels, 38 CloudWatch alarms, 7 platforms
- IISS-507 inventory API: 562 automated tests, 99% code coverage, Flask async
- Apr 17 incident: 9M Kafka messages queued, 7.5h processing delay, affected Winton/GS/other funds
- Lambda inventory: ~119 functions across 5 budget codes
- ECS clusters: 22 total, 5 budget codes (rpacfs1, ia-bpo, automationhub, meridian, citcoworks)
- EC2: 83 instances scanned, tag-based discovery (BudgetCode + AppName fallback)
- Container Insights: 5 of 6 Meridian clusters enabled on May 11–12 2026
- Secrets Manager 64KB limit: encountered when agentic CFN provisioner grew too large → S3 migration
- Grafana upgrade: 10.4 → 12.4 during development (May 13)
- CloudFormation stacks: 4 stacks deployed on May 11

### RPA Support
- 4 support rotations: Weeks 8, 12, 16, 20
- CAIS Deadline hotfix (Jun 8, IISS-706, 7h): UCM credential validation, empty creds from Secrets Manager rotation
- MESO month-end stuck tasks (Jul 1, IISS-741, Critical): retrigger for INNOCAP/SAMLMOS
- VPL IPV UI selector failure (Jul 8, IISS-753): 16h estimate
- VPL Pricing GTL incorrect booking (Jul 30, IISS-876)
- RPA platforms: Blue Prism (BPM) for daily/monthly/quarterly fund ops, UiPath Cloud + on-prem
- Key processes monitored: VPL (5 PM EST queue, 3 bots), Corporate Actions (Mandatory/Voluntary/Ops Transfer)

### SRE Context
- 4 golden signals: Latency, Traffic, Errors, Saturation (from Kri's training session May 25)
- Grafana AMG: Amazon Managed Grafana workspace, CloudWatch as data source
- CloudFormation IaC: parameterized YAML templates, Lambda provisioner for dynamic alarm deployment
- Observability gap (pre-internship): no proactive monitoring on Meridian, relied on business teams to flag issues
- MSK consumer lag: detection improved from 2–3 min to <30 sec after dashboard deployment
- Tag-based resource discovery: AppName tag required because CITCOWORKS and MERIDIAN share "Shared Cloud Artifacts" BudgetCode
- CloudWatch Metric Insights SQL limitation: only AVG/SUM/MIN/MAX (no p50/p99 in GROUP BY mode)

### Mitacs BSI Context
- Project: IT49539, title "Intelligent Automation and Reliability Engineering for Financial Services"
- Academic supervisor: Dr. Pawan Lingras, Saint Mary's University
- Industry supervisor: Mr. Kishor Deotale (Manager, CTM)
- 900 hours: Mar 15 – Aug 31, 2026
- Extension: Sept 1 – Dec 31, 2026 (Mitacs BSI renewal, $15,000 stipend)
- Graduation expected: December 2027

### Team
- Mentors: Ho Hoi Leung (Horace) — RPA Support KT, Kristia Marie Labos (Kri) — SRE KT, golden signals
- Co-interns: Sridhar Vadla, Soundarya Venkataraman
- CitcoWorks/Event Store KT: Bhanu Teja Murari (BMurari@citco.com, Innovation IT, HYD1)

### Training Week (Apr 13–18)
- Topics: RPA support processes, Blue Prism/UiPath architecture, CitcoWorks platform, Meridian platform
- Meridian platform: event processing (Event Routing Service, Action Processor, OpenSearch consumer)
- Æxeo Treasury platform (cloud-based wire approval and fund movement)
- MESO: high-memory/CPU autoscale issue (IISS-538 ~Jun 5)
- Event Store: structured logging, process identifiers, run IDs

### Kiro AI IDE (for ch3_tools.tex)
- Kiro: AI-powered development environment built on VS Code
- Used for: spec-driven development (Requirements → Design → Tasks), steering files, hooks, agentic execution
- Enabled rapid scaffolding of the ia-sre-resources-inventory Flask API (IISS-507)
- Kiro's spec workflow: .kiro/specs/ directory with requirements.md, design.md, tasks.md
- Agentic execution: sub-agents write code, run tests, create PRs autonomously
- Other AI tools: Amazon Q (memory bank), Claude Sonnet 4.5/4.6 (via Kiro), GitHub Copilot patterns

## Out of scope
- Do NOT modify `about_company.tex`, `work_logs.tex`, `cover_letter.tex`
- Do NOT delete any existing stub chapter files
- Do NOT run the build pipeline — just write the LaTeX source files
