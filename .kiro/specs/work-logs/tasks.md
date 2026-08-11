# Tasks: Work Logs Generation

## Phase 1: Branch & Setup
- [ ] Checkout or create `feature/work-logs` branch from `main`
- [ ] Verify all 20 repo paths are accessible and have `.git` directories

## Phase 2: Extract Commits
- [ ] Run `git log --oneline --after="2026-03-14" --author="bbhagat\|Bhavik"` across all repos
- [ ] Aggregate commits by date into a single timeline
- [ ] Map JIRA tickets from branch names and commit messages

## Phase 3: Generate Daily Markdown Files
- [ ] `smu/work-logs/2026-03/` — weeks 1–4 (part-time onboarding)
- [ ] `smu/work-logs/2026-04/` — training week + transition to full-time
- [ ] `smu/work-logs/2026-05/` — Grafana dashboard intensive
- [ ] `smu/work-logs/2026-06/` — dashboard completion + hotfixes
- [ ] `smu/work-logs/2026-07/` — SQS feature + support shifts
- [ ] `smu/work-logs/2026-08/` — final delivery + report writing

## Phase 4: Generate Excel
- [ ] Aggregate all markdown files into `output/WorkLogs.xlsx`
- [ ] Apply Francis format (Week | Date | Day | Task | Hrs | Cumulative)
- [ ] Add color-coding by weekday
- [ ] Add Legend sheet and Summary sheet
- [ ] Verify total = 900 hours

## Phase 5: Generate PDF
- [ ] Export `output/WorkLogs.xlsx` → `output/WorkLogs.pdf`
- [ ] Fallback: use LibreOffice if available, else flag for manual export

## Phase 6: LaTeX Integration
- [ ] Update `latex-report/appendices/work_logs.tex` with actual weekly totals
- [ ] Group by phase (Onboarding / Training / Core Dev / Delivery)

## Phase 7: Commit
- [ ] Commit all markdown files to `feature/work-logs`
- [ ] Commit `output/WorkLogs.xlsx` and `output/WorkLogs.pdf`
- [ ] Merge `feature/work-logs` → `release/v1.0` → `main`
