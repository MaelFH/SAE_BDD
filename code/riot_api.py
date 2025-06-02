import requests
import time
from config import API_KEY

HEADERS = {"X-Riot-Token": API_KEY}

def get_master_players(platform):
    url = f"https://{platform}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # Pour lever une erreur HTTP si besoin
    return response.json().get("entries", [])

def get_puuid(summoner_id, platform):
    url = f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("puuid")

def get_matches(puuid, region, start, end):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "queue": 420,  # Ranked Solo
        "startTime": start,
        "endTime": end,
        "count": 100
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def get_match_detail(match_id, region):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return None
