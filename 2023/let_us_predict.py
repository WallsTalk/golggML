
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np



df = pd.read_csv('2023/decent_data2.csv')
validation = pd.read_csv('2023/temp.csv')
#seasons = list(set(df["season"].tolist()))
df = df.drop(columns=df.filter(regex="(event|time)(id){0,1}[0-9]+").columns)

seasons = [12]
matches = [
    ["KT Rolster", "Bilibili Gaming"]
]

#learning_cols = df.filter(regex="[BR]{1}[TJMAS]{1}$").columns
pcols = df.filter(regex="(dmg-proc)B").columns
blcols = df.filter(regex="(dmg-proc)B").columns
rlcols = df.filter(regex="(dmg-proc)R").columns
lcols = list(blcols) + list(rlcols)
# for season in seasons:
#     for match in matches:
#         condition = (~df["turney"].str.contains("World")) & (df["teamB"] == match[0])
#         season = df.loc[df["season"]==season, :]
#         worlds = season.loc[condition, :]
#         regular = season.loc[condition, :]
#         #regular.
#         print(regular)

# make a set for each season of each team

cworlds = (df["turney"].str.contains("World"))
df[lcols] = df.loc[:, lcols].applymap(lambda x: float(x.replace("%", "")))

for season in seasons:
    s = df.loc[~cworlds & (df["season"] == season), :]
    teams = list(set(s.loc[:, "teamidB"].tolist() + s.loc[:, "teamidR"].tolist()))
    w = df.loc[cworlds & (df["season"] == season), :]
    for team in teams:
        w.loc[w["teamidB"] == team, blcols] = w.loc[w["teamidB"] == team, blcols].assign(**s.loc[s["teamidB"] == team, blcols].mean())
        w.loc[w["teamidR"] == team, rlcols] = w.loc[w["teamidR"] == team, rlcols].assign(**s.loc[s["teamidR"] == team, rlcols].mean())


trainw = w.loc[:, lcols]
result = w.loc[:, "result"]
model = RandomForestRegressor()
model.fit(trainw, result)


## SEASON 13 maches

s = df.loc[~cworlds & (df["season"] == 13), :]
teams = list(set(s.loc[:, "teamB"].tolist() + s.loc[:, "teamR"].tolist()))
print(teams)
matches = [
    ["PSG Talon", "Team BDS"],
    ["GAM Esports", "Team Whales"],
     ["CTBC Flying Oyster", "Team BDS"],
     ["LOUD", "GAM Esports"],
     ["Detonation FocusMe", "Team BDS"],
     ["Movistar R7", "GAM Esports"],
     ["CTBC Flying Oyster", "Team Whales"],
     ["PSG Talon", "LOUD"],
     ["Team BDS", "Team Whales"],
     ["Detonation FocusMe", "CTBC Flying Oyster"],
     ["LOUD", "GAM Esports"],
     ["PSG Talon", "Movistar R7"],
]
matches = matches + [[match[1], match[0]] for match in matches]
predictdf = pd.DataFrame(columns=trainw.columns)
for match in range(len(matches)):
    predictdf = pd.concat([predictdf, pd.concat([s.loc[s["teamB"] == matches[match][0], blcols].mean(), s.loc[s["teamR"] == matches[match][1], rlcols].mean()]).to_frame().T], ignore_index=True)

predictions = model.predict(predictdf)

predictions = [matches[i] + [predictions[i]]  for i in range(len(matches))]

validation["p"] = validation.loc[:, "result"]
for prediction in predictions:
    condition = (validation["teamB"] == prediction[0]) & (validation["teamR"] == prediction[1])
    validation.loc[condition, "p"] = prediction[2]#validation.loc[condition, ["error"]]#.applymap(lambda x: x-prediction[2])

validation.loc[:, "error"] = validation["result"] - validation["p"]
validation.loc[:, "error"] = validation["error"].apply(lambda x: abs(x))
print(validation[["teamB", "teamR", "result", "p", "error"]])

    # forest_model = RandomForestRegressor()
    # forest_model.fit(seasondf)
    # melb_preds = forest_model.predict(val_X)
    # print(mean_absolute_error(val_y, melb_preds))

    #lisset([team for teams in ["teamB", "teamR"] for team in df[teams].tolist()])
    x=1
    #df.columns[df.columns.str.contains(s)]

