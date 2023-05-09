from confTeams import get_teams
from firestoreClient import client_setup

# L3averages.py creates a new field for each game log. It takes a dictionary of stats to take an average of the last
# 3 games and the name of the new field for the average. Average points for each team in the game are used as an
# example. Naming conventions are standardized to use 'L3' in front of statistic and 'Opp' at the end of opponent stats.

# CHANGE STAT TO BE AVERAGED AND NAME OF NEW COLUMN
stat_dict = {'TmScore': 'L3Pts', 'OppScore': 'L3PtsOpp'}

# Creates connection to Firestore Database
db = client_setup()

# Specify conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for key, value in stat_dict.items():
    for conference in conferences:
        print(conference)
        # years to collect averages
        years = ['2023']

        # teams to collect averages
        teams = get_teams(conference)

        # collect averages for the last three games and add as a new column
        for year in years:
            print(year)
            collect = f'{year}GameLog'
            for team in teams:
                print(team)
                if team == 'connecticut' and (year == '2018' or year == '2019' or year == '2020'):
                    continue
                school = f'{team}'
                team_ref = db.collection(conference).document(school).collection(collect)
                games = team_ref.stream()

                prev1 = 0
                prev2 = 0
                prev3 = 0

                for game in games:
                    data = game.to_dict()
                    if prev1 == 0 and prev2 == 0 and prev3 == 0:
                        ref = team_ref.document(data['Date'])
                        ref.update({value: data[key]})
                    elif prev2 == 0 and prev3 == 0:
                        ref = team_ref.document(data['Date'])
                        ref.update({value: str(prev1)})
                    elif prev3 == 0:
                        ref = team_ref.document(data['Date'])
                        average = (prev1 + prev2) / 2
                        ref.update({value: str(average)})
                    else:
                        ref = team_ref.document(data['Date'])
                        average = (prev1 + prev2 + prev3) / 3
                        ref.update({value: str(round(average, 3))})

                    prev3 = prev2
                    prev2 = prev1
                    prev1 = float(data[key])
