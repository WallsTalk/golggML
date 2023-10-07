


import json
import pandas as pd
import os

def main():
    season = "12"
    current_game_colection = "game_collection2_" + season
    with open(os.path.join(os.getcwd(), "work_history", current_game_colection), "r") as game_history:
        game_history = [json.loads(game) for game in game_history.read().split("\n")[:-1]]

    statsdf = []
    for game in game_history:
        a = {
            "teamB": game["blue_team"],
            "resB": game["blue_result"],
            "teamR": game["red_team"],
            "resR": game["red_result"],

        }
        champ2role = {game["stats"]["champs"][i].replace(" ", "").lower(): game["stats"]["Role"][i] for i in range(10)}
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

        for stat, vals in game["stats"].items():
            stat_name = stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace(
                "+", "").lower()
            for i in range(10):
                if i < 5:
                    a[stat_name + "B" + game["stats"]["Role"][i][0]] = vals[i]
                else:
                    a[stat_name + "R" + game["stats"]["Role"][i][0]] = vals[i]

        for i in range(len(game["events"])):
            event = game["events"][i]
            a[f"time{i}"] = event[0]
            try:
                if event[5] == "kill;gold":
                    target = champ2role[event[5].lower()][0]
                else:
                    target = event[6]


                    a[f"event{i}"] = event[1][0]+ ";".join([champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]) + event[4] + target
            except KeyError as e:
                x=1

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