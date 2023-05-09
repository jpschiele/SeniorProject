from confTeams import get_teams
from firestoreClient import client_setup

# Fetch the service account key JSON file path and database URL from environment variables
db = client_setup()

# Specify conference
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for conference in conferences:
    print(conference)
    # years to collect averages for
    years = ['2021']

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

            for game in games:
                data = game.to_dict()
                ref = team_ref.document(data['Date'])
                offEFG = (float(data['FGA']) * float(data['FG%']) + 0.5 * float(data['3PA']) * float(data['3P%'])) / float(data['FGA'])
                defEFG = (float(data['FGAOpp']) * float(data['FG%Opp']) + 0.5 * float(data['3PAOpp']) * float(data['3P%Opp'])) / float(data['FGAOpp'])
                offTOP = float(data['TOV']) / (float(data['FGA']) - float(data['ORB']) + float(data['TOV']) + 0.475 * float(data['FTA']))
                defTOP = float(data['TOVOpp']) / (float(data['FGAOpp']) - float(data['ORBOpp']) + float(data['TOVOpp']) + 0.475 * float(data['FTAOpp']))
                offORB = float(data['ORB']) / (float(data['ORB']) + float(data['TRBOpp']) - float(data['ORBOpp']))
                defORB = float(data['ORB']) / (float(data['TRB']) - float(data['ORB']) + float(data['ORBOpp']))
                offFTR = float(data['FTA']) / float(data['FGA'])
                defFTR = float(data['FTAOpp']) / float(data['FGAOpp'])
                ref.update({'offEFG': offEFG, 'defEFG': defEFG, 'offTOP': offTOP, 'defTOP': defTOP,
                            'offORB': offORB, 'defORB': defORB, 'offFTR': offFTR, 'defFTR': defFTR})
