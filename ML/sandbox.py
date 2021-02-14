import sqlite3
import os

# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()

latest_games = [game_id[0] for game_id in c.execute("SELECT game_id FROM game;").fetchall()]

print(latest_games)

conn.close()
