import json
from bs4 import BeautifulSoup
import requests


# Now we have a whole list of games
# Let's fill db for each game create a tuple and insert
with open("list_of_games.txt", "r") as games_list_file:
    list_of_games = json.loads(games_list_file.read().replace("'", '"'))


#  dicts for tables maped by id of row and object of table
team_data = {}
game_data = {}
game_teams_picks_data = {}
champions_data = {}
for league, games in list_of_games.items():
    for game in games:
        link = "https://gol.gg/game/stats/%s/page-game/" % game[0]
        html_content = requests.get(link).text
        soup = BeautifulSoup(html_content, "lxml")

        # preppin game_data and team_data
        game_time = soup.find("div", attrs={"class": "col-6 text-center"}).contents[3].contents[0]
        blue_team = soup.find("div", attrs={"class": "col-12 blue-line-header"}).contents
        red_team = soup.find("div", attrs={"class": "col-12 red-line-header"}).contents
        blue_team_id = blue_team[1]['href'].split("/")[3]
        red_team_id = red_team[1]['href'].split("/")[3]

        # INSERT INTO GAME game_data =(27847, '2021-01-24', '11.1', '32:00', '1153', '1152') FOR EACH id
        game_data[game[0]] = (
            game[1],
            game[2],
            game_time,
            blue_team_id,
            red_team_id)

        # INSERT INTO TEAMS ('1153', 'Misfits Gaming', 'LEC'), ('1152', 'MAD Lions', 'LEC')  FOR EACH ID
        if blue_team_id not in team_data.keys():
            team_data[blue_team_id] = (blue_team[1].text, league)
        if red_team_id not in team_data.keys():
            team_data[red_team_id] = (blue_team[1].text, league)


        # just get all champs and bans for one side
        # INSERT INTO CHAMPIONS ('140', 'Kaisa') for each ID
        blue_bans = soup.find("div", attrs={"class": "col-10"})
        bans_
        for item in blue_bans.find_all("a"):
            champ_id = item['href'].split("/")[3]
            if champ_id not in champions_data.keys():
                champions_data[champ_id] = (item['title'].replace(" stats", ""),)

        # INSERT INTO GAME_TEAMS_PICKS () for each GAME ID and TEAM ID
        # blue team 1, red team 0  and  win is 1 and loss is 0
        result = {"WIN": 1, "LOSS": 0}
        game_teams_picks_data[[game[0], blue_team_id]] = ("1", result[blue_team[2].replace(" - ", "")], )


        #print(result[])
        #print(red_team[2].replace(" - ", ""))
        break
    break

print(team_data)
print(champions_data)
print(game_data)
