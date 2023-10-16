
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor



df = pd.read_csv('2023/decent_data2.csv')
#seasons = list(set(df["season"].tolist()))
df = df.drop(columns=df.filter(regex="(event|time)(id){0,1}[0-9]+").columns)

seasons = [12]
matches = [
    ["KT Rolster", "Bilibili Gaming"]
]

#learning_cols = df.filter(regex="[BR]{1}[TJMAS]{1}$").columns
learning_cols = df.filter(regex="dmg-proc").columns
for season in seasons:
    for match in matches:
        condition = (~df["turney"].str.contains("World")) & (df["teamB"] == match[0])
        season = df.loc[df["season"]==season, :]
        worlds = season.loc[condition, :]
        regular = season.loc[condition, :]
        regular.
        print(regular)

# make a set for each season of each team

condition_nw = (~df["turney"].str.contains("World"))
for season in seasons:
    s = df.loc[df["season"] == season, :]
    s = season.loc[:, learning_cols].apply( lambda x: x.replace("%", ""))
    print(season[learning_cols] )
    teams = list(set(df.loc[:, "teamidB"].tolist() + df.loc[:, "teamidR"].tolist()))
    #regular = season.loc[condition_nw, :]
    for team in teams:
        teamb = season.loc[season["teamidB"] == team, learning_cols]
        teamr = season.loc[season["teamidB"] == team, learning_cols]







    # forest_model = RandomForestRegressor()
    # forest_model.fit(seasondf)
    # melb_preds = forest_model.predict(val_X)
    # print(mean_absolute_error(val_y, melb_preds))

    #lisset([team for teams in ["teamB", "teamR"] for team in df[teams].tolist()])
    x=1
    #df.columns[df.columns.str.contains(s)]

