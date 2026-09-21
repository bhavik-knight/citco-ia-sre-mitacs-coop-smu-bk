"""
Utility functions for running subprocess commands and file operations.
"""
from pathlib import Path
import subprocess
from src.report_pipeline.logger import get_logger

logger = get_logger("PipelineUtils")

def run_command(cmd: list[str], cwd: Path) -> bool:
    """Execute a shell command in a specified directory with structured JSON logging."""
    logger.info("executing_command", command=" ".join(cmd), cwd=str(cwd))
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace")
    # MiKTeX exits with code 1 for "check for updates" nag — treat as success
    # Real failures produce no PDF and have actual error messages
    miktex_nag = "major issue: So far, you have not checked for MiKTeX updates" in res.stderr
    if res.returncode != 0 and not miktex_nag:
        logger.error("command_failed", exit_code=res.returncode, stderr=res.stderr.strip())
        return False
    logger.info("command_success", command=cmd[0])
    return True
