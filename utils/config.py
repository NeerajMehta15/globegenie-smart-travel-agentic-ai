import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

class config:
    """Central config class for app settings."""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

