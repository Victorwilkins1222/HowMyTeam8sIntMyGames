import requests
import time
import json
import os
from config import API_KEY

# Riot API is split into regional routing (for account/PUUID lookups)
# and platform routing (for match data). NA/BR/LAN/LAS/OCE use "americas"
REGION = "americas"  # regional routing value
HEADERS = {"X-Riot-Token": API_KEY}


def get_puuid(game_name, tag_line):
    """Get your PUUID from your Riot ID (the name#TAG format)."""
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()["puuid"]


def get_match_ids(puuid, count=50, queue=420):
    """Get a list of recent match IDs. queue=420 is Ranked Solo/Duo."""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {"start": 0, "count": count, "queue": queue}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def get_match_details(match_id):
    """Get full match data for a single match ID."""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def pull_all_matches(game_name, tag_line, count=50, save_dir="data"):
    """
    Pulls matches and saves EACH one as its own JSON file in save_dir,
    named by match ID. Skips matches already saved (resumable).
    """
    os.makedirs(save_dir, exist_ok=True)

    print(f"Getting PUUID for {game_name}#{tag_line}...")
    puuid = get_puuid(game_name, tag_line)

    print(f"Fetching last {count} ranked match IDs...")
    match_ids = get_match_ids(puuid, count=count)

    for i, match_id in enumerate(match_ids):
        file_path = os.path.join(save_dir, f"{match_id}.json")

        if os.path.exists(file_path):
            print(f"[{i+1}/{len(match_ids)}] {match_id} already saved, skipping.")
            continue
        print(f"[{i+1}/{len(match_ids)}] Fetching {match_id}...")
        try:
            match_data = get_match_details(match_id)
        except requests.exceptions.HTTPError as e:
            print(f"  Failed to fetch {match_id}: {e}")
            continue

        with open(file_path, "w") as f:
            json.dump(match_data, f)

        time.sleep(2.0)

    print(f"Done. Files saved in {save_dir}/")


def delete_all_matches(save_dir="data"):
    """Deletes every match JSON file in save_dir. Use when you want a clean slate."""
    deleted = 0
    for filename in os.listdir(save_dir):
        if filename.endswith(".json"):
            os.remove(os.path.join(save_dir, filename))
            deleted += 1
    print(f"Deleted {deleted} match files from {save_dir}/")