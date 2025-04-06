import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set. Please check your .env file.")
            
    def get_groq_api_key(self):
        return self.groq_api_key