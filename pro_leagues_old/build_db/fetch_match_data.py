import json
from bs4 import BeautifulSoup
import requests
import os
import time

# Root project dir
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

# Now we have a whole list of games
# Let's fill db for each game create a tuple and insert
path_to_list_of_games = os.path.join(root, "build_db", "list_of_games.json")
with open(path_to_list_of_games, "r") as games_list_file:
    list_of_games = json.loads(games_list_file.read().replace("'", '"'))

#  dicts for tables maped by id of row and object of table
all_data = {
    "team": {},
    "game": {},
    "game_team_picks": {},
    "game_team_stats": {}
}
headers = {
    "Origin": "https://gol.gg",
    "Referer": "https://gol.gg/",
    "sec-ch-ua": '"Google Chrome";v="90", " Not;A Brand";v="89", "Chromium";v="93"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/590.90 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
}
for league, games in list_of_games.items():
    print("Fetching stats for " + league + " ...")
    for game in games:
        link = "https://gol.gg/game/stats/%s/page-game/" % game[0]
        print(link)
        html_content = requests.get(link, headers=headers).text
        soup = BeautifulSoup(html_content, "lxml")

        # preppin game_data and team_data
        game_time = soup.find("div", attrs={"class": "col-6 text-center"}).contents[3].contents[0]
        blue_team = soup.find("div", attrs={"class": "col-12 blue-line-header"}).contents
        red_team = soup.find("div", attrs={"class": "col-12 red-line-header"}).contents
        blue_team_id = int(blue_team[1]['href'].split("/")[3])
        red_team_id = int(red_team[1]['href'].split("/")[3])

        # INSERT INTO GAME game_data =(27847, '2021-01-24', '11.1', '32:00', '1153', '1152') FOR EACH id
        all_data["game"][game[0]] = (
            game[1],
            game[2],
            game_time,
            blue_team_id,
            red_team_id)

        # INSERT INTO TEAMS ('1153', 'Misfits Gaming', 'LEC'), ('1152', 'MAD Lions', 'LEC')  FOR EACH ID
        if blue_team_id not in all_data["team"].keys():
            all_data["team"][blue_team_id] = (blue_team[1].text, league)
        if red_team_id not in all_data["team"].keys():
            all_data["team"][red_team_id] = (red_team[1].text, league)

        # getting picks and bans for eatch team
        blue_bans = []
        blue_picks = []
        red_bans = []
        red_picks = []
        bans_section = soup.find_all("div", text="Bans", attrs={"class": "col-2"})
        picks_section = soup.find_all("div", text="Picks", attrs={"class": "col-2"})
        for ban in bans_section[0].find_next("div", attrs={"class": "col-10"}).find_all("a"):
            blue_bans.append(int(ban['href'].split("/")[3]))
        for ban in bans_section[1].find_next("div", attrs={"class": "col-10"}).find_all("a"):
            red_bans.append(int(ban['href'].split("/")[3]))
        for pick in picks_section[0].find_next("div", attrs={"class": "col-10"}).find_all("a"):
            blue_picks.append(int(pick['href'].split("/")[3]))
        for pick in picks_section[1].find_next("div", attrs={"class": "col-10"}).find_all("a"):
            red_picks.append(int(pick['href'].split("/")[3]))

        # INSERT INTO GAME_TEAMS_PICKS (28463, '1109'): (0, 0, 119, 149, 75, 151, 4, 139, 96, 68, 134, 120)
        # for each GAME ID and TEAM ID
        # blue team 1, red team 0  and  win is 1 and loss is 0
        result = {"WIN": 1, "LOSS": 0}
        all_data["game_team_picks"][str((game[0], blue_team_id))] = (
                1,
                result[blue_team[2].replace("-", "").replace(" ", "")],
                *blue_picks,
                *blue_bans)
        all_data["game_team_picks"][str((game[0], red_team_id))] = (
                0,
                result[red_team[2].replace("-", "").replace(" ", "")],
                *red_picks,
                *red_bans)
        time.sleep(10)

        # now to load enhanced stats from other page tab
        link = "https://gol.gg/game/stats/%s/page-fullstats/" % game[0]
        html_content = requests.get(link, headers=headers).text
        soup = BeautifulSoup(html_content, "lxml")

        # INSERT INTO GAME_TEAMS_STATS (28463, '1105', "CS in Team's Jungle") ('5', '95', '16', '23', '0')
        # for each GAME ID and TEAM ID
        match_stats_table = soup.find("table", attrs={"class": "completestats tablesaw"}).find_all("tr")
        for stat_line in match_stats_table[3:]:
            stat_line_name = [stat_line.find_all("td")[0].text]
            stat_line_items = [item.text for item in stat_line.find_all("td")[1:]]
            all_data["game_team_stats"][str((game[0], blue_team_id, stat_line_name[0]))] = (*stat_line_items[:5],)
            all_data["game_team_stats"][str((game[0], red_team_id, stat_line_name[0]))] = (*stat_line_items[5:],)
        time.sleep(5)

# adding to files to insert into respective tables
path_for_data = os.path.join(root, "build_db", "data_for_tables")
for table, data in all_data.items():
    with open(os.path.join(path_for_data, table + ".json"), "w") as data_file:
        json.dump(all_data[table], data_file)
print("Saved stats to json.")
