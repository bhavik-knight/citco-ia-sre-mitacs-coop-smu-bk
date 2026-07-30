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

def test_logs_generation():
    """Verify that Major Project and Internship Excel/PDF logs generate successfully."""
    from src.report_pipeline import generate_all_logs
    from config import REPORT_TYPE
    import shutil
    
    # Use a temporary output directory inside output/
    test_out_dir = OUTPUT_DIR / "test_logs"
    test_out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        generate_all_logs(test_out_dir, active_type=REPORT_TYPE)
        
        # Check files exist
        assert (test_out_dir / "WorkLogs_MajorProject.xlsx").exists()
        assert (test_out_dir / "WorkLogs_MajorProject.pdf").exists()
        assert (test_out_dir / "WorkLogs_Internship.xlsx").exists()
        assert (test_out_dir / "WorkLogs_Internship.pdf").exists()
        assert (test_out_dir / "WorkLogs.xlsx").exists()
        assert (test_out_dir / "WorkLogs.pdf").exists()
    finally:
        # Cleanup
        if test_out_dir.exists():
            shutil.rmtree(test_out_dir)
