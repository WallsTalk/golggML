import sqlite3
import json
conn = sqlite3.connect("my_inting_data.db")


def win_status(participants):
    puuid = "uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA"
    for participant in participants:
        if participant["puuid"] == puuid:
            return participant["win"]



c = conn.cursor()
list_of_matches = c.execute("SELECT * FROM match_history;").fetchall()

c.execute("DELETE FROM match_history WHERE game_id LIKE 'status';")
conn.commit()
count = 0

champion_data = {
    "with": {},
    "against": {}
}
que_type = {
    420:  0,
    700: 0,
    440: 0
}
draft = {
    "my_team": "Ezreal,Malaphite,Evelynn,Karma".split(","),
    "enemy_team": "Pantheon,Kindred,Jhin,Kayle,Sona".split(",")
}
for match in list_of_matches:
    match_data = json.loads(match[1])
    if match_data["info"]["gameVersion"][:2] != "11" or match_data["info"]["queueId"] != 420:
        continue
    count += 1
    que_type[match_data["info"]["queueId"]] += 1
    participants = match_data["info"]["participants"]
    win = win_status(participants)
    puuid = "uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA"
    for participant in participants:
        if participant["puuid"] != puuid:
            champion = participant["championName"]

            # if participant has same win status as me he is on my team
#
            if win == participant["win"]:
                if champion in draft["my_team"]:
                    if champion not in champion_data["with"].keys():
                        champion_data["with"][champion] = {True: 0, False: 0}
                    champion_data["with"][champion][win] += 1
            else:
                if champion in draft["enemy_team"]:
                    if champion not in champion_data["against"].keys():
                        champion_data["against"][champion] = {True: 0, False: 0}
                    champion_data["against"][champion][win] += 1

conn.close()

list_with = []
list_against = []
for champ, stats in champion_data["with"].items():
    list_with.append((champ, sum(stats.values()), round(stats[True]/sum(stats.values()), 2)))

for champ, stats in champion_data["against"].items():
    list_against.append((champ, sum(stats.values()), round(stats[True]/sum(stats.values()), 2)))


list_with = sorted(list_with, key=lambda x: x[2])
for item in list_with:
    print(item)

print("\n############################################\n")

list_against = sorted(list_against, key=lambda x: x[2])
for item in list_against:
    print(item)

print(count)
print(que_type)