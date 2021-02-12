import json
import sqlite3
import os


sqlite3.connect('stats.db')
conn = sqlite3.connect('stats.db')
c = conn.cursor()

path_for_data = "data_for_tables/"
#data = {}
for file in os.listdir(path_for_data):
	with open(path_for_data + file, "r") as file_object:
		data = file_object.read()
		print(file)
		try:
			json.loads(data)
		except Exception as e:	
			print(data)
			print(e)
			file_object.close()
			break

conn.close()
# with open(path_for_data + "game_data.txt", "r") as games_data_file:
#     game_data = games_data_file.read()

# with open(path_for_data + "team_data.txt", "r") as team_data_file:
#     team_data = team_data_file.read()

# with open(path_for_data + "game_teams_picks_data.txt", "r") as game_teams_picks_data_file:
#     game_teams_picks_data = game_teams_picks_data_file.read()

# with open(path_for_data + "game_teams_stats_data.txt", "r") as game_teams_stats_data_file:
#     game_teams_stats_data = game_teams_stats_data_file.read()

