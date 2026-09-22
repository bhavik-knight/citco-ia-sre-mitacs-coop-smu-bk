# Grammarly Corrections — LaTeX Change Table

Generated from `correction.txt` (Christine, 2026-09-21).
Each row shows the file, exact current text in LaTeX, and the corrected text.

---

## Part 1 — Specific Page Corrections

| # | File | Current Text in LaTeX | Corrected Text | Status |
|---|------|-----------------------|----------------|--------|
| 1 | [acknowledgements.tex](../latex-report/pages/acknowledgements.tex) | `explore new technology stack that had not` | `explore a new technology stack that had not` | ✅ Fixed |
| ~~2~~ | ~~[certificate.tex](../latex-report/pages/certificate.tex)~~ | ~~`fulfillment`~~ | ~~`fulfilment`~~ | ❌ Removed — `fulfillment` is correct American English spelling |
| 3 | [new_ch03_team_composition.tex](../latex-report/chapters/new_ch03_team_composition.tex) | `The co-op period team comprised the following members:` | `The team during the co-op period comprised the following members:` | ✅ Fixed |
| 4 | [new_ch10_implementation.tex](../latex-report/chapters/new_ch10_implementation.tex) line 173 | `The SQS monitoring feature I added on introduced a` | `The SQS monitoring feature that I added uses a` | ✅ Fixed |
| 5 | [new_ch10_implementation.tex](../latex-report/chapters/new_ch10_implementation.tex) line 425 | `The IaC layer is a \textbf{Lambda-backed CloudFormation provisioner}` *(followed by newline then `I deployed via AWS SAM`)* | `The IaC layer is a \textbf{Lambda-backed CloudFormation provisioner} that I deployed via AWS SAM.` | ✅ Fixed |
| 6 | [new_ch11_weekly_breakdown.tex](../latex-report/chapters/new_ch11_weekly_breakdown.tex) line 624 | `consistent series colors across all timeseries panels` | `consistent series colors across all time-series panels` | ✅ Fixed |
| 7 | [new_ch11_weekly_breakdown.tex](../latex-report/chapters/new_ch11_weekly_breakdown.tex) line 1188 | `I grew the test suite from 60\% to 100\%` | `I increased test coverage from 60\% to 100\%` | ✅ Fixed |
| 8 | [new_ch11_weekly_breakdown.tex](../latex-report/chapters/new_ch11_weekly_breakdown.tex) line 1091 | `I grew the test suite to 562 tests at 99\% coverage` | `I increased the test suite to 562 tests at 99\% coverage` | ✅ Fixed |
| 9 | [new_ch11_weekly_breakdown.tex](../latex-report/chapters/new_ch11_weekly_breakdown.tex) line 1384 | `instead delivered the reports to business users via Microsoft Teams (files were too large for email).` | `instead delivered the reports to business users via Microsoft Teams because the files were too large to send by email.` | ✅ Fixed |

---

## Part 2 — DOCX-Only Changes (update manually in Word)

These items exist only in the DOCX — not in LaTeX. Find them in Word using the section and page references below.

| # | PDF Page | Section | Find in Word | Change to | Status |
|---|----------|---------|--------------|-----------|--------|
| A | p.51 | 10.4.4 Tag-Based Discovery | `two-stage filterin both` | `two-stage filter in both` | ✅ Already correct in LaTeX / check DOCX |
| B | p.61 | 10.3.4 Layer 4: IaC Provisioner | `provisionerI deployed` | `provisioner I deployed` | ✅ Already correct in LaTeX / check DOCX |
| C | p.65 | 10.7.1 Planning Document Deliverable | `started initial implementation` | `began the initial implementation` | ✅ Fixed in LaTeX (ch10 line 1004) |
| D | p.73 | 11.4 Week 4 (AWS learning) | `schema less design` | `schema-less design` | ✅ Fixed in LaTeX (ch11 line 52) |
| E | p.74 | 11.3 Week 3 (CTI dashboard) | `I first added CloudWatch metrics instrumentation` | No change needed — `first added` is correct here (means "the first thing I added") | ❌ Not a real issue |
| F | p.94 | 11.16 Week 16 | `80-minutes session on Thursday` | `an 80-minute session on Thursday` | ✅ Fixed in LaTeX (ch11 line 876) |
| G | p.94 | 11.21 Week 21 | `grew the test suite from 60% to 100%` | `increased test coverage from 60% to 100%` | ✅ Fixed in LaTeX |
| H | p.112 | 13.2.1 Incident Detection: From Hours to Seconds | `sub-30-second automated alerting represents a qualitative step change` | `automated alerting in under 30 seconds represents a substantial improvement` | ✅ Fixed in LaTeX (ch13 lines 106-107) |

---

## Part 3 — Global Find & Replace

| # | Find | Replace With | File scope | Status |
|---|------|-------------|------------|--------|
| 1 | `after-thought` | `afterthought` | All chapters | ✅ Not found — already correct |
| 2 | `screensharing` | `screen sharing` | All chapters | ✅ Not found — already correct |
| 3 | `follow the sun` / `follow-the-sun` | `Follow-the-Sun` (standardize) | All chapters | ✅ Not found — already correct |
| 4 | `workstream` | `work stream` | All chapters | ✅ Not found — already correct |
| 5 | `timeseries` | `time-series` (as modifier) or `time series` (as noun) | `new_ch11_weekly_breakdown.tex` | ✅ Fixed |
| 6 | `co-op placement` | Ensure consistent hyphenation throughout | All chapters | ✅ Consistent — `co-op` used correctly throughout |
| 7 | `real time` vs `real-time` | `real-time` when compound adjective, `real time` as adverb | All chapters | ✅ Both usages correct — `in real time` (adverb, no hyphen), `real-time health status` (adjective, hyphenated) |
| 8 | `codebase` / `code base` | Use `codebase` consistently | All chapters | ✅ `codebase` used consistently — `code base` not found anywhere |

---

## Part 4 — Observations (Your Decision Needed)

| # | Issue | Current usage | Recommendation |
|---|-------|--------------|----------------|
| 1 | AWS terminology | Alternates between `CloudWatch Metric Insights SQL`, `Metrics Insights SQL`, `Metric Search API` | ✅ Verified — all three are contextually correct. `CloudWatch Metric Insights SQL` and `Metric Insights SQL` are the same feature (short form acceptable). `SEARCH()` is a distinct older mechanism correctly identified as what was replaced. `Metric Search API` does not appear in LaTeX. No changes needed. |
| 2 | Dashboard row counts | Report mentions 13, 14, and 17 rows at different points | ✅ Verified — counts reflect different development stages: 13 rows at end of Week 11, 14 rows at v1 release (140h delivery), 17 rows as final state in ch10 implementation overview. Context is clear and correct — no changes needed. |
| 3 | Informal phrases | `chicken-and-egg problem`, `eagle-eye view`, `commit-dense day` | ✅ `eagle-eye` kept — mentioned by Mr. Deotale, appropriate. ✅ `chicken-and-egg` kept — established technical term for bootstrapping dependency. ✅ `commit-dense day` → `highest-commit day` fixed in LaTeX (ch11 line 240, Section 11.6 Week 6). Fix in Word: Section 11.6, find `most commit-dense day` → `highest-commit day`. |
| 4 | `production quality` / `production-ready` | Used inconsistently | ✅ Fixed — `production quality` as noun form is correct throughout. One instance in ch05 line 148 was missing hyphen as compound adjective (`production quality and reliability improvement` → `production-quality and reliability improvement`). All other usages verified correct. In Word: Section 5.2.5 (Work Stream 5), find `production quality and reliability improvement` → `production-quality and reliability improvement`. |
| 5 | Reference URL formatting | Some URLs may have broken spacing in bibliography | Check compiled PDF hyperlinks |
