#scoring formula for higher is better
#score = 100 × (you / (you + opponent))
#scoring formula for lower is better
#score = 100 × (opponent / (you + opponent))

import numpy as np
import pandas as pd


from Data_Loader import *
from Enums import *

GAME_LENGTH = 10
TEAM_SIZE = 5
def calculate_score(you, opponent, is_higher_score):
    if you + opponent == 0:
        return 50  # or 0, or whatever makes sense for a 0-0 tie
    if is_higher_score:
        score = 100 * (you / (you + opponent))
    else:
        score = 100 * (opponent / (you + opponent))
    return round(score)

def create_score (df):
    assert len(df) == 2, "this function needs a 2 row dataframe hint: get_matchup() is what is expected"
    kill_score = calculate_score(df.iloc[0,stats.kills.value],df.iloc[1,stats.kills.value],True)
    death_score = calculate_score(df.iloc[0,stats.deaths.value],df.iloc[1,stats.deaths.value],False)
    assist_score = calculate_score(df.iloc[0,stats.assists.value],df.iloc[1,stats.assists.value],True)
    dmg_score = calculate_score(df.iloc[0,stats.dmgs.value],df.iloc[1,stats.dmgs.value],True)
    gold_score = calculate_score(df.iloc[0,stats.gold.value],df.iloc[1,stats.gold.value],True)
    vision_score = calculate_score(df.iloc[0,stats.visions.value],df.iloc[1,stats.visions.value],True)
    cs_score = calculate_score(df.iloc[0,stats.cs.value],df.iloc[1,stats.cs.value],True)
    kill_participation_score =calculate_score( df.iloc[0,stats.kill_participation.value], df.iloc[1,stats.kill_participation.value], True)
    # divided by 8 cause 8 things duh
    score = round((kill_score+ death_score+ assist_score+ dmg_score+ gold_score+ vision_score+ cs_score+kill_participation_score)/8)
    return score
def get_matchup(df,role):
    matchup = df.iloc[[role.value,role.value+TEAM_SIZE]]
    return matchup
def grab_game(df,currentGameNumber):
    df_game = df.iloc[currentGameNumber*GAME_LENGTH:(currentGameNumber+1)*GAME_LENGTH]
    return df_game
def score_all_games(df):
    total_rows = len(df)
    num_games = total_rows // GAME_LENGTH

    for game_number in range(num_games):
        df_game = grab_game(df, game_number)

        for role in Role_enum:
            matchup = get_matchup(df_game, role)

            your_row_pos = df_game.index[role.value]
            opp_row_pos  = df_game.index[role.value + TEAM_SIZE]

            your_score = create_score(matchup)
            opp_score  = create_score(matchup.iloc[[1, 0]])  # swap perspective

            df.loc[your_row_pos, 'score'] = your_score
            df.loc[opp_row_pos, 'score']  = opp_score

    return df.tail(10)






