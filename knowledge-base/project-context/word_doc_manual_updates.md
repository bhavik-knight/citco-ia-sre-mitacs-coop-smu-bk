# Word Document Manual Update Notes

These are content changes made to the LaTeX PDF **after** the Word doc was last
converted. The Word doc scripts handled text replacements but the following
**new content / structural changes** need to be updated manually.

---

## 1. Chapter 10 — Support Model (Section 10.5 intro)

**What changed:** Added a formal three-tier support model definition before the
support rotation structure.

**Add this text** at the start of Section 10.5 (before "Each support week
followed a consistent daily rhythm"):

> The Citco IA support model operates across three tiers:
> - **L1 — Ask Citco RPA** (Work Stream 5): The LLM-powered self-service chatbot
>   that answers first-line queries from RPA operators about process status,
>   procedures, and Legal Entity assignments.
> - **L2 — Innovation IT Support** (Work Stream 4): The human-staffed
>   Follow-the-Sun rotation covering Manila (APAC), Dublin (EMEA), and Halifax
>   (NA) shifts. L2 handles Service Desk tickets that L1 cannot resolve.
> - **L3 — SRE** (our team): Escalation tier for infrastructure-level incidents
>   requiring cloud access, code-level fixes, or platform changes beyond the L2
>   operator scope.
>
> I held the North America L2 slot (11 AM–7 PM EST) once every four weeks,
> serving as the primary contact for RPA incidents during that window.

---

## 2. Chapter 10 — CAIS Deadline Description (Section 10.5.3)

**What changed:** Expanded the CAIS Deadline incident description with context
about what the bot does.

**Update** the CAIS Deadline bullet to read:

> **CAIS Deadline Pipeline Hotfix:** The CAIS Deadline bot — which uploads
> Standard Allocation Sheets to the PDS database and generates consolidated
> pricing reports for alternative investment clients — failed with
> SMBAuthenticationError: SpnegoError during UCM upload, blocking the automated
> generation of deadline pricing reports and the regulatory CAIS filing.
> A seven-hour investigation identified the root cause: constants.py cached
> credentials at module import time; a Secrets Manager rotation left empty
> values, causing silent authentication failures. Three fixes applied: fail-fast
> credential validation; guard against empty deadline_ids SQL clause; zip file
> existence check before upload. Filing completed before regulatory deadline.

---

## 3. Chapter 11 — Weekly Breakdown Expansions

**What changed:** All weeks W12–W24 were expanded from short stubs to ~1–1.5
pages each. The Word doc has the old shorter content.

**Weeks needing expansion in Word doc:**
- W12: Support Rotation #2 + Alarm Tuning — add RPA shift detail and EC2 dashboard
- W13: CAIS hotfix detail + per-panel folder refactor
- W14: Dashboard v728 final deployment detail
- W15: MSK refinements + 6 resource mapper Lambdas
- W16: Support Rotation #3 + ECS discoverers + Canada Day detail
- W17: Inventory API v1.5.0 + X-Ray architecture plan
- W18: Alarm email deep-links + dynamic alarm provisioner
- W19: CloudWatch Logs layer + saved queries + cross-platform filter fix
- W20: Support Rotation #4 + X-Ray tracing specs + v2.19.9 release
- W21: LLM Agent major refactor + EventBridge vs APScheduler decision
- W22: KB upload CLI + Bedrock externalisation + CodeBuild stabilisation
- W23: LLM Agent completion + X-Ray instrumentation + Citco SMTP alarm emails
- W24: Support Rotation #5 + KT handover + Mitacs BSI renewal
- W25: Final day

> **Tip:** Open the PDF at Chapter 11 and copy each week's text into Word.
> The PDF has the full expanded content.

---

## 4. Chapter 6.3.4 — RPA Support Acceptance Criteria

**What changed:** Updated to reference L2/L3 tiers:

> **SLA compliance:** Tickets are acknowledged within the L2 (Innovation IT)
> response SLA and carried over with complete handover notes per the IA Support
> Model. L3 (SRE) is escalated for incidents requiring infrastructure access or
> code-level fixes.

---

## 5. Chapter 2 — CAIS-Pricing first mention

**What changed:** Added "(Citco Alternative Investment Services)" on first mention.

Find: `CAIS-Pricing GenAI pipeline`
Replace with: `CAIS-Pricing (Citco Alternative Investment Services) GenAI pipeline`

---

## 6. Chapter 5 — CAIS-Pricing first mention

**What changed:** Added context on first mention.

Find: `the CAIS-Pricing Extract GenAI`
Replace with: `the CAIS-Pricing Extract GenAI (a Citco Alternative Investment Services pricing pipeline)`

---

## 7. Chapter 14 — CAIS Deadline Pipeline Hotfix (Section 14.4.1)

**What changed:** Expanded pipeline failure description.

Find: `The CAIS data pipeline failed silently`
Replace with: `The CAIS Deadline pipeline — responsible for uploading allocation
sheets to the PDS database and generating pricing reports for alternative
investment clients — failed silently`

---

## 8. Appendix — Work Logs

**What changed:** Corrected to 900h, 25 weeks, March 16 start date.

Update to read:
> The complete weekly work log documenting **900 hours** of co-op work across
> 25 weeks (March 16 – August 31, 2026) is provided in the supplementary file:
> BhavikBhagat_A00494758_WorkLogs.xlsx
>
> The work log includes:
> - Weekly task descriptions and hours logged per activity
> - Weekly hour totals and cumulative running total
> - Meeting and support shift hours tracked separately
> - Work stream categorization (WS1–WS6)
>
> An additional **120 hours** were dedicated to report writing and academic
> documentation (MCDA 5585 and 5586), bringing the total project effort to
> **1,020 hours**.

---

## 9. Chapter 8 Acceptance Criteria — SLA compliance

Already patched in Word doc via script. ✅

## 10. Text replacements already done via scripts ✅

The following were applied automatically via `patch_docx.py`:
- All JIRA numbers → descriptive names
- internship → co-op terminology (147 replacements)
- Grammar fixes (eagle-eye, I accompanied, 16-role, SLO orphan sentence)
- Name prefixes (Mr./Ms./Dr.) — 125 replacements
- CAIS double-hotfix artifact fixed

---

## Priority Order for Manual Updates

| Priority | Item | Effort |
|---|---|---|
| High | Ch11 weekly expansions (W12–W24) | Copy from PDF |
| High | Ch10 support tier definition | Add ~10 lines |
| Medium | Ch10 CAIS Deadline description | Update 1 bullet |
| Medium | Ch14 CAIS pipeline description | Update 1 sentence |
| Low | Ch2/Ch5 CAIS first mention | 1 word change each |
| Low | Appendix work logs | Update 1 paragraph |
