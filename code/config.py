import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

PLATFORM = "euw1"
REGION = "europe"

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

PERIODS = {
    "2023-2024": (1680307200, 1711929600),
    "2024-2025": (1711929600, 1743465600),
}
