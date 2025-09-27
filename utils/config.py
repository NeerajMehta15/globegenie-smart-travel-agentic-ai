import os
from dotenv import load_dotenv

# Load .env file from project root
load_dotenv()

# Try to fetch DB_PATH from env, fallback if not found
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPEN_AI", "")