# Submission 2 — Feedback Response

**Student:** Bhavik Kantilal Bhagat | A00494758
**Program:** MSc Computing and Data Analytics, Saint Mary's University
**Submission:** Mentor Submission 2 (September 2026)
**Previous Score:** 55/100 (Submission 1)

---

## How I Addressed Each Feedback Point


| #  | Feedback                                                                                                  | How Addressed                                                                                                                                                                                                                                                                                                                                                                            |
| ---- | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1  | **Cover Page** — font size for course number, A-number, and other details should match the sample report | Revised title page so that all cover page elements (course number MCDA 5585/5586, A-number, name, supervisors, degree) use a consistent 20pt bold Calibri hierarchy, matching the sample report formatting. Labels ("Submitted By:", "under the guidance of:") are in 14pt italic.                                                                                                       |
| 2  | **Mr./Ms. prefixes** — use appropriate prefixes for all individuals mentioned by name                    | All named individuals now carry correct prefixes throughout the report: Dr. Pawan Lingras, Mr. Kishor Deotale, Mr. Ho Hoi Leung, Ms. Kristia Marie Labos, Mr. Sridhar Vadla, Ms. Soundarya Venkataraman. Verified across all 15 chapters.                                                                                                                                                |
| 3  | **Certificate** — content and structure should follow the sample report exactly                          | Certificate page restructured to match the sample: single certifying paragraph followed by two-column signature blocks (Academic Supervisor left, Industry Supervisor right) with dotted signature lines and full institutional addresses.                                                                                                                                               |
| 4  | **Remove unnecessary headers** from the report                                                            | All orphan or redundant section headers removed. Created a box around text as per the sample report.                                                                                                                                                                                                                                                                                     |
| 5  | **Table of Contents** — font color should be black; only headings up to the second level                 | TOC font color is now black throughout (`\color{black}` applied to all TOC entries). Depth limited to level 1 (`\setcounter{tocdepth}{1}`), showing only chapters and sections — no subsections in TOC.                                                                                                                                                                                 |
| 6  | **List of Figures and List of Tables** — numbered starting from 1                                        | Both lists now start from 1 and are numbered sequentially. List of Figures: Figures 1–14. List of Tables: Tables 1–13. Verified in the compiled PDF.                                                                                                                                                                                                                                   |
| 7  | **Page numbers** — should be black or grey, not red                                                      | Page footer numbers are now rendered in grey (`#7F7F7F`). Maroon/red colour is reserved exclusively for chapter titles, section headings, and figure/table labels. Verified programmatically against the compiled PDF.                                                                                                                                                                   |
| 8  | **Excessive blank space on page 7** — move next section up                                               | Spacing adjustments applied, and no excessive gaps. If gap appears that is because only chapter/section heading could fit on that page at bottom without content for that section on the same page -- hence pushed to new page. Reviewed entire document for similar orphan space issues.                                                                                             |
| 9  | **JIRA ticket numbers** — do not provide meaningful context, please remove                               | All`IISS-xxx` numbered ticket references removed from the report body. The only remaining JIRA reference is a board name mention in Week 1 context ("the Citco JIRA board (IISS project)") which provides contextual meaning for the reader, not a ticket number.                                                                                                                        |
| 10 | **"Three insights…" heading** — move so heading and text begin on the same page                         | `\Needspace*` directive applied before the "Key Insights" subsection heading in Chapter 8 to ensure the heading and its following content always appear on the same page. Verified in compiled PDF — heading and all three insights appear together on page 31. (covered by #8)                                                                                                         |
| 11 | **Section 8.3 table placement** — tables should be within the section where they are discussed           | Requirements tables (Functional Requirements, Non-Functional Requirements) are now placed directly within their respective subsections (8.3.1 and 8.3.2) where they are introduced and discussed, not in a separate stub subsection.                                                                                                                                                     |
| 12 | **Separate subsections for only 1–2 lines** — combine short subsections with related sections           | Reviewed all chapters. Short stub subsections merged into their parent sections. Every subsection now contains substantive content — at minimum a full paragraph plus supporting detail.                                                                                                                                                                                                |
| 13 | **Implementation section** — revise to describe personal work in first person                            | Chapter 10 (Implementation & Architecture) is completely revised. Language changed to first-person throughout: "I implemented…", "I configured…", "I developed…", "I built…", "I added…". 29+ first-person action statements confirmed. Diagrams retained as they were original deliverables created during the placement (confirmed acceptable per clarification email).           |
| 14 | **Weekly Implementation** — each week should contain approximately one full page of content              | Chapter 11 expanded to 1,415 lines across 25 weeks. Full-time weeks (5–24) average 1–1.5 pages each. Part-time weeks (1–4) contain detailed content proportional to the 10–20h/week schedule confirmed by Dr. Pawan Lingras. Structure follows: context → technical work → outcomes per week. Also, Chapter 11 Weekley Implementation is revised, and chaged to first person tone. |
| 15 | **Work Logs** — tasks >4 hours should be broken into smaller realistic time blocks                       | All tasks in WorkLogs.xlsx are ≤4 hours. Verified programmatically: 0 tasks exceed 4 hours across all 25 weeks. Weeks 4–5 onwards (flagged in clarification email) have 10–19 tasks per week with granular descriptions. Total: 900 hours across 25 weeks.                                                                                                                            |
| 16 | **Appendix with feedback table**                                                                          | Feedback appendix added to the Cover Letter (Page 2) with a formatted table containing Date, Score, and full Feedback columns. All 16 feedback bullet points from Submission 1 are included.                                                                                                                                                                                             |

---

## Additional Improvements (Beyond Feedback)

- **Heading bold consistency:** All subsection (x.y.z) and subsubsection headings now use `\bfseries` (Calibri-Bold) consistently — previously `\fontseries{b}` was causing lighter rendering at the subsection level.
- **Subsubsection numbering:** 4th-level headings (used only in Chapter 10) are now unnumbered as they are navigational labels within a subsection, not independent numbered sections.
- **Long technical terms:** `\allowbreak{}` added inside long `\texttt{}` identifiers to prevent page-width overflow (e.g. `rpacfs1-cais-pricing-extract-genai-infrastructure`).
- **Table numbering:** Sequential table numbering verified — Tables 1–13 with no gaps.
- **URL hyperlink color:** References URLs now render in standard blue (hyperlinks) rather than maroon, consistent with web conventions.

---

## Grammarly & Language Corrections (Post-Submission 1)

The report was reviewed against Grammarly and a peer language review (Christine, Sep 21, 2026). The following corrections were applied:

| # | Location | Correction |
|---|----------|------------|
| 1 | Ch1 Acknowledgements | `explore new technology stack` → `explore a new technology stack` (missing article) |
| 2 | Ch3 Team Composition | `The co-op period team comprised` → `The team during the co-op period comprised` (word order) |
| 3 | Ch4 Tools | `CloudWatch Container Insights enabled to surface` → `enabled for task-level CPU and memory telemetry` (ambiguous phrasing) |
| 4 | Ch4 Tools | `Universal database client` → `Universal database clients` (plural); dropped `across the platforms` |
| 5 | Ch5 Project | `production quality and reliability improvement` → `production-quality and reliability improvement` (compound adjective hyphen) |
| 6 | Ch6 Project Goals | Architecture plan bullet — added em dashes around list to clarify `plan...is produced` subject-verb |
| 7 | Ch7 Learning Goals | `dual competency development expected` → `expected dual competency development` (word order) |
| 8 | Ch9 Methodologies | `signal most relevant to the April 17, 2026` → `most relevant signal to the April 17, 2026,` (word order + comma after year) |
| 9 | Ch10 Implementation | `I added on introduced` → `that I added uses a` (broken verb removed) |
| 10 | Ch10 Implementation | `Lambda-backed CloudFormation provisioner I deployed` → `provisioner that I deployed` (relative clause added) |
| 11 | Ch10 Implementation | `at the scale required` → `at the required scale` (word order) |
| 12 | Ch10 Implementation | `provisioner bootstrap --- acceptable` → `provisioner bootstrap, which is acceptable` (dangling modifier fixed) |
| 13 | Ch10 Implementation | `One lightweight ALB call per library` → `ALB calls` (plural) |
| 14 | Ch11 Weekly Breakdown | `The first added AutomationHub` → `In the first, I added AutomationHub`; `platform JIRAs` → `platform updates` (JIRA reference removed) |
| 15 | Ch11 Weekly Breakdown | `80-minute session` — added `an` before for grammatical article |
| 16 | Ch11 Weekly Breakdown | `commit-dense day` → `highest-commit day` (informal → formal) |
| 17 | Ch11 Weekly Breakdown | `I merged the release/SRE branch to master` → `into main` (correct git preposition and branch name) |
| 18 | Ch11 Weekly Breakdown | `Each morning I reviewed` → `Each morning, I reviewed` (comma after introductory phrase) |
| 19 | Ch11 Weekly Breakdown | `datasource` → `data source` (two words) — standardized consistently across all chapters |
| 20 | Ch11 Weekly Breakdown | `re-notification` → `renotification` (American English, no hyphen needed) |
| 21 | Ch11 Weekly Breakdown | `grew the test suite from 60%` → `increased test coverage from 60%` |
| 22 | Ch11 Weekly Breakdown | `grew the test suite to 562 tests` → `increased the test suite to 562 tests` |
| 23 | Ch11 Weekly Breakdown | `timeseries panels` → `time-series panels` (compound adjective hyphen) |
| 24 | Ch11 Weekly Breakdown | `files were too large for email` → `too large to send by email` (rephrased parenthetical) |
| 25 | Ch11 Weekly Breakdown | `140 hours` reference removed from Week 14 summary |
| 26 | Ch13 Achievements | `sub-30-second automated alerting...qualitative step change` → `automated alerting in under 30 seconds...substantial improvement` |
| 27 | Ch13 Achievements | `April 17, 2026 Meridian incident` → `April 17, 2026, Meridian incident` (comma after year) |
| 28 | Ch15 Future Work | `2--3 hour window` → `2--3-hour window` (compound adjective hyphen) |

---

## Submission Bundle


| File                                      | Description                            |
| ------------------------------------------- | ---------------------------------------- |
| `BhavikBhagat_A00494758_CoverLetter.pdf`  | Cover letter + feedback appendix table |
| `BhavikBhagat_A00494758_MajorReport.pdf`  | Main project report (129 pages)        |
| `BhavikBhagat_A00494758_MajorReport.docx` | Word format of report                  |
| `BhavikBhagat_A00494758_WorkLogs.xlsx`    | Weekly work logs (900 hours, 25 weeks) |
| `BhavikBhagat_A00494758_WorkLogs.pdf`     | PDF export of work logs                |

---

## Appendix B — Glossary of Terms and Abbreviations

A glossary appendix was added to the report (Appendix B) to assist readers unfamiliar with AWS, SRE, and Citco-specific terminology.

### AWS Services

| Term | Definition |
|------|-----------|
| AMG | Amazon Managed Grafana — fully managed Grafana service for observability dashboards |
| CloudFormation | AWS Infrastructure-as-Code service for provisioning resources via YAML/JSON templates |
| CloudWatch | AWS native observability service for metrics, logs, alarms, and dashboards |
| ECS | Amazon Elastic Container Service — managed container orchestration |
| ECR | Amazon Elastic Container Registry — managed Docker image registry |
| EKS | Amazon Elastic Kubernetes Service — managed Kubernetes |
| IAM | AWS Identity and Access Management |
| MSK | Amazon Managed Streaming for Apache Kafka |
| RDS | Amazon Relational Database Service |
| S3 | Amazon Simple Storage Service |
| SAM | AWS Serverless Application Model — Lambda deployment extension of CloudFormation |
| SNS | Amazon Simple Notification Service — pub/sub alarm fan-out |
| SQS | Amazon Simple Queue Service — managed message queue |
| SSM | AWS Systems Manager Parameter Store |
| X-Ray | AWS distributed tracing service |

### SRE and Observability

| Term | Definition |
|------|-----------|
| ADOT | AWS Distro for OpenTelemetry — distributed tracing collector |
| APM | Application Performance Monitoring |
| Error Budget | Permitted unreliability before SLO breach; calculated as 1 minus SLO target |
| Four Golden Signals | SRE minimum instrumentation: Latency, Traffic, Errors, Saturation |
| IaC | Infrastructure-as-Code |
| SLI | Service Level Indicator — specific metric measuring one golden signal |
| SLO | Service Level Objective — target threshold on an SLI |
| SRE | Site Reliability Engineering |

### Citco Platforms and Internal Terms

| Term | Definition |
|------|-----------|
| AutomationHub | UiPath-based RPA platform; one of the six IA budget_code platforms |
| BPM | Blue Prism — legacy RPA tool at Citco |
| budget_code | AWS resource tag attributing resources to a platform or cost centre |
| CAIS | Citco Alternative Investment Services pricing pipeline |
| CitcoWorks | Citco operations platform using Amazon Neptune for entity graph storage |
| CTM | Citco Technology Management — internal technology division |
| Follow-the-Sun | 24/7 RPA support model rotating across Manila, Dublin, and Halifax |
| ia-bpo | One of the six IA budget_code platforms |
| IA-IT-SRE | Intelligent Automation IT Site Reliability Engineering team |
| Meridian | Citco event processing platform using MSK Kafka and OpenSearch |
| MESO | Month-End Statement Operations — automated month-end reconciliation pipeline |
| rpacfs1 | One of the six IA budget_code platforms hosting the CAIS Pricing Extract pipeline |
| SD Portal | Service Desk Portal — internal ticketing system for RPA L2 support |
| UiPath | Cloud/on-premises RPA platform for new automation at Citco |
| VPL | Virtual Position Ledger — daily fund valuation process with 5 PM EST deadline |

### General Technical Terms

| Term | Definition |
|------|-----------|
| API | Application Programming Interface |
| BSI | Mitacs Business Strategy Internship |
| CI/CD | Continuous Integration / Continuous Deployment |
| KT | Knowledge Transfer |
| LLM | Large Language Model |
| MCDA | Master of Science in Computing and Data Analytics (SMU) |
| MSK consumer lag | Kafka messages awaiting consumption; primary SLI for Meridian health |
| OOM | Out of Memory — Lambda failure from exceeding memory allocation |
| PoC | Proof of Concept |
| RAG | Retrieval-Augmented Generation — LLM architecture with knowledge base retrieval |
| RCA | Root Cause Analysis |
| RPA | Robotic Process Automation — Blue Prism or UiPath automated workflows |
| SMU | Saint Mary University, Halifax, Nova Scotia |
| TDD | Test-Driven Development |
| WS | Work Stream — one of six parallel workstreams (WS1-WS6) |
