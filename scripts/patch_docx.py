"""
patch_docx.py
-------------
Applies targeted text patches to the Manual DOCX without touching formatting.
Patches mirror exactly what was changed in the LaTeX source.

Run:
    uv run python scripts/patch_docx.py
"""

import re
from pathlib import Path
from docx import Document

# Find the file
OUTPUT_DIR = Path("output")
INPUT = OUTPUT_DIR / "Manual_BhavikBhagat_A00494758_MajorReport.docx"
if not INPUT.exists():
    candidates = list(OUTPUT_DIR.glob("Manual*.docx"))
    if candidates:
        INPUT = candidates[0]
    else:
        raise FileNotFoundError("No Manual*.docx found in output/")

print(f"Patching: {INPUT}")

# ── EXACT STRING PATCHES ──────────────────────────────────────────────────────
# Applied in order — more specific first
PATCHES = [
    # Grammar: eagle-eye (regular and unicode hyphen variants)
    ("eagle-eye view",                      "single-pane-of-glass view"),
    ("eagle\u2010eye view",                 "single-pane-of-glass view"),
    ("eagle\u2011eye view",                 "single-pane-of-glass view"),

    # Grammar: I accompanied
    ("I accompanied the feature with automated tests",
     "The feature was validated with automated tests"),

    # Grammar: 16-role clarification (long form — may span runs so also handled by regex)
    ("A 16-role agent permission model provides",
     "A 16-role deployment (one role per AWS account) built on a three-role IAM chaining architecture provides"),

    # Grammar: orphan SLO sentence bridge
    ("not compute running error budget consumption or burn rate.",
     "not compute running error budget consumption or burn rate. This distinction is elaborated in the following subsection."),

    # Grammar: W9 sentence restructure
    ("Secrets Manager\u2014the first alarm that would have detected the April incident was now armed against live production traffic.",
     "Secrets Manager. With this deployment complete, the MSK consumer lag alarm was live against production traffic \u2014 the alarm that would have detected the April Meridian Incident was now operational."),
    ("Secrets Manager---the first alarm that would have detected the April incident was now armed against live production traffic.",
     "Secrets Manager. With this deployment complete, the MSK consumer lag alarm was live against production traffic --- the alarm that would have detected the April Meridian Incident was now operational."),

    # Co-op: fix double-placement from previous run
    ("co-op placement placement",           "co-op placement"),
    ("My co-op placement is within",        "My co-op placement is within"),  # guard no-op

    # Co-op: compound forms first
    ("pre-internship",                      "pre-placement"),
    ("post-internship",                     "post-placement"),
    ("Pre-Internship",                      "Pre-Placement"),
    ("Post-Internship",                     "Post-Placement"),
    ("internship-period",                   "co-op period"),
    ("Internship Period",                   "Co-op Period"),
    ("internship project",                  "co-op project"),
    ("my internship engagement",            "my co-op engagement"),
    ("this internship engagement",          "this co-op engagement"),
    ("Internship Work Logs",                "Co-op Work Logs"),
    ("internship deliverables",             "co-op deliverables"),

    # Co-op: "my/this/the internship" → "my/this/the co-op"
    ("my internship,",                      "my co-op,"),
    ("my internship.",                      "my co-op."),
    ("my internship ",                      "my co-op "),
    ("My internship ",                      "My co-op "),
    ("this internship,",                    "this co-op,"),
    ("this internship.",                    "this co-op."),
    ("this internship ",                    "this co-op "),
    ("This internship ",                    "This co-op "),
    ("the internship,",                     "the co-op,"),
    ("the internship.",                     "the co-op."),
    ("the internship ",                     "the co-op "),
    ("The internship ",                     "The co-op "),
    ("during the internship",               "during the co-op"),
    ("during my co-op placement",           "during my co-op"),  # fix over-replacement
    ("throughout the co-op placement",      "throughout the co-op"),

    # ── JIRA number replacements ──────────────────────────────────────────────
    # IISS-487 — proper full name
    ("Centralized Grafana AMG SRE Dashboard",   "Centralized Amazon Managed Grafana (AMG) Dashboard"),
    ("Centralized Grafana AMG Dashboard",        "Centralized Amazon Managed Grafana (AMG) Dashboard"),
    # Remove Key deliverables lines
    ("Key deliverables: IISS-435, IISS-455, IISS-461, IISS-469, IISS-482\u2013486.", ""),
    ("Key deliverable: IISS-487.",               ""),
    ("Key deliverable: IISS-507.",               ""),
    ("Key incident tickets: IISS-706, IISS-538, IISS-741, IISS-876.", ""),
    ("Key deliverable: IISS-824.",               ""),
    ("Key deliverables: IISS-509, IISS-919.",    ""),
    # Inline JIRA replacements
    ("IISS-435",    "CTI CloudWatch Pipeline Dashboard"),
    ("IISS-455",    "IA Lambda Monitoring Dashboard"),
    ("IISS-461",    "Lambda Inventory documentation"),
    ("IISS-469",    "Dashboard Extension and API Refactoring"),
    ("IISS-482\u2013486", "IA Infrastructure Monitoring Platform sub-stories"),
    ("IISS-482--486",     "IA Infrastructure Monitoring Platform sub-stories"),
    ("IISS-482",    "IA Infrastructure Monitoring Platform"),
    ("IISS-483",    "EC2 resource discovery"),
    ("IISS-484",    "ECS Monitoring Dashboard"),
    ("IISS-485",    "EKS Monitoring Dashboard"),
    ("IISS-487",    "Centralized Amazon Managed Grafana (AMG) Dashboard"),
    ("IISS-504",    "AUTOMATIONHUB budget code integration"),
    ("IISS-507\u2013510", "IA Infrastructure Inventory API"),
    ("IISS-507--510",     "IA Infrastructure Inventory API"),
    ("IISS-507",    "IA Infrastructure Inventory API"),
    ("IISS-508",    "dynamic tag discovery feature"),
    ("IISS-509",    "Infrastructure Inventory Dashboard"),
    ("IISS-510",    "multi-region resource API"),
    ("IISS-538",    "MESO ECS autoscaling incident"),
    ("IISS-706",    "CAIS Deadline credential hotfix"),
    ("IISS-741",    "MESO critical queue incident"),
    ("IISS-753",    "VPL IPV selector resilience issue"),
    ("IISS-824",    "RPA LLM Agent quality improvement programme"),
    ("IISS-837\u2013844", "X-Ray distributed tracing specifications"),
    ("IISS-837--844",     "X-Ray distributed tracing specifications"),
    ("IISS-838",    "Lambda Powertools X-Ray tracing specification"),
    ("IISS-839",    "ECS ADOT sidecar tracing specification"),
    ("IISS-840",    "EKS DaemonSet tracing specification"),
    ("IISS-841",    "API Gateway tracing specification"),
    ("IISS-842",    "SQS trace propagation specification"),
    ("IISS-843",    "MSK trace propagation specification"),
    ("IISS-844",    "EC2 X-Ray tracing specification"),
    ("IISS-845\u2013873", "log group discovery features"),
    ("IISS-845--873",     "log group discovery features"),
    ("IISS-845",    "log group observability feature"),
    ("IISS-876",    "VPL GTL booking error incident"),
    ("IISS-919",    "Infrastructure Monitoring Dashboard"),
    # Clean up artifacts
    ("escalated Centralized Amazon Managed Grafana (AMG) Dashboard to Critical",
     "escalated the dashboard project to Critical priority"),
    ("elevate Centralized Amazon Managed Grafana (AMG) Dashboard to",
     "elevate the dashboard project to"),
    ("Centralized Amazon Managed Grafana (AMG) Dashboard alarm set",
     "dashboard alarm set"),
    ("Centralized Amazon Managed Grafana (AMG) Dashboard infrastructure",
     "centralized AMG dashboard infrastructure"),
    ("Centralized Amazon Managed Grafana (AMG) Dashboard repository",
     "centralized AMG dashboard repository"),
    ("the the ",    "the "),
    ("The the ",    "The "),
    # CAIS context
    ("CAIS-Pricing (Citco Alternative Investment Services)",
     "CAIS-Pricing (Citco Alternative Investment Services)"),  # already correct
    # Double hotfix artifact
    ("CAIS Deadline credential hotfix hotfix", "CAIS Deadline credential hotfix"),
]

# ── REGEX PATCHES ─────────────────────────────────────────────────────────────
# Applied after exact patches — catch remaining standalone "internship"
REGEX_PATCHES = [
    # Fix any remaining "co-op placement placement" double
    (r'co-op placement placement', 'co-op placement'),
    # Remaining standalone internship — not preceded by Mitacs/BSI/900
    (r'(?<!Mitacs Business Strategy )(?<!Mitacs )(?<!BSI )(?<!900 )\binternship\b(?! hours)(?! extension)',
     'co-op'),
    (r'(?<!Mitacs Business Strategy )(?<!Mitacs )(?<!BSI )(?<!900 )\bInternship\b(?! Period)(?! Work Logs)',
     'Co-op'),
]


def patch_text(text: str) -> str:
    for old, new in PATCHES:
        text = text.replace(old, new)
    for pattern, replacement in REGEX_PATCHES:
        text = re.sub(pattern, replacement, text)
    return text


def patch_run(run) -> int:
    if not run.text:
        return 0
    patched = patch_text(run.text)
    if patched != run.text:
        run.text = patched
        return 1
    return 0


doc = Document(INPUT)
changed = 0

def patch_paragraph(para) -> int:
    """
    Patch a paragraph by working on the full text, then updating the first run.
    Preserves formatting of individual runs by only modifying run[0] text
    when the full paragraph text changes.
    """
    if not para.runs:
        return 0
    full = "".join(r.text for r in para.runs)
    patched = patch_text(full)
    if patched == full:
        return 0
    # Put all text into first run, clear the rest
    para.runs[0].text = patched
    for r in para.runs[1:]:
        r.text = ""
    return 1

for para in doc.paragraphs:
    changed += patch_paragraph(para)

for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                changed += patch_paragraph(para)

for section in doc.sections:
    for hdr_para in section.header.paragraphs:
        changed += patch_paragraph(hdr_para)
    for ftr_para in section.footer.paragraphs:
        changed += patch_paragraph(ftr_para)

doc.save(INPUT)
print(f"Saved: {INPUT}")
print(f"Total text changes applied: {changed}")
