import os
from dotenv import load_dotenv

load_dotenv()   # ❗ THIS WAS MISSING

CODA_API_TOKEN = os.getenv("CODA_API_TOKEN")
BASE_URL = "https://coda.io/apis/v1"

SCAN_INTERVAL = 3600  

DB_URL = "sqlite:///securecoda.db"