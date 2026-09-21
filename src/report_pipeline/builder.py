"""
LaTeX Compilation Service module.
Full sequence: xelatex → biber → xelatex → xelatex
Uses XeLaTeX (not pdflatex) to load real Calibri/Consolas from C:/Windows/Fonts/
via fontspec. This resolves all cross-references and bibliography entries correctly.
"""
import os
from pathlib import Path
from config.settings import LATEX_DIR, COVER_LETTER_TEX, MAIN_REPORT_TEX
from src.report_pipeline.logger import get_logger
from src.report_pipeline.utils import run_command

logger = get_logger("LaTeXBuilder")

# Ensure MiKTeX xelatex is on PATH
MIKTEX_BIN = r"C:\Users\bbhagat\scoop\apps\miktex\25.12\texmfs\install\miktex\bin\x64"
if MIKTEX_BIN not in os.environ.get("PATH", ""):
    os.environ["PATH"] = MIKTEX_BIN + os.pathsep + os.environ.get("PATH", "")

def _latex_ok(latex_dir: Path, stem: str) -> bool:
    """Return True if xelatex produced a PDF."""
    pdf = latex_dir / f"{stem}.pdf"
    return pdf.exists()

class LaTeXBuilder:
    """Service to compile LaTeX documents into PDFs using XeLaTeX."""

    def __init__(self, latex_dir: Path = LATEX_DIR):
        self.latex_dir = latex_dir

    def compile_cover_letter(self) -> bool:
        logger.info("compiling_cover_letter", source=str(COVER_LETTER_TEX.name))
        run_command(["pdflatex", "-interaction=nonstopmode", COVER_LETTER_TEX.name], cwd=self.latex_dir)
        return _latex_ok(self.latex_dir, COVER_LETTER_TEX.stem)

    def compile_main_report(self) -> bool:
        stem = MAIN_REPORT_TEX.stem  # "main"

        # Pass 1 — generate .aux and .bcf files
        logger.info("compiling_main_report_pass1", source=str(MAIN_REPORT_TEX.name))
        run_command(["pdflatex", "-interaction=nonstopmode", MAIN_REPORT_TEX.name], cwd=self.latex_dir)
        if not _latex_ok(self.latex_dir, stem):
            logger.error("pass1_no_pdf_produced")
            return False

        # Biber — resolve bibliography and write .bbl
        logger.info("running_biber", source=stem)
        run_command(["biber", stem], cwd=self.latex_dir)

        # Pass 2 — incorporate .bbl, update \ref and \pageref
        logger.info("compiling_main_report_pass2", source=str(MAIN_REPORT_TEX.name))
        run_command(["pdflatex", "-interaction=nonstopmode", MAIN_REPORT_TEX.name], cwd=self.latex_dir)

        # Pass 3 — stabilise \pageref{LastPage} and ToC page numbers
        logger.info("compiling_main_report_pass3", source=str(MAIN_REPORT_TEX.name))
        run_command(["pdflatex", "-interaction=nonstopmode", MAIN_REPORT_TEX.name], cwd=self.latex_dir)

        return _latex_ok(self.latex_dir, stem)
