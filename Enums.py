from enum import Enum

class Role_enum(Enum):
    Top = 0
    JG = 1
    Mid = 2
    Bot = 3
    Utility = 4

class stats(Enum):
    kills = 8
    deaths = 9
    assists = 10
    dmgs = 11
    gold = 12
    visions = 13
    cs = 14
    kill_participation = 15
