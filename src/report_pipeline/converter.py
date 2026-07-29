"""
PDF to DOCX Converter Service module.
"""
from pathlib import Path
from src.report_pipeline.logger import get_logger

logger = get_logger("DocxConverter")

class DocxConverter:
    """Service to convert compiled PDF report into editable DOCX format."""

    @staticmethod
    def convert_pdf_to_docx(pdf_path: Path, docx_path: Path) -> bool:
        if not pdf_path.exists():
            logger.error("source_pdf_not_found", path=str(pdf_path))
            return False

        logger.info("converting_pdf_to_docx", source=str(pdf_path), target=str(docx_path))
        try:
            from pdf2docx import Converter
            cv = Converter(str(pdf_path))
            cv.convert(str(docx_path), start=0, end=None)
            cv.close()
            logger.info("docx_conversion_success", docx=docx_path.name, size_bytes=docx_path.stat().st_size)
            return True
        except Exception as e:
            logger.error("docx_conversion_failed", error=str(e))
            return False
