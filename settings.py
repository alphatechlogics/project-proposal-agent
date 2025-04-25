import os
from dotenv import load_dotenv
from loguru import logger
import sys

class Config:    
    def __init__(self):
        self._setup_logging()
 
    def _setup_logging(self):
        logger.remove()  # Remove default handler
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <white>{message}</white>",
            level="INFO"
        )
        logger.add(
            "logs/app.log",
            rotation="500 MB",
            retention="10 days",
            level="DEBUG"
        )

            
    
