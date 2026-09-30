# Submission 3 — Feedback Response

**Student:** Bhavik Kantilal Bhagat | A00494758
**Program:** MSc Computing and Data Analytics, Saint Mary's University
**Submission:** Mentor Submission 3 (September 2026)
**Previous Score:** 78/100 (Submission 2, Sep 26, 2026)

---

## How I Addressed Each Feedback Point (Submission 2 → Submission 3)

| # | Feedback | How Addressed |
|----|-----------|---------------|
| 1 | **Cover letter** — no need to include sections for Supervisor Feedback or Committee Feedback at this stage | Removed both the Committee Feedback and Supervisor Feedback tables from the cover letter appendix. Only the Mentor Feedback table is now included. The Sep 26, 2026 (78%) feedback row has been added in reverse chronological order above the Aug 31, 2026 (55%) row. |
| 2 | **Status of Goals Overview table** — use "Completed" instead of check marks and highlight the corresponding cells in green (refer to sample report) | All 13 checkmarks (✓) replaced with "Completed" text. Each Status cell is highlighted with a green background (#A8D08D) sampled directly from the Neeyati Mehta sample report. Column widths adjusted for comfortable text fit. |
| 3 | **"Production incidents provided valuable learning experiences:"** — move to page 130 so the heading and its text begin on the same page | Added `\clearpage` before Section 14.4 (Production Incidents) in the LaTeX source. The section heading, introductory sentence, and all subsection content now start together at the top of a fresh page. |
| 4 | **Appendix should begin on a new page** | Added `\clearpage` before `\chapter{Appendix}` in the LaTeX source. The Appendix now always starts at the top of a new page, cleanly separated from Chapter 15 (Future Work). |
| 5 | **Mention the use of ChatGPT or any other LLM/AI tools in both the References section and the cover letter** | Three AI tools added to the References section with proper citations: [19] Kiro (Amazon Web Services), [22] Claude (Anthropic), [29] Grammarly (Grammarly Inc.). The cover letter paragraph updated to explicitly name: *"Grammarly for grammar checks, Claude (Anthropic) for assistance in structuring complex sentences, and Kiro IDE for AI-assisted documentation and code scaffolding."* |
| 6 | **Mr./Ms. prefixes** — use appropriate prefixes for all individuals mentioned by name in the work logs as well | Mr./Ms. prefixes applied to all individuals named in the WorkLogs.xlsx and WorkLogs.pdf: Mr. Kishor Deotale, Mr. Horace (Mr. Ho Hoi Leung), Ms. Kri, Mr. Sridhar, Ms. Soundarya, Mr. Bhanu, Mr. Nathaniel, Mr. Johansen. |

---

## Additional Improvements (Beyond Feedback)

- **LaTeX build engine fixed:** Switched from `pdflatex` to `xelatex` throughout the build pipeline. `pdflatex` was silently failing due to `fontspec` incompatibility and copying stale PDFs to output — all PDFs are now freshly compiled with the correct engine.
- **Appendix section renumbering:** A.0.1 / A.0.2 renumbered to A.1 (Work Logs) / A.2 (Glossary) / A.3 (References). Sections A.1 and A.2 are suppressed from the TOC (only "A  APPENDIX" appears) to match the sample report style.
- **Glossary header simplified:** A.2 heading changed from "Glossary of Terms and Abbreviations" to just "Glossary".
- **Glossary BPM definition corrected:** BPM entry corrected from "Blue Prism platform" to "Business Process Management — a discipline for modeling, automating, and optimizing business workflows; also used at Citco to refer to the Blue Prism platform..."
- **CFS added to glossary:** New entry added — "CFS — Citco Fund Services, the Citco business line providing fund administration, accounting, and investor services to hedge funds and alternative investment managers globally."
- **Section 15.3 removed:** "RPA Bot CloudWatch Integration" removed from Future Work. Remaining sections renumbered: 15.3 → Error Budget Burn-Rate Alerting, 15.4 → Tag Compliance Automation.
- **Layout fixes:** Multiple orphaned headings corrected with `\clearpage` or `\needspace` (Section 6.1, 10.4.5 Async Architecture, Chapter 2 Executive Summary). Figure 13 widened from 0.85 to 0.90 textwidth for improved readability.

---

## Submission Bundle

| File | Description |
|------|-------------|
| `BhavikBhagat_A00494758_CoverLetter.pdf` | Cover letter with Mentor Feedback appendix (Sep 26 / 78% + Aug 31 / 55%) |
| `BhavikBhagat_A00494758_MajorReport.pdf` | Main project report (129 pages) |
| `BhavikBhagat_A00494758_MajorReport.docx` | Word format of report (auto-converted) |
| `BhavikBhagat_A00494758_WorkLogs.xlsx` | Weekly work logs (900 hours, 25 weeks) with Mr./Ms. prefixes applied |
| `BhavikBhagat_A00494758_WorkLogs.pdf` | PDF export of work logs |
