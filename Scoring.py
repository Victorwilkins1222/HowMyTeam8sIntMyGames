
"""
import numpy as np
import pandas as pd


def add_lane_opponent_comparison(df):

    merged = df.merge(df, on=["match_id", "role"], suffixes=("", "_opp"))
    merged = merged[merged["team_id"] != merged["team_id_opp"]]
    merged["cs_diff_vs_lane_opponent"] = merged["cs"] - merged["cs_opp"]

    lane_data = merged[["match_id", "player_name", "role", "cs_diff_vs_lane_opponent"]]

    df = df.merge(lane_data, on=["match_id", "player_name", "role"], how="left")
    return df


def calculate_scores(df, weights=None):

    if weights is None:
        weights = {
            "kills": 1.0,
            "deaths": -1.5,
            "assists": 0.7,
            "vision_score": 0.5,
            "kill_participation": 1.0,
            "cs_diff_vs_lane_opponent": 1.0,
        }

    df["performance_score"] = 0.0

    for role, group in df.groupby("role"):
        idx = group.index
        score = np.zeros(len(group))

        for stat, weight in weights.items():
            values = group[stat].to_numpy(dtype=float)
            mean = np.mean(values)
            std = np.std(values)

            if std == 0:
                z = np.zeros(len(values))
            else:
                z = (values - mean) / std

            score += z * weight

        df.loc[idx, "performance_score"] = score

    df["performance_score"] = df["performance_score"].round(2)
    return df


def build_leaderboard(df, self_name=None):

    columns = [
        "match_id", "player_name", "role", "team_id", "win",
        "kills", "deaths", "assists", "vision_score",
        "kill_participation", "cs_diff_vs_lane_opponent", "performance_score"
    ]

    if self_name is None:
        leaderboard = df[columns].copy()
        return leaderboard.sort_values("performance_score")

    self_rows = df[df["player_name"] == self_name]
    other_rows = df[df["player_name"] != self_name][columns].copy()

    self_summary = pd.DataFrame([{
        "match_id": f"AVG of {len(self_rows)} games",
        "player_name": self_name,
        "role": "various" if self_rows["role"].nunique() > 1 else self_rows["role"].iloc[0],
        "team_id": "",
        "win": round(self_rows["win"].mean(), 2),
        "kills": round(self_rows["kills"].mean(), 2),
        "deaths": round(self_rows["deaths"].mean(), 2),
        "assists": round(self_rows["assists"].mean(), 2),
        "vision_score": round(self_rows["vision_score"].mean(), 2),
        "kill_participation": round(self_rows["kill_participation"].mean(), 2),
        "cs_diff_vs_lane_opponent": round(self_rows["cs_diff_vs_lane_opponent"].mean(), 2),
        "performance_score": round(self_rows["performance_score"].mean(), 2),
    }])

    leaderboard = pd.concat([self_summary, other_rows], ignore_index=True)
    leaderboard = leaderboard.sort_values("performance_score")
    return leaderboard


def run_full_pipeline(df, weights=None, self_name=None):

    df = add_lane_opponent_comparison(df)
    df = calculate_scores(df, weights=weights)
    leaderboard = build_leaderboard(df, self_name=self_name)
    return df, leaderboard
"""