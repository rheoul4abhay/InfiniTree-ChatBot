from dotenv import load_dotenv
import os

load_dotenv('../.env')
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")