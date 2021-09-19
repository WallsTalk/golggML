import requests
from bs4 import BeautifulSoup
import json
import os
import sqlite3
import time
import random

root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "pro_leagues", "summer_2021.db")
print(path_to_db)
conn = sqlite3.connect(path_to_db)
c = conn.cursor()

all_teams = c.execute("select team_name from teams;").fetchall()

conn.close()


# league_list = ['LPL', 'LEC', 'LCK', 'LCS']
# list_of_games = {}
# for league in league_list:
#     list_of_games[league] = []
#     make_random_int = random.randint(1, 164)
#     print(make_random_int)
#
#     link = "https://gol.gg/tournament/tournament-matchlist/" + league + "%20Spring%202021/"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
#     }
#     #html_content = requests.get(link, headers=headers).text
#
#     html_content = requests.get(link).text
#     count = 0
#
#     cheese = " too many requests. Try again in a few minutes."
#     while cheese == " too many requests. Try again in a few minutes.":
#         time.sleep(1)
#         cheese = requests.get(link, headers).text
#         print(count)
#         count += 1
#     print(count)

    #break
    #time.sleep(10)

    # soup = BeautifulSoup(html_content, "lxml")
    # match_table = soup.find("table", attrs={"class": "table_list footable toggle-square-filled"})
    # match_table_data = match_table.tbody.find_all("tr")
    # match_list = []