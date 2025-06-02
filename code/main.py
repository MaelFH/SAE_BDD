import time
from config import PLATFORM, REGION, PERIODS
from riot_api import get_master_players, get_puuid, get_matches, get_match_detail
from stats_processor import init_stats, process_match
from db import create_tables, insert_stats

def main():
    create_tables()
    players = get_master_players(PLATFORM)
    print(f"{len(players)} joueurs master+ trouvés")

    for period_name, (start_ts, end_ts) in PERIODS.items():
        print(f"📅 Traitement de la période {period_name}")
        stats = init_stats()

        for p in players[:10]:  # ⛔ Pour tests, limiter à 10
            try:
                summ_id = p["summonerId"]
                puuid = get_puuid(summ_id, PLATFORM)
                match_ids = get_matches(puuid, REGION, start_ts, end_ts)
                for match_id in match_ids:
                    match = get_match_detail(match_id, REGION)
                    if match:
                        process_match(match, stats)
                        time.sleep(1)  # ⚠️ éviter dépassement quota
            except Exception as e:
                print("Erreur:", e)

        insert_stats(stats, period_name)

if __name__ == "__main__":
    main()
