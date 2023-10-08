


import json
import pandas as pd
import os
import numpy as np
import math


def main():
    seasons = [str(i) for i in range(8, 14)]
    game_history = []
    for season in seasons[-1:]:
        current_game_colection = "game_collection3_" + season
        with open(os.path.join(os.getcwd(), "work_history", current_game_colection), "r") as game_history_file:
            game_history += [json.loads(game) for game in game_history_file.read().split("\n")[:-1]]

    statsdf = []
    with open(os.path.join(os.getcwd(), "event_dict.json"), "r") as event_file:
        event_dict = json.load(event_file)
    with open(os.path.join(os.getcwd(), "player.json"), "r") as event_file:
        player_dict = json.load(event_file)

    for game in game_history:
        a = {
            "teamB": game["blue_team"],
            "resB": game["blue_result"],
            "teamR": game["red_team"],
            "resR": game["red_result"],

        }
        if len(game["stats"]["Role"]) == 10 and len(game["stats"]["champs"]) == 10:
            champ2role = {game["stats"]["champs"][i].replace(" ", "").lower(): game["stats"]["Role"][i] for i in range(10)}
        else:
            continue

        if "bel" in champ2role:
            champ2role["belveth"] = champ2role["bel"]
        if "kha" in champ2role:
            champ2role["khazix"] = champ2role["kha"]
        if "kai" in champ2role:
            champ2role["kaisa"] = champ2role["kai"]
        if "rek" in champ2role:
            champ2role["reksai"] = champ2role["rek"]
        if "kog" in champ2role:
            champ2role["kogmaw"] = champ2role["kog"]
        if "cho" in champ2role:
            champ2role["chogath"] = champ2role["cho"]
        if "k" in champ2role:
            champ2role["ksante"] = champ2role["k"]

        for stat, vals in game["stats"].items():
            stat_name = stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace(
                "+", "").lower()
            for i in range(10):
                if i < 5:
                    a[stat_name + "B" + game["stats"]["Role"][i][0]] = vals[i]
                else:
                    a[stat_name + "R" + game["stats"]["Role"][i][0]] = vals[i]

        for player in range(len(game["stats"]["Player"])):
            if i < 5:
                a["pidB" + game["stats"]["Role"][i][0]] = player_dict[player[i]]
            else:
                a["pidR" + game["stats"]["Role"][i][0]] = player_dict[player[i]]

        for i in range(len(game["events"])):
            event = game["events"][i]
            a[f"time{i}"] = event[0]

            if "kill" in event[4] or "death" in event[4]:
                if event[5]:
                    target = champ2role[event[5].lower()][0]
                else:
                    continue
            else:
                target = event[6]

            a[f"event{i}"] = event_dict[event[1][0] + ";".join([champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]) + event[4] + target]



            x=1
        statsdf.append(a)
    statsdf = pd.DataFrame(statsdf)

    #     b = { stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items()}
    # statsdf = pd.DataFrame([{"teamB": game["blue_team"], "resB": game["blue_result"], "teamR": game["red_team"], "resR": game["red_result"]} | {stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items() for
    #   i in range(10)} for game in game_history])
    # champ2player = {}
    # eventdf = pd.DataFrame([[{f"time{i}": game["events"][i][0], f"event{i}": [game["events"][i][1], game["events"][i][2], game["events"][i][4], game["events"][i][6]] } for i in range(0, len(game["events"]))] for game in game_history])
    x=1

    #df[df.columns.map(lambda x: "B_" + x)] = df.applymap(lambda x: x[:5])
    #df = pd.DataFrame({("B_" + key: vals[:5], "R_" + key: vals[5:]) for game in game_stats for key, vals in game.items()})
    #
    # x = 1

if __name__ == "__main__":
    main()