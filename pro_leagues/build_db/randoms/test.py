import requests
import json

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer cXP58-fafBjtvjkPufepwqtGY4N6xPNZL9bOwP8cwP7LDFo23RE"
}
url = "https://api.pandascore.co/lol/leagues"

query_string = {"filter[id]": "4197", "filter[series][id]": "3669"}
LEC = requests.request("GET", url, headers=headers, params=query_string).text[1:-1]
print(LEC)
#for item in leagues:
   # print(item)
