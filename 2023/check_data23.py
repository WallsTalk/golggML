
import json
import pandas as pd
import os



def main():
    seasons = [13]
    game_history = []
    for season in seasons:
        current_game_colection = "game_collection3_" + str(season)
        with open(os.path.join(os.getcwd(), "work_history", current_game_colection), "r") as game_history_file:
            game_history += [json.loads(game) for game in game_history_file.read().split("\n")[:-1]]
    # with open(os.path.join(os.getcwd(), "history", "game_collection_worlds_13"), "r") as game_history_file:
    #     game_history += [json.loads(game) for game in game_history_file.read().split("\n")[:-1]]


    statsdf = []
    with open(os.path.join(os.getcwd(), "player_dict.json"), "r") as event_file:
        player_dict = json.load(event_file)

    actors_dict = {
        "T": 0,
        "J": 1,
        "M": 2,
        "A": 3,
        "S": 4
    }

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

            minutes = int(event[0].split(":")[0])
            seconds = int(event[0].split(":")[1])
            a[f"time{ i -drained_events}"] = minutes *60 + seconds
            # time is decided now what is the event?
            # which team?
            if event[1][0] == "b":
                a[f"side{i - drained_events}"] = 0
            else:
                a[f"side{i - drained_events}"] = 1

            #what happened
            objekt = event[4]
            actors = [champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]
            if "kill" in objekt:
                if event[5] and event[3]:
                    a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                    a[f"target{i - drained_events}"] = actors_dict[champ2role[event[5].lower()][0]]
                else:
                    drained_events += 1
                    continue
            elif "death" in objekt:
                drained_events += 1
                continue
            elif "PLATE" == objekt:
                drained_events += 1
                continue
            elif "dragon" in objekt:
                if actors:
                    a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                else:
                    drained_events += 1
                    continue
                a[f"target{i - drained_events}"] = 5
            elif "herald" in objekt:
                if actors:
                    a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                else:
                    drained_events += 1
                    continue
                a[f"target{i - drained_events}"] = 6
            elif "tower" in objekt:
                if actors:
                    a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                else:
                    a[f"actor{i - drained_events}"] = 6
                a[f"target{i - drained_events}"] = 7
            elif "inhib" in objekt:
                if actors:
                    a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                else:
                    a[f"actor{i - drained_events}"] = 6
                a[f"target{i - drained_events}"] = 8
            elif "baron" in objekt:
                a[f"actor{i - drained_events}"] = actors_dict[actors[0]]
                a[f"target{i - drained_events}"] = 9
            elif "nexus" in objekt:
                a[f"actor{i - drained_events}"] = 7
                a[f"target{i - drained_events}"] = 10



            # elif "tower" == event[4]:
            #     actor_cof = actor_c of //10
            #     event_cof = 50000
            #     if "NEXUS" in target:
            #         target_cof = 9000
            #     elif "T3" in target:
            #         target_cof = 0
            #     elif "T2" in target:
            #         target_cof = 3000
            #     elif "T1" in target:
            #         target_cof = 6000
            #     if "TOP" in target:
            #         target_cof += 300
            #     elif "MID" in target:
            #         target_cof += 600
            #     elif "BOT" in target:
            #         target_cof += 900
            #
            # elif "inhib" == event[4]:
            #     actor_cof = actor_cof / 10
            #     event_cof = 70000
            #     if "TOP" in target:
            #         target_cof = 300
            #     elif "MID" in target:
            #         target_cof += 600
            #     elif "BOT" in target:
            #         target_cof += 900


            # a[f"eventid{i}"] = int(event_dict[event[1][0] + ";".join([champ2role[champ.lower()][0] for champ in event[3].split(";") if champ]) + event[4] + target]) x=1
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
    statsdf.to_csv("23.csv", sep=",", index=False)
    #     b = { stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items()}
    # statsdf = pd.DataFrame([{"teamB": game["blue_team"], "resB": game["blue_result"], "teamR": game["red_team"], "resR": game["red_result"]} | {stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items() for
    #   i in range(10)} for game in game_history])
    # champ2player = {}
    # eventdf = pd.DataFrame([[{f"time{i}": game["events"][i][0], f"event{i}": [game["events"][i][1], game["events"][i][2], game["events"][i][4], game["events"][i][6]] } for i in range(0, len(game["events"]))] for game in game_history])
    x = 1

    # df[df.columns.map(lambda x: "B_" + x)] = df.applymap(lambda x: x[:5])
    # df = pd.DataFrame({("B_" + key: vals[:5], "R_" + key: vals[5:]) for game in game_stats for key, vals in game.items()})
    #
    # x = 1


if __name__ == "__main__":
    main()