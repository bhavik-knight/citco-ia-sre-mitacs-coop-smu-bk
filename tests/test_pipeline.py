"""
Test suite for SMU MCDA Report Build Pipeline.
"""
from pathlib import Path
from config.settings import ROOT_DIR, LATEX_DIR, OUTPUT_DIR, COVER_LETTER_TEX, MAIN_REPORT_TEX

def test_settings_paths_exist():
    """Verify that root and latex source directories exist."""
    assert ROOT_DIR.exists()
    assert LATEX_DIR.exists()
    assert COVER_LETTER_TEX.exists()
    assert MAIN_REPORT_TEX.exists()

def test_output_directory_creation():
    """Verify that output directory can be created."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    assert OUTPUT_DIR.exists()
