"""
pdf_to_text.py — Extract text from PDF files using PyMuPDF (fitz).

Handles two cases:
  1. Native text PDFs  — direct extraction via page.get_text()
  2. Image-based PDFs  — render each page to a high-res PNG, then read
                         the PNG with Kiro's image tool for manual review,
                         OR save pngs to a temp folder for external OCR.

Usage (CLI):
    uv run python src/pdf_to_text.py path/to/file.pdf
    uv run python src/pdf_to_text.py path/to/file.pdf --pages-dir /tmp/pages

Usage (API):
    from src.pdf_to_text import extract_text
    text = extract_text("path/to/file.pdf")   # returns str
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.exit("PyMuPDF not installed. Run: uv add pymupdf")


def extract_text(pdf_path: str, dpi: int = 300) -> str:
    """
    Extract all text from a PDF.

    Tries native text extraction first (fast, lossless).
    If a page has no native text, renders it to a greyscale image at
    `dpi` resolution and saves it next to the PDF as
    <pdf_stem>_pages/page_N.png for external OCR / manual review.

    Returns the concatenated text of all pages that have native text.
    Pages with no native text are noted as '[IMAGE PAGE — see PNG]'.
    """
    doc = fitz.open(pdf_path)
    pdf_stem = Path(pdf_path).stem
    png_dir = Path(pdf_path).parent / f"{pdf_stem}_pages"

    lines = []
    image_pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text").strip()
        if text:
            lines.append(f"--- page {i + 1} ---\n{text}")
        else:
            # Render to PNG for image-based pages
            png_dir.mkdir(exist_ok=True)
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
            out_path = png_dir / f"page_{i + 1}.png"
            pix.save(str(out_path))
            image_pages.append(str(out_path))
            lines.append(f"--- page {i + 1} (image — saved to {out_path}) ---\n[IMAGE PAGE — see PNG]")

    doc.close()

    if image_pages:
        print(
            f"[pdf_to_text] {len(image_pages)} image-based page(s) saved to PNGs:\n"
            + "\n".join(f"  {p}" for p in image_pages),
            file=sys.stderr,
        )

    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf", help="Path to the PDF file")
    parser.add_argument(
        "--dpi", type=int, default=300, help="DPI for image-page rendering (default: 300)"
    )
    args = parser.parse_args()

    text = extract_text(args.pdf, dpi=args.dpi)
    print(text)


if __name__ == "__main__":
    main()
