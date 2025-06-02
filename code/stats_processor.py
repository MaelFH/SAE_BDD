from collections import defaultdict

def init_stats():
    return defaultdict(lambda: {"picks": 0, "wins": 0, "bans": 0})

def process_match(match, stats):
    info = match["info"]
    for team in info.get("teams", []):
        for ban in team.get("bans", []):
            champ_id = ban.get("championId")
            if champ_id:
                stats[champ_id]["bans"] += 1

    for p in info["participants"]:
        champ_id = p["championId"]
        stats[champ_id]["picks"] += 1
        if p["win"]:
            stats[champ_id]["wins"] += 1
