import sqlite3


sqlite3.connect('stats.db')
conn = sqlite3.connect('stats.db')
c = conn.cursor()

# Create tables
with open("queries.sql", "r") as queries_file:
    queries = queries_file.read().split(";")
    list(map(lambda query: c.execute(query + ";"), queries))
    conn.commit()

conn.close()

# to write into tables use
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
