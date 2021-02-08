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
                list_of_games[league].append([game_id, tr.contents[5].contents[0], tr.contents[6].contents[0]])
                game_id += 1
                num_of_games -= 1

# Now we have a whole list of  games
for league, games in list_of_games.items():
    for game in games:
        print(game)
        link = "https://gol.gg/game/stats/%s/page-game/" % game[0]
        html_content = requests.get(link).text
        soup = BeautifulSoup(html_content, "lxml")
        #print(soup.prettify())
        game_time = soup.find("div", attrs={"class": "col-6 text-center"}).contents[3].contents[0]
        gold_dmg_tables = soup.find_all("table", attrs={"class": "small_table"})
        # take prec for each role by <td>
        gold_dist = {}
        dmg_dist = {}
        for item in gold_dmg_tables[0].find_all("tr")[1:]:
            gold_dist[item.contents[0].contents[0]] = [item.contents[1].contents[0], item.contents[3].contents[0]]
        for item in gold_dmg_tables[1].find_all("tr")[1:]:
            print(item)
            dmg_dist[item.contents[0].contents[0]] = [item.contents[1].contents[0], item.contents[3].contents[0]]
        print(gold_dist)
        print(dmg_dist)
        break
    break

    # ['\n', < tr > < td > < / td > < td
    #
    #
    # class ="blue_line text-center" > IG < / td > < td class ="red_line text-center" > RNG < / td > < / tr >, '\n', < tr > < td > TOP < / td > < td > 22.4 % < / td >
    #
    # < td > 22.2 % < / td > < / tr >, '\n', < tr > < td > JUNGLE < / td > < td > 20.9 % < / td >
    # < td > 20.8 % < / td > < / tr >, '\n', < tr > < td > MID < / td > < td > 22.2 % < / td >
    # < td > 18 % < / td > < / tr >, '\n', < tr > < td > ADC < / td > < td > 22.6 % < / td >
    # < td > 25.5 % < / td > < / tr >, '\n', < tr > < td > SUPPORT < / td > < td > 11.8 % < / td >
    # < td > 13.5 % < / td > < / tr >, '\n']

