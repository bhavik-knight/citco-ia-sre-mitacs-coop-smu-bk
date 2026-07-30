#!/usr/bin/env python3
"""
CLI entry point for SMU MCDA Major Project Report Build Pipeline.
Orchestrates LaTeX compilation, PDF-to-DOCX conversion, and bundle packaging.
"""
import shutil
import sys
from pathlib import Path

# Add project root to Python path
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
    SUBMISSION_REPORT_DOCX,
    REPORT_TYPE,
)
from src.report_pipeline import LaTeXBuilder, DocxConverter, get_logger, generate_all_logs

logger = get_logger("MainPipeline")

def main():
    logger.info("pipeline_started", root_dir=str(ROOT_DIR), output_dir=str(OUTPUT_DIR), report_type=REPORT_TYPE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Instantiate LaTeX Builder
    builder = LaTeXBuilder(latex_dir=LATEX_DIR)
    
    # 2. Compile Documents
    logger.info("step_compile_cover_letter")
    builder.compile_cover_letter()
    
    logger.info("step_compile_main_report")
    builder.compile_main_report()
    
    # 3. Copy PDFs to output/
    if COVER_LETTER_PDF.exists():
        shutil.copy(COVER_LETTER_PDF, SUBMISSION_COVER_LETTER_PDF)
        logger.info("artifact_copied", src=COVER_LETTER_PDF.name, dest=str(SUBMISSION_COVER_LETTER_PDF))

    if MAIN_REPORT_PDF.exists():
        shutil.copy(MAIN_REPORT_PDF, SUBMISSION_REPORT_PDF)
        logger.info("artifact_copied", src=MAIN_REPORT_PDF.name, dest=str(SUBMISSION_REPORT_PDF))
        
        # 4. Convert Main Report PDF to DOCX
        logger.info("step_convert_docx")
        DocxConverter.convert_pdf_to_docx(SUBMISSION_REPORT_PDF, SUBMISSION_REPORT_DOCX)

    # 5. Generate and Sync Work Logs
    logger.info("step_generate_work_logs")
    generate_all_logs(OUTPUT_DIR, active_type=REPORT_TYPE)

    # 6. Output Summary
    logger.info("pipeline_completed", output_directory=str(OUTPUT_DIR))
    for artifact in sorted(OUTPUT_DIR.iterdir()):
        if artifact.is_file():
            logger.info("bundle_artifact", filename=artifact.name, size_bytes=artifact.stat().st_size)

if __name__ == "__main__":
    main()
