from loguru import logger as loguru_logger
import sys
from pathlib import Path
from ..config.settings import settings

def setup_logger():
    """Configure the logger with appropriate settings."""
    # Remove default handler
    loguru_logger.remove()
    
    # Add console handler
    loguru_logger.add(
        sys.stderr,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True
    )
    
    # Add file handler
    log_file = settings.LOG_DIR / "app.log"
    loguru_logger.add(
        log_file,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        rotation="1 day",
        retention="7 days",
        compression="zip"
    )
    
    return loguru_logger

# Initialize logger
logger = setup_logger() 