
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def main ():
    df = pd.read_csv('decent_data.csv')
    df["turney"] = df["turney"].apply(lambda x: x.split(" 20")[0])
    all_turneys = list(set(df["turney"].tolist()))
    all_turneys = {all_turneys[i]: i for i in range(len(all_turneys))}
    all_teams = list(set([item for col, vals in df[["teamB", "teamR"]].items() for item in vals.tolist()]))
    all_teams = {all_teams[i]: i for i in range(len(all_teams))}

    df["turneyid"] = df.replace({"turney": all_turneys})["turney"]
    df["teamidB"] = df.replace({"teamB": all_teams})["teamB"]
    df["teamidR"] = df.replace({"teamR": all_teams})["teamR"]

    with open("event_dict.json", "r") as eventsf:
        events_dict = {v: k for k, v in json.load(eventsf).items()}

    df = df.dropna(subset=["time0"])

    season_df = df.loc[:, ["turneyid", "teamidB", "teamidR"] + list(df.filter(regex="pid").columns)]
    blue_teams = ["Team BDS", "LOUD", "Detonation FocusMe"] #"Movistar R7", "LOUD", "DetonatioN FocusMe"
    red_teams = ["Golden Guardians", "GAM Esports", "CTBC Flying Oyster"] #"PSG Talon", "GAM Esports", "CTBC Flying Oyster"
    predict_df = pd.DataFrame({
        "turneyid": [all_turneys["World Championship"]] * len(blue_teams),
        "teamidB": [all_teams[team] for team in blue_teams],
        "teamidR": [all_teams[team] for team in red_teams],
    } |
    {col: [df.loc[df["teamB"] == team, col].iloc[0] for team in blue_teams] for col in df[list(df.filter(regex="pidB"))].columns} |
    {col: [df.loc[df["teamR"] == team, col].iloc[0] for team in red_teams] for col in df[list(df.filter(regex="pidR"))].columns}
    )

    forest_model = RandomForestRegressor()
    i=0

    finished_df = pd.DataFrame(df.columns)
    while True:
        time_str = "time" + str(i)
        time = df[time_str]

        forest_model.fit(season_df, time)
        predict_df[time_str] = forest_model.predict(predict_df)
        predict_df[time_str] = predict_df[time_str].apply(lambda x: round(x))
        season_df[time_str] = time



        event_str = "event" + str(i)
        event = df[event_str]

        forest_model.fit(season_df, event)
        predict_df[event_str] = forest_model.predict(predict_df)
        predict_df[event_str] = predict_df[event_str].apply(lambda match: min(events_dict, key=lambda x: abs(x-match)))
        season_df[event_str] = event



        print(predict_df.iloc[:, 13:])
        finished_index = predict_df[(predict_df[event_str] == 6166) | (predict_df[event_str] == 417)].index
        finished_df.loc[len(finished_df)] = finished_index
        predict_df.drop(finished_index, inplace=True)

        if len(predict_df.index) > 0:
            i+=1
        else:
            break

    finished_df.to_csv("what_a_games.csv", sep=",", index=False)


    # forest_model = RandomForestRegressor()
    # forest_model.fit(seasondf)
    # melb_preds = forest_model.predict(val_X)
    # print(mean_absolute_error(val_y, melb_preds))

    #lisset([team for teams in ["teamB", "teamR"] for team in df[teams].tolist()])
    x=1
    #df.columns[df.columns.str.contains(s)]

if __name__== "__main__":
    main()