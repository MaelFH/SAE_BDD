API_KEY = "TA_CLE_API"

PLATFORM = "euw1"
REGION = "europe"

DB_PARAMS = {
    "dbname": "lol_db",
    "user": "postgres",
    "password": "ton_mot_de_passe",
    "host": "localhost",
    "port": 5432
}

# Timestamps Unix pour les périodes
PERIODS = {
    "2023-2024": (1680307200, 1711929600),  # 1 avril 2023 → 1 avril 2024
    "2024-2025": (1711929600, 1743465600),  # 1 avril 2024 → 1 avril 2025
}
