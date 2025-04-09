import os
from dotenv import load_dotenv
from flask import cli
from loguru import logger
import sys

class Config:
    def __init__(self):
        self._setup_logging()
        load_dotenv()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            logger.error("GROQ_API_KEY environment variable is not set")
            raise ValueError("GROQ_API_KEY environment variable is not set. Please check your .env file.")
    
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
            
    def get_groq_api_key(self):
        return self.groq_api_key
    


