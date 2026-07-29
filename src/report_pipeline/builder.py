"""
LaTeX Compilation Service module.
"""
from pathlib import Path
from config.settings import LATEX_DIR, COVER_LETTER_TEX, MAIN_REPORT_TEX
from src.report_pipeline.logger import get_logger
from src.report_pipeline.utils import run_command

logger = get_logger("LaTeXBuilder")

class LaTeXBuilder:
    """Service to compile LaTeX documents into PDFs."""
    
    def __init__(self, latex_dir: Path = LATEX_DIR):
        self.latex_dir = latex_dir

    def compile_cover_letter(self) -> bool:
        logger.info("compiling_cover_letter", source=str(COVER_LETTER_TEX.name))
        return run_command(["pdflatex", "-interaction=nonstopmode", COVER_LETTER_TEX.name], cwd=self.latex_dir)

    def compile_main_report(self) -> bool:
        logger.info("compiling_main_report_pass1", source=str(MAIN_REPORT_TEX.name))
        pass1 = run_command(["pdflatex", "-interaction=nonstopmode", MAIN_REPORT_TEX.name], cwd=self.latex_dir)
        if not pass1:
            return False
        logger.info("compiling_main_report_pass2", source=str(MAIN_REPORT_TEX.name))
        return run_command(["pdflatex", "-interaction=nonstopmode", MAIN_REPORT_TEX.name], cwd=self.latex_dir)
