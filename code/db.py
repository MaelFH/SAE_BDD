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

def insert_match_data(cursor, match_detail, period_name):
    """
    Insère les stats des champions extraites d’un match dans la BDD.
    
    Args:
        cursor : curseur PostgreSQL
        match_detail : dict JSON retourné par Riot API pour un match
        period_name : string pour identifier la période (ex: '2023-2024')
    """
    participants = match_detail["info"]["participants"]

    for p in participants:
        champ_id = p["championId"]
        champ_name = p["championName"]
        win = p["win"]
        pick = 1
        ban = 0  # Le match détail ne donne pas directement le ban, à gérer autrement

        # Exemple simple d'upsert : si le champion et période existe, on met à jour les compteurs
        cursor.execute("""
            INSERT INTO champion_stats (champion_id, champion_name, period, pick_count, win_count, ban_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (champion_id, period) DO UPDATE SET
                pick_count = champion_stats.pick_count + EXCLUDED.pick_count,
                win_count = champion_stats.win_count + EXCLUDED.win_count,
                ban_count = champion_stats.ban_count + EXCLUDED.ban_count;
        """, (champ_id, champ_name, period_name, pick, 1 if win else 0, ban))


