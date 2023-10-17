
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
pid = df.filter(regex="pid[BR]{1}").columns
blcols = df.filter(regex="(dmg-proc)B").columns
rlcols = df.filter(regex="(dmg-proc)R").columns
lcols = list(blcols) + list(rlcols)


cworlds = (df["turney"].str.contains("World"))
df[lcols] = df.loc[:, lcols].applymap(lambda x: float(x.replace("%", "")))

for season in seasons:
    s = df.loc[~cworlds & (df["season"] == season), :]
    w = df.loc[cworlds & (df["season"] == season), :]
    teams = list(set(w.loc[:, "teamB"].tolist() + w.loc[:, "teamR"].tolist()))
    for team in teams:
        for col in blcols:
            w.loc[w["teamB"] == team, col + "min"] = s.loc[s["teamB"] == team, col].min()
            w.loc[w["teamB"] == team, col + "max"] = s.loc[s["teamB"] == team, col].max()
            w.loc[w["teamB"] == team, col] = s.loc[s["teamB"] == team, col].mean()
        for col in rlcols:
            w.loc[w["teamR"] == team, col+"min"] = s.loc[s["teamR"] == team, col].min()
            w.loc[w["teamR"] == team, col + "max"] = s.loc[s["teamR"] == team, col].max()
            w.loc[w["teamR"] == team, col] = s.loc[s["teamR"] == team, col].mean()

        # w.loc[w["teamidB"] == team, blcols] = w.loc[w["teamidB"] == team, blcols].assign(
        #     **s.loc[s["teamidB"] == team, blcols].mean())
        # w.loc[w["teamidR"] == team, rlcols] = w.loc[w["teamidR"] == team, rlcols].assign(
        #     **s.loc[s["teamidR"] == team, rlcols].mean())

# w[list(blcols)[:1] + list(rlcols)[:1] + ["teamB", "teamR"]]
lcols = list(blcols) + list(rlcols)
lcols = list(lcols) + list(blcols+"min") +list(rlcols+"min") + list(blcols+"max") +list(rlcols+"max")

trainw = w.loc[:, list(lcols) + list(pid)]
result = w.loc[:, "result"]
model = RandomForestRegressor()
model.fit(trainw, result)


## SEASON 13 maches
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
s = df.loc[~cworlds & (df["season"] == 13), :]
predictdf = pd.DataFrame(columns=trainw.columns)
for match in range(len(matches)):
    predictdf.loc[match, :] = [s.loc[s["teamB"] == matches[match][0], col].mean() for col in blcols] + \
                              [s.loc[s["teamR"] == matches[match][1], col].mean() for col in rlcols] + \
                              [s.loc[s["teamB"] == matches[match][1], col].min() for col in rlcols] + \
                              [s.loc[s["teamR"] == matches[match][1], col].min() for col in rlcols] + \
                              [s.loc[s["teamB"] == matches[match][1], col].max() for col in rlcols] + \
                              [s.loc[s["teamR"] == matches[match][1], col].max() for col in rlcols] + \
                              s.loc[(s["teamB"] == matches[match][0]), df.filter(regex="pidB").columns].iloc[1].to_list() + \
                                s.loc[(s["teamR"] == matches[match][0]), df.filter(regex="pidR").columns].iloc[1].to_list()
# print(predictdf[list(blcols)[:1] + list(rlcols)[:1]])
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

