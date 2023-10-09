
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os
import numpy as np
import re
import json


df = pd.read_csv(os.path.join(os.getcwd(),"2023", 'decent_data2.csv'))
seasons = list(set(df["season"].tolist()))
df[df.filter(regex="event[0-9]+").columns].apply(lambda x: x.astype("string", errors='ignore'))

# revers sweeps
x = df.loc[df["turney"].str.contains("World"), ["gameid", "teamidB", "teamidR", "season", "result", "turney"]]
r = x["teamidR"].tolist()
b = x["teamidB"].tolist()
g = x["gameid"].tolist()
m = [previous := 0] and [
    previous := previous if not set([b[i], r[i]]).difference([b[i - 1], r[i - 1]]) and g[i] == g[
        i - 1] + 1 else previous + 1 for i in range(1, len(g))]


m = [0] + m
x["match_id"] = m
del r
del b
del g
del m

x2 = x.groupby("match_id").count()["result"].rename("match_length")
x = x.join(x2, on="match_id")

l5 = x.loc[x["match_length"] == 5]["result"].tolist()
l5 = [l5[x:x+5] for x in range(0, len(l5),5)]
s = x.loc[x["match_length"] == 5]["season"].tolist()
s = [s[x] for x in range(0, len(s), 5)]

for i in range(len(s)):
    print((s[i], l5[i]))

del l5
del s
del x
del x2

# longest game
for season in seasons:
    times = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), ["season"] + list(df.filter(regex="time[0-9]+").columns)].to_numpy()
    events = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), ["season"] + list(df.filter(regex="event[0-9]+").columns)].to_numpy()
    times = [times[i][j] for i in range(len(events)) for j in range(len(events[i])) if events[i][j] in ['rnexus', 'bnexus']]
    print(season, max(times)//60, max(times)%60)

del times
del events


# pentakills


# dragons
rex = "ocean-dragon|cloud-dragon|elder-dragon|fire-dragon|hextech-dragon|mountain-dragon|chemtech-dragon".split("|")
for season in seasons:
    events = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="event[0-9]+").columns)].to_numpy()
    events = [[k for k in rex if k in events[i][j]][0] for i in range(len(events)) for j in range(len(events[i])) if "dragon" in str(events[i][j]) ]
    dragons = np.unique(events, return_counts=True)
    print(season, {dragons[0][i]:dragons[1][i] for i in range(len(dragons[0]))})

del dragons
del events



# pentas
for season in seasons:
    player_dict = {}
    pentas = df.loc[(df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="penta-kills").columns)].to_numpy()
    players = df.loc[(df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="player").columns)].to_numpy()
    for g in range(len(pentas)):
        for p in range(len(pentas[g])):
            if pentas[g][p] > 0:
                if players[g][p] not in player_dict:
                    player_dict[players[g][p]] = 0
                player_dict[players[g][p]] += 1
    print(season, player_dict)


# Who will play the most different Champions at Worlds?
turneys= {}
for season in seasons:
    kills = df.loc[~(df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="^kills").columns)].to_numpy()
    players = df.loc[~(df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="player").columns)].to_numpy()
    turney_max = {0:[]}
    for k in range(len(kills)):
        if max(kills[k]) >= min(turney_max):
            for p in range(len(kills[k])):
                if kills[k][p] == max(kills[k]):
                    if int(max(kills[k])) not in turney_max:
                        turney_max[int(max(kills[k]))] = []
                    turney_max[int(max(kills[k]))].append(players[k][p])
            if len(turney_max) > 5:
                turney_max_l = sorted(turney_max, reverse=True)
                turney_max.pop(turney_max_l[5])

    turney_max_l = sorted(turney_max, reverse=True)
    turney_max = {i: turney_max[i] for i in turney_max_l}
    print(season, turney_max, indent=2)

# Who will have the highest KDA at Worlds?

for season in seasons:
    player_dict = {}
    kills = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="^kills").columns)].to_numpy()
    assists = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="^assists").columns)].to_numpy()
    deaths = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="^deaths").columns)].to_numpy()
    players = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), list(df.filter(regex="player").columns)].to_numpy()

    for k in range(len(kills)):
        for p in range(len(kills[k])):
            if players[k][p] not in player_dict:
                player_dict[players[k][p]] = {"k": 0, "d": 0, "a": 0}
            player_dict[players[k][p]]["k"] += kills[k][p]
            player_dict[players[k][p]]["d"] += deaths[k][p]
            player_dict[players[k][p]]["a"] += assists[k][p]

    print(season,  sorted(player_dict.items(), key=lambda x:x[1], reverse=True))
## Who will play the most different Champions at Worlds?

for season in seasons:
    player_dict = {}
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    champs = df.loc[cond, list(df.filter(regex="^assists").columns)].to_numpy()
    players = df.loc[cond, list(df.filter(regex="player").columns)].to_numpy()

    for k in range(len(players)):
        for p in range(len(players[k])):
            if players[k][p] not in player_dict:
                player_dict[players[k][p]] = []
            if champs[k][p] not in player_dict[players[k][p]]:
                player_dict[players[k][p]].append(champs[k][p])

    for player, champs in player_dict.items():
        player_dict[player] = len(champs)
    print(season,  sorted(player_dict.items(), key=lambda x:x[1], reverse=True))

# Which team will play the most different Champions at Worlds?

for season in seasons:
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    champs = df.loc[cond, list(df.filter(regex="^champs").columns)].to_numpy()
    teams = df.loc[cond, list(df.filter(regex="team[RB]").columns)].to_numpy()

    team_champs = {}
    for pair in range(len(teams)):
        if teams[pair][0] not in team_champs:
            team_champs[teams[pair][0]] = []
        for c in champs[pair][:5]:
            if c not in team_champs[teams[pair][0]]:
                team_champs[teams[pair][0]].append(c)

        if teams[pair][1] not in team_champs:
            team_champs[teams[pair][1]] = []
        for c in champs[pair][5:]:
            if c not in team_champs[teams[pair][1]]:
                team_champs[teams[pair][1]].append(c)

    team_champs = {team: len(team_champs[team]) for team in team_champs}
    print(season, sorted(team_champs.items(), key=lambda x: x[1], reverse=True))


# Who will have the most total Deaths at Worlds?
for season in seasons:
    champs_dict = {}
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    deaths = df.loc[cond, list(df.filter(regex="^deaths").columns)].to_numpy()
    champs = df.loc[cond, list(df.filter(regex="^champs").columns)].to_numpy()

    for k in range(len(champs)):
        for p in range(len(champs[k])):
            if champs[k][p] not in champs_dict:
                champs_dict[champs[k][p]] = 0

            champs_dict[champs[k][p]] += deaths[k][p]

    print(season, sorted(champs_dict.items(), key=lambda x: x[1], reverse=True))

# Who will be Picked the most during Champion Select at Worlds?
for season in seasons:
    champs_dict = {}
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    champs = df.loc[cond, list(df.filter(regex="^champs").columns)].to_numpy()

    for k in range(len(champs)):
        for p in range(len(champs[k])):
            if champs[k][p] not in champs_dict:
                champs_dict[champs[k][p]] = 0

            champs_dict[champs[k][p]] += 1
    print(season, sorted(champs_dict.items(), key=lambda x: x[1], reverse=True))

# Who will be played in the most different Roles at Worlds?

for season in seasons:
    champs_dict = {}
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    champs = df.loc[cond, list(df.filter(regex="^champs").columns)].to_numpy()

    for k in range(len(champs)):
        for p in range(len(champs[k])):
            if champs[k][p] not in champs_dict:
                champs_dict[champs[k][p]] = []
            if p == 0 or p == 5:
                if "t" not in champs_dict[champs[k][p]]:
                    champs_dict[champs[k][p]].append("t")
            if p == 1 or p == 6:
                if "j" not in champs_dict[champs[k][p]]:
                    champs_dict[champs[k][p]].append("j")
            if p == 2 or p == 7:
                if "m" not in champs_dict[champs[k][p]]:
                    champs_dict[champs[k][p]].append("m")
            if p == 3 or p == 8:
                if "a" not in champs_dict[champs[k][p]]:
                    champs_dict[champs[k][p]].append("a")
            if p == 4 or p == 9:
                if "s" not in champs_dict[champs[k][p]]:
                    champs_dict[champs[k][p]].append("s")


    champs_dict = {champ: len(champs_dict[champ]) for champ in champs_dict}
    print(season, sorted(champs_dict.items(), key=lambda x: x[1], reverse=True))


#Who will have the highest Win rate at Worlds? (Minimum 5 games played)

for season in seasons:
    champs_dict = {}
    cond = (~df["turney"].str.contains("World")) & (df["season"] == season)
    champs = df.loc[cond, list(df.filter(regex="^champs").columns)].to_numpy()

    for k in range(len(champs)):
        for p in range(len(champs[k])):