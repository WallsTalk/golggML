import requests
from bs4 import BeautifulSoup

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
        gold_list = soup.find_all("table", attrs={"class": "small_table"})[0].contents[3].contents
        print(gold_list[1].contents)
        print(gold_list[3].contents)
        break
    break

    # var
    # blueGoldData = {
    #     labels: ['MID', 'ADC', 'SUPPORT', 'JUNGLE', 'TOP'],
    #     datasets: [
    #         {
    #             label: 'Invictus Gaming',
    #             borderColor: 'rgba(97,148,188,1)',
    #             pointBackgroundColor: 'rgba(97,148,188,1)',
    #             data: [13.021, 13.271, 6.952, 12.294, 13.173]
    #         },
    #         {
    #             label: 'Royal Never Give Up',
    #             borderColor: 'rgba(238,50,51,1)',
    #             pointBackgroundColor: 'rgba(238,50,51,1)',
    #             data: [8.386, 11.916, 6.294, 9.68, 10.363]
    #         }
    #     ]
    # };

