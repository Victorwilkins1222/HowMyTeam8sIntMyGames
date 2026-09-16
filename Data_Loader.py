import json
import os
import pandas as pd


def load_matches_to_dataframe(data_dir="data"):
    """
    Reads every match JSON file in data_dir, flattens each player's stats
    into one row, and returns a single combined dataframe.
    """
    rows = []

    for filename in os.listdir(data_dir):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(data_dir, filename)
        with open(filepath) as f:
            match = json.load(f)

        match_id = match["metadata"]["matchId"]
        game_duration = match["info"]["gameDuration"]

        for participant in match["info"]["participants"]:
            rows.append({
                "match_id": match_id,
                "game_duration": game_duration,
                "player_name": participant.get("riotIdGameName", participant.get("summonerName")),
                "champion": participant["championName"],
                "role": participant["teamPosition"],
                "team_id": participant["teamId"],
                "win": participant["win"],
                "kills": participant["kills"],
                "deaths": participant["deaths"],
                "assists": participant["assists"],
                "damage_to_champions": participant["totalDamageDealtToChampions"],
                "gold_earned": participant["goldEarned"],
                "vision_score": participant["visionScore"],
                "cs": participant["totalMinionsKilled"] + participant["neutralMinionsKilled"],
                "kill_participation": participant["challenges"].get("killParticipation", 0),
            })

    df = pd.DataFrame(rows)
    return df