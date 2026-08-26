"""
format_docx.py
--------------
Applies Neeyati Mehta's Word document formatting to our converted DOCX.

Format extracted from NeeyatiMehta_A00477369_projectReport.docx:
  - Margins: 2.54cm (1") all sides, Letter paper
  - Body font: Calibri 12pt, justified, 1.5 line spacing
  - Heading 1: 16pt bold, SMU maroon #8A0027, centered
  - Heading 2: 14pt bold, SMU maroon #8A0027
  - Heading 3: 12pt bold, SMU maroon #8A0027
  - Space after paragraphs: 6pt

Run:
    uv run python scripts/format_docx.py
"""

from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

INPUT  = "output/BhavikBhagat_A00494758_MajorReport.docx"
OUTPUT = "output/BhavikBhagat_A00494758_MajorReport.docx"

SMU_MAROON = RGBColor(0x8A, 0x00, 0x27)

doc = Document(INPUT)

# ── 1. MARGINS ────────────────────────────────────────────────────────
for section in doc.sections:
    section.left_margin   = Cm(2.54)
    section.right_margin  = Cm(2.54)
    section.top_margin    = Cm(2.54)
    section.bottom_margin = Cm(2.54)

# ── 2. HEADING STYLES ─────────────────────────────────────────────────
heading_config = {
    "Heading 1": {"size": 16, "bold": True, "color": SMU_MAROON,
                  "align": WD_ALIGN_PARAGRAPH.CENTER,
                  "space_before": 12, "space_after": 6},
    "Heading 2": {"size": 14, "bold": True, "color": SMU_MAROON,
                  "align": WD_ALIGN_PARAGRAPH.LEFT,
                  "space_before": 10, "space_after": 4},
    "Heading 3": {"size": 12, "bold": True, "color": SMU_MAROON,
                  "align": WD_ALIGN_PARAGRAPH.LEFT,
                  "space_before": 2,  "space_after": 4},
    "Heading 4": {"size": 12, "bold": True, "color": SMU_MAROON,
                  "align": WD_ALIGN_PARAGRAPH.LEFT,
                  "space_before": 2,  "space_after": 2},
}

for style_name, cfg in heading_config.items():
    try:
        style = doc.styles[style_name]
    except KeyError:
        style = doc.styles.add_style(style_name, 1)  # 1 = paragraph style

    style.font.name  = "Calibri"
    style.font.size  = Pt(cfg["size"])
    style.font.bold  = cfg["bold"]
    style.font.color.rgb = cfg["color"]

    pf = style.paragraph_format
    pf.alignment    = cfg["align"]
    pf.space_before = Pt(cfg["space_before"])
    pf.space_after  = Pt(cfg["space_after"])

# ── 3. NORMAL / BODY STYLE ────────────────────────────────────────────
normal = doc.styles["Normal"]
normal.font.name  = "Calibri"
normal.font.size  = Pt(12)
normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

pf = normal.paragraph_format
pf.alignment          = WD_ALIGN_PARAGRAPH.JUSTIFY
pf.space_after        = Pt(6)
pf.line_spacing_rule  = WD_LINE_SPACING.MULTIPLE
pf.line_spacing       = 1.5

# ── 4. PER-PARAGRAPH PASS ─────────────────────────────────────────────
# pdf2docx creates mostly Normal paragraphs. Apply body formatting to
# all Normal paragraphs; skip headings (already styled above).
SKIP_STYLES = {"Heading 1", "Heading 2", "Heading 3", "Heading 4",
               "Title", "Subtitle"}

for para in doc.paragraphs:
    style_name = para.style.name if para.style else "Normal"
    if style_name in SKIP_STYLES:
        continue

    pf2 = para.paragraph_format

    # Only apply justify to body text paragraphs (not centered title pages)
    if pf2.alignment not in (WD_ALIGN_PARAGRAPH.CENTER,):
        pf2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Apply 1.5 line spacing if not already set
    if pf2.line_spacing is None or pf2.line_spacing_rule is None:
        pf2.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf2.line_spacing      = 1.5

    if pf2.space_after is None:
        pf2.space_after = Pt(6)

    # Reset any large indents inherited from PDF layout
    pf2.left_indent   = Pt(0)
    pf2.right_indent  = Pt(0)
    pf2.first_line_indent = Pt(0)

    # Ensure font name is Calibri on all runs
    for run in para.runs:
        if run.font.name is None or run.font.name == "":
            run.font.name = "Calibri"
        if run.font.size is None:
            run.font.size = Pt(12)

# ── 5. HEADER & FOOTER ───────────────────────────────────────────────
# Header: "MCDA 5585 / 5586 Major Project Report" (left) + page title (right)
# Footer: centered page number in SMU maroon
# Uses a tab stop to push right-side text to the right margin

PAGE_WIDTH_EMU = doc.sections[0].page_width
LEFT_MARGIN    = doc.sections[0].left_margin
RIGHT_MARGIN   = doc.sections[0].right_margin
TEXT_WIDTH_EMU = PAGE_WIDTH_EMU - LEFT_MARGIN - RIGHT_MARGIN

def add_border_bottom(paragraph):
    """Add a thin bottom border to a paragraph (header rule line)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')    # 0.5pt
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '8A0027')
    pBdr.append(bottom)
    pPr.append(pBdr)

def set_run_font(run, size_pt, bold=False, color=None, italic=False):
    run.font.name  = "Calibri"
    run.font.size  = Pt(size_pt)
    run.font.bold  = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def add_field(paragraph, field_type):
    """Insert a Word field (PAGE or NUMPAGES) into a paragraph."""
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = f' {field_type} '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    return run

for section in doc.sections:
    section.different_first_page_header_footer = False
    header = section.header
    footer = section.footer

    # ── Clear existing header/footer content ──────────────────────
    for p in header.paragraphs:
        p._element.getparent().remove(p._element)
    for p in footer.paragraphs:
        p._element.getparent().remove(p._element)

    # ── HEADER paragraph ──────────────────────────────────────────
    # "MCDA 5585 / 5586 Major Project Report [TAB] Bhavik Kantilal Bhagat"
    hdr_para = header.add_paragraph()
    pf_h = hdr_para.paragraph_format
    pf_h.space_before = Pt(0)
    pf_h.space_after  = Pt(2)

    # Tab stop at right edge of text area
    from docx.oxml import OxmlElement as OE
    pPr = hdr_para._p.get_or_add_pPr()
    tabs_el = OE('w:tabs')
    tab_el  = OE('w:tab')
    tab_el.set(qn('w:val'), 'right')
    tab_el.set(qn('w:pos'), str(int(TEXT_WIDTH_EMU / 914400 * 1440)))  # convert EMU→twips
    tabs_el.append(tab_el)
    pPr.append(tabs_el)

    # Left text
    r_left = hdr_para.add_run("MCDA 5585 / 5586 Major Project Report")
    set_run_font(r_left, 9, bold=False, color=RGBColor(0x44, 0x44, 0x44))

    # Tab + right text
    r_tab = hdr_para.add_run("\t")
    r_tab.font.name = "Calibri"
    r_tab.font.size = Pt(9)
    r_right = hdr_para.add_run("Bhavik Kantilal Bhagat — A00494758")
    set_run_font(r_right, 9, bold=False, color=RGBColor(0x44, 0x44, 0x44), italic=True)

    # Bottom border rule line
    add_border_bottom(hdr_para)

    # ── FOOTER paragraph ──────────────────────────────────────────
    ftr_para = footer.add_paragraph()
    ftr_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    ftr_para.paragraph_format.space_before = Pt(2)
    ftr_para.paragraph_format.space_after  = Pt(0)

    page_run = add_field(ftr_para, 'PAGE')
    set_run_font(page_run, 10, bold=False, color=SMU_MAROON)

    sep_run = ftr_para.add_run(" of ")
    set_run_font(sep_run, 10, bold=False, color=SMU_MAROON)

    total_run = add_field(ftr_para, 'NUMPAGES')
    set_run_font(total_run, 10, bold=False, color=SMU_MAROON)

# ── 6. SAVE ───────────────────────────────────────────────────────────
doc.save(OUTPUT)
print(f"Saved: {OUTPUT}")
print(f"Paragraphs processed: {len(doc.paragraphs)}")
