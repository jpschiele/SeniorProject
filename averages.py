from confTeams import get_teams
from firestoreClient import client_setup

# averages.py adds a new field to every individual game log. It takes a dictionary of stats to take an average of
# and the name of the new field for the average. Average points for each team in the game are used as an example.
# Naming conventions are standardized to use 'AVG' in front of statistic and 'Opp' at the end of opponent stats.

# CHANGE STAT TO BE AVERAGED AND NAME OF NEW COLUMN
stat_dict = {'TmScore': 'AVGPts', 'OppScore': 'AVGPtsOpp'}

# Creates connection with Firestore Database
db = client_setup()

# Specify conferences to get averages
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for key, value in stat_dict.items():
    for conference in conferences:
        print(conference)
        # years to collect averages
        years = ['2023']

        # teams to collect averages
        teams = get_teams(conference)

        # collect averages for the season up to current game and add as a new column
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

                total = 0
                count = 0

                for game in games:
                    data = game.to_dict()
                    if game.id == 'Averages':
                        continue
                    if total == 0:
                        ref = team_ref.document(data['Date'])
                        ref.update({value: data[key]})
                    else:
                        ref = team_ref.document(data['Date'])
                        average = total / count
                        ref.update({value: str(round(average, 3))})

                    count += 1
                    total += float(data[key])
