import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ecopulse.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

OPENAQ_API_KEY = os.getenv("OPENAQ_API_KEY", "")
DEMO_MODE = len(OPENAQ_API_KEY) == 0

CHENNAI_LAT = 13.0827
CHENNAI_LON = 80.2707
