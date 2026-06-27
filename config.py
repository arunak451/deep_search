import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "linkedin-data-api.p.rapidapi.com")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PORT = os.getenv("PORT", "3000")

def validate_config():
    """
    Validates that all required API keys are present.
    Prints warnings for any missing configuration.
    """
    missing = []
    if not GROQ_API_KEY:
        missing.append("GROQ_API_KEY")
    if not SERP_API_KEY:
        missing.append("SERP_API_KEY")
    if not RAPIDAPI_KEY:
        missing.append("RAPIDAPI_KEY")
    if not YOUTUBE_API_KEY:
        missing.append("YOUTUBE_API_KEY")
    if not NEWS_API_KEY:
        missing.append("NEWS_API_KEY")
        
    if missing:
        print(f"⚠️ Warning: The following environment variables are missing: {', '.join(missing)}")
        print("Some modules may fail or be skipped during execution.\n")
        return False
    return True
