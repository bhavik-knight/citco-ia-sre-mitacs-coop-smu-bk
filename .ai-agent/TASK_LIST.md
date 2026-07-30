# TASK LIST - SMU MCDA Major Project Report

## Phase 1: Context & Setup (Completed)
- [x] Analyze `templates/reportWritingGraduationProcess.pdf` for program rules and deadlines
- [x] Analyze Neeyati Mehta's high-scoring benchmark report (`NeeyatiMehta_A00477369_projectReport.pdf`), cover letter, and work logs
- [x] Establish consolidated AI context memory bank in `.ai-agent/`
- [x] Verify LaTeX compiler (`pdflatex`), `pandoc` (v3.7.0.2), and `pdf2docx` toolchain

## Phase 2: Report Structure (Completed - Neeyati Mehta Standard)
- [x] Create modular LaTeX structure in `latex-report/`:
  - [x] `pages/title_page.tex` (Title Page)
  - [x] `pages/certificate.tex` (Dual-signature Certificate)
  - [x] `pages/acknowledgements.tex` (Acknowledgements)
  - [x] `pages/abstract.tex` (Abstract & Statement of Hours)
  - [x] `chapters/about_company.tex` (Ch 1: About Company & Team)
  - [x] `chapters/project_overview.tex` (Ch 2: Project Overview & Scope)
  - [x] `chapters/learning_goals.tex` (Ch 3: Technical & Non-Technical Learning Goals)
  - [x] `chapters/tools_technologies.tex` (Ch 4: Tools & Technologies)
  - [x] `chapters/requirements_elicitation.tex` (Ch 5: Requirements Elicitation & Stakeholders)
  - [x] `chapters/methodologies.tex` (Ch 6: Technical Methodologies)
  - [x] `chapters/implementation.tex` (Ch 7: In-Depth Implementation & Architecture)
  - [x] `chapters/weekly_breakdown.tex` (Ch 8: Weekly Implementation Breakdown)
  - [x] `chapters/challenges_achievements.tex` (Ch 9: Achievements, Challenges & Mitigation)
  - [x] `chapters/conclusion.tex` (Ch 10: Conclusion & Future Scope)
  - [x] `appendices/work_logs.tex` (Appendix: Hourly Activity Logs Summary)

## Phase 3: Drafting & Content Population (Next)
- [ ] Receive project metadata (Project Title, Company Name, Industry Supervisor Name/Title, Date Ranges)
- [ ] Populate Chapter 1 (About Company & Team)
- [ ] Populate Chapter 2 (Project Overview) & Chapter 3 (Learning Goals)
- [ ] Populate Chapter 4 (Tools & Tech) & Chapter 5 (Requirements)
- [ ] Populate Chapter 6 (Methodologies) & Chapter 7 (Implementation)
- [ ] Populate Chapter 8 (Weekly Breakdown) & Chapter 9 (Challenges & Achievements)
- [ ] Prepare Excel log file template (`WorkLogs.xlsx`) with weekly breakdown (200h tech + 40h writing)
- [ ] Export PDF copy of logs (`WorkLogs.pdf`)

## Phase 4: Compilation & 5-File Bundle Packaging
- [x] Verify LaTeX build to `main.pdf`
- [x] Verify automated conversion to `Project_Report.docx` via `pdf2docx`
- [ ] Package final 5-file bundle:
  1. `CoverLetter.pdf`
  2. `Project_Report.pdf`
  3. `Project_Report.docx`
  4. `WorkLogs.xlsx`
  5. `WorkLogs.pdf`
