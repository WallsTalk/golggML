
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import os
import numpy as np
import re


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


# pentakills


# dragons
rex = "ocean-dragon|cloud-dragon|elder-dragon|fire-dragon|hextech-dragon|mountain-dragon|chemtech-dragon".split("|")
for season in seasons:
    events = df.loc[(~df["turney"].str.contains("World")) & (df["season"] == season), ["season"] + list(df.filter(regex="event[0-9]+").columns)].to_numpy()
    events = [[k for k in rex if k in events[i][j]][0] for i in range(len(events)) for j in range(len(events[i])) if "dragon" in str(events[i][j]) ]
    dragons = np.unique(events, return_counts=True)
    print(season, {dragons[0][i]:dragons[1][i] for i in range(len(dragons[0]))})





