


import json
import pandas as pd
import os

def main():
    season = "13"
    current_game_colection = "game_collection2_" + season
    with open(os.path.join(os.getcwd(), "history", current_game_colection), "r") as game_history:
        game_history = [json.loads(game) for game in game_history.read().split("\n")[:-1]]

    game_stats = [game["stats"] for game in game_history]
    #df = pd.DataFrame([game["stats"] for game in game_history])
    df = pd.DataFrame([{"teamB": game["blue_team"], "resB": game["blue_result"], "teamR": game["red_team"], "resR": game["blue_result"]} | {stat.replace(" ", "-").replace("@", "at").replace("%", "-proc").replace("'", "").replace("+", "").lower() + ("B" if i < 5 else "R") + game["stats"]["Role"][i][0]: vals[i] for stat, vals in game["stats"].items() for
      i in range(10)} for game in game_history])
    x=1
    print(df)
    #df[df.columns.map(lambda x: "B_" + x)] = df.applymap(lambda x: x[:5])
    #df = pd.DataFrame({("B_" + key: vals[:5], "R_" + key: vals[5:]) for game in game_stats for key, vals in game.items()})
    #
    # x = 1

if __name__ == "__main__":
    main()