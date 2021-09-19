import sqlite3
import json
from datetime import datetime




# this method defines match status if I won or Lost
def my_win_status(participants):
    puuid = "uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA"
    for participant in participants:
        if participant["puuid"] == puuid:
            return participant["win"]

def format_time_info(start_time):
    pass



conn = sqlite3.connect("my_inting_data.db")
# Get match history
c = conn.cursor()
list_of_matches = c.execute("SELECT * FROM match_history;").fetchall()

#c.execute("DELETE FROM match_history WHERE game_id LIKE 'EUN1_2894086929';")
conn.commit()
conn.close()
count = 0



que_type = {
    420:  0,
    700: 0,
    440: 0
}

weekdays_hours = dict([(x, dict([(x, { True: 0, False: 0 }) for x in range(0, 24)])) for x in range(0, 7)])
for match in list_of_matches:
    match_data = json.loads(match[1])

    # patch or season or game type check
    if match_data["info"]["gameVersion"][:2] != "11" or match_data["info"]["queueId"] != 420:
        continue
    
    #total games count
    count += 1

    # counting how many games of each que type
    que_type[match_data["info"]["queueId"]] += 1
    participants = match_data["info"]["participants"]
    win = my_win_status(participants)
    
    game_start = match_data["info"]["gameStartTimestamp"]
    game_start_date = datetime.fromtimestamp(game_start/1000)

    weekdays_hours[game_start_date.weekday()][game_start_date.hour][win] += 1


for weekday, hours in weekdays_hours.items():
    print(weekday)
    for hour, stats in hours.items():
        if sum(stats.values()) != 0:
            avrg = round(stats[True]/sum(stats.values()), 2)
        print(hour, stats, avrg)

    print("\n\n")
    # 


print(count)