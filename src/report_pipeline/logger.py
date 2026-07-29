"""
Structured logging module using structlog for JSON formatting.
"""
import logging
import sys
import structlog

def get_logger(name: str = "BuildPipeline") -> structlog.stdlib.BoundLogger:
    """Initialize and return a structlog JSON logger."""
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
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
    return structlog.get_logger(name)
