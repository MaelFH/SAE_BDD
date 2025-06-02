import psycopg2
from config import DB_PARAMS

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def create_tables():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS champion_stats (
                id SERIAL PRIMARY KEY,
                champion_id INTEGER,
                period TEXT,
                picks INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                bans INTEGER DEFAULT 0
            );
            """)
        conn.commit()

def insert_stats(stats, period):
    with connect_db() as conn:
        with conn.cursor() as cur:
            for champ_id, data in stats.items():
                cur.execute("""
                    INSERT INTO champion_stats (champion_id, period, picks, wins, bans)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (champion_id, period) DO UPDATE
                    SET picks = EXCLUDED.picks,
                        wins = EXCLUDED.wins,
                        bans = EXCLUDED.bans;
                """, (champ_id, period, data["picks"], data["wins"], data["bans"]))
        conn.commit()
