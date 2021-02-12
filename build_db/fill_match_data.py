import json
import sqlite3
import os


print("Reading data for tables from json.")
path_for_data = os.path.join("build_db", "data_for_tables")
for file in os.listdir(path_for_data):
	with open(os.path.join(path_for_data, file), "r") as data_file:
		json.loads(data_file.read())


path_to_db = os.path.join("ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()
conn.close()

