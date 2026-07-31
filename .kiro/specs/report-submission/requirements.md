# Requirements: Report Submission — August 1, 2026

## Deadline
August 1, 2026 (night) — all 5 files must be ready.

## Deliverables (Strict 5-File Bundle)
1. `output/CoverLetter.pdf`
2. `output/Project_Report.pdf` (20-page benchmark, LaTeX compiled)
3. `output/Project_Report.docx` (auto-converted from PDF)
4. `output/WorkLogs.xlsx` (900-hour weekly timesheet)
5. `output/WorkLogs.pdf` (PDF export of xlsx)

## Current State

### Done
- [x] LaTeX structure (10 chapters, front matter, appendices)
- [x] `chapters/about_company.tex` — fully populated
- [x] Cover letter template exists (`cover_letter.tex`)
- [x] Build pipeline works (`build_reports.py` + MiKTeX)
- [x] Work logs generator produces xlsx (major_project + internship modes)
- [x] Calendar meetings parsed (119 hrs)
- [x] Ad-hoc calls logged (20.5 hrs)
- [x] Knowledge base consolidated (30 files)
- [x] Full JIRA context captured (IISS-487: 140h, plus 7 other tickets)
- [x] RPA support context captured (4 weeks, 35 tickets, 5 JIRAs)

### Needs Work
- [ ] Chapter 2: Project Overview & Scope
- [ ] Chapter 3: Learning Goals
- [ ] Chapter 4: Tools & Technologies
- [ ] Chapter 5: Requirements Elicitation & Stakeholders
- [ ] Chapter 6: Technical Methodologies
- [ ] Chapter 7: Implementation & Architecture (main content chapter)
- [ ] Chapter 8: Weekly Implementation Breakdown
- [ ] Chapter 9: Challenges, Achievements & Mitigation
- [ ] Chapter 10: Conclusion & Future Scope
- [ ] Cover letter finalization
- [ ] Work logs xlsx with accurate weekly hours
- [ ] Final build and verify all 5 files

## Content Sources for Chapters

### Chapter 2 (Project Overview)
- IISS-487 description (Grafana dashboard scope)
- IISS-482 description (IA Resources monitoring)
- Mitacs BSI renewal form (project title, streams)
- .ai-agent/CONTEXT.md (3 project streams)

### Chapter 3 (Learning Goals)
- Technical: AWS (CloudWatch, Grafana, ECS, Lambda, X-Ray), Python, IaC, SRE practices
- Non-technical: Agile, JIRA workflow, cross-team communication, production incident response

### Chapter 4 (Tools & Technologies)
- AWS services (CloudWatch, Grafana, ECS, Lambda, S3, CloudFormation, SSM, X-Ray)
- Python (boto3, pytest, Hypothesis, structlog, Flask)
- RPA platforms (Blue Prism, UiPath Cloud/On-Prem)
- DevOps (Git/CodeCommit, cfn-lint, pre-commit)
- Databases (PostgreSQL, SQL Server, DBeaver)
- Monitoring (Grafana, CloudWatch Logs Insights, Container Insights)

### Chapter 5 (Requirements)
- Kishor as primary stakeholder (requested IISS-487)
- SRE team needs (single-pane dashboard, alerting, auto-healing roadmap)
- RPA support team needs (process monitoring, incident response)

### Chapter 6 (Methodologies)
- Agile/Kanban (JIRA board, sprints)
- IaC (CloudFormation, parameterized templates)
- Test-driven development (960+ tests, property-based testing)
- Design-first approach (.kiro specs, requirements→design→tasks)

### Chapter 7 (Implementation) — MOST IMPORTANT
- Grafana dashboard architecture (14 rows, 110+ panels, Lambda provisioner)
- Resource discovery API (3-tier fallback, tag-based discovery)
- Alarm notification pipeline (Re-Notifier Lambda, composite alarms)
- CloudWatch dashboard platform (Lambda/EC2/ECS/EKS/SQS)
- CAIS Deadline hotfix (credential validation, fail-fast)
- Container Insights audit and reversion
- RPA support process improvements

### Chapter 8 (Weekly Breakdown)
- Weeks 1-4: Part-time, onboarding, access setup, AWS learning
- Week 5: Training week (full-time transition)
- Weeks 6-7: CloudWatch dashboards (IISS-455, 469)
- Weeks 8: Support shift #1 + Grafana IISS-487 kickoff
- Weeks 9-11: Grafana dashboard intensive (May 11-27, 80+ hours)
- Week 12: Support shift #2 + IISS-538/706
- Weeks 13-15: Dashboard completion (alarms, deep-links, restructure)
- Week 16: Support shift #3 + IISS-741
- Weeks 17-19: SQS feature, backend API, X-Ray investigation
- Week 20: Support shift #4 + IISS-876

### Chapter 9 (Challenges & Achievements)
- Achievements: 140h Grafana dashboard, 960+ tests, 5 production JIRAs
- Challenges: IAM permissions, Secrets Manager 64KB limit, CloudWatch limitations
- Mitigation: Multi-agent system, S3 migration, AppName fallback pattern

### Chapter 10 (Conclusion)
- Summary of contributions
- Future scope: X-Ray tracing, auto-healing, UAT/PRD deployment

## Priority Order
1. Chapter 7 (Implementation) — longest, most important
2. Chapter 2 (Project Overview) — sets the stage
3. Chapter 8 (Weekly Breakdown) — shows progression
4. Chapter 9 (Challenges/Achievements) — demonstrates value
5. Chapters 3, 4, 5, 6 — shorter, template-driven
6. Chapter 10 (Conclusion) — brief wrap-up
7. Cover letter finalization
8. Work logs xlsx update
9. Final build → 5 files
