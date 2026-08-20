"""
LaTeX Compilation Service module.
Full sequence: pdflatex → biber → pdflatex → pdflatex
This resolves all cross-references (\ref, \pageref, \pageref{LastPage})
and bibliography entries correctly.
"""
from pathlib import Path
from config.settings import LATEX_DIR, COVER_LETTER_TEX, MAIN_REPORT_TEX
from src.report_pipeline.logger import get_logger
from src.report_pipeline.utils import run_command

logger = get_logger("LaTeXBuilder")

def _latex_ok(latex_dir: Path, stem: str) -> bool:
    """Return True if pdflatex produced a PDF, regardless of MiKTeX nag exit code."""
    pdf = latex_dir / f"{stem}.pdf"
    return pdf.exists()

class LaTeXBuilder:
    """Service to compile LaTeX documents into PDFs."""

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
