import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "change-this-secret-key-in-env")
JOW_EMAIL = os.getenv("JOW_EMAIL", "")
JOW_PASSWORD = os.getenv("JOW_PASSWORD", "")

BASE_DIR = Path(__file__).resolve().parent.parent
KEYWORDS_FILE = BASE_DIR / "data" / "meat_keywords.json"

def load_meat_keywords() -> list[str]:
    if not KEYWORDS_FILE.exists():
        return []
    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [k.lower() for k in data.get("keywords", [])]