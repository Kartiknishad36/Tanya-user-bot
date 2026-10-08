import os
from dotenv import load_dotenv

load_dotenv()

# Required
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")

# Optional
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
CMD_PREFIX = os.getenv("CMD_PREFIX", ".")
PORT = int(os.getenv("PORT", "10000"))

# AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Features
LOG_CHAT = os.getenv("LOG_CHAT", "")
PM_PERMIT = os.getenv("PM_PERMIT", "True").lower() in ("true", "1", "yes")
MAX_PM_FLOOD = int(os.getenv("MAX_PM_FLOOD", "5"))

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Bot Info
BOT_NAME = "Tanya UserBot"
BOT_VERSION = "2.0.0"
BOT_CREATOR = "@Kartiknishad36"
