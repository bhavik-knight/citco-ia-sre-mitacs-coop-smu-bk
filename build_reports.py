#!/usr/bin/env python3
"""
Build pipeline for SMU MCDA Major Project Report.

Steps:
  1. Generate WorkLogs Excel from daily markdown files
  2. Compile cover_letter.tex → PDF (xelatex)
  3. Compile main.tex → PDF (xelatex × 3 passes + biber)
  4. Copy PDFs to output/

Run:
    uv run python build_reports.py

Output files:
    output/BhavikBhagat_A00494758_CoverLetter.pdf
    output/BhavikBhagat_A00494758_MajorReport.pdf
    output/BhavikBhagat_A00494758_WorkLogs.xlsx
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import (
    LATEX_DIR,
    OUTPUT_DIR,
    COVER_LETTER_PDF,
    MAIN_REPORT_PDF,
    SUBMISSION_COVER_LETTER_PDF,
    SUBMISSION_REPORT_PDF,
)
from src.report_pipeline import LaTeXBuilder, get_logger

logger = get_logger("MainPipeline")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("pipeline_started", output_dir=str(OUTPUT_DIR))

    # ── 1. Generate WorkLogs Excel ────────────────────────────────────
    logger.info("step_generate_worklogs")
    result = subprocess.run(
        ["uv", "run", "python", "scripts/generate_worklogs_excel.py"],
        cwd=ROOT_DIR,
    )
    if result.returncode != 0:
        logger.error("worklogs_generation_failed")
    else:
        logger.info("worklogs_generated")

    # ── 2. Compile LaTeX ──────────────────────────────────────────────
    builder = LaTeXBuilder(latex_dir=LATEX_DIR)

    logger.info("step_compile_cover_letter")
    builder.compile_cover_letter()

    logger.info("step_compile_main_report")
    builder.compile_main_report()

    # ── 3. Copy PDFs to output/ ───────────────────────────────────────
    if COVER_LETTER_PDF.exists():
        shutil.copy(COVER_LETTER_PDF, SUBMISSION_COVER_LETTER_PDF)
        logger.info("artifact_copied", file=SUBMISSION_COVER_LETTER_PDF.name)
    else:
        logger.error("cover_letter_pdf_missing")

    if MAIN_REPORT_PDF.exists():
        shutil.copy(MAIN_REPORT_PDF, SUBMISSION_REPORT_PDF)
        logger.info("artifact_copied", file=SUBMISSION_REPORT_PDF.name)
    else:
        logger.error("main_report_pdf_missing")

    # ── 4. Summary ────────────────────────────────────────────────────
    logger.info("pipeline_completed")
    print("\n=== Output bundle ===")
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.is_file() and not f.name.startswith("~$"):
            size_kb = f.stat().st_size // 1024
            print(f"  {f.name:<55} {size_kb:>6} KB")


if __name__ == "__main__":
    main()
