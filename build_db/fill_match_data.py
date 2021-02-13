import json
import sqlite3
import os

#root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

# Reading from files into dict
print("Reading data for tables from json.")
path_for_data = os.path.join(root, "build_db", "data_for_tables")
all_data = {}
for file in os.listdir(path_for_data):
	with open(os.path.join(path_for_data, file), "r") as data_file:
		all_data[file.replace(".json", "")] = json.loads(data_file.read())


path_to_db = os.path.join(root, "ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()

for table, data in all_data.items():
	for key, row in data.items():
		key_list = key.replace("(", "").replace(")", "").replace(" ", "").replace("'", "").split(",")
		values = tuple(key_list + row)

		c.execute("INSERT INTO %s VALUES %s", (table, values))
		break
	conn.commit()
conn.close()

