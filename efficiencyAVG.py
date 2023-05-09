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

            offEFG = 0
            defEFG = 0
            offTOP = 0
            defTOP = 0
            offORB = 0
            defORB = 0
            offFTR = 0
            defFTR = 0
            count = 0

            for game in games:
                data = game.to_dict()
                count += 1
                offEFG += float(data['offEFG'])
                defEFG += float(data['defEFG'])
                offTOP += float(data['offTOP'])
                defTOP += float(data['defTOP'])
                offORB += float(data['offORB'])
                defORB += float(data['defORB'])
                offFTR += float(data['offFTR'])
                defFTR += float(data['defFTR'])

            ref = team_ref.document('Averages')
            ref.set({'offEFG': (offEFG / count), 'defEFG': (defEFG / count), 'offTOP': (offTOP / count),
                        'defTOP': (defTOP / count), 'offORB': (offORB / count), 'defORB': (defORB / count),
                        'offFTR': (offFTR / count), 'defFTR': (defFTR / count)})
