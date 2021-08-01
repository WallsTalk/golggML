import requests
import json
import sqlite3


match_list_by_acc = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA/ids?type=ranked&start=0&count=100"

header = {
    "api_key": "RGAPI-7e0eb530-03a7-448f-85a3-65f59f8556e3"
}

# dict_keys(['id', 'accountId', 'puuid', 'name', 'profileIconId', 'revisionDate', 'summonerLevel'])
# acc_info = json.loads(requests.get(summoner_by_name_url + "Catuin", header).content)
# print(acc_info["puuid"])
bad_responses = [400, 401, 403, 404, 405, 415, 429, 500, 502, 503, 504]
match_list_response = requests.get(match_list_by_acc, header)
if match_list_response.status_code not in bad_responses:
    match_list = json.loads(match_list_response.content)
else:
    print(match_list_response.content, "when trying to fetch match list_of_matches")
    exit(1)

conn = sqlite3.connect("my_inting_data.db")
c = conn.cursor()


#query = "CREATE TABLE IF NOT EXISTS match_history (game_id varchar unique, match_data varchar);"
list_of_matches = [match[0] for match in c.execute("SELECT game_id FROM match_history;").fetchall()]
match_info_by_id = "https://europe.api.riotgames.com/lol/match/v5/matches/"


for match in match_list:
    if match not in list_of_matches:
        answer = requests.get(match_info_by_id + match, header)
        if answer.status_code not in bad_responses:
            match_data = json.dumps(json.loads(answer.content))
            c.execute("INSERT INTO match_history VALUES (?, ?)", (match, match_data))
            conn.commit()
            print("added", match)
        else:
            print(answer.content, match, "\n")


conn.close()



#b'{"id":"qKn9_p7lnPMLtpLC7MZfRh96MmOQo384woGg1dGKpZiK0hI","accountId":"ny-ZNbnF3w1uYrYMKkrdU9CdF-9If60WdE9MgF_qNZrtMgo","puuid":"uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA","name":"Catuin","profileIconId":932,"revisionDate":1625342299000,"summonerLevel":352}'