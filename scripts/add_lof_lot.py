"""
add_lof_lot.py
--------------
1. Applies SMU maroon (#8A0027) 10pt italic to the Caption style
2. Inserts List of Figures and List of Tables after the TOC page
3. Re-applies Caption style to all figure/table captions

Run:
    uv run python scripts/add_lof_lot.py
"""

import re
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

SMU_MAROON = RGBColor(0x8A, 0x00, 0x27)
DOCX_PATH  = "output/Manual_BhavikBhagat_A00494758_MajorReport.docx"

doc = Document(DOCX_PATH)

# ── 1. Style the Caption paragraph style ─────────────────────────────────────
cap_style = doc.styles["Caption"]
cap_style.font.name   = "Calibri"
cap_style.font.size   = Pt(10)
cap_style.font.italic = True
cap_style.font.bold   = False
cap_style.font.color.rgb = SMU_MAROON
cap_style.paragraph_format.space_before = Pt(4)
cap_style.paragraph_format.space_after  = Pt(6)
cap_style.paragraph_format.alignment    = WD_ALIGN_PARAGRAPH.CENTER

print("Caption style updated: Calibri 10pt italic maroon")

# ── 2. Re-apply Caption style to all real captions ──────────────────────────
CAPTION_RE = re.compile(r'^(Figure|Table)\s+\d+[\.\d]*\s*[:\u2014\u2013\-]')
cap_count = 0
for para in doc.paragraphs:
    if CAPTION_RE.match(para.text.strip()):
        if para.style.name != "Caption":
            para.style = cap_style
        # Also clear any run-level font overrides so style takes effect
        for run in para.runs:
            run.font.name   = None
            run.font.size   = None
            run.font.italic = None
            run.font.bold   = None
            run.font.color.rgb = None
        cap_count += 1

print(f"Caption style applied to {cap_count} paragraphs")

# ── 3. Insert LoF and LoT after the Table of Contents ────────────────────────
# Find the TOC paragraph (contains "Table of Contents" or "Contents")
toc_idx = -1
for i, para in enumerate(doc.paragraphs):
    t = para.text.strip()
    if t in ("Table of Contents", "Contents") and para.style.name.startswith("Heading"):
        toc_idx = i
        break

# Find the end of TOC (next heading after TOC)
toc_end = toc_idx + 1
for i in range(toc_idx + 1, len(doc.paragraphs)):
    if doc.paragraphs[i].style.name.startswith("Heading") and \
       doc.paragraphs[i].text.strip() not in ("Table of Contents", "Contents", ""):
        toc_end = i
        break

print(f"TOC found at paragraph {toc_idx}, ends at {toc_end}")

def insert_paragraph_after(doc_obj, idx, text, style_name):
    """Insert a new paragraph after paragraph at idx."""
    ref_para = doc_obj.paragraphs[idx]
    new_p = OxmlElement("w:p")
    ref_para._p.addnext(new_p)
    # Get the newly inserted paragraph object
    new_para = doc_obj.paragraphs[idx + 1]
    new_para.text = text
    new_para.style = doc_obj.styles[style_name]
    return new_para

def insert_toc_field(doc_obj, idx, field_instruction):
    """Insert a paragraph with a TOC field instruction after paragraph at idx."""
    ref_para = doc_obj.paragraphs[idx]
    new_p = OxmlElement("w:p")
    ref_para._p.addnext(new_p)
    new_para = doc_obj.paragraphs[idx + 1]

    # Build field: {TOC \h \z \c "Figure"}
    run = new_para.add_run()
    r_el = run._r

    fldChar_begin = OxmlElement("w:fldChar")
    fldChar_begin.set(qn("w:fldCharType"), "begin")
    fldChar_begin.set(qn("w:dirty"), "true")
    r_el.append(fldChar_begin)

    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = field_instruction
    run2 = new_para.add_run()
    run2._r.append(instrText)

    fldChar_end = OxmlElement("w:fldChar")
    fldChar_end.set(qn("w:fldCharType"), "end")
    run3 = new_para.add_run()
    run3._r.append(fldChar_end)

    return new_para

if toc_idx >= 0:
    insert_idx = toc_end - 1
else:
    # No TOC heading found — insert LoF/LoT before Chapter 1 (first numbered heading)
    insert_idx = -1
    for i, para in enumerate(doc.paragraphs):
        t = para.text.strip()
        if re.match(r'^1\.\s+', t) and para.style.name.startswith("Heading"):
            insert_idx = i - 1  # insert before "1. ABOUT COMPANY..."
            break
    if insert_idx < 0:
        insert_idx = 23  # fallback: before paragraph 24

    print(f"No TOC heading — inserting LoF/LoT before Chapter 1 (paragraph {insert_idx})")

if insert_idx >= 0:
    # Insert: LoF heading + LoF field + LoT heading + LoT field
    # Insert in reverse order so final order is correct

    # Page break before LoF
    ref_para = doc.paragraphs[insert_idx]
    new_p = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    pb = OxmlElement("w:pageBreak")
    pPr.append(pb)
    new_p.append(pPr)
    ref_para._p.addnext(new_p)
    insert_idx += 1

    # LoT heading
    ref_para = doc.paragraphs[insert_idx]
    new_p2 = OxmlElement("w:p")
    ref_para._p.addnext(new_p2)
    lot_h = doc.paragraphs[insert_idx + 1]
    lot_h.style = doc.styles["Heading 1"]
    lot_h.add_run("List of Tables")
    insert_idx += 1

    # LoT field
    insert_toc_field(doc, insert_idx, ' TOC \\h \\z \\c "Table" ')
    insert_idx += 1

    # LoF heading
    ref_para = doc.paragraphs[insert_idx]
    new_p3 = OxmlElement("w:p")
    ref_para._p.addnext(new_p3)
    lof_h = doc.paragraphs[insert_idx + 1]
    lof_h.style = doc.styles["Heading 1"]
    lof_h.add_run("List of Figures")
    insert_idx += 1

    # LoF field
    insert_toc_field(doc, insert_idx, ' TOC \\h \\z \\c "Figure" ')

    print("Inserted List of Figures and List of Tables with TOC fields")
else:
    print("WARNING: Could not find insertion point")

# ── 4. Save ───────────────────────────────────────────────────────────────────
doc.save(DOCX_PATH)
print(f"Saved: {DOCX_PATH}")
print()
print("IMPORTANT: Open the DOCX in Word, then press Ctrl+A → F9 to update all fields.")
print("The LoF and LoT will populate with figure/table titles and page numbers.")
