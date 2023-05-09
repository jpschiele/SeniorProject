import firebase_admin
from confTeams import get_teams
from firestoreClient import client_setup

# CHANGE STAT TO BE AVERAGED AND NAME OF NEW COLUMN
stat_dict = {'TRBOpp': 'L3TRBOpp', '3P%': 'L33PPer',
             '3P%Opp': 'L33PPerOpp', 'FG%': 'L3FGPer', 'FG%Opp': 'L3FGPerOpp', 'FTA': 'L3FTA', 'FTAOpp': 'L3FTAOpp',
             'PF': 'L3PF', 'PFOpp': 'L3PFOpp', 'TOV': 'L3TOV', 'TOVOpp': 'L3TOVOpp'}

# Fetch the service account key JSON file path and database URL from environment variables
db = client_setup()

# Specify conference
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for key, value in stat_dict.items():
    for conference in conferences:
        print(conference)
        # years to collect averages for
        years = ['2023']

        # teams to collect averages for
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
