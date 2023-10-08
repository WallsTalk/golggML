
import json
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def main ():
    df = pd.read_csv('12.csv')
    #ordinal_encoder = OrdinalEncoder()
    #df[["teamB", "teamR"]] = ordinal_encoder.fit_transform(df[["teamB", "teamR"]])
    with open("event_dict.json", "r") as eventsf:
        events_dict = {v: k for k, v in json.load(eventsf).items()}

    df = df.dropna(subset=["time0"])
    predict_df = df[df["turney"].str.contains("World Championship")].head(1)
    seasondf_main = df[~df["turney"].str.contains("World Championship")]
    season_df = seasondf_main[list(seasondf_main.filter(regex="pid").columns)]
    predict_df = predict_df[list(seasondf_main.filter(regex="pid").columns)]
    forest_model = RandomForestRegressor()
    i=0
    while True:
        time_str = "time" + str(i)
        time = seasondf_main[time_str]
        print(time)
        x=1
        x=1