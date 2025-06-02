from riot_api import get_master_players, get_puuid, get_matches, get_match_detail
from db import connect_db, insert_match_data  # adapte selon ta base
from config import PLATFORM, REGION, PERIODS
import time
import requests

MAX_RETRIES = 5
RETRY_WAIT = 30  # secondes à attendre en cas de 429

def safe_api_call(func, *args, **kwargs):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"[429 Too Many Requests] Pause {RETRY_WAIT}s avant retry...")
                time.sleep(RETRY_WAIT)
                retries += 1
            else:
                raise e
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            raise e
    raise Exception(f"Échec après {MAX_RETRIES} retries.")

def main():
    conn = connect_db()
    cursor = conn.cursor()

    players = safe_api_call(get_master_players, PLATFORM)

    for period_name, (start_ts, end_ts) in PERIODS.items():
        print(f"Traitement période {period_name}")

        # Limite pour tests : modifie ou enlève slice [:5]
        for player in players[:5]:
            try:
                puuid = safe_api_call(get_puuid, player["summonerId"], PLATFORM)
                matches = safe_api_call(get_matches, puuid, REGION, start_ts, end_ts)

                for match_id in matches:
                    try:
                        match_detail = safe_api_call(get_match_detail, match_id, REGION)
                        if match_detail:
                            insert_match_data(cursor, match_detail, period_name)
                            conn.commit()
                            print(f"Match {match_id} inséré.")
                        else:
                            print(f"Match {match_id} introuvable.")
                    except Exception as e:
                        print(f"Erreur match {match_id}: {e}")

            except Exception as e:
                print(f"Erreur joueur {player['summonerName']}: {e}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
