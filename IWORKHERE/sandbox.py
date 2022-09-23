import sqlite3
import os
import pandas as pd

# Root project dir


# conn = sqlite3.connect(path_to_db)
# c = conn.cursor()
# # for item in output:
# #     c.execute("INSERT INTO champions VALUES %s" % item)
# #     conn.commit()
# #latest_games = [game_id[0] for game_id in c.execute("SELECT game_id FROM game;").fetchall()]
#
# output = c.execute("SELECT count(*) FROM game;").fetchall()

# for item in output:
#     print(item)
#
# ########### winnning caries
# output = c.execute("SELECT "
#                    "stats.game_id,"
#                    "stats.team_id,"
#                   # "picks.result, "
#                    "picks.top_pick_id, "
#                    "picks.jg_pick_id, "
#                    "picks.mid_pick_id, "
#                    "picks.adc_pick_id, "
#                    "picks.sup_pick_id,"
#                    "stats.top,"
#                    "stats.jg,"
#                    "stats.mid,"
#                    "stats.adc,"
#                    "stats.sup "
#                    "FROM game_team_stats as stats "
#                    "INNER JOIN game_team_picks as picks "
#                    "ON (stats.game_id == picks.game_id) AND (stats.team_id == picks.team_id)"
#                    "WHERE (stats.stat_type == 'DMG%') AND (picks.result == 1);").fetchall()
#
# #print(output)
# format_output = [{"game": game[0],
#                   "team": c.execute("SELECT team_name FROM teams WHERE team_id == %s" % (game[1])).fetchone()[0],
#                   "team_id": game[1],
#                   "picks": {c.execute("SELECT champion_name FROM champions WHERE champion_id == %s;" % game[2]).fetchone()[0]: float(game[7].replace("%", "")),
#                           c.execute("SELECT champion_name FROM champions WHERE champion_id == %s;" % game[3]).fetchone()[0]: float(game[8].replace("%", "")),
#                           c.execute("SELECT champion_name FROM champions WHERE champion_id == %s;" % game[4]).fetchone()[0]: float(game[9].replace("%", "")),
#                           c.execute("SELECT champion_name FROM champions WHERE champion_id == %s;" % game[5]).fetchone()[0]: float(game[10].replace("%", "")),
#                           c.execute("SELECT champion_name FROM champions WHERE champion_id == %s;" % game[6]).fetchone()[0]: float(game[11].replace("%", ""))}
#                 }for game in output]
#
# team_stats = {}
#
# for game in format_output:
#     if game["team"] in team_stats:
#         team_stats[game["team"]].append(max(game["picks"], key=game["picks"].get))
#     else:
#         team_stats[game["team"]] = [max(game["picks"], key=game["picks"].get)]
#
#
#
#
# team_stats = {team: {one_carry: carry.count(one_carry) for one_carry in set(carry)} for team, carry in team_stats.items()}
#
# with open("carry_champs.txt", "w") as carry_file:
#     for key, val in team_stats.items():
#         a = (key, sorted(val.items(), key=lambda x: x[1], reverse=True), len(val))
#         carry_file.write(str(a) + "\n")
# conn.close()
############# loosing caries
# query = "SELECT stats.game_id,stats.team_id,picks.top_pick_id, picks.jg_pick_id,picks.mid_pick_id,picks.adc_pick_id,picks.sup_pick_id,stats.top,stats.jg,stats.mid,stats.adc,stats.sup FROM game_team_stats as stats INNER JOIN game_team_picks as picks ON (stats.game_id == picks.game_id) AND (stats.team_id == picks.team_id) " \
#         "WHERE (stats.stat_type == 'DMG%') AND (picks.result == 1);"
import sqlite3
import os
import pandas as pd

# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "IWORKHERE", "stats.db")
print(path_to_db)
all_game_data = "SELECT "\
                   "stats.game_id," "stats.team_id, team.team_name," \
                    "picks.result, picks.team_color,"\
                   "picks.top_pick_id, picks.jg_pick_id, picks.mid_pick_id, picks.adc_pick_id, picks.sup_pick_id,"\
                   "stats.stat_type, stats.top,stats.jg,stats.mid,stats.adc,stats.sup "\
                   "FROM game_team_stats as stats "\
                   "INNER JOIN game_team_picks as picks "\
                   "ON (stats.game_id == picks.game_id) AND (stats.team_id == picks.team_id)"\
                    "INNER JOIN teams as team "\
                    "ON (team.team_id == picks.team_id);"
conn = sqlite3.connect("C:\\Users\\PC\\PycharmProjects\\golggML\\IWORKHERE\\stats.db")
df = pd.read_sql_query(all_game_data, conn)
print(df["stat_type"].unique())
print(df[["team_id", "team_name", "result", "team_color", "stat_type", "top", "jg", "mid", "adc", "sup"]])
# for game in output:
#     print(game)
conn.close()

