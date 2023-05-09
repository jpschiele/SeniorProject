from confTeams import get_teams
from firestoreClient import client_setup

db = client_setup()

conferences = ['ACC', 'Big10', 'Big12', 'BigEast', 'PAC12', 'SEC']

for conference in conferences:

    teams = get_teams(conference)

    years = ['2023']

    for year in years:
        win_count = 0
        lose_count = 0
        game_count = 0

        for team in teams:

            # Get the data from the Firestore database
            school = f'{team}'
            collect = f'{year}GameLog'
            data_ref = db.collection(conference).document(school).collection(collect)
            data_docs = data_ref.stream()

            for doc in data_docs:
                data = doc.to_dict()
                if data['Result'] == "W":
                    win_count += 1
                    game_count += 1
                elif data['Result'] == "L":
                    lose_count += 1
                    game_count += 1
                else:
                    print(f'no win or loss for {data["Date"]}')

        print(f'{conference} {year}:\n{win_count} wins\n{lose_count} losses\n{game_count} games\n')
