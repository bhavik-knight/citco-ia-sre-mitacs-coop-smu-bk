# PROJECT CONTEXT & RULES (SMU MCDA Major Project Report)

## 1. Official Mitacs & Citco Internship Information
- **Student Name**: Bhavik Kantilal Bhagat
- **Student ID**: A00494758
- **Program**: Master of Science in Computing and Data Analytics (MCDA)
- **University**: Saint Mary's University, Department of Mathematics and Computing Science, Halifax, NS
- **Academic Supervisor**: Dr. Pawan Lingras
- **Partner Organization**: Citco Technology Management (CTM) / Citco (Canada) Inc.
- **Manager / Industry Supervisor**: Mr. Kishor Deotale
- **Senior Team Mentors**: Ho Hoi Leung (Horace), Kristia Marie Labos (Kri)
- **SMU Co-workers & Team Members**: Sridhar Vadla, Soundarya Venkataraman
- **Funding Application**: Mitacs Business Strategy Internship (BSI) IT49539
- **Official Project Title**: *Intelligent Automation and Reliability Engineering for Financial Services*
- **Internship Start Date**: March 15, 2026
- **Internship End Date**: August 31, 2026
- **Total Logged Hours**: 900 hours
- **Work Schedule**:
  - March 15 -- April 15, 2026: Part-time transition (~10--20 hours/week)
  - April 15 -- August 31, 2026: Full-time (~40+ hours/week)

## 2. Technical Architecture & Project Streams (Mitacs BSI Scope)
- **Stream 1: Site Reliability Engineering (SRE) & Operational Observability**
  - SLIs/SLOs definition, Telemetry instrumentation (Prometheus/Grafana), Golden signals monitoring
  - Intelligent BOT Operations & RPA Reliability engineering
  - Automated Disaster Recovery (DR) validation and health check probes
  - Performance optimization & high-throughput financial system tuning
- **Stream 2: Intelligent Automation & Predictive Operations**
  - AI-driven Incident Prediction & Log Anomaly Detection (Machine Learning, Root-Cause Analysis / RCA)
  - Self-Healing Systems (Automated runbooks, remediation scripts, configuration drift detection)
  - Infrastructure-as-Code (Terraform/Ansible) & Secure CI/CD pipelines
  - Policy-as-Code & Automated Release Orchestration
- **Stream 3: Advanced Monitoring & Capacity Analytics**
  - Real-Time Synthetic Monitoring Probes & SLA tracking calculators
  - Predictive Analytics & Capacity Forecasting for cloud/on-prem financial infrastructure

## 3. Neeyati Mehta Benchmark Structure in `latex-report/`
- **Title Page**: Single-page layout with high-res SMU Logo & SMU Maroon theme (`#8A0027`)
- **Pages (`pages/`)**: Title Page, Dual-Sign Certificate (Dr. Lingras + Kishor Deotale), Acknowledgements (Horace, Kri, Sridhar, Soundarya), Abstract & 900h Statement
- **Chapters (`chapters/`)**:
  - `chapters/about_company.tex`: Citco Technology Management Canada & CTM Team Structure
  - `chapters/project_overview.tex`: Project Background, Scope & Subprojects
  - `chapters/learning_goals.tex`: Technical & Non-Technical Learning Goals
  - `chapters/tools_technologies.tex`: Tools, Infrastructure & Technologies
  - `chapters/requirements_elicitation.tex`: Stakeholder Identification & Elicitation
  - `chapters/methodologies.tex`: Data Preprocessing, ML & SRE Methodologies
  - `chapters/implementation.tex`: Detailed System Architecture & Pipeline Code
  - `chapters/weekly_breakdown.tex`: Weekly Implementation Narrative (Weeks 1..24)
  - `chapters/challenges_achievements.tex`: Achievements, Technical Challenges & Mitigation
  - `chapters/conclusion.tex`: Conclusions, Timesheet Summary & Future Scope
- **Appendices (`appendices/`)**: Work Logs Summary

## 4. Strict 5-File Submission Bundle (`output/`)
Automated via `uv run python build_reports.py`:
1. `output/CoverLetter.pdf`: Cover Letter + Feedback Appendix table
2. `output/Project_Report.pdf`: Compiled LaTeX Report (20-page benchmark)
3. `output/Project_Report.docx`: Converted DOCX report via `pdf2docx`
4. `output/WorkLogs.xlsx`: Detailed weekly activity log (900h)
5. `output/WorkLogs.pdf`: PDF export of `WorkLogs.xlsx`
