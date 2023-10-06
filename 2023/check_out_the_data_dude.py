


import json
import pandas as pd


def main():
    with open("game_collection_12", "r") as game_history:
        game_history = [json.loads(game) for game in game_history.read().split("\n")[:-1]]
    count = {}
    count2 = 0
    tur = []
    for game in game_history:
        if not game["events"]:
            if game["turney"] not in count:
                count[game["turney"]] = 0
            count[game["turney"]] += 1

    print(count, count2)
    print(set(tur))
    # game_stats = [game["stats"] for game in game_history]
    # #df = pd.DataFrame([game["stats"] for game in game_history])
    # df = pd.DataFrame([{stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items() for
    #   i in range(10)} for game in game_history])
    # #df[df.columns.map(lambda x: "B_" + x)] = df.applymap(lambda x: x[:5])
    # #df = pd.DataFrame({("B_" + key: vals[:5], "R_" + key: vals[5:]) for game in game_stats for key, vals in game.items()})
    #
    # x = 1

if __name__ == "__main__":
    main()