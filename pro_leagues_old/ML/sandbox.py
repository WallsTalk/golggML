import sqlite3
import os
import pandas as pd
import numpy as py
import date


# for next year, just make corelation between kda of roles and worlds standings


# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "ML", "stats.db")
#conn = sqlite3.connect(path_to_db)
conn = sqlite3.connect("stats.db")
c = conn.cursor()

# STEP 1 MAKE a dataframe of team/picks/stats tables for wanted date
# region = {"LEC": [], "LPL": [], "LCK": [], "LCS": []}
# for t in c.execute("SELECT * FROM team;").fetchall():
#     region[t[2]].append([t[1], t[0]])
games = pd.read_sql_query("SELECT * FROM game;", conn)
gt_picks = pd.read_sql_query("SELECT * FROM game_team_picks;", conn)
gt_stats = pd.read_sql_query("SELECT * FROM game_team_stats;", conn)
teams = dict(map(lambda team: (team[1], team[0]), c.execute("SELECT * FROM team;").fetchall()))


conn.commit()
conn.close()

df = pd.merge(games, gt_stats, on="game_id")
df = pd.merge(df, gt_picks, on=["game_id", "team_id"])
df['game_date'] = pd.to_datetime(df['game_date'])
df = df[df['game_date'] > datetime.datetime(2021, 5, 1)]


# df = df.set_index(['game_id'])
# df = df.loc['2021-05-01 10':]





# STEP 2 MAKE AVG stats of all the teams for each role

stat_types = df["stat_type"].unique().tolist()
roles = ["top", "jg", "mid", "adc", "sup"]
team_stats = {}
for team_id in teams.values():
    team_stats[team_id] = {}
    team_df = df[df["team_id"] == team_id]
    for role in roles:
        team_stats[team_id][role] = {} 
        for stat in stat_types:
            column = team_df[role][team_df["stat_type"]==stat]
            if stat in ["GOLD%", "VS%", "DMG%", "KP%"]:
                column = column.apply(lambda x: np.nan if str(x) == '' else x)
                column = column.apply(lambda x: x.replace('%', '') if '%' in str(x) else x)
            elif stat == "KDA":
                column = column.apply(lambda x: 0 if x == 'Perfect KDA' else float(x))
                column = column.apply(lambda x: column.max() if x == 'Perfect KDA' else x)
            
            team_stats[team_id][role][stat] = float("{0:.2f}".format(pd.to_numeric(column).mean()))


worlds_teams = ['Royal Never Give Up', 'Funplus Phoenix', 'Edward Gaming', 'Rogue', 'Fnatic', 'MAD Lions', 'DWG KIA', 'T1', 'Gen.G eSports', '100 Thieves', 'Team Liquid']


def show_comparison_stats(stat_to_check):
    data_kda = {"team":[], "top":[], "jg":[], "mid":[], "adc":[], "sup":[]}
    for team in worlds_teams:
        data_kda["team"].append(team)
        for role in team_stats[teams[team]]:
            data_kda[role].append(team_stats[teams[team]][role][stat_to_check])
    kda = pd.DataFrame(data=data_kda)
    print(stat_to_check)
    for role in roles:
        print(role)
        print(kda.sort_values(role, ascending=False))
# lambda x: pd.to_numeric()

show_comparison_stats('VisionScore')


# region kda insights
for reg in region.keys():
    for role in roles:
        reg_teams = list(map(lambda x: float(team_stats[x[1]][role]['KDA']), region[reg]))
        print(reg, role , min(reg_teams), max(reg_teams),  max(reg_teams) - min(reg_teams))

### for avg analysis use: 'GPM', 'DPM', 'TotaldamagetoChampion', 'Totaldamagetaken'
### for defeat analysis use: 'DMG%', 'GOLD%', 'KP%'
### for tempo analysis use: 'GD@15', 'CSD@15', 'XPD@15', 'LVLD@15', 'K+APerMinute'

coff_power = {"top": 1.5, "jg": 2, "mid": 2, "adc": 1, "sup": 1}
coff_kp = {"top": 1, "jg": 2, "mid": 2, "adc": 1, "sup": 2}
coff_econ = {"top": 2, "jg": 2, "mid": 2, "adc": 2, "sup": 1}


# how mutch teams dps
# dps.   
def calculate_dps(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['DPM'] * coff_power[role]
    return round(score/1000-2.5, 2)


def calculate_meta(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['DMG%'] * coff_power[role]
        score += team_stats[team][role]['KP%'] * coff_kp[role]
    return round(score/100-6, 2)


#this function looks at avg dmg dealt against avg dmg taken
# raw_team fighting
# from 0 to 2
def calculate_team_fighting(team):
    score = {"dealt": 0, "taken": 0}
    for role in roles:
        score["dealt"] += team_stats[team][role]['TotaldamagetoChampion']
        score["taken"] += team_stats[team][role]['Totaldamagetaken']
    score = score["dealt"]/score["taken"]
    return round(score*10-6, 2)


# 15 mins lead
# from 0 to 8
def calculate_early_lead(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['GD@15'] * coff_power[role]
        score += team_stats[team][role]['CSD@15'] * coff_econ[role]
        score += team_stats[team][role]['XPD@15'] * coff_econ[role]
    return round(score/1000, 2)


# Gold per minute
# economy
def calculate_economy(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['GPM'] * coff_power[role]
    return round(score/1000-2, 2)


#K+A perminute
#0-2
def calculate_tempo(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['K+APerMinute'] * coff_kp[role]    
    return round(score-1, 2)


# from 0 to 3
def calculate_execution(team):
    score = 0
    for role in roles:
        score += team_stats[team][role]['KDA'] * coff_power[role]   
    return round(score/5-5, 2)

def make_list(look_at):
    column = [
    calculate_dps(look_at),
    calculate_meta(look_at),
    calculate_team_fighting(look_at),
    calculate_early_lead(look_at),
    calculate_economy(look_at),
    calculate_tempo(look_at),
    calculate_execution(look_at)
    ]  
    return column 

world_stats_dict = {team: make_list(teams[team]) for team in worlds_teams}
world_stats_df = pd.DataFrame(data=world_stats_dict)

for team in worlds_teams:
    team
    world_stats_df[team][5]





