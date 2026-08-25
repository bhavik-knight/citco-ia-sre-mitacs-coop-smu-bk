# Requirements: Neeyati Template Alignment

## Objective
Align the report's chapter structure and tone with Neeyati Mehta's MCDA
project report (reference: `templates/samples/NeeyatiMehta_A00477369_projectReport.docx`).

Two categories of changes:

### REQ-1: Chapter Opener Tone
Neeyati never opens a chapter with "This chapter documents/provides/covers...".
She opens directly with personal, substantive first sentences like:
- "During my tenure at Wellnify, I set several technical and conceptual learning goals..."
- "The projects undertaken at Wellnify aimed to enhance the app's functionality..."
- "In conclusion, I have contributed significantly to two pivotal projects..."

All "This chapter..." meta-intro sentences must be removed or replaced with
direct, first-person content openers.

### REQ-2: Requirements Elicitation as Separate Chapter
Neeyati has Requirements Elicitation as a standalone chapter (ch8, ~5 pages).
Currently it is merged inside `new_ch07_methodologies.tex` (lines 300–551).
It must be extracted into `new_ch08_requirements_elicitation.tex`, and all
subsequent chapters renumbered +1 (ch08→ch09 through ch13→ch14).

## Acceptance Criteria
- [ ] No chapter in the report opens with "This chapter documents...", "This chapter
  provides...", "This chapter covers...", or any variation
- [ ] `new_ch08_requirements_elicitation.tex` exists containing Stakeholder
  Identification + Requirements Elicitation + Functional/Non-Functional Requirements
- [ ] `new_ch07_methodologies.tex` contains only SRE Principles + Observability
  Gap Analysis + Dynatrace parity (ends before Stakeholder Identification)
- [ ] All 14 chapters compile without errors
- [ ] `main.tex` inputs 14 chapters in correct order
- [ ] No broken `\ref{}` or `\label{}` cross-references
- [ ] Branch: `feature/report-chapters`; merged to `release/v1.0` when complete
