#match_up = ['Fnatic', '']
# >>> team_stats.keys()
# dict_keys([1105, 1109, 1107, 1116, 1113, 1111, 1104, 1102, 1103, 1108, 1112, 1114, 1110, 1101, 1106, 1117, 1115, 1154, 1151, 1148, 1150, 1153, 1147, 1149, 1152, 1156, 1155, 1092, 1093, 1096, 1098, 1097, 1091, 1125, 1094, 1126, 1099, 1129, 1133, 1128, 1132, 1131, 1130, 1134, 1136, 1127, 1135])
# >>> print(team_stats[1105].keys())
# dict_keys(['top', 'jg', 'mid', 'adc', 'sup'])
# >>> print(team_stats[1105]["top"].keys())
# dict_keys(['Kills', 'Deaths', 'Assists', 'KDA', 'CS', '"CSinTeamsJungle"', 'CSinEnemyJungle', 'CSM', 'Golds', 'GPM', 'GOLD%', 'VisionScore', 'Wardsplaced', 'Wardsdestroyed', 'ControlWardsPurchased', 'VSPM', 'WPM', 'VWPM', 'WCPM', 'VS%', 'TotaldamagetoChampion', 'PhysicalDamage', 'MagicDamage', 'TrueDamage', 'DPM', 'DMG%', 'K+APerMinute', 'KP%', 'Solokills', 'Doublekills', 'Triplekills', 'Quadrakills', 'Pentakills', 'GD@15', 'CSD@15', 'XPD@15', 'LVLD@15', 'Damagedealttoturrets', 'Totalheal', 'Damageselfmitigated', 'Timeccingothers', 'Totaldamagetaken'])
# >>> print(team_stats[1105]["top"]["Kills"])
# ['3', '3', '5', '3', '1', '0', '2', '4', '14', '2', '2', '4', '0', '0', '0', '1', '2', '4', '5', '14', '3', '0', '2', '2', '3', '0', '2', '6', '2', '0', '3', '1', '1', '2', '1', '1', '5', '2', '6', '3', '2', '2', '2', '1', '4', '2', '9', '4', '5', '6', '0', '0', '5', '0', '5', '5', '0', '6', '3', '5', '1', '0', '1', '4', '4', '1', '0', '1', '3', '10', '2', '4', '5']
# >>> print(len(team_stats[1105]["top"]["Kills"]))
# 73
# >>> print(teams[1105])
# Invictus Gaming

# Leaderboard for KDA

# # this function looks at avg dmg dealt against other teams avg dmg taken 
# # team fighting
# def calculate_team_fighting(team1, team2):
#     t1_score = {"dealt": 0, "taken": 0}
#     t2_score = {"dealt": 0, "taken": 0}
#     for role in roles:
#         t1_score["dealt"] += team_stats[team1][role]['TotaldamagetoChampion']
#         t1_score["taken"] += team_stats[team1][role]['Totaldamagetaken']
#         t2_score["dealt"] += team_stats[team2][role]['TotaldamagetoChampion']
#         t2_score["taken"] += team_stats[team2][role]['Totaldamagetaken']
#     score = (t1_score["dealt"]/t1_score["taken"]) - (t2_score["dealt"]/t2_score["taken"])
#     return score

# calculate_team_fighting(*vs)


# # how fast teams grow gold
# # economy
# def calculate_economy(team1, team2):
#     score = 0
#     for role in roles:
#         score += (team_stats[team1][role]['GPM'] - team_stats[team2][role]['GPM']) * coff_power[role]
#     return score

# calculate_economy(*vs)



# # how mutch teams dps
# # dps
# def calculate_dps(team1, team2):
#     score = 0
#     for role in roles:
#         score += (team_stats[team1][role]['DPM'] - team_stats[team2][role]['DPM']) * coff_power[role]
#     return score

# calculate_dps(*vs)



# def calculate_meta(team1, team2):
#     score = 0
#     for role in roles:
#         score += (team_stats[team1][role]['DMG%'] - team_stats[team2][role]['DMG%']) * coff_power[role]
#         score += (team_stats[team1][role]['KP%'] - team_stats[team2][role]['KP%']) * coff_kp[role]
#     return score

# vs = [teams['T1'], teams['100 Thieves']]
# vs = [teams['Royal Never Give Up'], teams['Fnatic']]
# vs = [teams['DWG KIA'], teams['Funplus Phoenix']]
# vs = [teams['Rogue'], teams['DWG KIA']]
# vs = [teams['T1'], teams['Edward Gaming']]
# vs = [teams['Rogue'], teams['Funplus Phoenix']]
# vs = [teams['MAD Lions'], teams['Gen.G eSports']]
# vs = [teams['MAD Lions'], teams['Team Liquid']]
# vs = [teams['Gen.G eSports'], teams['Team Liquid']]
# vs = [teams['DWG KIA'], teams['Funplus Phoenix']]


# #def calculate_tempo(team1, team2):
# #     score = 0
# #     for role in roles:
# #         score += (team_stats[team1][role]['GD@15'] * coff_power[role])/(team_stats[team2][role]['GD@15'] * coff_power[role])
# #         score += (team_stats[team1][role]['CSD@15'] * coff_econ[role])/(team_stats[team2][role]['CSD@15'] * coff_econ[role])
# #         score += (team_stats[team1][role]['XPD@15'] * coff_econ[role])/(team_stats[team2][role]['XPD@15'] * coff_econ[role])
# #         score += (team_stats[team1][role]['K+APerMinute'] * coff_kp[role])/(team_stats[team2][role]['K+APerMinute'] * coff_kp[role])
# #     return score/4

# def calculate_early_lead(team1, team2):
#     score = 0
#     for role in roles:
#         score += (team_stats[team1][role]['GD@15'] - team_stats[team2][role]['GD@15']) * coff_power[role]
#         score += (team_stats[team1][role]['CSD@15'] - team_stats[team2][role]['CSD@15']) * coff_econ[role]
#         score += (team_stats[team1][role]['XPD@15'] - team_stats[team2][role]['XPD@15']) * coff_econ[role]
#     return score

# def calculate_tempo(team1, team2):
#     score = 0
#     for role in roles:
#         score += (team_stats[team1][role]['K+APerMinute'] - team_stats[team2][role]['K+APerMinute']) * coff_kp[role]    
#     return score

# calculate_tempo(*vs)
# calculate_early_lead(*vs)
# calculate_fighting(*vs)
# calculate_dps(*vs) # bonus points if economy is better, - points if its worse
# calculate_economy(*vs)
# calculate_meta(*vs)





# def calculate_economy(team1, team2):
#     score
#     for role in roles:
#         t1_score[role] = team_stats[team1][role]['GPM']
#         t2_score[role] = team_stats[team2][role]['GPM']
#     return score
