import sqlite3
import os
import pandas as pd
import numpy as py
import date


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

#match_up = ['Fnatic', '']
# >>> team_stats.keys()
# dict_keys([1105, 1109, 1107, 1116, 1113, 1111, 1104, 1102, 1103, 1108, 1112, 1114, 1110, 1101, 1106, 1117, 1115, 1154, 1151, 1148, 1150, 1153, 1147, 1149, 1152, 1156, 1155, 1092, 1093, 1096, 1098, 1097, 1091, 1125, 1094, 1126, 1099, 1129, 1133, 1128, 1132, 1131, 1130, 1134, 1136, 1127, 1135])
# >>> print(team_stats[1105].keys())
# dict_keys(['top', 'jg', 'mid', 'adc', 'sup'])
# >>> print(team_stats[1105]["top"].keys())
# dict_keys(['Kills', 'Deaths', 'Assists', 'KDA', 'CS', '"CSinTeamsJungle"', 'CSinEnemyJungle', 'CSM', 'Golds', 'GPM', 'GOLD%', 'VisionScore', 'Wardsplaced', 'Wardsdestroyed', 'ControlWardsPurchased', 'VSPM', 'WPM', 'VWPM', 'WCPM', 'VS%', 'TotaldamagetoChampion', 'PhysicalDamage', 'MagicDamage', 'TrueDamage', 'DPM', 'DMG%', 'K+APerMinute', 'KP%', 'Solokills', 'Doublekills', 'Triplekills', 'Quadrakills', 'Pentakills', 'GD@15', 'CSD@15', 'XPD@15', 'LVLD@15', 'Damagedealttoturrets', 'Totalheal', 'Damageselfmitigated', 'Timeccingothers', 'Totaldamagetaken'])
# >>> print(team_stats[1105]["top"]["Kills"])
# ['3', '3', '5', '3', '1', '0', '2', '4', '14', '2', '2', '4', '0', '0', '0', '1', '2', '4', '5', '14', '3', '0', '2', '2', '3', '0', '2', '6', '2', '0', '3', '1', '1', '2', '1', '1', '5', '2', '6', '3', '2', '2', '2', '1', '4', '2', '9', '4', '5', '6', '0', '0', '5', '0', '5', '5', '0', '6', '3', '5', '1', '0', '1', '4', '4', '1', '0', '1', '3', '10', '2', '4', '5']
# >>> print(len(team_stats[1105]["top"]["Kills"]))
# 73
# >>> print(teams[1105])
# Invictus Gaming

# Leaderboard for KDA
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




# this function looks at avg dmg dealt against other teams avg dmg taken "{0:.2f}".format(
def calculate_dmg_trade(team1, team2):
    t1_score = {"dealt": 0, "taken": 0}
    t2_score = {"dealt": 0, "taken": 0}
    for role in roles:
        t1_score["dealt"] += team_stats[team1][role]['TotaldamagetoChampion']
        t1_score["taken"] += team_stats[team1][role]['Totaldamagetaken']
        t2_score["dealt"] += team_stats[team2][role]['TotaldamagetoChampion']
        t2_score["taken"] += team_stats[team2][role]['Totaldamagetaken']
    print(t1_score["taken"] - t2_score["dealt"])
    print(t2_score["taken"] - t1_score["dealt"])

calculate_dmg_trade(teams['Rogue'], teams['DWG KIA'])



