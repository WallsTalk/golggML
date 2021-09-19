import requests
import json

 #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

# https://developers.pandascore.co/reference/get_lol_teams_teamidorslug_stats
# https://app.pandascore.co/dashboard/main


headers = {
    "Accept": "application/json",
    "Authorization": "Bearer cXP58-fafBjtvjkPufepwqtGY4N6xPNZL9bOwP8cwP7LDFo23RE"
}


#GET ALL LEAGUES for dataset
# url = "https://api.pandascore.co/lol/leagues"
# leagues_info = {}
# for league_to_check in ["LCK", "LPL", "LCS", "LEC"]:
#    querystring = {"filter[name]": league_to_check}
#    response = requests.request("GET", url, headers=headers, params=querystring).text[2:-3]
#    for league in response.split("}},{"):
#       league_str = "{" + league + "}}"
#       leagues_info[league_to_check] = league_str

# with open("leagues.txt", "w") as leagues:
#    leagues.write(json.dumps(leagues_info))






url = "https://api.pandascore.co/lol/series/%s/teams"

with open("leagues.txt", "r") as leagues:
   leagues_json = json.loads(leagues.read())
   for league, info in leagues_json.items():
      info_json = json.loads(info)
      for serie in info_json["series"]:
         if "Summer 2021" in serie.values():
            response = requests.get(url % serie["id"], headers=headers).text
            print(response + "\n")

# https://developers.pandascore.co/reference/get_lol_series_serieidorslug_teams_teamidorslug_stats