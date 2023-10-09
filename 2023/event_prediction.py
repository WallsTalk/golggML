
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# C:/Users/PC/PycharmProjects/golggML/2023/event_prediction.py:8: DtypeWarning: Columns (822,825,828,831,834,837,840,843,846,849,852,855,858,861,864,867,870,873,876,879,882,885,888,891,894,897,900,903,906,909,912,915,918,921,924,927,930,933,936,939,942,945,948,951,954,957,960,963,966,969,972,975,978,981,984,987,990,993,996,999,1002,1005,1008,1011,1014,1017,1020,1023,1026,1029,1032,1035,1038,1041,1044,1047,1050,1053,1056,1059,1062,1065,1068,1071,1074,1077,1080,1083,1086,1089,1092,1095,1098,1101,1104,1107,1110,1113,1116,1119,1122,1125,1128,1131,1134,1137,1140,1143,1146,1149,1152,1155,1158,1161,1164,1167,1170,1173,1176,1179,1182,1185,1188,1191,1194,1197,1200,1203,1206,1209,1212,1215,1218,1221,1224,1227,1230,1233,1236,1239) have mixed types. Specify dtype option on import or set low_memory=False.
def main ():
    df = pd.read_csv('decent_data2.csv')
    df.drop(df.filter(regex="event[0-9]+"), axis=1, inplace=True)
    df.dropna(subset=["time0", "eventid0"], inplace=True)

    season_df = df.loc[:, list(df.filter(regex="pid").columns) + ["turneyid", "teamidB", "teamidR"]]
    blue_teams = ["Team BDS", "LOUD", "Detonation FocusMe"] #"Movistar R7", "LOUD", "DetonatioN FocusMe"
    red_teams = ["Golden Guardians", "GAM Esports", "CTBC Flying Oyster"] #"PSG Talon", "GAM Esports", "CTBC Flying Oyster"
    predict_df = pd.DataFrame(
    {col: [df.loc[df["teamB"] == team, col].iloc[0] for team in blue_teams] for col in df[list(df.filter(regex="pidB"))].columns} |
    {col: [df.loc[df["teamR"] == team, col].iloc[0] for team in red_teams] for col in df[list(df.filter(regex="pidR"))].columns} |
    {
        "turneyid": [df.loc[df["turney"] == "World Championship", "turneyid"].iloc[0]] * len(blue_teams),
        "teamidB": [df.loc[df["teamB"] == team, "teamidB"].iloc[0] for team in blue_teams],
        "teamidR": [df.loc[df["teamB"] == team, "teamidR"].iloc[0] for team in red_teams],
    }
    )

    time_model = RandomForestRegressor()
    event_model = RandomForestRegressor()
    i=0

    finished_df = pd.DataFrame(df.columns)
    while True:
        time_str = "time" + str(i)
        time = df[time_str]
        x=1
        time_model.fit(season_df, time)
        predict_df[time_str] = time_model.predict(predict_df)
        predict_df[time_str] = predict_df[time_str].apply(lambda x: round(x))
        season_df[time_str] = time

        event_str = "eventid" + str(i)
        event = df[event_str]

        event_model.fit(season_df, event)
        predict_df[event_str] = event_model.predict(predict_df)
        predict_df[event_str] = predict_df[event_str].apply(lambda x: round(x))
        season_df[event_str] = event



        print(predict_df.iloc[:, 13:])
        finished_index = predict_df[(predict_df[event_str] == 6166) | (predict_df[event_str] == 417)].index
        if len(finished_index) > 0:
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