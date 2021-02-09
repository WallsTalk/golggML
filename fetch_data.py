import requests
from bs4 import BeautifulSoup

league_list = ['LPL', 'LEC', 'LCK', 'LCS']
league_list = ['LEC']

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


# Now we have a whole list of  games
# Let's fill db for each game create a tuple and insert
for league, games in list_of_games.items():
    for game in games:
        print(game)
        link = "https://gol.gg/game/stats/%s/page-game/" % game[0]
        html_content = requests.get(link).text
        soup = BeautifulSoup(html_content, "lxml")

        game_time = soup.find("div", attrs={"class": "col-6 text-center"}).contents[3].contents[0]
        blue_team = soup.find("div", attrs={"class": "col-12 blue-line-header"}).contents
        red_team = soup.find("div", attrs={"class": "col-12 red-line-header"}).contents

        # INSERT INTO GAME game_data =(27847, '2021-01-24', '11.1', '32:00', '1153', '1152')
        game_data = game + [game_time, blue_team[1]['href'].split("/")[3], red_team[1]['href'].split("/")[3]]
        game_data = tuple(game_data)
        
        # for each in team_data = [('1153', 'Misfits Gaming', 'LEC'), ('1152', 'MAD Lions', 'LEC')] INSERT INTO TEAMS
        team_data = [
            (blue_team[1]['href'].split("/")[3], blue_team[1].text, league),
            (red_team[1]['href'].split("/")[3], red_team[1].text, league)
            ]


        # gold_dmg_tables = soup.find_all("table", attrs={"class": "small_table"})
        # take prec for each role by <td>
        # gold_dist = {}
        # dmg_dist = {}
        # for item in gold_dmg_tables[0].find_all("tr")[1:]:
        #     gold_dist[item.contents[0].contents[0]] = [item.contents[1].contents[0], item.contents[3].contents[0]]
        # for item in gold_dmg_tables[1].find_all("tr")[1:]:
        #     print(item)
        #     #dmg_dist[item.contents[0].contents[0]] = [item.contents[1].contents[0], item.contents[3].contents[0]]
        # print(gold_dist)
        # print(dmg_dist)
        break
