import requests
from bs4 import BeautifulSoup
import json
import os


print("Fetching match history.")
league_list = ['LPL', 'LEC', 'LCK', 'LCS']
list_of_games = {}
for league in league_list:
    list_of_games[league] = []
    link = "https://gol.gg/tournament/tournament-matchlist/" + league + "%20Spring%202021/"
    html_content = requests.get(link).text
    soup = BeautifulSoup(html_content, "lxml")
    match_table = soup.find("table", attrs={"class": "table_list footable toggle-square-filled"})
    match_table_data = match_table.tbody.find_all("tr")
    match_list = []
    for tr in match_table_data:

        # if match hasnt happened the value is 3
        if len(tr.contents[2].contents[0]) == 5:
            games_list = tr.contents[2].contents[0].split(" - ")
            num_of_games = int(games_list[0]) + int(games_list[1])

            # For each game in the series id goes up + 1
            game_id = int(tr.contents[0].contents[0]['href'].split("/")[3])
            while num_of_games > 0:
                list_of_games[league].append([game_id, tr.contents[6].contents[0], tr.contents[5].contents[0]])
                game_id += 1
                num_of_games -= 1

#root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
print("Saving match history to json.")
path_for_data = os.path.join(root, "build_db", "list_of_games.json")
with open(path_for_data, "w") as games_list_file:
    json.dump(list_of_games, games_list_file)
