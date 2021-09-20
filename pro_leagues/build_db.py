import requests
import json
import sqlite3
from sqlite3 import IntegrityError
import os
# https://developers.pandascore.co/reference/get_lol_teams_teamidorslug_stats
# https://app.pandascore.co/dashboard/main

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer cXP58-fafBjtvjkPufepwqtGY4N6xPNZL9bOwP8cwP7LDFo23RE"
}

# #GET ALL LEAGUES for dataset
# # todo not the best way to get leaguess try: "https://api.pandascore.co/lol/series"
# url = "https://api.pandascore.co/lol/leagues"
# leagues_info = {}
#
# for league_to_check in ["LCK", "LPL", "LCS", "LEC"]:
#     querystring = {"filter[name]": league_to_check}
#     response = requests.request("GET", url, headers=headers, params=querystring).text[2:-3]
#     for league in response.split("}},{"):
#         league_str = "{" + league + "}}"
#         leagues_info[league_to_check] = json.loads(league_str)
#
# url = "https://api.pandascore.co/lol/series/%s/teams"
#
root = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
path_to_db = os.path.join(root, "pro_leagues", "summer_2021.db")
conn = sqlite3.connect(path_to_db)
c = conn.cursor()


# for league, info in leagues_info.items():
#     for serie in info["series"]:
#         if "Summer 2021" in serie.values():
#             response = requests.get(url % serie["id"], headers=headers).text[1:-1]
#             league_teams = response.split('{"acronym"')
#
#             teams = {}
#             for item in league_teams[1:-1]:
#                 team_object = json.loads('{"acronym"' + item[:-1])
#                 teams[team_object["acronym"]] = team_object
#                 sqlite_insert_with_param = """INSERT INTO teams (team_id, team_name, region, serie_id, players) VALUES (?, ?, ?, ?, ?);"""
#                 data_tuple = (team_object["id"], team_object["acronym"], league, serie["id"], json.dumps(team_object["players"]))
#                 try:
#                     c.execute(sqlite_insert_with_param, data_tuple)
#                 except IntegrityError:
#                     pass
#                 conn.commit()
#
url = "https://api.pandascore.co/lol/series/%s/teams/%s/stats"

all_teams = c.execute("select team_id, team_name, region, serie_id from teams;").fetchall()

for team in all_teams:
    #req_url = url % (team[3], team[0])
    req_url = f"https://api.pandascore.co/lol/teams/{team[0]}/stats"
    print(req_url)
    response = requests.get(req_url, headers=headers).text
    print(response)
    break


conn.close()


