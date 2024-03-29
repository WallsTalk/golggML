
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random


def main():
    season = "13"

    with open(os.path.join(os.getcwd(), "turneys", season), "r") as turneys2023:
        turneys2023 = turneys2023.read().split("\n")

    current_game_colection = "game_collection2_" + season
    with open(os.path.join(os.getcwd(), "history", current_game_colection), "r") as game_history:
        game_history = [json.loads(game)["game_id"] for game in game_history.read().split("\n")[:-1]]

    with open(os.path.join(os.getcwd(), "history", current_game_colection), "a") as game_collection:

        for turney in turneys2023[:1]:
            print(turney)
            turney_soup = BeautifulSoup(requests.get("https://gol.gg/tournament/tournament-matchlist/"+turney.replace(" ", "%20")).text, "lxml")
            matches = [
                [int(tr.find("a")["href"].split("/")[3]) + game for game in range(sum([int(score) for score in tr.find("td", attrs={"class": "text-center"}).text.split('-')]))]
                for tr in turney_soup.find("table", attrs={"class": ['table_list', 'footable', 'toggle-square-filled']}).find("tbody").find_all("tr")
            ]
            # returns list of matches [53505, 53506, 53507]
            headers = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en-US,en;q=0.9",
                "Connection":"keep-alive",
                "Cookie":"_ga=GA1.1.862741513.1678448535; PHPSESSID=hev7qrliqfegmadj5hb6l3kvfs; __gads=ID=85c732651646df88-22e005f149dd00ba\":\"T=1678448535\":\"RT=1696504555\":\"S=ALNI_MaeGx17UhzNLjX6qz9RVLBOHRtghQ; __gpi=UID=000009d6ca104a0a\":\"T=1678448535\":\"RT=1696504555\":\"S=ALNI_MZDr7ytxsOyPozB4UkuYJIeMqZ9aA; _ga_J1K08MER9S=GS1.1.1696496780.10.1.1696504563.0.0.0",
                "Host":"gol.gg",
                "Referer":"https://gol.gg/game/stats/53506/page-fullstats/",
                "Sec-Fetch-Dest":"document",
                "Sec-Fetch-Mode":"navigate",
                "Sec-Fetch-Site":"same-origin",
                "Sec-Fetch-User":"?1",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
                "sec-ch-ua":"\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
                "sec-ch-ua-mobile":"?0",
                "sec-ch-ua-platform":"Windows",
            }

            time.sleep(random.randint(1,4))
            for match in matches:
                for game in match:
                    if game not in game_history:
                        print(match, game)
                        href_game = BeautifulSoup(requests.get(f"https://gol.gg/game/stats/{game}/page-game/", headers=headers).text, "lxml")
                        blue_team = href_game.find("div", attrs={"class": "col-12 blue-line-header"}).text.split(" - ")[0].replace("\n", "")
                        blue_result = href_game.find("div", attrs={"class": "col-12 blue-line-header"}).text.split(" - ")[1]
                        red_team = href_game.find("div", attrs={"class": "col-12 red-line-header"}).text.split(" - ")[0].replace("\n", "")
                        red_result = href_game.find("div", attrs={"class": "col-12 red-line-header"}).text.split(" - ")[1].replace(
                            " ", "")
                        # get game stats
                        x=1
                        href_game = BeautifulSoup(requests.get(f"https://gol.gg/game/stats/{game}/page-fullstats/", headers=headers).text, "lxml")
                        stats = {col.find_all("td")[0].text: [val.text for val in col.find_all("td")[1:]] for col in href_game.find("table", attrs={"class": ["completestats", "tablesaw", "tablesaw-swipe"]}).find_all("tr")[1:]}
                        stats["champs"] = [champ["alt"] for champ in href_game.find("table", attrs={"class": ["completestats", "tablesaw", "tablesaw-swipe"]}).find("thead").find_all("img")]

                        # get game timeline

                        try:
                            href_timeline = BeautifulSoup(requests.get(f"https://gol.gg/game/stats/{game}/page-timeline/", headers=headers).text, "lxml")

                        #cols = [col.text for col in href_timeline.find("table", attrs={"class": ['nostyle', 'timeline', 'trhover']}).find_all("tr")[0].find_all("th")]
                            events = [
                                [
                                    val.find("img")["src"].replace("../_img/", "").replace(".png", "").replace("-icon", "").replace("champions_icon/", "")
                                    if val.find("img") else val.text for val in event.find_all("td")
                                ]
                                for event in href_timeline.find("table", attrs={"class": ['nostyle', 'timeline', 'trhover']}).find_all("tr")[1:]
                            ]
                        except AttributeError:
                            events = []


                        match_object = {
                            "season": season,
                            "blue_team": blue_team,
                            "blue_result": blue_result,
                            "red_team": red_team,
                            "red_result": red_result,
                            "turney": turney,
                            "game_id": game,
                            "stats": stats,
                            "events": events
                        }
                        game_collection.write(json.dumps(match_object) + "\n")

                        time.sleep(random.randint(1,4))


if __name__ == "__main__":
    main()