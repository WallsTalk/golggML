# import sqlite3
# import os

# # Check games in stats.db that dont have stats in corresponding table
# root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
# path_to_db = os.path.join(root, "ML", "stats.db")
# conn = sqlite3.connect(path_to_db)
# c = conn.cursor()

# print("Cleaning up corrupted matches...")
# game_ids = [item[0] for item in c.execute("select game_id from game;").fetchall()]

# print("Current total matches: " + str(len(game_ids)))

# for game_id in game_ids:
#     picks = c.execute("select * from game_team_picks where game_id = %s" % game_id).fetchall()
#     stats = c.execute("select * from game_team_stats where game_id = %s" % game_id).fetchall()
#     if len(stats) != 84 or len(picks) != 2:
#         c.execute("delete from game where game_id = %s" % game_id)
#         c.execute("delete from game_team_picks where game_id = %s" % game_id)
#         c.execute("delete from game_team_stats where game_id = %s" % game_id)
#     conn.commit()

# game_ids_after = [item[0] for item in c.execute("select game_id from game;").fetchall()]
# conn.close()
# print("Removed %s corrupted matches." % str(len(game_ids) - len(game_ids_after)))

# print("Total matches in stats.db: " + str(len(game_ids_after)))
# print("Done.")

