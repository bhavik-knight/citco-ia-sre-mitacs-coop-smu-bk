"""
Structured logging module using structlog for JSON formatting.
Supports console output and persistent file logging under logs/.
"""
import logging
import sys
from pathlib import Path
import structlog
from config.settings import APP_LOGS_DIR

def get_logger(name: str = "BuildPipeline") -> structlog.stdlib.BoundLogger:
    """Initialize and return a structlog JSON logger writing to console and logs/build.log."""
    log_file = APP_LOGS_DIR / "build.log"
    
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    # Configure handlers: stdout + file log in logs/
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(log_file), encoding="utf-8")
    ]
    
    logging.basicConfig(format="%(message)s", handlers=handlers, level=logging.INFO)
    return structlog.get_logger(name)
