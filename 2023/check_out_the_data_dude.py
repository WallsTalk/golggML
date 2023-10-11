


import json
import pandas as pd
import os
import numpy as np
import math


def main():
    seasons = [str(i) for i in range(8, 14)]
    game_history = []
    # for season in seasons:
    #     current_game_colection = "game_collection3_" + season
    #     with open(os.path.join(os.getcwd(), "work_history", current_game_colection), "r") as game_history_file:
    #         game_history += [json.loads(game) for game in game_history_file.read().split("\n")[:-1]]
    with open(os.path.join(os.getcwd(), "history", "game_collection_worlds_13"), "r") as game_history_file:
        game_history += [json.loads(game) for game in game_history_file.read().split("\n")[:-1]]


    statsdf = []
    with open(os.path.join(os.getcwd(), "player_dict.json"), "r") as event_file:
        player_dict = json.load(event_file)

    for game in game_history:
        a = {
            "season": game["season"],
            "turney": game["turney"],
            "gameid": game["game_id"],
            "teamB": game["blue_team"],
            "resB": game["blue_result"],
            "teamR": game["red_team"],
            "resR": game["red_result"],

        }

        # this one is temp
        for i in range(len(game["stats"]["Player"])):
            if i < 5:
                a["pidB" + game["stats"]["Role"][i][0]] = player_dict[game["stats"]["Player"][i]]
            else:
                a["pidR" + game["stats"]["Role"][i][0]] = player_dict[game["stats"]["Player"][i]]
        #

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

        drained_events = 0
        for i in range(len(game["events"])):
            event = game["events"][i]
            if "PLATE" == event[4]:
                drained_events +=1
                continue
            minutes = int(event[0].split(":")[0])
            seconds = int(event[0].split(":")[1])
            a[f"time{i-drained_events}"] = minutes*60 + seconds


            if "kill" in event[4] or "death" in event[4]:
                if event[5]:
                    target = champ2role[event[5].lower()][0]
                else:
                    continue
            else:
                target = event[6]

            actors = [champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]
            a[f"event{i-drained_events}"] = event[1][0] + ";".join(actors) + event[4].replace("gold", "") + target
            x=1
            if event[1][0] == "b":
                team_cof = 0
            else:
                team_cof = 500000
            # kill, dragon, herald, tower, baron, inhib, nexus
            event_cof = 0

            actor_cof = 0
            target_cof = 0
            if actors:
                if actors[0] == "T":
                    actor_cof = 100
                elif actors[0] == "J":
                    actor_cof = 300
                elif actors[0] == "M":
                    actor_cof = 500
                elif actors[0] == "A":
                    actor_cof = 700
                elif actors[0] == "S":
                    actor_cof = 900
                actor_cof += len(actors) - 1
                if target == "T":
                    target_cof = 10
                if target == "J":
                    target_cof = 30
                if target == "M":
                    target_cof = 50
                if target == "A":
                    target_cof = 70
                if target == "S":
                    target_cof = 90


            if "dragon" in event[4]:
                event_cof = 20000
            elif "herald" == event[4]:
                event_cof = 30000
            elif "tower" == event[4]:
                actor_cof = actor_cof//10
                event_cof = 50000
                if "NEXUS" in target:
                    target_cof = 9000
                elif "T3" in target:
                    target_cof = 0
                elif "T2" in target:
                    target_cof = 3000
                elif "T1" in target:
                    target_cof = 6000
                if "TOP" in target:
                    target_cof += 300
                elif "MID" in target:
                    target_cof += 600
                elif "BOT" in target:
                    target_cof += 900

            elif "inhib" == event[4]:
                actor_cof = actor_cof / 10
                event_cof = 70000
                if "TOP" in target:
                    target_cof = 300
                elif "MID" in target:
                    target_cof += 600
                elif "BOT" in target:
                    target_cof += 900
            elif "baron" == event[4]:
                event_cof = 80000
            elif "nexus" == event[4]:
                event_cof = 90000

            a[f"eventid{i-drained_events}"] = (minutes+1)*1000000 + team_cof + event_cof + actor_cof + target_cof
            #a[f"eventid{i}"] = int(event_dict[event[1][0] + ";".join([champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]) + event[4] + target])


        x=1
        statsdf.append(a)


    statsdf = pd.DataFrame(statsdf)
    statsdf["turney"] = statsdf["turney"].apply(lambda x: x.split(" 20")[0])
    all_turneys = list(set(statsdf["turney"].tolist()))
    all_turneys = {all_turneys[i]: i for i in range(len(all_turneys))}
    statsdf["turneyid"] = statsdf.replace({"turney": all_turneys})["turney"]
    all_teams = list(set([item for col, vals in statsdf[["teamB", "teamR"]].items() for item in vals.tolist()]))
    all_teams = {all_teams[i]: i for i in range(len(all_teams))}
    statsdf["teamidB"] = statsdf.replace({"teamB": all_teams})["teamB"]
    statsdf["teamidR"] = statsdf.replace({"teamR": all_teams})["teamR"]
    statsdf["result"] = statsdf["resB"].apply(lambda x: 1 if x == "WIN" else 0)

    print(statsdf.shape)
    statsdf.to_csv("temp.csv", sep=",", index=False)
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