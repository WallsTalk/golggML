


import json
import pandas as pd


def main():
    with open("game_collection", "r") as game_history:
        game_history = [json.loads(game) for game in game_history.read().split("\n")[:-1]]
    game_stats = [game["stats"] for game in game_history]
    #df = pd.DataFrame([game["stats"] for game in game_history])

    #df[df.columns.map(lambda x: "B_" + x)] = df.applymap(lambda x: x[:5])
    df = pd.DataFrame({("B_" + key: vals[:5], "R_" + key: vals[5:]) for game in game_stats for key, vals in game.items()})
    x = 1

if __name__ == "__main__":
    main()