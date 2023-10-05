import sqlite3
import os
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# for next year, just make corelation between kda of roles and worlds standings


# Root project dir
# root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
# path_to_db = os.path.join(root, "ML", "stats.db")
#conn = sqlite3.connect(path_to_db)
conn = sqlite3.connect("stats.db")
c = conn.cursor()

# STEP 1 MAKE a dataframe of team/picks/stats tables for wanted date

games = pd.read_sql_query("SELECT * FROM game;", conn)
gt_picks = pd.read_sql_query("SELECT * FROM game_team_picks;", conn)
gt_stats = pd.read_sql_query("SELECT * FROM game_team_stats;", conn)
teams_tuple = c.execute("SELECT * FROM team;").fetchall()
teams = {team[1]: [] for team in teams_tuple}

for team in teams_tuple:
    teams[team[1]] += [team[0]]

print(teams)

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
worlds_teams = ['Royal Never Give Up', 'Funplus Phoenix', 'Edward Gaming', 'LNG Esports', 'Rogue', 'Fnatic', 'MAD Lions', 'DWG KIA', 'T1', 'Hanwha Life eSports', 'Gen.G eSports', '100 Thieves', 'Team Liquid', 'Cloud9', 'Detonation FocusMe']
groups = {
"Group A": [[0, 0], [("DWG KIA", '#1aaf6c', "DWG"), ("Funplus Phoenix", '#DC0303', "FPX"), ("Rogue", '#0B1BA2', "RGE"), ('Cloud9', '#E7EE00', 'C9')]],
"Group B": [[0, 1], [("Edward Gaming", '#0B1BA2', "EDG"), ("T1", '#DC0303', "T1"), ("100 Thieves", '#1aaf6c', "100T"),  ('Detonation FocusMe', '#E7EE00', 'DFM')]],
"Group C": [[1, 0], [("Fnatic", '#0B1BA2', "FNC"), ("Royal Never Give Up", '#DC0303', "RNG"), ('Hanwha Life eSports', '#E7EE00', 'HNW'), ]],
"Group D": [[1, 1], [("MAD Lions", '#DC0303', "MAD"), ("Gen.G eSports", '#1aaf6c', "GEN"), ("Team Liquid", '#0B1BA2', "TL"), ('LNG Esports', '#E7EE00', 'LNG')]]
}
coff_power = {"top": 1.5, "jg": 2, "mid": 2, "adc": 1, "sup": 1}
coff_kp = {"top": 1, "jg": 2, "mid": 2, "adc": 1, "sup": 2}
coff_econ = {"top": 2, "jg": 2, "mid": 2, "adc": 2, "sup": 1}
coff_brain = {"top": 1, "jg": 2, "mid": 2, "adc": 1, "sup": 1}
column_names = {0: 'dps', 1: 'meta', 2: 'vitality', 3: 'gold_digging', 4: 'blood_shed', 5: 'execution'}

# how mutch teams dps
# dps.   
def calculate_dps(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['DPM'] * coff_power[role]
    return score


def calculate_meta(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['DMG%'] * coff_power[role]
        score += stats[team][role]['KP%'] * coff_kp[role]
    return score


#this function looks at avg dmg dealt against avg dmg taken
# raw_team fighting
# from 0 to 2
def calculate_team_fighting(team, stats):
    score = {"dealt": 0, "taken": 0}
    for role in roles:
        score["dealt"] += stats[team][role]['TotaldamagetoChampion']
        score["taken"] += stats[team][role]['Totaldamagetaken']
    score = score["dealt"]/score["taken"]
    return score


# 15 mins lead
# from 0 to 8
def calculate_early_lead(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['GD@15'] * coff_power[role]
        score += stats[team][role]['CSD@15'] * coff_econ[role]
        score += stats[team][role]['XPD@15'] * coff_econ[role]
    return score


# Gold per minute
# economy
def calculate_economy(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['GPM'] * coff_power[role]
    return score


#K+A perminute
#0-2
def calculate_tempo(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['K+APerMinute'] * coff_kp[role]    
    return score


# from 0 to 3
def calculate_execution(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['KDA'] * coff_power[role]   
    return round(score/5-5, 2)



def make_list(look_at, from_stats):
    column = [
    calculate_dps(look_at, from_stats),
    calculate_meta(look_at, from_stats),
    calculate_team_fighting(look_at, from_stats),
    calculate_economy(look_at, from_stats),
    calculate_tempo(look_at, from_stats),
    calculate_execution(look_at, from_stats)
    ]  
    return column



def make_role_stats(team_df):
    role_stats = {}
    for role in roles:
        role_stats[role] = {} 
        for stat in stat_types:
            column = team_df[role][team_df["stat_type"]==stat]
            if stat in ["GOLD%", "VS%", "DMG%", "KP%"]:
                column = column.apply(lambda x: np.nan if str(x) == '' else x)
                column = column.apply(lambda x: x.replace('%', '') if '%' in str(x) else x)
            elif stat == "KDA":
                column = column.apply(lambda x: 0 if x == 'Perfect KDA' else float(x))
                column = column.apply(lambda x: column.max() if x == 'Perfect KDA' else x)  
            role_stats[role][stat] = float("{0:.2f}".format(pd.to_numeric(column).mean()))
    return role_stats

def make_team_stats_avg():
    team_stats = {}
    for team_id in teams.values():
        team_stats[team_id] = {}
        team_df = df[df["team_id"] in team_id]
        team_stats[team_id] = make_role_stats(team_df)
    return team_stats

def make_team_stats_lost():
    team_stats = {}
    for team_id in teams.values():
        team_stats[team_id] = {}
        team_df = df[(df["team_id"] == team_id) & (df["result"] == 0)]
        team_stats[team_id] = make_role_stats(team_df)
    return team_stats


def make_team_stats_blue():
    team_stats = {}
    for team_id in teams.values():
        team_stats[team_id] = {}
        team_df = df[(df["team_id"] == team_id) & (df["b_team_id"] == team_id)]
        team_stats[team_id] = make_role_stats(team_df)
    return team_stats

def make_team_stats_red():
    team_stats = {}
    for team_id in teams.values():
        team_stats[team_id] = {}
        team_df = df[(df["team_id"] == team_id) & (df["r_team_id"] == team_id)]
        team_stats[team_id] = make_role_stats(team_df)
    return team_stats



def calculate_brain(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['Deaths'] * coff_brain[role]
    return score

def calculate_teamwork(team, stats):
    score = 0
    for role in roles:
        score += stats[team][role]['Assists'] * coff_kp[role]
    return score

def calculate_balance(team, stats=df):
    blue_games = []
    red_games = []
    for game in df["game_id"][df["team_id"]==team].unique():
        blue_games += stats["result"][(stats["b_team_id"]==team) & (stats["team_id"]==team) & (stats["game_id"]==game)].unique().tolist()
        red_games += stats["result"][(stats["r_team_id"]==team) & (stats["team_id"]==team) & (stats["game_id"]==game)].unique().tolist()
    b_wr = sum(blue_games)/len(blue_games)
    r_wr = sum(red_games)/len(red_games)
    if b_wr > r_wr:
        score = r_wr/b_wr
    elif r_wr > b_wr:
        score = b_wr/r_wr
    else:
        score = 1
    return score

### for avg analysis use: 'GPM', 'DPM', 'TotaldamagetoChampion', 'Totaldamagetaken'
### for defeat analysis use: 'DMG%', 'GOLD%', 'KP%'
### for tempo analysis use: 'GD@15', 'CSD@15', 'XPD@15', 'LVLD@15', 'K+APerMinute'


avg_stats = make_team_stats_avg()
lost_stats = make_team_stats_lost()
# blue_stats = make_team_stats_blue()
# red_stats = make_team_stats_red()





world_stats_dict = {team: make_list(teams[team], avg_stats) for team in worlds_teams}
df_world_stats = pd.DataFrame(data=world_stats_dict).T.rename(columns=column_names)
df_world_stats.reset_index(level=0, inplace=True)
df_world_stats = df_world_stats.rename(columns={"index" : "team_name"})
df_world_stats["spirit"] = np.nan
df_world_stats["brain"] = np.nan
df_world_stats["teamwork"] = np.nan
df_world_stats["balance"] = np.nan

world_stats_dict_spirit = {team: make_list(teams[team], lost_stats) for team in worlds_teams}
df_world_stats_spirit = pd.DataFrame(data=world_stats_dict_spirit).T.rename(columns=column_names)
df_world_stats_spirit.reset_index(level=0, inplace=True)
df_world_stats_spirit = df_world_stats_spirit.rename(columns={"index" : "team_name"})
for team in worlds_teams:
    df_world_stats.loc[df_world_stats["team_name"]==team, "spirit"] = sum(df_world_stats_spirit[df_world_stats_spirit["team_name"]==team].iloc[:, [1, 3, 4, 5, 6]].values.tolist()[0]) + 3
    df_world_stats.loc[df_world_stats["team_name"]==team, "brain"] = calculate_brain(teams[team], lost_stats)
    df_world_stats.loc[df_world_stats["team_name"]==team, "teamwork"] = calculate_teamwork(teams[team], lost_stats)
    df_world_stats.loc[df_world_stats["team_name"]==team, "balance"] = calculate_balance(teams[team])

df_world_stats["brain"] = [(val-max(df_world_stats["brain"].tolist()))*(-1)+1 for val in df_world_stats["brain"].tolist()]


for column in df_world_stats.columns[1:]:
    normalised = [val/max(df_world_stats[column].tolist()) for val in df_world_stats[column].tolist()]
    df_world_stats[column] = normalised




print(df_world_stats.sort_values("balance", ascending=False))




def add_to_star(place, team, color, label=None):
    values = df_world_stats.loc[df_world_stats["team_name"]==team].values[0][1:].tolist()
    values += values[:1]
    print(place)
    if label != None:
        ax[place[0], place[1]].plot(angles, values, color=color, linewidth=1, label=label)
    else:
        ax[place[0], place[1]].plot(angles, values, color=color, linewidth=1, label=team)
    ax[place[0], place[1]].fill(angles, values, color=color, alpha=0.25)

labels = df_world_stats.columns[1:]
points = len(df_world_stats.columns[1:])
angles = np.linspace(0, 2 * np.pi, points, endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(2, 2, figsize=(6, 6), subplot_kw=dict(polar=True))
for group, teams in groups.items():
    for team in teams[1]:
        print(teams[0], *team)
        add_to_star(teams[0], *team)
    ax[teams[0][0], teams[0][1]].set_theta_offset(np.pi / 2)
    ax[teams[0][0], teams[0][1]].set_theta_direction(-1)
    # Edit x axis labels
    for label, angle in zip(ax[teams[0][0], teams[0][1]].get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
    ## Customize your graphic
    # Change the location of the gridlines or remove them
    ax[teams[0][0], teams[0][1]].set_rgrids([0.2, 0.4, 0.6 , 0.8, 1])
    # #ax.set_rgrids([]) # This removes grid lines
    # # Change the color of the ticks
    ax[teams[0][0], teams[0][1]].tick_params(colors='#222222')
    # # Make the y-axis labels larger, smaller, or remove by setting fontsize
    ax[teams[0][0], teams[0][1]].tick_params(axis='y', labelsize=0)
    # # Make the x-axis labels larger or smaller.
    ax[teams[0][0], teams[0][1]].tick_params(axis='x', labelsize=13)
    # # Change the color of the circular gridlines.
    ax[teams[0][0], teams[0][1]].grid(color='#AAAAAA')
    # # Change the color of the outer circle
    ax[teams[0][0], teams[0][1]].spines['polar'].set_color('#222222')
    # # Change the circle background color
    ax[teams[0][0], teams[0][1]].set_facecolor('#FAFAFA')
    # # Add title and legend
    ax[teams[0][0], teams[0][1]].set_title(group, y=1.08)
    ax[teams[0][0], teams[0][1]].legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    # # Draw axis lines for each angle and label.
    ax[teams[0][0], teams[0][1]].set_thetagrids(np.degrees(angles[:-1]), labels)

plt.show()




# for group, teams in groups.items():
#     fig, ax = plt.subplots(2, 2, figsize=(6, 6), subplot_kw=dict(polar=True))
#     for team in teams:
#         add_to_star(*team)
#     ## Fix axis to star from top
#     ax.set_theta_offset(np.pi / 2)
#     ax.set_theta_direction(-1)
#     ## Edit x axis labels
#     for label, angle in zip(ax.get_xticklabels(), angles):
#         if angle in (0, np.pi):
#             label.set_horizontalalignment('center')
#         elif 0 < angle < np.pi:
#             label.set_horizontalalignment('left')
#         else:
#             label.set_horizontalalignment('right')
#     ## Customize your graphic
#     # Change the location of the gridlines or remove them
#     ax.set_rgrids([0.2, 0.4, 0.6 , 0.8, 1])
#     # #ax.set_rgrids([]) # This removes grid lines
#     # # Change the color of the ticks
#     ax.tick_params(colors='#222222')
#     # # Make the y-axis labels larger, smaller, or remove by setting fontsize
#     ax.tick_params(axis='y', labelsize=0)
#     # # Make the x-axis labels larger or smaller.
#     ax.tick_params(axis='x', labelsize=13)
#     # # Change the color of the circular gridlines.
#     ax.grid(color='#AAAAAA')
#     # # Change the color of the outer circle
#     ax.spines['polar'].set_color('#222222')
#     # # Change the circle background color
#     ax.set_facecolor('#FAFAFA')
#     # # Add title and legend
#     ax.set_title(group, y=1.08)
#     ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
#     # # Draw axis lines for each angle and label.
#     ax.set_thetagrids(np.degrees(angles[:-1]), labels)





