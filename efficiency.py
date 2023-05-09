from confTeams import get_teams
from firestoreClient import client_setup

# efficiency.py calculates eight different efficiency ratings for each team in each game. These ratings are used when
# training the logistic and linear regression models.

# Creates connection with Firestore Database
db = client_setup()

# Specify conferences
conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

# Creates new efficiency fields for each game log
for conference in conferences:
    print(conference)
    # years to collect averages for
    years = ['2021']

    # teams to collect averages for
    teams = get_teams(conference)

    # calculate efficiency ratings for each team in every game
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

            # possessions = field goal attempts - offensive rebounds + turnovers + 0.475 * free throw attempts
            # EFG = (field goals made + 0.5 * 3 point attempts) / field goal attempts
            # TOP = turnovers / possessions
            # ORB = offensive rebounds / (offensive rebounds + opponent defensive rebounds)
            # FTR = free throw attempts / field goal attempts
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
