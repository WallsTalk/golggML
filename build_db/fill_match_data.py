import json
import sqlite3
import os
from datetime import datetime

# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

# Reading from files into dict
path_for_data = os.path.join(root, "build_db", "data_for_tables")
all_data = {}
failed_data = {}
for file in os.listdir(path_for_data):
	with open(os.path.join(path_for_data, file), "r") as data_file:
		all_data[file.replace(".json", "")] = json.loads(data_file.read())
		failed_data[file.replace(".json", "")] = {}


path_to_db = os.path.join(root, "ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()


# If insertion fails we should save all game ID's and then remove data for tehse games
for table, data in all_data.items():
	for key, row in data.items():
		try:
			key_list = key.replace("(", "").replace(")", "").replace(" ", "").replace("'", "").split(",")
			values = tuple(key_list + row)
			c.execute("INSERT INTO %s VALUES %s" % (table, values))
		except Exception as e:
			if table != "team":
				if key_list[0] not in failed_data[table].keys():
					failed_data[table][key_list[0]] = [(key_list, values, e)]
				else:
					failed_data[table][key_list[0]].append((key_list, values, e))

	conn.commit()
conn.close()
print("Values transferred from json to database.")


# Log errors
logs_path = os.path.join(root, "build_db", "logs.log")
with open(logs_path, "w") as logs:
	logs.write(str(datetime.now()) + "\n")
	for table, game_ids in failed_data.items():
		logs.write(table + " | Corrupted games count in tables: " + str(len(game_ids)) + "\n")
		for game_id, values in game_ids.items():
			logs.write(str(game_id) + "\n")
			logs.write(str(values) + "\n")
print("Logged errors.")
