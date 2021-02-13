import sqlite3
import os

#root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()

output = c.execute("select * from game_team_stats;").fetchall()

for row in output:
    print(row)

conn.close()
