from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import  Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    INPUT_DIR: Path = DATA_DIR / "input"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    LOG_DIR: Path = PROJECT_ROOT / "logs"
    
    # Groq settings
    GROQ_API_KEY: str = Field(env="GROQ_API_KEY")
    GROQ_MODEL: str = Field(env="GROQ_MODEL")

    TEMPERATURE: float = Field(default=0.7, env="TEMPERATURE")
    MAX_TOKENS: int = Field(default=2000, env="MAX_TOKENS")
    
    # Document processing settings
    DOCUMENT_SETTINGS: Dict[str, Any] = {
        "input_formats": [".docx", ".pdf"],
        "output_formats": [".docx", ".xlsx"],
        "max_file_size": 20 * 1024 * 1024,  # 20MB
    }
    
    # AI Agent settings
    AGENT_SETTINGS: Dict[str, Any] = {
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.95,
        "top_k": 50,
    }
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in [self.INPUT_DIR, self.OUTPUT_DIR, self.LOG_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

# Create global settings instance
settings = Settings()