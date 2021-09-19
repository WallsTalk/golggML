import sqlite3
import json
conn = sqlite3.connect("my_inting_data.db")


# this method defines match status if I won or Lost
def my_win_status(participants):
    puuid = "uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA"
    for participant in participants:
        if participant["puuid"] == puuid:
            return participant["win"]


# Get match history
c = conn.cursor()
list_of_matches = c.execute("SELECT * FROM match_history;").fetchall()

#c.execute("DELETE FROM match_history WHERE game_id LIKE 'EUN1_2894086929';")
conn.commit()
conn.close()
count = 0



# Here specify what champs are locked in champ select
options = "Tristana,Kassadin,DrMundo,Soraka,Mordekaiser,Amumu,Camille,Leona,Diana,Katarina,Janna,Khazix,Vayne,Tryndamere,Chogath,Diana,Yasuo,Tristana,Heimerdinger,Volibear,Kaisa,Malphite,Gragas,Lux,Jhin,Trundle,Thresh,Shaco,Shen,Yasuo,Twitch,Zyra,Graves,Talon,Kennen,Jinx,Jhin,Akshan,Karma,Teemo,Gwen,Kennen,RekSai,Yorick,Ezreal,Karma,Shaco,Akali,Sion,Ezreal,Lucian,Kindred,Azir,Caitlyn,Lux,XinZhao,DrMundo,Samira,Kassadin,Tristana,Ahri,Graves,TahmKench,Ezreal,XinZhao,Vladimir,Morgana,Renekton,Urgot,Varus,Irelia,Diana,Rakan,Twitch,Vladimir,Malphite,Trundle,Kayn,Ahri,Yone,Tristana,Volibear,Zed,Nautilus,Jhin,Aatrox,MasterYi,Samira,Gwen,Leblanc,Teemo,Ahri,LeeSin,Ezreal,Lulu,Nunu,Ahri,Riven,XinZhao,Leblanc,Kindred,Karma,Caitlyn,Tristana,Taric,JarvanIV,Fiora,Fizz,Katarina,Twitch,LeeSin,Karma,Thresh,Akshan,Zac,Nasus,Nidalee,Syndra,Amumu,Gnar,Lulu,Ziggs,Tristana,Diana,Caitlyn,Poppy,Nidalee,Irelia,Caitlyn,Morgana,XinZhao,Lucian,Camille,Ornn,Jinx,Akali,Cassiopeia,Lulu,Rengar,Kaisa,Vladimir,Ziggs,Vayne,TahmKench,Viego,Zac,Jhin,Talon,Vladimir,Sylas,Irelia,Seraphine,Kaisa,LeeSin,Katarina,Irelia,Zyra,XinZhao,Varus,Darius,Kassadin,Akshan,LeeSin,Ziggs,Soraka,Irelia,Darius,Kindred,Lucian,Kayn,Kaisa,Camille,Lulu,Kaisa,Orianna,MasterYi,XinZhao,LeeSin,Malphite,Sivir,Kayle,Khazix,Leblanc,Nasus,Lillia,Diana,Draven,Yuumi,Wukong,Akali,Diana,Ezreal,Graves,Jhin,TahmKench,Thresh,Garen,XinZhao,Leblanc,Samira,Janna,Vayne,Yasuo,Neeko,Kaisa,Nocturne,Camille,Qiyana,Mordekaiser,Samira,Nasus,Khazix,Seraphine,Nami"
draft = {
    "my_team": "".split(","),
    "enemy_team": "".split(",")
}



def select_tip(champs_record):
    #list_of_champ_record = [(champ, sum(champ_record[champ].values()), round(champ_record[champ][True]/sum(champ_record[champ].values()), 2)) for champ in champ_record.keys()]
    dict_of_champ_record = {}

    # {"wr": {True: 0, False: 0}, "syn_record": {}, "rec": []}
    for champ, stats in champs_record.items():
        for syn_champ, syn_stats in stats["syn_record"].items():
            if syn_champ not in dict_of_champ_record.keys():
                dict_of_champ_record[syn_champ] = {"win_rates_per_champ": [], "relevance": 0}
            # from evry teammate champion we gather champs we played with win ratios, and add them to a list of 4 winratios
            dict_of_champ_record[syn_champ]["win_rates_per_champ"].append(round(syn_stats[True]/sum(syn_stats.values()), 2))
            dict_of_champ_record[syn_champ]["relevance"] += len(syn_stats.values())

    tips = {"Bad": [], "Good": []}
    for champ, ratios in dict_of_champ_record.items():
        avrg = round(sum(ratios["win_rates_per_champ"])/len(ratios["win_rates_per_champ"]), 2)

        if avrg >= 0.8:
            tips["Good"].append([champ, ratios["relevance"], avrg])
        if avrg < 0.5:
            tips["Bad"].append([champ, ratios["relevance"], avrg])
    return(tips)


champion_data = {
    "with": {},
    "against": {}
}
que_type = {
    420:  0,
    700: 0,
    440: 0
}
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
    
    
    puuid = "uSeXv-1ss9cJrzBC9ZxEdWvyWLanYqK0ZhnIamsmdLhlqCDdDO9_QEgSLzjXB1-sqx06OceNxCi6LA"
    
    # check my champ for this game
    for participant in participants:
        if participant["puuid"] == puuid:
            my_champ = participant["championName"]

    # make stats of this game
    for participant in participants:
        if participant["puuid"] != puuid:
            champion = participant["championName"]

            # if participant has same win status as me he is on my team
            # tracking win ratio with that champ on my team overal, 
            # tracking win ration of champs I played with that champion 
            # and overal record of that champ on my team
            if win == participant["win"]:
                if champion in draft["my_team"]:
                    if champion not in champion_data["with"].keys():
                        champion_data["with"][champion] = {"wr": {True: 0, False: 0}, "syn_record": {}, "rec": []}
                    champion_data["with"][champion]["wr"][win] += 1

                    if my_champ not in champion_data["with"][champion]["syn_record"].keys():
                        champion_data["with"][champion]["syn_record"][my_champ] = {True: 0, False: 0}
                    champion_data["with"][champion]["syn_record"][my_champ][win] += 1

                    champion_data["with"][champion]["rec"].append(int(win))

            # tracking win ratio with that champ on enemy team overal, 
            # tracking win ration of champs I played against that champion 
            # and overal record of that champ on enemy team vs me
            else:
                if champion in draft["enemy_team"]:
                    if champion not in champion_data["against"].keys():
                        champion_data["against"][champion] = {"wr": {True: 0, False: 0}, "syn_record": {}, "rec": []}
                    champion_data["against"][champion]["wr"][win] += 1

                    if my_champ not in champion_data["against"][champion]["syn_record"].keys():
                        champion_data["against"][champion]["syn_record"][my_champ] = {True: 0, False: 0}
                    champion_data["against"][champion]["syn_record"][my_champ][win] += 1

                    champion_data["against"][champion]["rec"].append(int(win))



list_with = []
list_against = []
for champ, stats in champion_data["with"].items():
    list_with.append((
        champ, 
        sum(stats["wr"].values()), 
        round(stats["wr"][True]/sum(stats["wr"].values()), 2), 
        stats["rec"][-5:],
        ))

for champ, stats in champion_data["against"].items():
    list_against.append((champ, sum(stats["wr"].values()), round(stats["wr"][True]/sum(stats["wr"].values()), 2), stats["rec"][-5:]))

if len(list_with) != 0 and len(list_against) != 0:
    print("\n\n\n\n#######################################")
    print("######### THIS IS THE REPORT ##########")
    print("#######################################")


    print("\n### OUR_TEAM ###")
    for item in list_with:
        print(item)
    tips = select_tip(champion_data["with"])
    print("\nGood:\n", tips["Good"])
    print("\nBAD:\n",tips["Bad"])
    print("\nAverage chance: ", round(sum([wr[2] for wr in list_with])/len(list_with), 2))


    print("\n")  
    print("### ENEMY_TEAM ###")
    for item in list_against:
        print(item)

    tips = select_tip(champion_data["against"])
    print("\nGood:\n", tips["Good"])
    print("\nBAD:\n",tips["Bad"])
    print("\nAverage chance: ", round(sum([wr[2] for wr in list_against])/len(list_against), 2))


    print("\n\n\n")
    print("Total games: ", count)
    print("Games per queue type registered: ", que_type)
else:
    print("\n### No requested champions ###\n")


# list_with = sorted(list_with, key=lambda x: x[2])
# for item in list_with:
#     print(item)

# print("\n############################################\n")

# list_against = sorted(list_against, key=lambda x: x[2])
# for item in list_against:
#     print(item)
