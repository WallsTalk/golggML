
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np



df = pd.read_csv('decent_data2.csv')
validation = pd.read_csv('temp.csv')
#seasons = list(set(df["season"].tolist()))
df = df.drop(columns=df.filter(regex="(event|time)(id){0,1}[0-9]+").columns)

# matches = [
#     ["PSG Talon", "Team BDS"],
#     ["GAM Esports", "Team Whales"],
#      ["CTBC Flying Oyster", "Team BDS"],
#      ["LOUD", "GAM Esports"],
#      ["Detonation FocusMe", "Team BDS"],
#      ["Movistar R7", "GAM Esports"],
#      ["CTBC Flying Oyster", "Team Whales"],
#      ["PSG Talon", "LOUD"],
#      ["Team BDS", "Team Whales"],
#      ["Detonation FocusMe", "CTBC Flying Oyster"],
#      ["LOUD", "GAM Esports"],
#      ["PSG Talon", "Movistar R7"],
# ]
# matches = [
#     ["Gen.G eSports", "GAM Esports"],
#     ["T1", "Team Liquid"],
#      ["KT Rolster", "Bilibili Gaming"],
#      ["Dplus KIA", "G2 Esports"],
#      ["JD Gaming", "Team BDS"],
#      ["LNG Esports", "Fnatic"],
#      ["Weibo Gaming", "NRG"],
#     ["Cloud9", "MAD Lions"]
# ]
# winners = ["Gen.G eSports","KT Rolster","G2 Esports","LNG Esports","JD Gaming","Cloud9","T1","Weibo Gaming"]
# winners = [	"Dplus KIA","Bilibili Gaming","GAM Esports","Fnatic","Team BDS","MAD Lions","Team Liquid","NRG"]
# winners = ["KT Rolster", "T1", "LNG Esports", "Gen.G eSports"]
# winners = ["Cloud9", "JD Gaming", "Team Liquid", "Dplus KIA", "Weibo Gaming", "Fnatic", "Bilibili Gaming", "G2 Esports"]
# winners = ["Team BDS", "NRG", "MAD Lions", "GAM Esports"]
#winners = ["T1", "LNG Esports", "G2 Esports", "JD Gaming", "Fnatic", "Dplus KIA", "GAM Esports", "MAD Lions"]
winners = ['LNG Esports', 'T1', 'G2 Esports', 'JD Gaming', 'Bilibili Gaming']
matches = [[winners[winner], winners[wwiner]] if i ==0 else [winners[wwiner], winners[winner]] for winner in range(len(winners)) for wwiner in range(winner+1,len(winners)) for i in range(2)]

seasons = [8, 9, 10, 11, 12]

#learning_cols = df.filter(regex="[BR]{1}[TJMAS]{1}$").columns

pid = df.filter(regex="pid[BR]{1}").columns
blcols = df.filter(regex="(dmg-proc|gold-proc)B").columns
rlcols = df.filter(regex="(dmg-proc|gold-proc)R").columns

lcols = list(blcols) + list(rlcols)


cworlds = (df["turney"].str.contains("World"))
df[lcols] = df.loc[:, lcols].applymap(lambda x: float(x.replace("%", "")) if type(x) == str else x)

lcols = list(blcols) + list(rlcols)
lcols = list(lcols) + list(blcols+"min") +list(rlcols+"min") + list(blcols+"max") +list(rlcols+"max")
ww = pd.DataFrame(columns=df.columns)
for season in seasons:
    s = df.loc[~cworlds & (df["season"] == season), :].copy()
    w = df.loc[cworlds & (df["season"] == season), :].copy()
    teams = list(set(w.loc[:, "teamB"].tolist() + w.loc[:, "teamR"].tolist()))
    for team in teams:
        for col in blcols:
            w.loc[w["teamB"] == team, col + "min"] = np.array(sorted(s.loc[s["teamB"] == team, col].to_list())[:5]).mean()
            w.loc[w["teamB"] == team, col + "max"] = np.array(sorted(s.loc[s["teamB"] == team, col].to_list())[-5:]).mean()
            w.loc[w["teamB"] == team, col] = s.loc[s["teamB"] == team, col].mean()
        for col in rlcols:
            w.loc[w["teamR"] == team, col+"min"] = np.array(sorted(s.loc[s["teamR"] == team, col].to_list())[:5]).mean()
            w.loc[w["teamR"] == team, col + "max"] = np.array(sorted(s.loc[s["teamR"] == team, col].to_list())[-5:]).mean()
            w.loc[w["teamR"] == team, col] = s.loc[s["teamR"] == team, col].mean()
    ww = pd.concat([ww, w])


trainw = ww.loc[:, list(lcols) + list(pid)]
result = ww.loc[:, "result"]
# matches = matches + [[match[1], match[0]] for match in matches]





    ## SEASON 13 maches
_ranger = 40
for i in range(_ranger):
    model = RandomForestRegressor()
    model.fit(trainw, result)

    s = df.loc[~cworlds & (df["season"] == 13), :]
    predictdf = pd.DataFrame(columns=trainw.columns)
    for match in range(len(matches)):
        predictdf.loc[match, :] = [s.loc[s["teamB"] == matches[match][0], col].mean() for col in blcols] + \
                                  [s.loc[s["teamR"] == matches[match][1], col].mean() for col in rlcols] + \
                                  [s.loc[s["teamB"] == matches[match][1], col].min() for col in rlcols] + \
                                  [s.loc[s["teamR"] == matches[match][1], col].min() for col in rlcols] + \
                                  [s.loc[s["teamB"] == matches[match][1], col].max() for col in blcols] + \
                                  [s.loc[s["teamR"] == matches[match][1], col].max() for col in rlcols] + \
                                  s.loc[(s["teamB"] == matches[match][0]), df.filter(regex="pidB").columns].iloc[1].to_list() + \
                                    s.loc[(s["teamR"] == matches[match][0]), df.filter(regex="pidR").columns].iloc[1].to_list()
    # print(predictdf[list(blcols)[:1] + list(rlcols)[:1]])
    predictions = model.predict(predictdf)

    matches = [matches[i] + [predictions[i]] for i in range(len(matches))]

stats_dict = { }
for match in matches:
    if match[0] not in stats_dict:
        stats_dict[match[0]] = 0
    if match[1] not in stats_dict:
        stats_dict[match[1]] = 0

    temp = [0, 0]
    for stat in match[2:]:
        if float(stat) > 0.51:
            temp[0] += 1
        elif float(stat) < 0.49:
            temp[1] += 1
        else:
            temp[1] += 0.5
            temp[1] += 0.5

    if temp[0] - temp[1] > 4:
        stats_dict[match[0]] += 1
    elif temp[0] - temp[1] < -4:
        stats_dict[match[1]] += 1
    else:
        stats_dict[match[0]] += 0.5
        stats_dict[match[1]] += 0.5

# print(stats_dict)
print(dict(sorted(stats_dict.items(), key=lambda x:x[1], reverse=True)))
#validation["p"] = validation.loc[:, "result"]
# for prediction in predictions:
#     # condition = (validation["teamB"] == prediction[0]) & (validation["teamR"] == prediction[1])
#     # validation.loc[condition, "p"] = prediction[2]
#     print()
# validation.loc[:, "error"] = validation["result"] - validation["p"]
# validation.loc[:, "error"] = validation["error"].apply(lambda x: abs(x))
# print(validation[["teamB", "teamR", "result", "p", "error"]])
del ww
del w
del trainw
del predictdf
del cworlds
del result
del s
del model
del rlcols
del blcols