
from bs4 import BeautifulSoup
import requests
import os
import sqlite3


root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "ML", "../../IWORKHERE/stats.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
}
url = "https://gol.gg/champion/list/season-S12/split-Summer/tournament-ALL/"
html_content = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_content, "lxml")
#soup_table = soup.find("table", attrs={"class": "table_list playerslist tablesaw trhover tablesaw-swipe tablesaw-sortable"})
all_champs = soup.find_all("td", attrs={"style": "vertical-align:middle"})
c.execute("CREATE TABLE IF NOT EXISTS champions (champion_id integer, champion_name varchar);")
conn.commit()
for champ in all_champs:
    info = champ.find("a")
    data_tuple = (info["href"].split("/")[2], info["title"].replace(" stats", ""))
    sqlite_insert_with_param = """INSERT INTO champions
                                (champion_id, champion_name)
                              VALUES (?, ?);"""

    c.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()
    print(info["href"].split("/")[2], info["title"].replace(" stats", ""))

# url = "https://gol.gg/teams/list/season-S12/split-Summer/tournament-ALL/"
# html_content = requests.get(url, headers=headers).text
# soup = BeautifulSoup(html_content, "lxml")
# #print(soup)
# all_teams = soup.find_all("a")
# c.execute("CREATE TABLE IF NOT EXISTS teams (team_id integer unique, team_name varchar, region varchar);")
# conn.commit()
# for team in all_teams:
#     try:
#         if "stats" in team["title"]:
#             print(team["href"].split("/")[2])
#             data_tuple = (team["href"].split("/")[2], team["title"], "dunno")
#             sqlite_insert_with_param = """INSERT INTO teams (team_id, team_name, region) VALUES (?, ?, ?);"""
#             c.execute(sqlite_insert_with_param, data_tuple)
#             conn.commit()
#     except KeyError:
#         pass
# print()


conn.close()