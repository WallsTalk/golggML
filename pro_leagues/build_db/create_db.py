
import sqlite3
import os


# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "ML", "stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()

# Create tables
path_to_queries = os.path.join(root, "build_db", "queries.sql")
with open(path_to_queries, "r") as queries_file:
    queries = queries_file.read().split(";")
    list(map(lambda query: c.execute(query + ";"), queries))
    conn.commit()
conn.close()
print("Created tables.")
